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
# Copyright (c) 2021 United States Government as represented by
# the National Aeronautics and Space Administration. No copyright is
# claimed in the United States under Title 17, U.S.Code. All Other
# Rights Reserved.
#

"""
Module for unittest of the TimeInterval class.<br>

Copyright &copy; 2021 United States Government as represented by the
National Aeronautics and Space Administration. No copyright is claimed in
the United States under Title 17, U.S.Code. All Other Rights Reserved.
"""

import xml.etree.ElementTree as ET
import unittest
#from datetime import datetime, timezone
#from typing import List

from context import sscws  # pylint: disable=unused-import

# pylint: disable=import-error
from sscws.bfieldmodels import BFieldModel, Tsyganenko89cBFieldModel
from sscws.conjunctions import BoxConjunctionArea, ConditionOperator, \
    DistanceConjunctionArea, ExecuteOptions, GroundStation, \
    GroundStationCondition, GroundStationConjunction, \
    LeadSatelliteCondition, QueryResultType, \
    RegionCondition, ResultOptions, Satellite, SatelliteCondition
from sscws.coordinates import CoordinateSystem, CoordinateSystemType, \
    SurfaceGeographicCoordinates
from sscws.filteroptions import MappedRegionFilterOptions, \
    SpaceRegionsFilterOptions
from sscws.formatoptions import FormatOptions
from sscws.outputoptions import LocationFilter
from sscws.request import QueryRequest
from sscws.timeinterval import TimeInterval
from sscws.tracing import BFieldTraceDirection, TraceCoordinateSystem, \
    TraceType
# pylint: enable=import-error



#pylint: disable=line-too-long
class TestBoxConjunctionArea(unittest.TestCase):
    """
    Class for unittest of BoxConjunctionArea class.
    """

    def __init__(self, *args, **kwargs):
        super(TestBoxConjunctionArea, self).__init__(*args, **kwargs)
        self.maxDiff = None


    def test_box_conjunction_area(self):
        """
        Test BoxConjunctionArea class.
        """

        box_conjunction_area = BoxConjunctionArea(TraceCoordinateSystem.GEO, 3.00, 10.00)
        box_conjunction_area_xml_str = \
            ET.tostring(box_conjunction_area.xml_element()).decode('utf-8')

        #print(box_conjunction_area_xml_str)
        self.assertEqual(box_conjunction_area_xml_str, '<ConjunctionArea xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="BoxConjunctionArea"><CoordinateSystem>Geo</CoordinateSystem><DeltaLatitude>3.0</DeltaLatitude><DeltaLongitude>10.0</DeltaLongitude></ConjunctionArea>')


class TestDistanceConjunctionArea(unittest.TestCase):
    """
    Class for unittest of DistanceConjunctionArea class.
    """

    def test_distance_conjunction_area(self):
        """
        Test DistanceConjunctionArea class.
        """

        distance_conjunction_area = DistanceConjunctionArea(400.0)
        distance_conjunction_area_xml_str = \
            ET.tostring(distance_conjunction_area.xml_element()).decode('utf-8')

        #print(distance_conjunction_area_xml_str)
        self.assertEqual(distance_conjunction_area_xml_str, '<ConjunctionArea xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="DistanceConjunctionArea"><Radius>400.0</Radius></ConjunctionArea>')


class TestExecuteOptions(unittest.TestCase):
    """
    Class for unittest of ExecuteOptions class.
    """

    def test_execute_options(self):
        """
        Test ExecuteOptions class.
        """

        execute_options = ExecuteOptions()
        execute_options_xml_str = \
            ET.tostring(execute_options.xml_element()).decode('utf-8')

        #print(execute_options_xml_str)
        self.assertEqual(execute_options_xml_str, '<ExecuteOptions><WaitForResult>true</WaitForResult></ExecuteOptions>')


class TestResultOptions(unittest.TestCase):
    """
    Class for unittest of ResultOptions class.
    """

    def test_result_options(self):
        """
        Test ResultOptions class.
        """

        result_options = ResultOptions()
        result_options_xml_str = \
            ET.tostring(result_options.xml_element()).decode('utf-8')

        #print(result_options_xml_str)
        self.assertEqual(result_options_xml_str, '<ResultOptions><IncludeQueryInResult>false</IncludeQueryInResult><QueryResultType>Xml</QueryResultType><TraceCoordinateSystem>Geo</TraceCoordinateSystem><SubSatelliteCoordinateSystem>Geo</SubSatelliteCoordinateSystem><SubSatelliteCoordinateSystemType>Spherical</SubSatelliteCoordinateSystemType></ResultOptions>')

        result_options = ResultOptions(True, QueryResultType.LISTING,
                                       FormatOptions(),
                                       TraceCoordinateSystem.GM,
                                       CoordinateSystem.GM,
                                       CoordinateSystemType.CARTESIAN)
        result_options_xml_str = \
            ET.tostring(result_options.xml_element()).decode('utf-8')

        #print(result_options_xml_str)
        self.assertEqual(result_options_xml_str, '<ResultOptions><IncludeQueryInResult>true</IncludeQueryInResult><QueryResultType>Listing</QueryResultType><FormatOptions><DateFormat>yyyy_ddd</DateFormat><TimeFormat>hh_hhhh</TimeFormat><DistanceFormat>IntegerKm</DistanceFormat><DistanceDigits>1</DistanceDigits><DegreeFormat>Decimal</DegreeFormat><DegreeDigits>1</DegreeDigits><LatLonFormat>Lat90Lon360</LatLonFormat><Cdf>false</Cdf><LinesPerPage>55</LinesPerPage></FormatOptions><TraceCoordinateSystem>Gm</TraceCoordinateSystem><SubSatelliteCoordinateSystem>Gm</SubSatelliteCoordinateSystem><SubSatelliteCoordinateSystemType>Cartesian</SubSatelliteCoordinateSystemType></ResultOptions>')


class TestSatellite(unittest.TestCase):
    """
    Class for unittest of Satellite class.
    """

    def test_satellite(self):
        """
        Test Satellite class.
        """

        satellite = Satellite('themisa')
        satellite_xml_str = \
            ET.tostring(satellite.xml_element()).decode('utf-8')

        #print(satellite_xml_str)
        self.assertEqual(satellite_xml_str, '<Satellite><Id>themisa</Id></Satellite>')

        satellite = Satellite('themisa', 
                               BFieldTraceDirection.SAME_HEMISPHERE)
        satellite_xml_str = \
            ET.tostring(satellite.xml_element()).decode('utf-8')

        #print(satellite_xml_str)
        self.assertEqual(satellite_xml_str, '<Satellite><Id>themisa</Id><BFieldTraceDirection>SameHemisphere</BFieldTraceDirection></Satellite>')


class TestSatelliteCondition(unittest.TestCase):
    """
    Class for unittest of SatelliteCondition class.
    """

    def test_satellite(self):
        """
        Test SatelliteCondition class.
        """

        sats = [
            Satellite('themisa', BFieldTraceDirection.SAME_HEMISPHERE),
            Satellite('themisb', BFieldTraceDirection.SAME_HEMISPHERE),
        ]
        satellite = SatelliteCondition(sats, 1)
        satellite_xml_str = \
            ET.tostring(satellite.xml_element()).decode('utf-8')

        #print(satellite_xml_str)
        self.assertEqual(satellite_xml_str, '<Conditions xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="SatelliteCondition"><Satellite><Id>themisa</Id><BFieldTraceDirection>SameHemisphere</BFieldTraceDirection></Satellite><Satellite><Id>themisb</Id><BFieldTraceDirection>SameHemisphere</BFieldTraceDirection></Satellite><SatelliteCombination>1</SatelliteCombination></Conditions>')


    def test_satellite_condition_exceptions(self):
        """
        Test for construction exceptions.
        """
        sats = [
            Satellite('themisa', BFieldTraceDirection.SAME_HEMISPHERE),
            Satellite('themisb', BFieldTraceDirection.SAME_HEMISPHERE),
        ]
        with self.assertRaises(ValueError):
            SatelliteCondition(sats, 5)


class TestGroundStation(unittest.TestCase):
    """
    Class for unittest of GroundStation class.
    """

    def test_satellite(self):
        """
        Test GroundStation class.
        """

        location = SurfaceGeographicCoordinates(59.98, -111.84)
  
        ground_station = GroundStation('FSMI', 'THM_Fort Smith', 
                                       location)
        ground_station_xml_str = \
            ET.tostring(ground_station.xml_element()).decode('utf-8')

        #print(ground_station_xml_str)
        self.assertEqual(ground_station_xml_str, '<GroundStation><Id>FSMI</Id><Name>THM_Fort Smith</Name><Location><Latitude>59.98</Latitude><Longitude>-111.84</Longitude></Location></GroundStation>')


class TestGroundStationConjunction(unittest.TestCase):
    """
    Class for unittest of GroundStationConjunction class.
    """

    def test_ground_station_conjunction(self):
        """
        Test GroundStationConjunction class.
        """

        location = SurfaceGeographicCoordinates(59.98, -111.84)
  
        box_conjunction_area = BoxConjunctionArea(TraceCoordinateSystem.GEO,
                                                  3.00, 10.00)

        ground_station = GroundStationConjunction('FSMI', 'THM_Fort Smith', 
                                       location, box_conjunction_area)
        ground_station_xml_str = \
            ET.tostring(ground_station.xml_element()).decode('utf-8')

        #print(ground_station_xml_str)
        self.assertEqual(ground_station_xml_str, '<GroundStation><Id>FSMI</Id><Name>THM_Fort Smith</Name><Location><Latitude>59.98</Latitude><Longitude>-111.84</Longitude></Location><ConjunctionArea xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="BoxConjunctionArea"><CoordinateSystem>Geo</CoordinateSystem><DeltaLatitude>3.0</DeltaLatitude><DeltaLongitude>10.0</DeltaLongitude></ConjunctionArea></GroundStation>')


class TestGroundStationCondition(unittest.TestCase):
    """
    Class for unittest of GroundStationCondition class.
    """
    def __init__(self, *args, **kwargs):
        super(TestGroundStationCondition, self).__init__(*args, **kwargs)
        self.maxDiff = None


    def test_ground_station_conjunction(self):
        """
        Test GroundStationCondition class.
        """

        location = SurfaceGeographicCoordinates(59.98, -111.84)
  
        box_conjunction_area = BoxConjunctionArea(TraceCoordinateSystem.GEO,
                                                  3.00, 10.00)

        ground_station = GroundStationConjunction('FSMI', 'THM_Fort Smith', 
                                       location, box_conjunction_area)
        ground_stations = [ground_station]

        ground_station_condition = \
            GroundStationCondition(ground_stations,
                                   TraceCoordinateSystem.GEO,
                                   TraceType.B_FIELD)

        ground_station_condition_xml_str = \
            ET.tostring(ground_station_condition.xml_element()).decode('utf-8')

        #print(ground_station_condition_xml_str)
        self.assertEqual(ground_station_condition_xml_str, '<Conditions xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="GroundStationCondition"><GroundStation><Id>FSMI</Id><Name>THM_Fort Smith</Name><Location><Latitude>59.98</Latitude><Longitude>-111.84</Longitude></Location><ConjunctionArea xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="BoxConjunctionArea"><CoordinateSystem>Geo</CoordinateSystem><DeltaLatitude>3.0</DeltaLatitude><DeltaLongitude>10.0</DeltaLongitude></ConjunctionArea></GroundStation><CoordinateSystem xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="TraceCoordinateSystem">Geo</CoordinateSystem><TraceType>BField</TraceType></Conditions>')


class TestLeadSatelliteCondition(unittest.TestCase):
    """
    Class for unittest of LeadSatelliteCondition class.
    """
    def __init__(self, *args, **kwargs):
        super(TestLeadSatelliteCondition, self).__init__(*args, **kwargs)
        self.maxDiff = None


    def test_satellite(self):
        """
        Test LeadSatelliteCondition class.
        """

        sats = [
            Satellite('themisa', BFieldTraceDirection.SAME_HEMISPHERE),
            Satellite('themisb', BFieldTraceDirection.SAME_HEMISPHERE),
        ]
        conjunction_area = DistanceConjunctionArea(100.0)
        satellite = LeadSatelliteCondition(sats, conjunction_area,
                                           TraceType.RADIAL)
        satellite_xml_str = \
            ET.tostring(satellite.xml_element()).decode('utf-8')

        #print(satellite_xml_str)
        self.assertEqual(satellite_xml_str, '<Conditions xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="LeadSatelliteCondition"><Satellite><Id>themisa</Id><BFieldTraceDirection>SameHemisphere</BFieldTraceDirection></Satellite><Satellite><Id>themisb</Id><BFieldTraceDirection>SameHemisphere</BFieldTraceDirection></Satellite><ConjunctionArea xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="DistanceConjunctionArea"><Radius>100.0</Radius></ConjunctionArea><TraceType>Radial</TraceType></Conditions>')


class TestRegionCondition(unittest.TestCase):
    """
    Class for unittest of RegionCondition class.
    """
    def __init__(self, *args, **kwargs):
        super(TestRegionCondition, self).__init__(*args, **kwargs)
        self.maxDiff = None


    def test_satellite(self):
        """
        Test RegionCondition class.
        """

        space_regions = \
            SpaceRegionsFilterOptions(True, True, True, True, True, True,
                                      True, True, True, True, True)
        location_filter = LocationFilter(1000.0, 1000.0, True, True)
        radial_trace_regions = \
            MappedRegionFilterOptions(location_filter, location_filter,
                                      location_filter, location_filter,
                                      location_filter, True)
        b_field_trace_regions = radial_trace_regions
        region_condition = RegionCondition(ConditionOperator.ANY, 
                                           space_regions,
                                           radial_trace_regions,
                                           b_field_trace_regions)
        region_condition_xml_str = \
            ET.tostring(region_condition.xml_element()).decode('utf-8')

        #print(region_condition_xml_str)
        self.assertEqual(region_condition_xml_str, '<Conditions xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="RegionCondition"><ConditionOperator>Any</ConditionOperator><SpaceRegions><InterplanetaryMedium>true</InterplanetaryMedium><DaysideMagnetosheath>true</DaysideMagnetosheath><NightsideMagnetosheath>true</NightsideMagnetosheath><DaysideMagnetosphere>true</DaysideMagnetosphere><NightsideMagnetosphere>true</NightsideMagnetosphere><PlasmaSheet>true</PlasmaSheet><TailLobe>true</TailLobe><HighLatitudeBoundaryLayer>true</HighLatitudeBoundaryLayer><LowLatitudeBoundaryLayer>true</LowLatitudeBoundaryLayer><DaysidePlasmasphere>true</DaysidePlasmasphere><NightsidePlasmasphere>true</NightsidePlasmasphere></SpaceRegions><RadialTraceRegions><Cusp><Minimum>true</Minimum><Maximum>true</Maximum><LowerLimit>1000.0</LowerLimit><UpperLimit>1000.0</UpperLimit></Cusp><Cleft><Minimum>true</Minimum><Maximum>true</Maximum><LowerLimit>1000.0</LowerLimit><UpperLimit>1000.0</UpperLimit></Cleft><AuroralOval><Minimum>true</Minimum><Maximum>true</Maximum><LowerLimit>1000.0</LowerLimit><UpperLimit>1000.0</UpperLimit></AuroralOval><PolarCap><Minimum>true</Minimum><Maximum>true</Maximum><LowerLimit>1000.0</LowerLimit><UpperLimit>1000.0</UpperLimit></PolarCap><MidLatitude><Minimum>true</Minimum><Maximum>true</Maximum><LowerLimit>1000.0</LowerLimit><UpperLimit>1000.0</UpperLimit></MidLatitude><LowLatitude>true</LowLatitude></RadialTraceRegions><BFieldTraceRegions><Cusp><Minimum>true</Minimum><Maximum>true</Maximum><LowerLimit>1000.0</LowerLimit><UpperLimit>1000.0</UpperLimit></Cusp><Cleft><Minimum>true</Minimum><Maximum>true</Maximum><LowerLimit>1000.0</LowerLimit><UpperLimit>1000.0</UpperLimit></Cleft><AuroralOval><Minimum>true</Minimum><Maximum>true</Maximum><LowerLimit>1000.0</LowerLimit><UpperLimit>1000.0</UpperLimit></AuroralOval><PolarCap><Minimum>true</Minimum><Maximum>true</Maximum><LowerLimit>1000.0</LowerLimit><UpperLimit>1000.0</UpperLimit></PolarCap><MidLatitude><Minimum>true</Minimum><Maximum>true</Maximum><LowerLimit>1000.0</LowerLimit><UpperLimit>1000.0</UpperLimit></MidLatitude><LowLatitude>true</LowLatitude></BFieldTraceRegions></Conditions>')


class TestQueryRequest(unittest.TestCase):
    """
    Class for unittest of QueryRequest class.
    """
    def __init__(self, *args, **kwargs):
        super(TestQueryRequest, self).__init__(*args, **kwargs)
        self.maxDiff = None


    def test_satellite(self):
        """
        Test QueryRequest class.
        """

        b_field_model = BFieldModel(external=Tsyganenko89cBFieldModel())

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
            QueryRequest('Example QueryRequest',
                         TimeInterval('2008-01-05T10:00:00Z',
                                      '2008-01-05T11:59:59Z'),
                         ConditionOperator.ALL,
                         conditions)

        query_request_xml_str = \
            ET.tostring(query_request.xml_element()).decode('utf-8')

        #print(query_request_xml_str)
        self.assertEqual(query_request_xml_str, '<QueryRequest xmlns="http://sscweb.gsfc.nasa.gov/schema"><Request><Description>Example QueryRequest</Description><TimeInterval><Start>2008-01-05T10:00:00+00:00</Start><End>2008-01-05T11:59:59+00:00</End></TimeInterval><BFieldModel><InternalBFieldModel>IGRF</InternalBFieldModel><TraceStopAltitude>100</TraceStopAltitude><ExternalBFieldModel xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="Tsyganenko89cBFieldModel"><KeyParameterValues>KP3_3_3</KeyParameterValues></ExternalBFieldModel></BFieldModel><ExecuteOptions><WaitForResult>true</WaitForResult></ExecuteOptions><ResultOptions><IncludeQueryInResult>false</IncludeQueryInResult><QueryResultType>Xml</QueryResultType><TraceCoordinateSystem>Geo</TraceCoordinateSystem><SubSatelliteCoordinateSystem>Geo</SubSatelliteCoordinateSystem><SubSatelliteCoordinateSystemType>Spherical</SubSatelliteCoordinateSystemType></ResultOptions><ConditionOperator>All</ConditionOperator><Conditions xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="SatelliteCondition"><Satellite><Id>themisa</Id><BFieldTraceDirection>SameHemisphere</BFieldTraceDirection></Satellite><Satellite><Id>themisb</Id><BFieldTraceDirection>SameHemisphere</BFieldTraceDirection></Satellite><Satellite><Id>themisc</Id><BFieldTraceDirection>SameHemisphere</BFieldTraceDirection></Satellite><Satellite><Id>themisd</Id><BFieldTraceDirection>SameHemisphere</BFieldTraceDirection></Satellite><Satellite><Id>themise</Id><BFieldTraceDirection>SameHemisphere</BFieldTraceDirection></Satellite><SatelliteCombination>2</SatelliteCombination></Conditions><Conditions xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="GroundStationCondition"><GroundStation><Id>FSMI</Id><Name>THM_Fort Smith</Name><Location><Latitude>59.98</Latitude><Longitude>-111.84</Longitude></Location><ConjunctionArea xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="BoxConjunctionArea"><CoordinateSystem>Geo</CoordinateSystem><DeltaLatitude>3.0</DeltaLatitude><DeltaLongitude>10.0</DeltaLongitude></ConjunctionArea></GroundStation><GroundStation><Id>WHOR</Id><Name>THM_White Horse</Name><Location><Latitude>61.01</Latitude><Longitude>-135.22</Longitude></Location><ConjunctionArea xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="BoxConjunctionArea"><CoordinateSystem>Geo</CoordinateSystem><DeltaLatitude>3.0</DeltaLatitude><DeltaLongitude>10.0</DeltaLongitude></ConjunctionArea></GroundStation><GroundStation><Id>FSIM</Id><Name>THM_Fort Simpson</Name><Location><Latitude>61.8</Latitude><Longitude>-121.2</Longitude></Location><ConjunctionArea xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="BoxConjunctionArea"><CoordinateSystem>Geo</CoordinateSystem><DeltaLatitude>3.0</DeltaLatitude><DeltaLongitude>10.0</DeltaLongitude></ConjunctionArea></GroundStation><GroundStation><Id>GAK</Id><Name>THM_HAARP/Gakona</Name><Location><Latitude>62.4</Latitude><Longitude>-145.2</Longitude></Location><ConjunctionArea xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="BoxConjunctionArea"><CoordinateSystem>Geo</CoordinateSystem><DeltaLatitude>3.0</DeltaLatitude><DeltaLongitude>10.0</DeltaLongitude></ConjunctionArea></GroundStation><CoordinateSystem xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="TraceCoordinateSystem">Geo</CoordinateSystem><TraceType>BField</TraceType></Conditions></Request></QueryRequest>')



if __name__ == '__main__':
    unittest.main()
