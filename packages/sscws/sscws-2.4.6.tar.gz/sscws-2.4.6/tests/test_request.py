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
Module for unittest of the TimeInterval class.<br>

Copyright &copy; 2020 United States Government as represented by the
National Aeronautics and Space Administration. No copyright is claimed in
the United States under Title 17, U.S.Code. All Other Rights Reserved.
"""

import xml.etree.ElementTree as ET
import unittest
#from datetime import datetime, timezone

from context import sscws  # pylint: disable=unused-import

from sscws.bfieldmodels import *
from sscws.coordinates import *
from sscws.conjunctions import BoxConjunctionArea, ConditionOperator,\
    GroundStationCondition, GroundStationConjunction,\
    Satellite, SatelliteCondition
from sscws.filteroptions import LocationFilterOptions,\
    MappedRegionFilterOptions, RegionFilterOptions, SpaceRegionsFilterOptions
from sscws.formatoptions import FormatOptions
from sscws.outputoptions import BFieldTraceOptions, CoordinateOptions,\
    DistanceFromOptions, LocationFilter, OutputOptions, RegionOptions,\
    ValueOptions
from sscws.regions import Hemisphere, HemisphereRegions
from sscws.request import DataRequest, QueryRequest, SatelliteSpecification
from sscws.timeinterval import TimeInterval
from sscws.tracing import BFieldTraceDirection, TraceCoordinateSystem, TraceType



class TestDataRequest(unittest.TestCase):
    """
    Class for unittest of DataRequest class.
    """

    def __init__(self, *args, **kwargs):
        super(TestDataRequest, self).__init__(*args, **kwargs)
        self.maxDiff = None


    def test_data_request(self):
        """
        Test DataRequest class.
        """

        sats = [SatelliteSpecification('themisa', 2),
                SatelliteSpecification('themisb', 2)]
        b_field_model = BFieldModel(external=Tsyganenko96BFieldModel())
        #b_field_model = BFieldModel(external=Tsyganenko87BFieldModel())
        #b_field_model = None
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
            coord_options, None, None,
            RegionOptions(True, True, True, True),
            ValueOptions(True, True, True, True),
            DistanceFromOptions(True, True, True, True),
            b_field_trace_options
            )

        loc_filter = LocationFilter(0, 100000, True, True)
        loc_filter_options = LocationFilterOptions(True, loc_filter,
                                                   loc_filter, loc_filter,
                                                   loc_filter, loc_filter,
                                                   loc_filter, loc_filter)

        hemisphere_region = HemisphereRegions(True, True)
        trace_regions = MappedRegionFilterOptions(hemisphere_region,
                                                  hemisphere_region,
                                                  hemisphere_region,
                                                  hemisphere_region,
                                                  hemisphere_region,
                                                  True)

        srfo = SpaceRegionsFilterOptions()

        rfo = RegionFilterOptions(srfo, trace_regions, trace_regions)

        format_options = FormatOptions()

        location_request = DataRequest('Example DataRequest',
                                       TimeInterval('2020-10-02T00:00:00Z',
                                                    '2020-10-03T00:00:00Z'),
                                       sats, b_field_model,
                                       output_options, rfo,
                                       loc_filter_options,
                                       format_options)

        location_request_xml_str = \
            ET.tostring(location_request.xml_element()).decode('utf-8')

        #print(location_request_xml_str)

        self.assertEqual(location_request_xml_str, '<DataRequest xmlns="http://sscweb.gsfc.nasa.gov/schema"><Description>Example DataRequest</Description><TimeInterval><Start>2020-10-02T00:00:00+00:00</Start><End>2020-10-03T00:00:00+00:00</End></TimeInterval><BFieldModel><InternalBFieldModel>IGRF</InternalBFieldModel><TraceStopAltitude>100</TraceStopAltitude><ExternalBFieldModel xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="Tsyganenko96BFieldModel"><SolarWindPressure>2.1</SolarWindPressure><DstIndex>-20</DstIndex><ByImf>0.0</ByImf><BzImf>0.0</BzImf></ExternalBFieldModel></BFieldModel><Satellites><Id>themisa</Id><ResolutionFactor>2</ResolutionFactor></Satellites><Satellites><Id>themisb</Id><ResolutionFactor>2</ResolutionFactor></Satellites><OutputOptions><AllLocationFilters>true</AllLocationFilters><MinMaxPoints>2</MinMaxPoints><CoordinateOptions><CoordinateSystem>Gse</CoordinateSystem><Component>X</Component></CoordinateOptions><CoordinateOptions><CoordinateSystem>Gse</CoordinateSystem><Component>Y</Component></CoordinateOptions><CoordinateOptions><CoordinateSystem>Gse</CoordinateSystem><Component>Z</Component></CoordinateOptions><CoordinateOptions><CoordinateSystem>Gse</CoordinateSystem><Component>Lat</Component></CoordinateOptions><CoordinateOptions><CoordinateSystem>Gse</CoordinateSystem><Component>Lon</Component></CoordinateOptions><CoordinateOptions><CoordinateSystem>Gse</CoordinateSystem><Component>Local_Time</Component></CoordinateOptions><RegionOptions><Spacecraft>true</Spacecraft><RadialTracedFootpoint>true</RadialTracedFootpoint><NorthBTracedFootpoint>true</NorthBTracedFootpoint><SouthBTracedFootpoint>true</SouthBTracedFootpoint></RegionOptions><ValueOptions><RadialDistance>true</RadialDistance><BFieldStrength>true</BFieldStrength><DipoleLValue>true</DipoleLValue><DipoleInvLat>true</DipoleInvLat></ValueOptions><DistanceFromOptions><NeutralSheet>true</NeutralSheet><BowShock>true</BowShock><MPause>true</MPause><BGseXYZ>true</BGseXYZ></DistanceFromOptions><BFieldTraceOptions><CoordinateSystem>Geo</CoordinateSystem><Hemisphere>North</Hemisphere><FootpointLatitude>true</FootpointLatitude><FootpointLongitude>true</FootpointLongitude><FieldLineLength>true</FieldLineLength></BFieldTraceOptions><BFieldTraceOptions><CoordinateSystem>Geo</CoordinateSystem><Hemisphere>South</Hemisphere><FootpointLatitude>true</FootpointLatitude><FootpointLongitude>true</FootpointLongitude><FieldLineLength>true</FieldLineLength></BFieldTraceOptions></OutputOptions><RegionFilterOptions><SpaceRegions><InterplanetaryMedium>false</InterplanetaryMedium><DaysideMagnetosheath>false</DaysideMagnetosheath><NightsideMagnetosheath>false</NightsideMagnetosheath><DaysideMagnetosphere>false</DaysideMagnetosphere><NightsideMagnetosphere>false</NightsideMagnetosphere><PlasmaSheet>false</PlasmaSheet><TailLobe>false</TailLobe><HighLatitudeBoundaryLayer>false</HighLatitudeBoundaryLayer><LowLatitudeBoundaryLayer>false</LowLatitudeBoundaryLayer><DaysidePlasmasphere>false</DaysidePlasmasphere><NightsidePlasmasphere>false</NightsidePlasmasphere></SpaceRegions><RadialTraceRegions><Cusp><North>true</North><South>true</South></Cusp><Cleft><North>true</North><South>true</South></Cleft><AuroralOval><North>true</North><South>true</South></AuroralOval><PolarCap><North>true</North><South>true</South></PolarCap><MidLatitude><North>true</North><South>true</South></MidLatitude><LowLatitude>true</LowLatitude></RadialTraceRegions><MagneticTraceRegions><Cusp><North>true</North><South>true</South></Cusp><Cleft><North>true</North><South>true</South></Cleft><AuroralOval><North>true</North><South>true</South></AuroralOval><PolarCap><North>true</North><South>true</South></PolarCap><MidLatitude><North>true</North><South>true</South></MidLatitude><LowLatitude>true</LowLatitude></MagneticTraceRegions></RegionFilterOptions><LocationFilterOptions><AllFilters>true</AllFilters><DistanceFromCenterOfEarth><Minimum>true</Minimum><Maximum>true</Maximum><LowerLimit>0</LowerLimit><UpperLimit>100000</UpperLimit></DistanceFromCenterOfEarth><MagneticFieldStrength><Minimum>true</Minimum><Maximum>true</Maximum><LowerLimit>0</LowerLimit><UpperLimit>100000</UpperLimit></MagneticFieldStrength><DistanceFromNeutralSheet><Minimum>true</Minimum><Maximum>true</Maximum><LowerLimit>0</LowerLimit><UpperLimit>100000</UpperLimit></DistanceFromNeutralSheet><DistanceFromBowShock><Minimum>true</Minimum><Maximum>true</Maximum><LowerLimit>0</LowerLimit><UpperLimit>100000</UpperLimit></DistanceFromBowShock><DistanceFromMagnetopause><Minimum>true</Minimum><Maximum>true</Maximum><LowerLimit>0</LowerLimit><UpperLimit>100000</UpperLimit></DistanceFromMagnetopause><DipoleLValue><Minimum>true</Minimum><Maximum>true</Maximum><LowerLimit>0</LowerLimit><UpperLimit>100000</UpperLimit></DipoleLValue><DipoleInvariantLatitude><Minimum>true</Minimum><Maximum>true</Maximum><LowerLimit>0</LowerLimit><UpperLimit>100000</UpperLimit></DipoleInvariantLatitude></LocationFilterOptions><FormatOptions><DateFormat>yyyy_ddd</DateFormat><TimeFormat>hh_hhhh</TimeFormat><DistanceFormat>IntegerKm</DistanceFormat><DistanceDigits>1</DistanceDigits><DegreeFormat>Decimal</DegreeFormat><DegreeDigits>1</DegreeDigits><LatLonFormat>Lat90Lon360</LatLonFormat><Cdf>false</Cdf><LinesPerPage>55</LinesPerPage></FormatOptions></DataRequest>')


class TestQueryRequest(unittest.TestCase):
    """
    Class for unittest of QueryRequest class.
    """

    def __init__(self, *args, **kwargs):
        super(TestQueryRequest, self).__init__(*args, **kwargs)
        self.maxDiff = None


    def test_data_request(self):
        """
        Test QueryRequest class.
        """

        b_field_model = BFieldModel(external=Tsyganenko96BFieldModel())

        sats = [
            Satellite('themisa', BFieldTraceDirection.SAME_HEMISPHERE),
            #Satellite('themisb', BFieldTraceDirection.SAME_HEMISPHERE),
            #Satellite('themisc', BFieldTraceDirection.SAME_HEMISPHERE),
            #Satellite('themisd', BFieldTraceDirection.SAME_HEMISPHERE),
            #Satellite('themise', BFieldTraceDirection.SAME_HEMISPHERE),
        ]
        satellite_condition = SatelliteCondition(sats, 1)

        box_conjunction_area = BoxConjunctionArea(TraceCoordinateSystem.GEO,
                                                  3.00, 10.00)
        ground_stations = [
            GroundStationConjunction('FSMI', 'THM_Fort Smith',\
                SurfaceGeographicCoordinates(59.98, -111.84),\
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

        conjunction_request = \
            QueryRequest('Example QueryRequest',
                         TimeInterval('2020-10-02T00:00:00Z',
                                      '2020-10-03T00:00:00Z'),
                         ConditionOperator.ALL,
                         conditions)

        conjunction_request_xml_str = \
            ET.tostring(conjunction_request.xml_element()).decode('utf-8')

        #print(conjunction_request_xml_str)

        self.assertEqual(conjunction_request_xml_str, '<QueryRequest xmlns="http://sscweb.gsfc.nasa.gov/schema"><Request><Description>Example QueryRequest</Description><TimeInterval><Start>2020-10-02T00:00:00+00:00</Start><End>2020-10-03T00:00:00+00:00</End></TimeInterval><BFieldModel><InternalBFieldModel>IGRF</InternalBFieldModel><TraceStopAltitude>100</TraceStopAltitude><ExternalBFieldModel xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="Tsyganenko89cBFieldModel"><KeyParameterValues>KP3_3_3</KeyParameterValues></ExternalBFieldModel></BFieldModel><ExecuteOptions><WaitForResult>true</WaitForResult></ExecuteOptions><ResultOptions><IncludeQueryInResult>false</IncludeQueryInResult><QueryResultType>Xml</QueryResultType><TraceCoordinateSystem>Geo</TraceCoordinateSystem><SubSatelliteCoordinateSystem>Geo</SubSatelliteCoordinateSystem><SubSatelliteCoordinateSystemType>Spherical</SubSatelliteCoordinateSystemType></ResultOptions><ConditionOperator>All</ConditionOperator><Conditions xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="SatelliteCondition"><Satellite><Id>themisa</Id><BFieldTraceDirection>SameHemisphere</BFieldTraceDirection></Satellite><SatelliteCombination>1</SatelliteCombination></Conditions><Conditions xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="GroundStationCondition"><GroundStation><Id>FSMI</Id><Name>THM_Fort Smith</Name><Location><Latitude>59.98</Latitude><Longitude>-111.84</Longitude></Location><ConjunctionArea xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="BoxConjunctionArea"><CoordinateSystem>Geo</CoordinateSystem><DeltaLatitude>3.0</DeltaLatitude><DeltaLongitude>10.0</DeltaLongitude></ConjunctionArea></GroundStation><CoordinateSystem xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="TraceCoordinateSystem">Geo</CoordinateSystem><TraceType>BField</TraceType></Conditions></Request></QueryRequest>')


if __name__ == '__main__':
    unittest.main()
