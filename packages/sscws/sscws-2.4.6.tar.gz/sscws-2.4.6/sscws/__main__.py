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
Example Satellite Situation Center (SSC) web services client.
https://sscweb.gsfc.nasa.gov/WebServices/REST/.

Copyright &copy; 2013-2025 United States Government as represented by the
National Aeronautics and Space Administration. No copyright is claimed in
the United States under Title 17, U.S.Code. All Other Rights Reserved.
"""

import sys
import getopt
import json
import xml.etree.ElementTree as ET
import logging
import logging.config
from typing import List
#from datetime import timedelta
import time
import urllib3
import numpy as np


#import matplotlib as mpl
#from mpl_toolkits.mplot3d import Axes3D  # pylint: disable=unused-import
try:
    import matplotlib.pyplot as plt
    PLT_AVAILABLE = True
except ImportError:
    PLT_AVAILABLE = False


from sscws.sscws import SscWs
from sscws.bfieldmodels import BFieldModel, Tsyganenko89cBFieldModel
try:
    from sscws.cdf import Cdf
    CDF_AVAILABLE = True
except ImportError:
    CDF_AVAILABLE = False
from sscws.conjunctions import BoxConjunctionArea, ConditionOperator,\
    GroundStationCondition, GroundStationConjunction,\
    Satellite, SatelliteCondition, TraceCoordinateSystem
from sscws.coordinates import CoordinateComponent, CoordinateSystem,\
    SurfaceGeographicCoordinates
from sscws.filteroptions import LocationFilterOptions,\
    MappedRegionFilterOptions, RegionFilterOptions,\
    SpaceRegionsFilterOptions
#from sscws.formatoptions import CdfFormatOptions
from sscws.outputoptions import CoordinateOptions, BFieldTraceOptions,\
    DistanceFromOptions, LocationFilter, OutputOptions, RegionOptions,\
    ValueOptions
from sscws.regions import Hemisphere, HemisphereRegions
from sscws.request import DataRequest, QueryRequest, SatelliteSpecification
from sscws.timeinterval import TimeInterval
from sscws.tracing import BFieldTraceDirection, TraceType


logging.basicConfig()
LOGGING_CONFIG_FILE = 'logging_config.json'
try:
    with open(LOGGING_CONFIG_FILE, 'r', encoding='utf-8') as fd:
        logging.config.dictConfig(json.load(fd))
except BaseException as exc:    # pylint: disable=broad-except
    if not isinstance(exc, FileNotFoundError):
        print('Logging configuration failed')
        print('Exception: ', exc)
        print('Ignoring failure')
        print()


ENDPOINT = "https://sscweb.gsfc.nasa.gov/WS/sscr/2/"
#ENDPOINT = "http://sscweb-dev.sci.gsfc.nasa.gov/WS/sscr/2/"
#ENDPOINT = "http://localhost:8383/WS/sscr/2/"
#CA_CERTS = '/etc/pki/ca-trust/extracted/openssl/ca-bundle.trust.crt'


def print_usage(
        name: str
    ) -> None:
    """
    Prints program usage information to stdout.

    Parameters
    ----------
    name
        name of this program

    Returns
    -------
    None
    """
    print(f'USAGE: {name} [-e url][-d][-c cacerts][-h]')
    print('WHERE: url = SSC web service endpoint URL')
    print('       -d disables TLS server certificate validation')
    print('       -n disables the use of http caching')
    print('       cacerts = CA certificate filename')


# pylint: disable=too-many-locals,too-many-branches,too-many-statements
def example(
        argv: List[str]
    ) -> None:
    """
    Example Coordinate Data Analysis System (CDAS) web service client.
    Includes example calls to most of the web services.

    Parameters
    ----------
    argv
        Command-line arguments.<br>
        -e url or --endpoint=url where url is the cdas web service endpoint
            URL to use.<br>
        -c url or --cacerts=filename where filename is the name of the file
            containing the CA certificates to use.<br>
        -d or --disable-cert-check to disable verification of the server's
            certificate
        -n or --nocache disables the use of http caching
        -h or --help prints help information.
    """

    try:
        opts = getopt.getopt(argv[1:], 'he:c:dn',
                             ['help', 'endpoint=', 'cacerts=',
                              'disable-cert-check', 'nocache'])[0]
    except getopt.GetoptError:
        print('ERROR: invalid option')
        print_usage(argv[0])
        sys.exit(2)

    endpoint = ENDPOINT
    ca_certs = None
    disable_ssl_certificate_validation = False
    disable_cache = False

    for opt, arg in opts:
        if opt in ('-e', '--endpoint'):
            endpoint = arg
        elif opt in ('-c', '--cacerts'):
            ca_certs = arg
        elif opt in ('-d', '--disable-cert-check'):
            disable_ssl_certificate_validation = True
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        elif opt in ('-n', '--nocache'):
            disable_cache = True
        elif opt in ('-h', '--help'):
            print_usage(argv[0])
            sys.exit()

    ssc = SscWs(endpoint=endpoint, ca_certs=ca_certs,
                disable_ssl_certificate_validation=
                disable_ssl_certificate_validation,
                disable_cache = disable_cache, user_agent='Example')

    #obs_ids = ['ace', 'wind']
    #result = ssc.get_observatories(obs_ids)
    result = ssc.get_observatories()
    if result['HttpStatus'] == 200:
        print('SSC Observatories:')
        for observatory in result['Observatory']:

            print((f"{observatory['Id']:15s} {observatory['Name']:20.20s} "
                   f"{observatory['StartTime'].isoformat():25s}"))
    else:
        print('ssc.get_observatories failed with status = ',
              result['HttpStatus'])
        if 'ErrorMessage' in result:
            print('ErrorMessage = ', result['ErrorMessage'])
            print('ErrorDescription = ', result['ErrorDescription'])
        else:
            print('HttpText = ', result['ErrorText'])


    result = ssc.get_ground_stations()
    if result['HttpStatus'] == 200:
        print('SSC Ground Stations:')
        for ground_station in result['GroundStation']:

            location = ground_station['Location']

            print((f"{ground_station['Id']:5s} {ground_station['Name']:20.20s} "
                   f"{location['Latitude']:7.2f} {location['Longitude']:7.2f}"))
    else:
        print('ssc.get_ground_stations failed with status = ',
              result['HttpStatus'])

    obs_id = 'iss'
    example_interval = ssc.get_example_time_interval(obs_id)
    print('example_interval = ', example_interval)

    # A simple request.
    result = ssc.get_locations(['iss'],
                               ['2020-01-01T00:00:00Z',
                                '2020-01-01T01:00:00Z'])
    #print(result)
    if result['HttpStatus'] == 200:

        if PLT_AVAILABLE:
            figure = plt.figure()
            axis = figure.add_subplot(projection='3d')
            data = result['Data'][0]
            coords = data['Coordinates'][0]
            title = data['Id'] + ' Orbit (' + \
                coords['CoordinateSystem'].value.upper() + ')'
            axis.plot(coords['X'], coords['Y'], coords['Z'], label=title)
            axis.legend()
            plt.show()
        else:
            print('-----------------------------------------------------')
            print('Skipping plot of data because it requires matplotlib.')
            print('To enable plotting, do the following:')
            print('pip install matplotlib')
            print('And the re-run this example.')
            print('-----------------------------------------------------')
        SscWs.print_locations_result(result)
    else:
        print('ssc.get_locations failed with status = ',
              result['HttpStatus'])
    #return

    # A complex data request.
    example_request = create_example_data_request()
    #example_request = create_swarma_btrace_request()
    #print('request:')
    #print(ET.tostring(example_request.xml_element()).decode('utf-8'))
#    example_request.interval.end += timedelta(days=210)
#    while True:
    print('request.interval: ', example_request.interval)
    start = time.time()
    result = ssc.get_locations(example_request)
    end = time.time()
    print('WS time: ', end -start)

    #print('result = ', result)
    if result['HttpStatus'] == 200:
        #pass
        #print('data = ', result['Data'])
        SscWs.print_locations_result(result)
        #locations = ssc.get_locations_from_file(result)
        #print('locations:', locations)
    else:
        print('ssc.get_locations failed with status = ', result['HttpStatus'])
        if 'ErrorMessage' in result:
            print('ErrorMessage = ', result['ErrorMessage'])
            print('ErrorDescription = ', result['ErrorDescription'])
        else:
            print('HttpText = ', result['ErrorText'])
        #print('request:')
        #print(ET.tostring(example_request.xml_element()).decode('utf-8'))
#        break
#        example_request.interval.end += timedelta(days=1)

    try:
        # Repeat request except get the CDF
        #example_request.format_options = CdfFormatOptions()
        #result = ssc.get_locations(example_request)

        print('request.interval: ', example_request.interval)
        start = time.time()
        result = ssc.get_locations2(example_request)
        end = time.time()
        print('WS time: ', end -start)
        #print('result = ', result)
        if result['HttpStatus'] == 200:
            SscWs.print_locations_result(result)
        else:
            print('ssc.get_locations failed with status = ', result['HttpStatus'])
            if 'ErrorMessage' in result:
                print('ErrorMessage = ', result['ErrorMessage'])
                print('ErrorDescription = ', result['ErrorDescription'])
            else:
                print('HttpText = ', result['ErrorText'])
    except ModuleNotFoundError as error:
        print(error)
        print('skipping get_locations2')


    # A conjunction query request
    query_request = create_example_query_request()
    #print('request:')
    #print(ET.tostring(query_request.xml_element()).decode('utf-8'))
    result = ssc.get_conjunctions(query_request)

    if result['HttpStatus'] == 200:
        SscWs.print_conjunction_result(result)
    else:
        print('ssc.get_conjunctions failed with status = ',
              result['HttpStatus'])
        if 'ErrorMessage' in result:
            print('ErrorMessage = ', result['ErrorMessage'])
            print('ErrorDescription = ', result['ErrorDescription'])
        else:
            print('HttpText = ', result['ErrorText'])
        #print('request:')
        #print(ET.tostring(query_request.xml_element()).decode('utf-8'))

# pylint: enable=too-many-locals,too-many-branches,too-many-statements


def test_cdf(
    ) -> None:
    """
    Tests reading an ssc cdf and printing some values.

    """
    cdf = Cdf()
    cdf.open('themisa_20230523085913_101794.cdf')
    #for name in cdf.get_variable_names():
    #    var_info = cdf.get_variable_info(name)
    #    print(var_info)
    #    data = cdf.get_variable_data(name, 0, var_info['Last_Rec'])
    #    print(data)

    stop_altitude = cdf.get_b_trace_stop_altitude()
    print('stop_altitude:', stop_altitude)
    #sat_name = cdf.get_satellite_name()
    #print('sat_name:', sat_name)
    sat_data = cdf.get_satellite_data()
    #print('sat_data:', sat_data)
    result = {
        'Data': np.empty(1, dtype=object)
    }
    result['Data'][0] = sat_data
    #print('result = ', result)
    SscWs.print_locations_result(result)


#########################
def create_swarma_btrace_request(
    ) -> ET:
    """
    Create a swarma b-trace example to debugging problem with
    returned lat/lon values DataRequest.

    Returns
    -------
    ET
        ElementTree representation of an example DataRequest.
    """
    sats = [SatelliteSpecification('swarma', 1)]

    b_field_model = BFieldModel(external=Tsyganenko89cBFieldModel())
    coord_options = [
        CoordinateOptions(CoordinateSystem.GSE, CoordinateComponent.X),
        CoordinateOptions(CoordinateSystem.GSE, CoordinateComponent.Y),
        CoordinateOptions(CoordinateSystem.GSE, CoordinateComponent.Z),
        CoordinateOptions(CoordinateSystem.GSE, CoordinateComponent.LAT),
        CoordinateOptions(CoordinateSystem.GSE, CoordinateComponent.LAT),
        CoordinateOptions(CoordinateSystem.GSE, CoordinateComponent.LON),
        CoordinateOptions(CoordinateSystem.GSE, CoordinateComponent.LOCAL_TIME)
        ]
    b_field_trace_options = [
        BFieldTraceOptions(CoordinateSystem.GEO, Hemisphere.NORTH,
                           True, True, True),
        BFieldTraceOptions(CoordinateSystem.GEO, Hemisphere.SOUTH,
                           True, True, True)
        ]

    output_options = OutputOptions(
        coord_options,
        None, None,
        RegionOptions(True, True, True, True),
        ValueOptions(True, True, True, True),
        DistanceFromOptions(True, True, True, True),
        b_field_trace_options
        )
    loc_filter = LocationFilter(0, 100000, True, True)
    # pylint: disable=unused-variable
    loc_filter_options = \
        LocationFilterOptions(True, loc_filter, loc_filter, loc_filter,
                              loc_filter, loc_filter, loc_filter,
                              loc_filter)
    # pylint: enable=unused-variable

    hemisphere_region = HemisphereRegions(True, True)
    trace_regions = MappedRegionFilterOptions(hemisphere_region,
                                              hemisphere_region,
                                              hemisphere_region,
                                              hemisphere_region,
                                              hemisphere_region,
                                              True)
    srfo = SpaceRegionsFilterOptions(True, True, True, True, True, True,
                                     True, True, True, True, True)

    # pylint: disable=unused-variable
    rfo = RegionFilterOptions(srfo, trace_regions, trace_regions)
    # pylint: enable=unused-variable

    #format_options = CdfFormatOptions()
    format_options = None

    loc_request = DataRequest('swarma b-trace locator request.',
                              TimeInterval('2020-01-01T00:00:00Z',
                                           '2020-01-01T00:10:00Z'),
                              sats, b_field_model,
                              output_options, None,
                              None, format_options)
#                              loc_filter_options)
    return loc_request
#########################

def create_example_data_request(
    ) -> ET:
    """
    Create an example DataRequest.

    Returns
    -------
    ET
        ElementTree representation of an example DataRequest.
    """
    sats = [SatelliteSpecification('themisa', 2),
            SatelliteSpecification('themisb', 2)]
    b_field_model = BFieldModel(external=Tsyganenko89cBFieldModel())
    coord_options = [
        CoordinateOptions(CoordinateSystem.GSE, CoordinateComponent.X),
        CoordinateOptions(CoordinateSystem.GSE, CoordinateComponent.Y),
        CoordinateOptions(CoordinateSystem.GSE, CoordinateComponent.Z),
        CoordinateOptions(CoordinateSystem.GSE, CoordinateComponent.LAT),
        CoordinateOptions(CoordinateSystem.GSE, CoordinateComponent.LON),
        CoordinateOptions(CoordinateSystem.GSE, CoordinateComponent.LOCAL_TIME)
        ]
    b_field_trace_options = [
        BFieldTraceOptions(CoordinateSystem.GEO, Hemisphere.NORTH,
                           True, True, True),
        BFieldTraceOptions(CoordinateSystem.GEO, Hemisphere.SOUTH,
                           True, True, True)
        ]

    output_options = OutputOptions(
        coord_options,
        None, None,
        RegionOptions(True, True, True, True),
        ValueOptions(True, True, True, True),
        DistanceFromOptions(True, True, True, True),
        b_field_trace_options
        )
    loc_filter = LocationFilter(0, 100000, True, True)
    # pylint: disable=unused-variable
    loc_filter_options = \
        LocationFilterOptions(True, loc_filter, loc_filter, loc_filter,
                              loc_filter, loc_filter, loc_filter,
                              loc_filter)
    # pylint: enable=unused-variable

    hemisphere_region = HemisphereRegions(True, True)
    trace_regions = MappedRegionFilterOptions(hemisphere_region,
                                              hemisphere_region,
                                              hemisphere_region,
                                              hemisphere_region,
                                              hemisphere_region,
                                              True)
    srfo = SpaceRegionsFilterOptions(True, True, True, True, True, True,
                                     True, True, True, True, True)

    # pylint: disable=unused-variable
    rfo = RegionFilterOptions(srfo, trace_regions, trace_regions)
    # pylint: enable=unused-variable

    #format_options = CdfFormatOptions()
    format_options = None

    loc_request = DataRequest('Example locator request.',
                              TimeInterval('2020-10-02T00:00:00Z',
                                           '2020-10-02T01:00:00Z'),
                              sats, b_field_model,
                              output_options, None,
                              None, format_options)
#                              loc_filter_options)
    return loc_request


def create_example_query_request(
    ) -> ET:
    """
    Create an example QueryRequest.

    Returns
    -------
    ET
        ElementTree representation of an example QueryRequest.
    """
    # pylint: disable=unused-variable
    b_field_model = BFieldModel(external=Tsyganenko89cBFieldModel())
    # pylint: enable=unused-variable

    sats = [
        Satellite('themisa', BFieldTraceDirection.SAME_HEMISPHERE),
        Satellite('themisb', BFieldTraceDirection.SAME_HEMISPHERE),
        Satellite('themisc', BFieldTraceDirection.SAME_HEMISPHERE),
        Satellite('themisd', BFieldTraceDirection.SAME_HEMISPHERE),
        Satellite('themise', BFieldTraceDirection.SAME_HEMISPHERE)
    ]
    satellite_condition = SatelliteCondition(sats, 2)

    box_conjunction_area = BoxConjunctionArea(TraceCoordinateSystem.GEO,
                                              3.00, 10.00)
    ground_stations = [
        GroundStationConjunction('FSMI', 'THM_Fort Smith',\
            SurfaceGeographicCoordinates(59.98, -111.84),\
            box_conjunction_area),
        GroundStationConjunction('WHOR', 'THM_White Horse',\
            SurfaceGeographicCoordinates(61.01, -135.22),\
            box_conjunction_area),
        GroundStationConjunction('FSIM', 'THM_Fort Simpson',\
            SurfaceGeographicCoordinates(61.80, -121.20),\
            box_conjunction_area),
        GroundStationConjunction('GAK', 'THM_HAARP/Gakona',\
            SurfaceGeographicCoordinates(62.40, -145.20),\
            box_conjunction_area)
    ]
    ground_station_condition = \
        GroundStationCondition(ground_stations,
                               TraceCoordinateSystem.GEO,
                               TraceType.B_FIELD)
    conditions = [
        satellite_condition,
        ground_station_condition
    ]
    query_request = \
        QueryRequest('Magnetic conjunction of at least 2 THEMIS ' +
                     'satellites with one of 4 THEMIS ground ' +
                     'stations during 2008 doy=1-5.',
                     TimeInterval('2008-01-05T10:00:00Z',
                                  '2008-01-05T11:59:59Z'),
                     ConditionOperator.ALL,
                     conditions)

    return query_request


if __name__ == '__main__':
    #test_cdf()
    example(sys.argv)
