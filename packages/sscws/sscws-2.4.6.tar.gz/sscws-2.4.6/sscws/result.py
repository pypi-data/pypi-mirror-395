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
# Copyright (c) 2013-2023 United States Government as represented by
# the National Aeronautics and Space Administration. No copyright is
# claimed in the United States under Title 17, U.S.Code. All Other
# Rights Reserved.
#

"""
Module defining classes to represent the Result class and its
sub-classes from
<https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.<br>

Copyright &copy; 2013-2023 United States Government as represented by the
National Aeronautics and Space Administration. No copyright is claimed in
the United States under Title 17, U.S.Code. All Other Rights Reserved.
"""

import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Any, Callable, Dict, List
from abc import ABCMeta, abstractmethod
from enum import Enum
import dateutil.parser
import numpy as np

from sscws import NAMESPACES as NS
from sscws.coordinates import CoordinateSystem
from sscws.regions import FootpointRegion, Hemisphere, SpaceRegion


class ResultStatusCode(Enum):
    """
    Enumerations representing the ResultStatusCode defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    SUCCESS = 'Success'
    CONDITIONAL_SUCCESS = 'ConditionalSuccess'
    ERROR = 'Error'


class ResultStatusSubCode(Enum):
    """
    Enumerations representing the ResultStatusSubCode defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    SUCCESS = 'Success'
    MISSING_REQUEST = 'MissingRequest'
    MISSING_SATELLITES = 'MissingSatellites'
    INVALID_BEGIN_TIME = 'InvalidBeginTime'
    INVALID_END_TIME = 'InvalidEndTime'
    INVALID_SATELLITE = 'InvalidSatellite'
    INVALID_TIME_RANGE = 'InvalidTimeRange'
    INVALID_RESOLUTION_FACTOR = 'InvalidResolutionFactor'
    MISSING_OUTPUT_OPTIONS = 'MissingOutputOptions'
    MISSING_COORD_OPTIONS = 'MissingCoordOptions'
    MISSING_COORD_SYSTEM = 'MissingCoordSystem'
    INVALID_COORD_SYSTEM = 'InvalidCoordSystem'
    MISSING_COORD_COMPONENT = 'MissingCoordComponent'
    MISSING_GRAPH_OPTIONS = 'MissingGraphOptions'
    MISSING_COORDINATE_SYSTEM = 'MissingCoordinateSystem'
    MISSING_COORDINATE_COMPONENT = 'MissingCoordinateComponent'
    SERVER_ERROR = 'ServerError'


class Result(metaclass=ABCMeta):
    """
    Class representing a Result from
    <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Parameters
    ----------
    status_code
        Result status code.
    status_sub_code
        Result status sub-code.
    status_text
        Result status text.

    Notes
    -----
    Although this class is essentially a dictionary, it was defined as a
    class to make certain that it matched the structure and key names
    of a Result from
    <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    It also needs to function as a base class for the concrete
    sub-classes of a Result.

    """
    @abstractmethod
    def __init__(
            self,
            status_code: ResultStatusCode,
            status_sub_code: ResultStatusSubCode,
            status_text: List[str]):

        self._status_code = status_code
        self._status_sub_code = status_sub_code
        self._status_text = status_text


    @property
    def status_code(self) -> ResultStatusCode:
        """
        Gets the status_code value.

        Returns
        -------
        str
            status_code value.
        """
        return self._status_code


    @status_code.setter
    def status_code(self, value: ResultStatusCode):
        """
        Sets the status_code value.

        Parameters
        ----------
        value
            status_code value.
        """
        self._status_code = value



    @property
    def status_sub_code(self) -> ResultStatusSubCode:
        """
        Gets the status_sub_code value.

        Returns
        -------
        str
            status_sub_code value.
        """
        return self._status_sub_code


    @status_sub_code.setter
    def status_sub_code(self, value: ResultStatusSubCode):
        """
        Sets the status_sub_code value.

        Parameters
        ----------
        value
            status_sub_code value.
        """
        self._status_sub_code = value



    @property
    def status_text(self) -> List[str]:
        """
        Gets the status_text value.

        Returns
        -------
        str
            status_text value.
        """
        return self._status_text


    @status_text.setter
    def status_text(self, value: List[str]):
        """
        Sets the status_text value.

        Parameters
        ----------
        value
            status_text value.
        """
        self._status_text = value


    @staticmethod
    def get_result(
            result_element: ET
        ) -> Dict:
        """
        Produces a Result from the given xml representation of a Result.

        Parameters
        ----------
        result_element
            ElementTree representation of a Result from
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

        Returns
        -------
        Dict
            Dict representation of the given ElementTree Result
            as described in
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

        Raises
        ------
        ValueError
            If the given xml is not a valid XML representation of Result.
        """

        result_type = result_element.get(\
            '{http://www.w3.org/2001/XMLSchema-instance}type')

        if result_type == 'DataResult':
            return Result.get_data_result(result_element)

        if result_type == 'FileResult':
            return Result.get_file_result(result_element)

        if result_type == 'QueryDataResult':
            return Result.get_query_result(result_element)

        raise ValueError('Unrecognized Result type = ' + result_type)


    @staticmethod
    def get_status(
            result_element: ET
        ) -> Dict:
        """
        Produces a Dict representation of a Result with the StatusCode and
        SubStatusCode values from the given xml representation of a Result.

        Parameters
        ----------
        result_element
            ElementTree representation of a Result from
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

        Returns
        -------
        Dict
            Dict representation of the given ElementTree Result
            as described in
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>
            containing the StatusCode and SubStatusCode values.

        Raises
        ------
        ValueError
            If the given xml is not a valid XML representation of a
            DataResult.
        """

        return {
            'StatusCode': ResultStatusCode(\
                 result_element.find('ssc:StatusCode', namespaces=NS).text),
            'StatusSubCode': ResultStatusSubCode(\
                 result_element.find('ssc:StatusSubCode', namespaces=NS).text)
        }


    # pylint: disable=too-many-locals
    # pylint: disable=too-many-branches
    @staticmethod
    def get_data_result(
            data_result_element: ET
        ) -> Dict:
        """
        Produces a Dict representation of a DataResult from the given
        xml representation of a DataResult.

        Parameters
        ----------
        data_result_element
            ElementTree representation of a DataResult from
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

        Returns
        -------
        Dict
            Dict representation of the given ElementTree DataResult
            as described in
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

        Raises
        ------
        ValueError
            If the given xml is not a valid XML representation of a
            DataResult.
        """

        result = Result.get_status(data_result_element)

        data_elements = data_result_element.findall('ssc:Data', namespaces=NS)
        if data_elements is not None:
            data_len = len(data_elements)
        else:
            data_len = 0
        result['Data'] = np.empty(data_len, dtype=object)

        for data_i, data_element in enumerate(data_elements):

            result['Data'][data_i] = {
                'Id': data_element.find('ssc:Id', namespaces=NS).text,
            }
            coords_elements = data_element.findall('ssc:Coordinates',
                                                   namespaces=NS)

            if coords_elements is not None:
                coords_len = len(coords_elements)
            else:
                coords_len = 0
            result['Data'][data_i]['Coordinates'] =\
                np.empty(coords_len, dtype=object)

            for coords_i, coords_element in enumerate(coords_elements):

                coord_system = coords_element.find(\
                            'ssc:CoordinateSystem', namespaces=NS).text

                result['Data'][data_i]['Coordinates'][coords_i] = {
                    'CoordinateSystem': CoordinateSystem(coord_system)
                }

                for name in ['X', 'Y', 'Z', 'Latitude', 'Longitude',
                             'LocalTime']:
                    result['Data'][data_i]['Coordinates'][coords_i][name] = \
                        Result._get_data(coords_element, name, float)

            result['Data'][data_i]['Time'] = \
                Result._get_data(data_element, 'Time', datetime)


            b_trace_data_elements = data_element.findall(\
                   'ssc:BTraceData', namespaces=NS)
            if b_trace_data_elements is not None:
                b_trace_data_len = len(b_trace_data_elements)
            else:
                b_trace_data_len = 0

            result['Data'][data_i]['BTraceData'] = \
                np.empty(b_trace_data_len, dtype=object)

            for b_trace_data_i, b_trace_data in \
                enumerate(b_trace_data_elements):

                result['Data'][data_i]['BTraceData'][b_trace_data_i] = {
                    'CoordinateSystem': CoordinateSystem(\
                        b_trace_data.find(\
                            'ssc:CoordinateSystem', namespaces=NS).text),
                    'Hemisphere': Hemisphere(b_trace_data.find(\
                            'ssc:Hemisphere', namespaces=NS).text),
                }
                for name in ['Latitude', 'Longitude', 'ArcLength']:
                    result['Data'][data_i]['BTraceData'][b_trace_data_i][name] = \
                        Result._get_data(b_trace_data, name, float)


            for name in ['RadialLength', 'MagneticStrength',
                         'NeutralSheetDistance', 'BowShockDistance',
                         'MagnetoPauseDistance', 'DipoleLValue',
                         'DipoleInvariantLatitude']:
                result['Data'][data_i][name] = \
                    Result._get_data(data_element, name, float)


            result['Data'][data_i]['SpacecraftRegion'] = \
                Result._get_data(data_element, 'SpacecraftRegion',
                                 SpaceRegion)

            for name in ['BGseX', 'BGseY', 'BGseZ']:
                result['Data'][data_i][name] = \
                    Result._get_data(data_element, name, float)

            for name in ['RadialTracedFootpointRegions',
                         'NorthBTracedFootpointRegions',
                         'SouthBTracedFootpointRegions']:
                result['Data'][data_i][name] = \
                    Result._get_data(data_element, name,
                                     FootpointRegion)

        return result
    # pylint: enable=too-many-locals
    # pylint: enable=too-many-branches


    @staticmethod
    def _get_data(
            data_element: ET,
            name: str,
            value_type: Callable[[str], Any],
        ) -> np.ndarray:
        """
        Produces an np.ndarray(m, dtype=value_type) representation of the
        values of specified element in the given data_element ET.

        Parameters
        ----------
        data_element
            ElementTree representation of a DataResult from
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
        name
            Name of element in data_element to get values of.
        value_type
            Type of values to get.

        Returns
        -------
        np.ndarray
            np.ndarray representation of the specified values from
            data_element.
        """
        data_elements = data_element.findall('ssc:' + name, namespaces=NS)
        if data_elements is not None:
            size = len(data_elements)
        else:
            size = 0
        values = np.empty(size, dtype=value_type)
        for index, value in enumerate(data_elements):
            if value_type is datetime:
                values[index] = dateutil.parser.parse(value.text)
            else:
                values[index] = value_type(value.text)

        return values


    @staticmethod
    def get_file_result(
            file_result_element: ET
        ) -> Dict:
        """
        Produces a Dict representation of a FileResult from the given
        xml representation of a FileResult.

        Parameters
        ----------
        file_result_element
            ElementTree representation of a FileResult from
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

        Returns
        -------
        Dict
            Dict representation of the given ElementTree FileResult
            as described in
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

        Raises
        ------
        ValueError
            If the given xml is not a valid XML representation of a
            FileResult.
        """

        result = Result.get_status(file_result_element)
        result['Files'] = []

        for file_description in file_result_element.findall(\
                'ssc:Files', namespaces=NS):
            result['Files'].append({
                'Name': file_description.find('ssc:Name', namespaces=NS).text,
                'MimeType': file_description.find('ssc:MimeType',
                                                  namespaces=NS).text,
                'Length': int(file_description.find('ssc:Length',
                                                    namespaces=NS).text),
                'LastModified': dateutil.parser.parse(\
                    file_description.find('ssc:LastModified',
                                          namespaces=NS).text)
            })
        return result


    @staticmethod
    def __get_conjunction_description(
            description: ET
        ) -> Dict:

        conjunction = {}

        location = description.find('ssc:Location', namespaces=NS)
        if location is not None:
            conjunction['Location'] = Result.__get_location(location)

        trace_description = description.find('ssc:TraceDescription',
                                             namespaces=NS)
        if trace_description is not None:
            conjunction['TraceDescription'] = \
                Result.__get_trace_description(trace_description)

        return conjunction


    @staticmethod
    def __get_location(
            location: ET
        ) -> Dict:
        """
        Produces a Dict representation of the given Location element's
        value (type or subtype of SurfaceGeographicCoordinates).

        Parameters
        ----------
        location
            Location ET from which to get the value.

        Returns
        -------
        Dict
            Dict representation of the given Location element's value
            (type or subtype of SurfaceGeographicCoordinates).

        Raises
        ------
        ValueError
            If the xsi:type value is unrecognized.
        """

        loc_type = location.get(\
                       '{http://www.w3.org/2001/XMLSchema-instance}type')

        if loc_type == 'RadiusGeographicCoordinates':
            location = {
                'Latitude': float(location.find('ssc:Latitude',
                                                namespaces=NS).text),
                'Longitude': float(location.find('ssc:Longitude',
                                                 namespaces=NS).text),
                'Radius': float(location.find('ssc:Radius',
                                              namespaces=NS).text)
            }
        elif loc_type == 'SurfaceGeographicCoordinates':
            location = {
                'Latitude': float(location.find('ssc:Latitude',
                                                namespaces=NS).text),
                'Longitude': float(location.find('ssc:Longitude',
                                                 namespaces=NS).text),
            }
        else:
            raise ValueError('Unrecongized Location xsi:type = ' + loc_type)

        return location


    @staticmethod
    def __get_trace_description(
            trace_element: ET
        ) -> Dict:
        """
        Produces a Dict representation of the given TraceDescription
        element's value.

        Parameters
        ----------
        trace_element
            TraceDescription ET from which to get the value.

        Returns
        -------
        Dict
            Dict representation of the given TraceDescription element's
            value.
        """

        return {
            'Location': Result.__get_location(\
                trace_element.find('ssc:Location', namespaces=NS)),
            'ArcLength': float(trace_element.find(\
                                   'ssc:ArcLength', namespaces=NS).text),
            'Target': Result.__get_target(\
                                 trace_element.find('ssc:Target',
                                                    namespaces=NS))
        }


    @staticmethod
    def __get_target(
            target: ET
        ) -> Dict:
        """
        Produces a Dict representation of the given Target element's
        value (subtype of TraceTarget).

        Parameters
        ----------
        target
            TraceTarget ET from which to get the value.

        Returns
        -------
        Dict
            Dict representation of the given Target element's value
            (subtype of TraceTarget).

        Raises
        ------
        ValueError
            If the xsi:type value is unrecognized.
        """

        target_type = target.get(\
                          '{http://www.w3.org/2001/XMLSchema-instance}type')

        if target_type == 'GroundStationTarget':
            target = {
                'GroundStation': target.find('ssc:GroundStation',
                                             namespaces=NS).text
            }
        elif target_type == 'SatelliteTarget':
            target = {
                'LeadSatellite': target.find('ssc:LeadSatellite',
                                             namespaces=NS).text,
                'Distance': float(target.find('ssc:Distance',
                                              namespaces=NS).text),
            }
        else:
            raise ValueError('Unrecongized Target xsi:type = ' +
                             target_type)
        return target


    # pylint: disable=too-many-locals
    @staticmethod
    def get_query_result(
            query_result_element: ET
        ) -> Dict:  # pylint: disable=too-many-locals
        """
        Produces a Dict representation of a QueryDataResult from the given
        xml representation of a QueryDataResult.

        Parameters
        ----------
        query_result_element
            ElementTree representation of a QueryDataResult from
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

        Returns
        -------
        Dict
            Dict representation of the given ElementTree QueryDataResult
            as described in
            <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

        Raises
        ------
        ValueError
            If the given xml is not a valid XML representation of a
            QueryResult.
        """

        result = Result.get_status(query_result_element)
        conjunction_elements = query_result_element.findall(\
                                   'ssc:Conjunction', namespaces=NS)
        if conjunction_elements is not None:
            conjunction_len = len(conjunction_elements)
        else:
            conjunction_len = 0

        result['Conjunction'] = np.empty(conjunction_len, dtype=object)

        for conjunction_i, conjunction in enumerate(conjunction_elements):

            time_interval = conjunction.find(\
                                'ssc:TimeInterval', namespaces=NS)
            start = dateutil.parser.parse(\
                        time_interval.find('ssc:Start', namespaces=NS).text)
            end = dateutil.parser.parse(\
                      time_interval.find('ssc:End', namespaces=NS).text)
            sat_description_elements = \
                conjunction.findall('ssc:SatelliteDescription', namespaces=NS)
            if sat_description_elements is not None:
                sat_description_len = len(sat_description_elements)
            else:
                sat_description_len = 0
            sat_descriptions = np.empty(sat_description_len, dtype=object)
            for sat_description_i, sat_description in \
                enumerate(sat_description_elements):

                description_elements = \
                    sat_description.findall('ssc:Description', namespaces=NS)
                if description_elements is not None:
                    description_len = len(description_elements)
                else:
                    description_len = 0
                descriptions = np.empty(description_len, dtype=object)
                for description_i, description in \
                    enumerate(description_elements):

                    descriptions[description_i] = \
                        Result.__get_conjunction_description(description)

                sat_descriptions[sat_description_i] = {
                    'Satellite': sat_description.find(\
                        'ssc:Satellite', namespaces=NS).text,
                    'Description': descriptions
                }

            result['Conjunction'][conjunction_i] = {
                'TimeInterval': {
                    'Start': start,
                    'End': end
                },
                'SatelliteDescription': sat_descriptions
            }

        return result
    # pylint: enable=too-many-locals
