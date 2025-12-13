#!/usr/bin/env python3

#
# NOSA HEADER START
#
# The contents of this file are subject to the terms of the NASA Open
# Source Agreement (NOSA), Version 1.3 only (the "Agreement").  You may
# not use this file except in compliance with the Agreement.
#
# You can obtain a copy of the agreement at
#   docs/NASA_Open_Source_Agreement_1.3.txt
# or
#   https://sscweb.gsfc.nasa.gov/WebServices/NASA_Open_Source_Agreement_1.3.txt.
#
# See the Agreement for the specific language governing permissions
# and limitations under the Agreement.
#
# When distributing Covered Code, include this NOSA HEADER in each
# file and include the Agreement file at
# docs/NASA_Open_Source_Agreement_1.3.txt.  If applicable, add the
# following below this NOSA HEADER, with the fields enclosed by
# brackets "[]" replaced with your own identifying information:
# Portions Copyright [yyyy] [name of copyright owner]
#
# NOSA HEADER END
#
# Copyright (c) 2013-2025 United States Government as represented by
# the National Aeronautics and Space Administration. No copyright is
# claimed in the United States under Title 17, U.S.Code. All Other
# Rights Reserved.
#

"""
Module for accessing the Satellite Situation Center (SSC) web services
https://sscweb.gsfc.nasa.gov/WebServices/REST/.
<br>

Copyright &copy; 2013-2025 United States Government as represented by the
National Aeronautics and Space Administration. No copyright is claimed in
the United States under Title 17, U.S.Code. All Other Rights Reserved.
"""

import sys
import os
from urllib.parse import urlparse
from tempfile import mkstemp
import platform
from datetime import timedelta
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError
import time
import logging
from typing import Dict, List, Optional, Union
import requests
import dateutil.parser


import numpy as np

try:
    import requests_cache
    CACHE_AVAILABLE = True
except ImportError:
    CACHE_AVAILABLE = False

from sscws import __version__, RETRY_LIMIT, NAMESPACES as NS
try:
    from sscws.cdf import Cdf
    CDF_AVAILABLE = True
except ImportError as error:
    CDF_AVAILABLE = False
from sscws.coordinates import CoordinateSystem, CoordinateComponent
from sscws.formatoptions import CdfFormatOptions
from sscws.outputoptions import CoordinateOptions, OutputOptions
from sscws.request import DataRequest, QueryRequest, SatelliteSpecification
from sscws.result import Result
from sscws.timeinterval import TimeInterval



class SscWs:
    """
    Class representing the web service interface to NASA's
    Satelite Situation Center (SSC) <https://sscweb.gsfc.nasa.gov/>.

    Parameters
    ----------
    endpoint
        URL of the SSC web service.  If None, the default is
        'https://sscweb.gsfc.nasa.gov/WS/sscr/2/'.
    timeout
        Number of seconds to wait for a response from the server.
    proxy
        HTTP proxy information.  For example,<pre>
        proxies = {
          'http': 'http://10.10.1.10:3128',
          'https': 'http://10.10.1.10:1080',
        }</pre>
        Proxy information can also be set with environment variables.
        For example,<pre>
        $ export HTTP_PROXY="http://10.10.1.10:3128"
        $ export HTTPS_PROXY="http://10.10.1.10:1080"</pre>
    ca_certs
        Path to certificate authority (CA) certificates that will
        override the default bundle.
    disable_ssl_certificate_validation
        Flag indicating whether to validate the SSL certificate.
    user_agent
        A value that is appended to the HTTP User-Agent values.
    disable_cache
        Flag indicating whether to disable HTTP caching.

    Notes
    -----
    The logger used by this class has the class' name (SscWs).  By default,
    it is configured with a NullHandler.  Users of this class may configure
    the logger to aid in diagnosing problems.

    This class is dependent upon xml.etree.ElementTree module which is
    vulnerable to an "exponential entity expansion" and "quadratic blowup
    entity expansion" XML attack.  However, this class only receives XML
    from the (trusted) SSC server so these attacks are not a threat.  See
    the xml.etree.ElementTree "XML vulnerabilities" documentation for
    more details
    <https://docs.python.org/3/library/xml.html#xml-vulnerabilities>.
    """
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments
    def __init__(
            self,
            endpoint=None,
            timeout=None,
            proxy=None,
            ca_certs=None,
            disable_ssl_certificate_validation=False,
            user_agent=None,
            disable_cache=False):

        self.logger = logging.getLogger(type(self).__name__)
        self.logger.addHandler(logging.NullHandler())

        self.retry_after_time = None

        self.logger.debug('endpoint = %s', endpoint)
        self.logger.debug('ca_certs = %s', ca_certs)
        self.logger.debug('disable_ssl_certificate_validation = %s',
                          disable_ssl_certificate_validation)
        self.logger.debug('disable_cache = %s', disable_cache)

        if endpoint is None:
            self._endpoint = 'https://sscweb.gsfc.nasa.gov/WS/sscr/2/'
        else:
            self._endpoint = endpoint

        self._user_agent = 'sscws/' + __version__ + ' (' + \
            platform.python_implementation() + ' ' \
            + platform.python_version() + '; '+ platform.platform() + ')'

        if user_agent is not None:
            self._user_agent += ' (' + user_agent + ')'

        self._request_headers = {
            'Content-Type' : 'application/xml',
            'Accept' : 'application/xml',
            'User-Agent' : self._user_agent
        }
        if CACHE_AVAILABLE and disable_cache is not True:
            self._session = requests_cache.CachedSession('sscws_cache',
                                                         cache_control=True)
        else:
            self._session = requests.Session()

        #self._session.max_redirects = 0
        self._session.headers.update(self._request_headers)

        if ca_certs is not None:
            self._session.verify = ca_certs

        if disable_ssl_certificate_validation is True:
            self._session.verify = False

        if proxy is not None:
            self._proxy = proxy

        self._timeout = timeout

        self._cache = {
            'Observatories': {
                'ETag': None,
                'Value': None
            },
            'GroundStations': {
                'Last-Modified': None,
                'Value': None
            }
        }

    # pylint: enable=too-many-arguments


    def __str__(self) -> str:
        """
        Produces a string representation of this object.

        Returns
        -------
        str
            A string representation of this object.
        """
        return 'SscWs(endpoint=' + self._endpoint + ', timeout=' + \
               str(self._timeout) + ')'


    def __del__(self):
        """
        Destructor.  Closes all network connections.
        """

        self.close()


    def close(self) -> None:
        """
        Closes any persistent network connections.  Generally, deleting
        this object is sufficient and calling this method is unnecessary.
        """
        self._session.close()


    def get_observatories(
            self,
            obs_ids: Optional[List[str]] = None
        ) -> Dict:
        """
        Gets a description of the available SSC observatories.

        Parameters
        ----------
        obs_ids
            Optional list of observatory identifiers to get.  If none
            are given, all are returned.

        Returns
        -------
        Dict
            Dictionary whose structure mirrors ObservatoryResponse from
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>
            with the addition of the following key/values:<br>
            - HttpStatus: with the value of the HTTP status code.
              Successful == 200.<br>
            When HttpStatus == 200:<br>
            - Observatories: containing a List of Dictionaries describing
              each observatory (keys: Id, Name, Resolution, StartTime,
              EndTime, ResourceId).<br>
            When HttpStatus != 200:<br>
            - HttpText: containing a string representation of the HTTP
              entity body.<br>
            When HttpText is a standard SSC WS error entity body the
            following key/values (convenience to avoid parsing
            HttpStatus):<br>
            - ErrorMessage: value from HttpText.<br>
            - ErrorDescription: value from HttpText.<br>
        """
        url = self._endpoint + 'observatories'
        params = []

        if obs_ids is None:
            obs_ids = []
        for obs_id in obs_ids:
            params.append(('id', obs_id))

        headers = None
        if self._cache['Observatories']['ETag'] is not None:
            headers = {
                'If-None-Match': self._cache['Observatories']['ETag']
            }

        response = self._session.get(url, timeout=self._timeout,
                                     headers=headers, params=params)

        #self.logger.debug(f'url = {response.url}, '\
        #    'status = {response.status_code}')

        if response.status_code == 304:
            return self._cache['Observatories']['Value']

        status = self.__get_status(response)
        if response.status_code != 200:
            self.logger.warning('%s failed with status %d', response.url,
                                response.status_code)
            return status

        observatory_response = ET.fromstring(response.text)

        result = {
            'Observatory': []
        }

        for observatory in observatory_response.findall('ssc:Observatory',
                                                        namespaces=NS):
            result['Observatory'].append({
                'Id': observatory.find('ssc:Id', namespaces=NS).text,
                'Name': observatory.find('ssc:Name', namespaces=NS).text,
                'Resolution': int(observatory.find('ssc:Resolution',
                                                   namespaces=NS).text),
                'StartTime': dateutil.parser.parse(observatory.find(\
                    'ssc:StartTime', namespaces=NS).text),
                'EndTime': dateutil.parser.parse(observatory.find(\
                    'ssc:EndTime', namespaces=NS).text),
                'ResourceId': observatory.find('ssc:ResourceId',
                                               namespaces=NS).text
            })

        result.update(status)

        if 'ETag' in response.headers:
            etag = response.headers['ETag']
            # workaround old apache bugs that are still causing problems
            etag = etag.replace('-gzip', '')
            self._cache['Observatories']['ETag'] = etag
            self._cache['Observatories']['Value'] = result
        else:
            self._cache['Observatories']['ETag'] = None
            self._cache['Observatories']['Value'] = None

        return result


    def get_ground_stations(
            self
        ) -> Dict:
        """
        Gets a description of the available SSC ground stations.

        Returns
        -------
        Dict
            Dictionary whose structure mirrors GroundStationResponse from
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>
            with the addition of the following key/values:<br>
            - HttpStatus: with the value of the HTTP status code.
              Successful == 200.<br>
            When HttpStatus != 200:<br>
            - HttpText: containing a string representation of the HTTP
              entity body.<br>
            When HttpText is a standard SSC WS error entity body the
            following key/values (convenience to avoid parsing
            HttpStatus):<br>
            - ErrorMessage: value from HttpText.<br>
            - ErrorDescription: value from HttpText.<br>
        """
        url = self._endpoint + 'groundStations'

        self.logger.debug('request url = %s', url)

        headers = None
        if self._cache['GroundStations']['Last-Modified'] is not None:
            headers = {
                'If-Modified-Since': self._cache['GroundStations']['Last-Modified']
            }

        response = self._session.get(url, timeout=self._timeout,
                                     headers=headers)

        if response.status_code == 304:
            return self._cache['GroundStations']['Value']

        status = self.__get_status(response)
        if response.status_code != 200:
            return status

        ground_station_response = ET.fromstring(response.text)

        result = {
            'GroundStation': []
        }

        for ground_station in ground_station_response.findall(\
                'ssc:GroundStation', namespaces=NS):

            location = ground_station.find('ssc:Location', namespaces=NS)
            latitude = float(location.find('ssc:Latitude', namespaces=NS).text)
            longitude = float(location.find('ssc:Longitude',
                                            namespaces=NS).text)

            result['GroundStation'].append({
                'Id': ground_station.find('ssc:Id', namespaces=NS).text,
                'Name': ground_station.find('ssc:Name', namespaces=NS).text,
                'Location': {
                    'Latitude': latitude,
                    'Longitude': longitude
                }
            })

        result.update(status)

        if 'Last-Modified' in response.headers:
            self._cache['GroundStations']['Last-Modified'] = response.headers['Last-Modified']
            self._cache['GroundStations']['Value'] = result
        else:
            self._cache['GroundStations']['Last-Modified'] = None
            self._cache['GroundStations']['Value'] = None

        return result


    def get_example_time_interval(
            self,
            observatory: str
        ) -> TimeInterval:
        """
        Gets a small example time interval for the specified observatory.

        Parameters:
        -----------
        observatory
            Specifies the observatory.

        Returns
        -------
        TimeInterval
            A small example time interval for the specified observatory.
        """

        for obs in self.get_observatories()['Observatory']:
            if obs['Id'] == observatory:
                end = obs['EndTime']
                return TimeInterval(end - timedelta(hours=2), end)

        return None


    def get_locations(
            self,
            param1: Union[List[str], DataRequest],
            time_range: Union[List[str], TimeInterval] = None,
            coords: List[CoordinateSystem] = None
        ) -> Dict:
        """
        Gets the specified locations.  Complex requests (requesting
        magnetic field model values) require a single DataRequest
        parameter.  Simple requests (for only x, y, z, lat, lon,
        local_time) require at least the first two paramters.

        Parameters
        ----------
        param1
            A locations DataRequest or a list of observatory identifier
            (returned by get_observatories).
        time_range
            A TimeInterval or two element array of ISO 8601 string
            values of the start and stop time of requested data.  The
            datetime values should have a UTC timezone.  If the values
            have no timezone, it will be set to UTC.  A datetime with
            a non-UTC timezone, will have its value adjusted to UTC and
            the returned data may not have the expected range.
        coords
            Array of CoordinateSystem values that location information
            is to be in.  If None, default is CoordinateSystem.GSE.

        Returns
        -------
        Dict
            Dictionary whose structure mirrors Result from
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>
            with the addition of the following key/values:<br>
            - HttpStatus: with the value of the HTTP status code.
              Successful == 200.<br>
            When HttpStatus == 200:<br>
            - Data: List of SatelliteData dictionaries.<br>
            When HttpStatus != 200:<br>
            - HttpText: containing a string representation of the HTTP
              entity body.<br>
            When HttpText is a standard SSC WS error entity body the
            following key/values (convenience to avoid parsing
            HttpStatus):<br>
            - ErrorMessage: value from HttpText.<br>
            - ErrorDescription: value from HttpText.<br>

        Raises
        ------
        ValueError
            If param1 is not a DataRequest and time_range is missing or
            time_range does not contain valid values.
        """

        if isinstance(param1, DataRequest):
            request = param1
        else:
            request = SscWs.__create_locations_request(param1, time_range,
                                                       coords)
        return self.__get_locations(request)


    def get_locations2(
            self,
            param1: Union[List[str], DataRequest],
            time_range: Union[List[str], TimeInterval] = None,
            coords: List[CoordinateSystem] = None
        ) -> Dict:
        """
        Gets the specified locations using CDF instead of XML.  This
        method is faster, supports larger requests, and the server 
        supports more concurrency with this method than with the 
        `SscWs.get_locations` method.  Complex requests (requesting
        magnetic field model values) require a single DataRequest
        parameter.  Simple requests (for only x, y, z, lat, lon,
        local_time) require at least the first two paramters.

        Parameters
        ----------
        param1
            A locations DataRequest or a list of observatory identifier
            (returned by get_observatories).
        time_range
            A TimeInterval or two element array of ISO 8601 string
            values of the start and stop time of requested data.  The
            datetime values should have a UTC timezone.  If the values
            have no timezone, it will be set to UTC.  A datetime with
            a non-UTC timezone, will have its value adjusted to UTC and
            the returned data may not have the expected range.
        coords
            Array of CoordinateSystem values that location information
            is to be in.  If None, default is CoordinateSystem.GSE.

        Returns
        -------
        Dict
            Dictionary whose structure mirrors Result from
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>
            with the addition of the following key/values:<br>
            - HttpStatus: with the value of the HTTP status code.
              Successful == 200.<br>
            When HttpStatus != 200:<br>
            - HttpText: containing a string representation of the HTTP
              entity body.<br>
            When HttpText is a standard SSC WS error entity body the
            following key/values (convenience to avoid parsing
            HttpStatus):<br>
            - ErrorMessage: value from HttpText.<br>
            - ErrorDescription: value from HttpText.<br>

        Raises
        ------
        ValueError
            If param1 is not a DataRequest and time_range is missing or
            time_range does not contain valid values.
        ModuleNotFoundExcepttion
            If cdflib is not installed.

        Warnings
        --------
        This method is experimental and may be eliminated or changed
        significantly in future releases.  Code expecting a stable API
        should use `SscWs.get_locations` instead.  The results returned 
        are compatible with `SscWs.get_locations` except that the numpy 
        array of datetime.datetime values are returned as a numpy array 
        of numpy.datetime64 values.  This method requires the 
        cdflib module to be installed.

        See Also
        --------
        SscWs.get_locations : Gets the specified locations.
        """

        if not CDF_AVAILABLE:
            raise ModuleNotFoundError('cdflib module not installed')

        if isinstance(param1, DataRequest):
            request = param1
        else:
            request = SscWs.__create_locations_request(param1, time_range,
                                                       coords)
        if request.format_options is None:
            request.format_options = CdfFormatOptions()

        request.format_options.cdf = True

        result = self.__get_locations(request)

        if result['HttpStatus'] == 200:
            #print('result = ', result)
            result = self.get_locations_from_file(result)

        return result


    def download(
            self,
            url: str
        ) -> str:
        """
        Downloads the file specified by the given URL to a temporary
        file without reading all of it into memory.  This method
        utilizes the connection pool and persistent HTTP connection
        to the SscWs server.

        Parameters
        ----------
        url
            URL of file to download.
        Returns
        -------
        str
            name of tempory file or None if there was an error.
        """
        suffix = os.path.splitext(urlparse(url).path)[1]

        file_descriptor, tmp_filename = mkstemp(suffix=suffix)

        with self._session.get(url, stream=True,
                               timeout=self._timeout) as response:

            with open(tmp_filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:  # filter out keep-alive new chunks
                        file.write(chunk)
            os.close(file_descriptor)

        return tmp_filename


    def get_locations_from_file(
            self,
            results: Result
        ) -> Dict:
        """
        Gets the given file(s) from the server and returns the contents
        in a dictionary.

        Parameters
        ----------
        results
            results to get locations from.

        Returns
        -------
        Dict
            Dictionary whose structure mirrors Result from
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>
            with the addition of the following key/values:<br>
            - HttpStatus: with the value of the HTTP status code.
              Successful == 200.<br>
            When HttpStatus != 200:<br>
            - HttpText: containing a string representation of the HTTP
              entity body.<br>
            When HttpText is a standard SSC WS error entity body the
            following key/values (convenience to avoid parsing
            HttpStatus):<br>
            - ErrorMessage: value from HttpText.<br>
            - ErrorDescription: value from HttpText.<br>
        """
        locations_result = {}
        locations_result['HttpStatus'] = results['HttpStatus']
        locations_result['StatusCode'] = results['StatusCode']
        locations_result['StatusSubCode'] = results['StatusSubCode']
        locations_result['Data'] = np.empty(len(results['Files']), dtype=object)
        #print('results = ', results)
        for index in range(len(results['Files'])):
            tmp_cdf_file = 'unset'
            try:
                result_url = results['Files'][index]['Name']
                tmp_cdf_file = self.download(result_url)
                #print('tmp_cdf_file', tmp_cdf_file)
                cdf = Cdf()
                cdf.open(tmp_cdf_file)
                locations_result['Data'][index] = cdf.get_satellite_data()
                #cdf.close() ???
                os.remove(tmp_cdf_file)
                #print('tmp_cdf_file', tmp_cdf_file, 'retained')
            except:
                self.logger.error('Exception from read_data(%s): %s',
                                  tmp_cdf_file, sys.exc_info()[0])
                self.logger.error('CDF file has been retained.')
                raise
        return locations_result


    def get_client_library_example(
            self,
            obs_id: str,
            language: str = 'Python'
        ) -> str:
        """
        Gets client library example code for the given observatory and
        programming language.

        Parameters
        ----------
        observatory
            The observatory to use in the example code.  It must be an Id
            returned by get_observatories.
        language
            The programming language of the example code.  It must be 
            either Python or IDL.

        Returns
        -------
        str
            Requested client library example code.
        """
        library = 'sscwsPy'
        if language.lower() == 'idl':
            library = 'sscwsIdl'

        response = requests.get(self._endpoint + 'observatories/' +
            obs_id + '/clientLibraryExample/' + library,
            timeout=self._timeout)

        if response.status_code != 200:
            self.logger.warning('%s failed with status %d', response.url,
                                response.status_code)
            return None

        return response.text


    @staticmethod
    def __create_locations_request(
            obs_ids: List[str],
            time_range: Union[List[str], TimeInterval] = None,
            coords: List[CoordinateSystem] = None
        ) -> DataRequest:
        """
        Creates a "simple" (only x, y, z, lat, lon, local_time in GSE)
        locations DataRequest for the given values.
        More complicated requests should be made with DataRequest
        directly.

        Parameters
        ----------
        obs_ids
            A list of observatory identifier (returned by
            get_observatories).
        time_range
            A TimeInterval or two element array of ISO 8601 string
            values of the start and stop time of requested data.
        coords
            Array of CoordinateSystem values that location information
            is to be in.  If None, default is CoordinateSystem.GSE.
        Returns
        -------
        DataRequest
            A simple locations DataRequest based upon the given values.
        Raises
        ------
        ValueError
            If time_range is missing or time_range does not contain
            valid values.
        """

        sats = []
        for sat in obs_ids:
            sats.append(SatelliteSpecification(sat, 1))

        if time_range is None:
            raise ValueError('time_range value is required when ' +
                             '1st is not a DataRequest')

        if isinstance(time_range, list):
            time_interval = TimeInterval(time_range[0], time_range[1])
        else:
            time_interval = time_range

        if coords is None:
            coords = [CoordinateSystem.GSE]

        coord_options = []
        for coord in coords:
            coord_options.append(
                CoordinateOptions(coord, CoordinateComponent.X))
            coord_options.append(
                CoordinateOptions(coord, CoordinateComponent.Y))
            coord_options.append(
                CoordinateOptions(coord, CoordinateComponent.Z))
            coord_options.append(
                CoordinateOptions(coord, CoordinateComponent.LAT))
            coord_options.append(
                CoordinateOptions(coord, CoordinateComponent.LON))
            coord_options.append(
                CoordinateOptions(coord, CoordinateComponent.LOCAL_TIME))

        return DataRequest(None, time_interval, sats, None,
                           OutputOptions(coord_options), None, None)


    def __get_locations(
            self,
            request: DataRequest
        ) -> Dict:
        """
        Gets the given locations DataRequest.

        Parameters
        ----------
        request
            A locations DataRequest.
        Returns
        -------
        Dict
            Dictionary whose structure mirrors Result from
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>
            with the addition of the following key/values:<br>
            - HttpStatus: with the value of the HTTP status code.
              Successful == 200.<br>
            When HttpStatus != 200:<br>
            - HttpText: containing a string representation of the HTTP
              entity body.<br>
            When HttpText is a standard SSC WS error entity body the
            following key/values (convenience to avoid parsing
            HttpStatus):<br>
            - ErrorMessage: value from HttpText.<br>
            - ErrorDescription: value from HttpText.<br>
        """
        url = self._endpoint + 'locations'

        self.logger.debug('__get_locations: POST request url = %s', url)

        xml_data_request = request.xml_element()

        #self.logger.debug('request XML = %s',
        #                  ET.tostring(xml_data_request))

        for retries in range(RETRY_LIMIT): # pylint: disable=unused-variable

            response = self._session.post(url,
                                          data=ET.tostring(xml_data_request),
                                          timeout=self._timeout)
            if response.status_code == 429 or \
               response.status_code == 503 and \
               'Retry-After' in response.headers:

                retry_after = response.headers['Retry-After']

                self.logger.debug('429/503 status with Retry-After header: %s',
                                  retry_after)
                retry_after = int(retry_after)

                self.logger.info('Sleeping %d seconds before retrying request',
                                 retry_after)
                time.sleep(retry_after)
            else:
                break

        return self.__get_result(response)


    @staticmethod
    def __get_status(
            response: requests.Response
        ) -> Dict:
        """
        Gets status information from the given response.  In particular,
        when status_code != 200, an attempt is made to extract the SSC WS
        ErrorMessage and ErrorDescription from the response.

        Parameters
        ----------
        response
            requests Response object.

        Returns
        -------
        Dict
            Dict containing the following:<br>
            - HttpStatus: the HTTP status code<br>
            additionally, when HttpStatus != 200<br>
            - ErrorText: a string representation of the entire entity
              body<br>
            - ErrorMessage: SSC WS ErrorMessage (when available)<br>
            - ErrorDescription: SSC WS ErrorDescription (when available)
        """
        http_result = {
            'HttpStatus': response.status_code
        }

        if response.status_code != 200:

            http_result['ErrorText'] = response.text
            try:
                error_element = ET.fromstring(response.text)
                http_result['ErrorMessage'] = error_element.findall(\
                    './/xhtml:p[@class="ErrorMessage"]/xhtml:b',
                    namespaces=NS)[0].tail
                http_result['ErrorDescription'] = error_element.findall(\
                    './/xhtml:p[@class="ErrorDescription"]/' +
                    'xhtml:b', namespaces=NS)[0].tail
            except ParseError:
                pass  # ErrorText is the best we can do

        return http_result


    def __get_result(
            self,
            response: requests.Response
        ) -> Dict:
        """
        Creates a dict representation of a Result from the given response.

        Parameters
        ----------
        response
            A response from a web service request.

        Returns
        -------
        Dict
            Dict representation of a Result as described in
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>
            with the addition of an HttpStatus key with the value of the
            HTTP status code.  When HttpStatus != 200, a key named
            HttpText will contain a string representation of the entity
            body.  And if the HttpText is a standard SSC WS error
            entity body, then keys named ErrorMessage and ErrorDescription
            will contain the values from the SSC WS error entity body
            (saving the caller the trouble of parsing HttpText).
        """

        status = self.__get_status(response)
        if response.status_code != 200:
            return status

        element = ET.fromstring(response.text)

        result_element = element.find('ssc:Result', namespaces=NS)

        if result_element is None:
            result_element = element.find('ssc:QueryResult', namespaces=NS)

        result = Result.get_result(result_element)
        result.update(status)
        return result


    def get_conjunctions(
            self,
            query: QueryRequest
        ) -> Dict:
        """
        Gets the conjunctions specified by query.

        Parameters
        ----------
        query
            Conjunction query request.
        Returns
        -------
        Dict
            Dictionary whose structure mirrors QueryResult from
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>
            with the addition of the following key/values:<br>
            - HttpStatus: with the value of the HTTP status code.
              Successful == 200.<br>
            When HttpStatus != 200:<br>
            - HttpText: containing a string representation of the HTTP
              entity body.<br>
            When HttpText is a standard SSC WS error entity body the
            following key/values (convenience to avoid parsing
            HttpStatus):<br>
            - ErrorMessage: value from HttpText.<br>
            - ErrorDescription: value from HttpText.<br>
        Raises
        ------
        ValueError
            If query is invalid.
        """

        url = self._endpoint + 'conjunctions'

        self.logger.debug('POST request url = %s', url)

        xml_query_request = query.xml_element()

        self.logger.debug('request XML = %s',
                          ET.tostring(xml_query_request))

        for retries in range(RETRY_LIMIT):  # pylint: disable=unused-variable

            response = self._session.post(url,
                                          data=ET.tostring(xml_query_request),
                                          timeout=self._timeout)
            if response.status_code == 429 or \
               response.status_code == 503 and \
               'Retry-After' in response.headers:

                retry_after = response.headers['Retry-After']

                self.logger.debug('429/503 status with Retry-After header: %s',
                                  retry_after)
                retry_after = int(retry_after)

                self.logger.info('Sleeping %d seconds before retrying request',
                                 retry_after)
                time.sleep(retry_after)
            else:
                break

        status = self.__get_status(response)
        if response.status_code != 200:
            return status

        #self.logger.debug('response XML = %s', response.text)

        result = self.__get_result(response)
        result.update(status)
        return result


    @staticmethod
    def print_files_result(
            result: Dict):
        """
        Prints a Result containing files names document.

        Parameters
        ----------
        result
            Dict representation of Result as described
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
        """
        for file in result['Files']:
            print(file['Name'])


    # pylint: disable=too-many-branches
    @staticmethod
    def print_locations_result(
            result: Dict
        ) -> None:
        """
        Prints a Dict representation of a Result.

        Parameters
        ----------
        result
            Dict representation of a Result as described
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
        """

        #print('StatusCode:', result['StatusCode'],
        #      'StatusSubCode:', result['StatusSubCode'])
        #print(result)

        if 'Files' in result:
            SscWs.print_files_result(result)
            return

        for data in result['Data']:
            if 'Coordinates' not in data:
                continue
            for coords in data['Coordinates']:
                print(data['Id'], coords['CoordinateSystem'].value)
                print('Time                     ', 'X                     ',
                      'Y                     ', 'Z                     ')
                for index in range(min(len(data['Time']), len(coords['X']))):
                    print(data['Time'][index], coords['X'][index],
                          coords['Y'][index], coords['Z'][index])

                if 'BTraceData' in data:
                    for b_trace in data['BTraceData']:

                        print(b_trace['CoordinateSystem'].value,
                              b_trace['Hemisphere'].value,
                              'Magnetic Field-Line Trace Footpoints')
                        print('Time                          ', 'Latitude        ',
                              'Longitude   ', 'Arc Length')
                        for index in range(min(len(data['Time']),
                                               len(b_trace['Latitude']))):
                            print(data['Time'][index],
                                  (f"{b_trace['Latitude'][index]:15.5f} "
                                   f"{b_trace['Longitude'][index]:15.5f} "
                                   f"{b_trace['ArcLength'][index]:15.5f}"))

                quantities = ['RadialLength', 'MagneticStrength',
                              'NeutralSheetDistance', 'BowShockDistance',
                              'MagnetoPauseDistance', 'DipoleLValue',
                              'DipoleInvariantLatitude', 'SpacecraftRegion',
                              'RadialTracedFootpointRegions',
                              'NorthBTracedFootpointRegions',
                              'SouthBTracedFootpointRegions']

                for quantity in quantities:
                    SscWs.print_time_series(quantity, data)

                if 'BGseX' in data and data['BGseX'] is not None:

                    min_len = min(len(data['Time']), len(data['BGseX']))
                    if min_len > 0:
                        print(f"{'Time':25s} {'B Strength GSE':^30s}")
                        print(f"{'':25s} {'X':^9s} {'Y':^9s} {'Z':^9s}")
                        for index in range(min_len):
                            bgse_time = data['Time'][index]
                            try:
                                iso_time = bgse_time.isoformat()
                            except AttributeError:
                                iso_time = str(bgse_time)
                            print((f"{iso_time:25s} "
                                   f"{data['BGseX'][index]:9.6f} "
                                   f"{data['BGseY'][index]:9.6f} "
                                   f"{data['BGseZ'][index]:9.6f}"))

                if 'NorthBTracedFootpointRegion' in data and \
                   'SouthBTracedFootpointRegion' in data:

                    min_len = min(len(data['Time']),
                                  len(data['NorthBTracedFootpointRegion']))
                    if min_len > 0:
                        print('                 B-Traced Footpoint Region')
                        print('Time                     ', 'North            ',
                              'South           ')
                        for index in range(min_len):
                            print(data['Time'][index],
                                  data['NorthBTracedFootpointRegion'][index].value,
                                  data['SouthBTracedFootpointRegion'][index].value)
    # pylint: enable=too-many-branches


    @staticmethod
    def print_time_series(
            name: str,
            data: Dict
        ) -> None:
        """
        Prints the given time-series data.

        Parameters
        ----------
        name
            Name (key) of data to print.
        data
            Dict containing the values to print.
        """

        if name in data and data[name] is not None:
            min_len = min(len(data['Time']), len(data[name]))
            if min_len > 0:
                print('Time                     ', name)
                for index in range(min_len):
                    print(data['Time'][index], data[name][index])


    @staticmethod
    def print_conjunction_result(
            result: Dict
        ) -> None:
        """
        Prints the given Dict representation of a QueryResult.

        Parameters
        ----------
        result
            Dict representation of QueryResult as described
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
        """

        print('StatusCode:', result['StatusCode'],
              'StatusSubCode:', result['StatusSubCode'])
        #print(result)

        for conjunction in result['Conjunction']:
            print(conjunction['TimeInterval']['Start'].isoformat(), 'to',
                  conjunction['TimeInterval']['End'].isoformat())
            print((f"  {'Satellite':10s} {'Lat':>7s} {'Lon':>7s} "
                   f"{'Radius':>9s} {'Ground Stations':20s} {'Lat':>7s} "
                   f"{'Lon':>7s} {'ArcLen':>9s}"))
            for sat in conjunction['SatelliteDescription']:
                for description in sat['Description']:
                    trace = description['TraceDescription']
                    print((f"  {sat['Satellite']:10s} "
                           f"{description['Location']['Latitude']:7.2f} "
                           f"{description['Location']['Longitude']:7.2f} "
                           f"{description['Location']['Radius']:9.2f} "
                           f"{trace['Target']['GroundStation']:20s} "
                           f"{trace['Location']['Latitude']:7.2f} "
                           f"{trace['Location']['Longitude']:7.2f} "
                           f"{trace['ArcLength']:9.2f}"))
