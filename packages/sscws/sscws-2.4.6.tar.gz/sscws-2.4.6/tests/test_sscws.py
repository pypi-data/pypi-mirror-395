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
# Copyright (c) 2020 United States Government as represented by
# the National Aeronautics and Space Administration. No copyright is
# claimed in the United States under Title 17, U.S.Code. All Other
# Rights Reserved.
#

"""
Module for unittest of the SscWs class.<br>

Copyright &copy; 2020 United States Government as represented by the
National Aeronautics and Space Administration. No copyright is claimed in
the United States under Title 17, U.S.Code. All Other Rights Reserved.
"""

import unittest
from datetime import datetime, timezone

from context import sscws  # pylint: disable=unused-import

from sscws.sscws import SscWs  # pylint: disable=import-error
from sscws.coordinates import CoordinateComponent, CoordinateSystem,\
    SurfaceGeographicCoordinates
from sscws.conjunctions import BoxConjunctionArea, ConditionOperator,\
    GroundStationCondition, GroundStationConjunction,\
    Satellite, SatelliteCondition, TraceCoordinateSystem
from sscws.request import DataRequest, QueryRequest, SatelliteSpecification
from sscws.result import ResultStatusCode, ResultStatusSubCode
from sscws.timeinterval import TimeInterval
from sscws.tracing import BFieldTraceDirection, TraceType



class TestSscWs(unittest.TestCase):
    """
    Class for unittest of SscWs class.
    """

    def __init__(self, *args, **kwargs):
        super(TestSscWs, self).__init__(*args, **kwargs)
        self._ssc = SscWs()
        #self._ssc = SscWs(endpoint='https://sscweb-dev.sci.gsfc.nasa.gov/WS/sscr/2/', disable_ssl_certificate_validation=True)


    def test_get_observatories(self):
        """
        Test for get_observatories function.
        """

        result = self._ssc.get_observatories()

        self.assertEqual(result['HttpStatus'], 200)
        obs = result['Observatory']
        self.assertTrue(len(obs) > 0)
        self.assertTrue(obs[0].get('Id'))
        self.assertTrue(obs[0].get('Name'))
        self.assertTrue(obs[0].get('Resolution'))
        self.assertTrue(obs[0].get('StartTime'))
        self.assertTrue(obs[0].get('EndTime'))
        self.assertTrue(obs[0].get('ResourceId'))

        # the following requires version 2.4.16 on the server
        #result = self._ssc.get_observatories(['ace', 'wind'])

        #self.assertEqual(result['HttpStatus'], 200)
        #obs = result['Observatory']
        #self.assertTrue(len(obs) == 2)
        #self.assertTrue(obs[0].get('Id') == 'ace')


    def test_get_ground_stations(self):
        """
        Test for get_ground_stations function.
        """

        result = self._ssc.get_ground_stations()

        self.assertEqual(result['HttpStatus'], 200)
        gs = result['GroundStation']
        self.assertTrue(len(gs) > 0)
        self.assertTrue(gs[0].get('Id'))
        self.assertTrue(gs[0].get('Name'))
        self.assertTrue(gs[0].get('Location'))
        location = gs[0]['Location']
        self.assertTrue(location.get('Latitude'))
        self.assertTrue(location.get('Longitude'))


    def test_get_client_library_example(self):
        """
        Test for get_client_library_example function.
        """

        result = self._ssc.get_client_library_example('ace', 'Python')
        self.assertTrue(result is not None and len(result) > 0)
        self.assertTrue('from sscws.sscws import SscWs' in result)

        result = self._ssc.get_client_library_example('ace', 'IDL')
        self.assertTrue(result is not None and len(result) > 0)
        self.assertTrue('compile_opt idl2' in result)

        result = self._ssc.get_client_library_example('___', 'IDL')
        self.assertTrue(result is None)


    def test_get_locations_exceptions(self):
        """
        Test for get_locations function exceptions.
        """

        with self.assertRaises(TypeError):
            self._ssc.get_locations()

        #with self.assertRaises(ValueError):
        #    self._ssc.get_locations(['iss'])

        with self.assertRaises(ValueError):
            self._ssc.get_locations(['iss'], ['abc', 'def'])


    def test_get_locations(self):
        """
        Test for get_locations function.
        """

        sats = ['iss']
        time_range = ['2020-01-01T00:00:00Z', '2020-01-01T01:00:00Z']
        coords = [CoordinateSystem.GSE]

        result = self._ssc.get_locations(sats, time_range, coords)

        self.assertEqual(result['HttpStatus'], 200)
        self.assertEqual(result['StatusCode'], 
                         ResultStatusCode.SUCCESS)
        self.assertEqual(result['StatusSubCode'], 
                         ResultStatusSubCode.SUCCESS)
        data = result['Data']
        self.assertEqual(len(data), len(sats))
        for index in range(len(sats)):
            self.assertEqual(data[index]['Id'], sats[index])
            # might want a better test for array values than just size > 0
            self.assertTrue(data[index].get('Time').size > 0)
            coordinates = data[index]['Coordinates']
            self.assertEqual(coordinates[index]['CoordinateSystem'], 
                             coords[index])
            self.assertTrue(coordinates[index].get('X').size > 0)
            self.assertTrue(coordinates[index].get('Y').size > 0)
            self.assertTrue(coordinates[index].get('Z').size > 0)
            self.assertTrue(coordinates[index].get('Latitude').size > 0)
            self.assertTrue(coordinates[index].get('Longitude').size > 0)


    def test_get_conjunctions(self):
        """
        Test for get_conjunctions function.
        """

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

        result = self._ssc.get_conjunctions(query_request)

        self.assertEqual(result['HttpStatus'], 200)
        self.assertEqual(result['StatusCode'], 
                         ResultStatusCode.SUCCESS)
        self.assertEqual(result['StatusSubCode'], 
                         ResultStatusSubCode.SUCCESS)
        conjunctions = result['Conjunction']
        self.assertEqual(len(conjunctions), 7)
        # what else do I want to check ???
        #for conjunction in conjunctions:
        #    conjunction['TimeInterval']
        #    conjunction['SatelliteDescription']


if __name__ == '__main__':
    unittest.main()
