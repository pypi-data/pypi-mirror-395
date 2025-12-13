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
Module defining classes to represent conjunction related classes from
<https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.<br>

Copyright &copy; 2013-2023 United States Government as represented by the
National Aeronautics and Space Administration. No copyright is claimed in
the United States under Title 17, U.S.Code. All Other Rights Reserved.
"""

# pylint: disable=duplicate-code
# pylint: disable=too-many-lines

import xml.etree.ElementTree as ET
from enum import Enum
from abc import ABCMeta
from typing import List

from sscws.coordinates import CoordinateSystem, CoordinateSystemType, \
    SurfaceGeographicCoordinates
from sscws.filteroptions import SpaceRegionsFilterOptions
from sscws.formatoptions import FormatOptions
from sscws.tracing import BFieldTraceDirection, TraceCoordinateSystem, \
    TraceRegions, TraceType


class ConditionOperator(Enum):
    """
    Enumerations representing the ConditionOperator defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    ALL = 'All'
    ANY = 'Any'


class ConjunctionAreaType(Enum):
    """
    Enumerations representing the ConjunctionAreaType defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    GEO_BOX = 'GeoBox'
    GM_BOX = 'GmBox'
    DISTANCE = 'Distance'


class QueryResultType(Enum):
    """
    Enumerations representing the QueryResultType defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    XML = 'Xml'
    LISTING = 'Listing'


class ConjunctionArea(metaclass=ABCMeta):
    """
    Class representing a ConjunctionArea defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Parameters
    ----------
    sub_type
        Sub-type name.
    """
    def __init__(self,
                 sub_type: str):

        self._sub_type = sub_type


    def xml_element(self) -> ET:
        """
        Produces the XML Element representation of this object.

        Returns
        -------
        ET
            XML Element represenation of this object.
        """

        builder = ET.TreeBuilder()
        builder.start('ConjunctionArea', {
            'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
            'xsi:type': self._sub_type + 'ConjunctionArea'
        })
        builder.end('ConjunctionArea')
        return builder.close()


    @property
    def sub_type(self) -> str:
        """
        Gets the sub_type value.

        Returns
        -------
        str
            sub_type value.
        """
        return self._sub_type


    @sub_type.setter
    def sub_type(self, value: str):
        """
        Sets the sub_type value.

        Parameters
        ----------
        value
            new sub_type value.
        """
        self._sub_type = value


class BoxConjunctionArea(ConjunctionArea):
    """
    Class representing a BoxConjunctionArea defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Parameters
    ----------
    coordinate_system
        (Trace) Coordinate system.
    delta_latitude
        Delta Latitude in degrees.
    delta_longitude
        Delta Longitude in degrees.
    """
    def __init__(self,
                 coordinate_system: TraceCoordinateSystem,
                 delta_latitude: float,
                 delta_longitude: float):

        super().__init__('Box')

        self._coordinate_system = coordinate_system
        self._delta_latitude = delta_latitude
        self._delta_longitude = delta_longitude


    @property
    def coordinate_system(self) -> TraceCoordinateSystem:
        """
        Gets the coordinate_system value.

        Returns
        -------
        TraceCoordinateSystem
            coordinate_system value.
        """
        return self._coordinate_system


    @coordinate_system.setter
    def coordinate_system(self, value: TraceCoordinateSystem):
        """
        Sets the coordinate_system value.

        Parameters
        ----------
        value
            new coordinate_system value.
        """
        self._coordinate_system = value


    @property
    def delta_latitude(self) -> float:
        """
        Gets the delta_latitude value.

        Returns
        -------
        float
            delta_latitude value.
        """
        return self._delta_latitude


    @delta_latitude.setter
    def delta_latitude(self, value: float):
        """
        Sets the delta_latitude value.

        Parameters
        ----------
        value
            new delta_latitude value.
        """
        self._delta_latitude = value


    @property
    def delta_longitude(self) -> float:
        """
        Gets the delta_longitude value.

        Returns
        -------
        float
            delta_longitude value.
        """
        return self._delta_longitude


    @delta_longitude.setter
    def delta_longitude(self, value: float):
        """
        Sets the delta_longitude value.

        Parameters
        ----------
        value
            new delta_longitude value.
        """
        self._delta_longitude = value


    def xml_element(self) -> ET:
        """
        Produces the XML Element representation of this object.

        Returns
        -------
        ET
            XML Element represenation of this object.
        """
        xml_element = super().xml_element()

        builder = ET.TreeBuilder()
        builder.start('CoordinateSystem', {})
        builder.data(self._coordinate_system.value)
        builder.end('CoordinateSystem')
        xml_element.append(builder.close())

        builder = ET.TreeBuilder()
        builder.start('DeltaLatitude', {})
        builder.data(str(self._delta_latitude))
        builder.end('DeltaLatitude')
        xml_element.append(builder.close())

        builder = ET.TreeBuilder()
        builder.start('DeltaLongitude', {})
        builder.data(str(self._delta_longitude))
        builder.end('DeltaLongitude')
        xml_element.append(builder.close())

        return xml_element


class DistanceConjunctionArea(ConjunctionArea):
    """
    Class representing a DistanceConjunctionArea defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Parameters
    ----------
    radius
        Radius in km.
    """
    def __init__(self,
                 radius: float):

        super().__init__('Distance')

        self._radius = radius


    @property
    def radius(self) -> float:
        """
        Gets the radius value.

        Returns
        -------
        float
            radius value.
        """
        return self._radius


    @radius.setter
    def radius(self, value: float):
        """
        Sets the radius value.

        Parameters
        ----------
        value
            new radius value.
        """
        self._radius = value


    def xml_element(self) -> ET:
        """
        Produces the XML Element representation of this object.

        Returns
        -------
        ET
            XML Element represenation of this object.
        """
        xml_element = super().xml_element()

        builder = ET.TreeBuilder()
        builder.start('Radius', {})
        builder.data(str(self._radius))
        builder.end('Radius')
        xml_element.append(builder.close())

        return xml_element


class ExecuteOptions:
    """
    Class representing an ExecuteOptions from
    <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Parameters
    ----------
    wait_for_result
        Boolean indicating whether the results are returned in the
        response to this request or whether the results become
        available at a later time.  Currently, a value of
        "false" (and the corresponding ResultEmailAddress
        value below) is ignored.  That is, a client must
        always wait on the result.
    result_email_address
        When wait_for_result is false, e-mail address where a
        "query complete" e-mail message is to be sent.
    """
    def __init__(self,
                 wait_for_result: bool = True,
                 result_email_address: str = None):

        self._wait_for_result = wait_for_result
        self._result_email_address = result_email_address


    @property
    def wait_for_result(self) -> bool:
        """
        Gets the wait_for_result value.

        Returns
        -------
        bool
            wait_for_result value.
        """
        return self._wait_for_result


    @wait_for_result.setter
    def wait_for_result(self, value: bool):
        """
        Sets the wait_for_result value.

        Parameters
        ----------
        value
            new wait_for_result value.
        """
        self._wait_for_result = value


    @property
    def result_email_address(self) -> str:
        """
        Gets the result_email_address value.

        Returns
        -------
        str
            result_email_address value.
        """
        return self._result_email_address


    @result_email_address.setter
    def result_email_address(self, value: str):
        """
        Sets the result_email_address value.

        Parameters
        ----------
        value
            new result_email_address value.
        """
        self._result_email_address = value


    def xml_element(self) -> ET:
        """
        Produces the XML Element representation of this object.

        Returns
        -------
        ET
            XML Element represenation of this object.
        """
        builder = ET.TreeBuilder()

        builder.start('ExecuteOptions', {})
        builder.start('WaitForResult', {})
        builder.data(str(self._wait_for_result).lower())
        builder.end('WaitForResult')

        if self._result_email_address is not None:
            builder.start('ResultEmailAddress', {})
            builder.data(self._result_email_address)
            builder.end('ResultEmailAddress')

        builder.end('ExecuteOptions')

        return builder.close()


class ResultOptions:
    """
    Class representing a RequestOptions from
    <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Parameters
    ----------
    include_query_in_result
        Boolean indicating whether to include a copy of the query in the
        results.
    query_result_type
        Requested QueryResultType
    format_options
        Format options.
    trace_coordinate_system
        Trace coordinate system.
    sub_satellite_coordinate_system
        Sub-satellite coordinate system.
    sub_satellite_coordinate_system_type
        Sub-satellite coordinate system type.
    """
    def __init__(self,
                 include_query_in_result: bool = False,
                 query_result_type: QueryResultType = QueryResultType.XML,
                 format_options: FormatOptions = None,
                 trace_coordinate_system: TraceCoordinateSystem = \
                     TraceCoordinateSystem.GEO,
                 sub_satellite_coordinate_system: CoordinateSystem = \
                     CoordinateSystem.GEO,
                 sub_satellite_coordinate_system_type: CoordinateSystemType = \
                     CoordinateSystemType.SPHERICAL
                ):    # pylint: disable=too-many-arguments

        self._include_query_in_result = include_query_in_result
        self._query_result_type = query_result_type
        self._format_options = format_options
        self._trace_coordinate_system = trace_coordinate_system
        self._sub_satellite_coordinate_system = \
            sub_satellite_coordinate_system
        self._sub_satellite_coordinate_system_type = \
            sub_satellite_coordinate_system_type


    @property
    def include_query_in_result(self) -> bool:
        """
        Gets the include_query_in_result value.

        Returns
        -------
        bool
            include_query_in_result value.
        """
        return self._include_query_in_result


    @include_query_in_result.setter
    def include_query_in_result(self, value: bool):
        """
        Sets the include_query_in_result value.

        Parameters
        ----------
        value
            new include_query_in_result value.
        """
        self._include_query_in_result = value


    @property
    def query_result_type(self) -> QueryResultType:
        """
        Gets the query_result_type value.

        Returns
        -------
        QueryResultType
            query_result_type value.
        """
        return self._query_result_type


    @query_result_type.setter
    def query_result_type(self, value: QueryResultType):
        """
        Sets the query_result_type value.

        Parameters
        ----------
        value
            new query_result_type value.
        """
        self._query_result_type = value


    @property
    def format_options(self) -> FormatOptions:
        """
        Gets the format_options value.

        Returns
        -------
        FormatOptions
            format_options value.
        """
        return self._format_options


    @format_options.setter
    def format_options(self, value: FormatOptions):
        """
        Sets the format_options value.

        Parameters
        ----------
        value
            new format_options value.
        """
        self._format_options = value


    @property
    def trace_coordinate_system(self) -> TraceCoordinateSystem:
        """
        Gets the trace_coordinate_system value.

        Returns
        -------
        TraceCoordinateSystem
            trace_coordinate_system value.
        """
        return self._trace_coordinate_system


    @trace_coordinate_system.setter
    def trace_coordinate_system(self, value: TraceCoordinateSystem):
        """
        Sets the trace_coordinate_system value.

        Parameters
        ----------
        value
            new trace_coordinate_system value.
        """
        self._trace_coordinate_system = value


    @property
    def sub_satellite_coordinate_system(self) -> CoordinateSystem:
        """
        Gets the sub_satellite_coordinate_system value.

        Returns
        -------
        CoordinateSystem
            sub_satellite_coordinate_system value.
        """
        return self._sub_satellite_coordinate_system


    @sub_satellite_coordinate_system.setter
    def sub_satellite_coordinate_system(self, value: CoordinateSystem):
        """
        Sets the sub_satellite_coordinate_system value.

        Parameters
        ----------
        value
            new sub_satellite_coordinate_system value.
        """
        self._sub_satellite_coordinate_system = value


    @property
    def sub_satellite_coordinate_system_type(self) -> CoordinateSystemType:
        """
        Gets the sub_satellite_coordinate_system_type value.

        Returns
        -------
        CoordinateSystemType
            sub_satellite_coordinate_system_type value.
        """
        return self._sub_satellite_coordinate_system_type


    @sub_satellite_coordinate_system_type.setter
    def sub_satellite_coordinate_system_type(self,
                                             value: CoordinateSystemType):
        """
        Sets the sub_satellite_coordinate_system_type value.

        Parameters
        ----------
        value
            new sub_satellite_coordinate_system_type value.
        """
        self._sub_satellite_coordinate_system_type = value


    def xml_element(self) -> ET:
        """
        Produces the XML Element representation of this object.

        Returns
        -------
        ET
            XML Element represenation of this object.
        """
        builder = ET.TreeBuilder()
        builder.start('ResultOptions', {})
        builder.start('IncludeQueryInResult', {})
        builder.data(str(self._include_query_in_result).lower())
        builder.end('IncludeQueryInResult')
        builder.start('QueryResultType', {})
        builder.data(self._query_result_type.value)
        builder.end('QueryResultType')
        builder.end('ResultOptions')
        xml_element = builder.close()

        if self._format_options is not None:
            xml_element.append(self._format_options.xml_element())

        builder = ET.TreeBuilder()
        builder.start('TraceCoordinateSystem', {})
        builder.data(self._trace_coordinate_system.value)
        builder.end('TraceCoordinateSystem')
        xml_element.append(builder.close())

        builder = ET.TreeBuilder()
        builder.start('SubSatelliteCoordinateSystem', {})
        builder.data(self._sub_satellite_coordinate_system.value)
        builder.end('SubSatelliteCoordinateSystem')
        xml_element.append(builder.close())

        builder = ET.TreeBuilder()
        builder.start('SubSatelliteCoordinateSystemType', {})
        builder.data(self._sub_satellite_coordinate_system_type.value)
        builder.end('SubSatelliteCoordinateSystemType')

        xml_element.append(builder.close())

        return xml_element


class Satellite:
    """
    Class representing a Satellite defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Parameters
    ----------
    identifier
        Selected satellite identifier.
    b_field_trace_direction
        Magnetic field tracing direction.  This value is only
        required if magnetic field tracing is specified in a
        RegionCondition.
    """
    def __init__(self,
                 identifier: str,
                 b_field_trace_direction: BFieldTraceDirection = None):

        self._identifier = identifier
        self._b_field_trace_direction = b_field_trace_direction


    def xml_element(self) -> ET:
        """
        Produces the XML Element representation of this object.

        Returns
        -------
        ET
            XML Element represenation of this object.
        """

        builder = ET.TreeBuilder()
        builder.start('Satellite', {})
        builder.start('Id', {})
        builder.data(self._identifier)
        builder.end('Id')
        if self._b_field_trace_direction is not None:
            builder.start('BFieldTraceDirection', {})
            builder.data(self._b_field_trace_direction.value)
            builder.end('BFieldTraceDirection')
        builder.end('Satellite')
        return builder.close()


    @property
    def identifier(self) -> str:
        """
        Gets the identifier value.

        Returns
        -------
        str
            identifier value.
        """
        return self._identifier


    @identifier.setter
    def identifier(self, value: str):
        """
        Sets the identifier value.

        Parameters
        ----------
        value
            new identifier value.
        """
        self._identifier = value


    @property
    def b_field_trace_direction(self) -> BFieldTraceDirection:
        """
        Gets the b_field_trace_direction value.

        Returns
        -------
        str
            b_field_trace_direction value.
        """
        return self._b_field_trace_direction


    @b_field_trace_direction.setter
    def b_field_trace_direction(self, value: BFieldTraceDirection):
        """
        Sets the b_field_trace_direction value.

        Parameters
        ----------
        value
            new b_field_trace_direction value.
        """
        self._b_field_trace_direction = value


class Condition(metaclass=ABCMeta):
    """
    Class representing a Condition defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Parameters
    ----------
    sub_type
        Sub-type name.
    """
    def __init__(self,
                 sub_type: str):

        self._sub_type = sub_type


    def xml_element(self) -> ET:
        """
        Produces the XML Element representation of this object.

        Returns
        -------
        ET
            XML Element represenation of this object.
        """

        builder = ET.TreeBuilder()
        builder.start('Conditions', {
            'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
            'xsi:type': self._sub_type + 'Condition'
        })
        builder.end('Conditions')
        return builder.close()


    @property
    def sub_type(self) -> str:
        """
        Gets the sub_type value.

        Returns
        -------
        str
            sub_type value.
        """
        return self._sub_type


    @sub_type.setter
    def sub_type(self, value: str):
        """
        Sets the sub_type value.

        Parameters
        ----------
        value
            new sub_type value.
        """
        self._sub_type = value


class SatelliteCondition(Condition):
    """
    Class representing a SatelliteCondition defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Parameters
    ----------
    satellite
        Satellites.
    satellite_combination
        The minimum number of satellites that must satisfy this condition.

    Raises
    ------
    ValueError
        If minumum number of satellites is greater than number of
        satellites.
    """
    def __init__(self,
                 satellite: List[Satellite],
                 satellite_combination: int):

        super().__init__('Satellite')

        if satellite_combination > len(satellite):
            raise ValueError('satellite_combination > len(satellite)')

        self._satellite = satellite
        self._satellite_combination = satellite_combination


    def xml_element(self) -> ET:
        """
        Produces the XML Element representation of this object.

        Returns
        -------
        ET
            XML Element represenation of this object.
        """

        xml_element = super().xml_element()

        for sat in self._satellite:
            xml_element.append(sat.xml_element())

        builder = ET.TreeBuilder()
        builder.start('SatelliteCombination', {})
        builder.data(str(self._satellite_combination))
        builder.end('SatelliteCombination')
        xml_element.append(builder.close())

        return xml_element


    @property
    def satellite_combination(self) -> int:
        """
        Gets the satellite_combination value.

        Returns
        -------
        str
            satellite_combination value.
        """
        return self._satellite_combination


    @satellite_combination.setter
    def satellite_combination(self, value: int):
        """
        Sets the satellite_combination value.

        Parameters
        ----------
        value
            new satellite_combination value.
        """
        self._satellite_combination = value


class GroundStation:
    """
    Class representing a GroundStation defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Parameters
    ----------
    identifier
        Ground station idenifier.
    name
        Ground station name.
    location
        Ground station location.
    """
    def __init__(self,
                 identifier: str,
                 name: str,
                 location: SurfaceGeographicCoordinates):

        self._identifier = identifier
        self._name = name
        self._location = location


    def xml_element(self) -> ET:
        """
        Produces the XML Element representation of this object.

        Returns
        -------
        ET
            XML Element represenation of this object.
        """

        builder = ET.TreeBuilder()
        builder.start('GroundStation', {})
        builder.start('Id', {})
        builder.data(self._identifier)
        builder.end('Id')
        builder.start('Name', {})
        builder.data(self._name)
        builder.end('Name')
        builder.end('GroundStation')
        xml_element = builder.close()
        xml_element.append(self._location.xml_element('Location'))

        return xml_element


    @property
    def identifier(self) -> str:
        """
        Gets the identifier value.

        Returns
        -------
        str
            identifier value.
        """
        return self._identifier


    @identifier.setter
    def identifier(self, value: str):
        """
        Sets the identifier value.

        Parameters
        ----------
        value
            new identifier value.
        """
        self._identifier = value


    @property
    def name(self) -> str:
        """
        Gets the name value.

        Returns
        -------
        str
            name value.
        """
        return self._name


    @name.setter
    def name(self, value: str):
        """
        Sets the name value.

        Parameters
        ----------
        value
            new name value.
        """
        self._name = value


    @property
    def location(self) -> SurfaceGeographicCoordinates:
        """
        Gets the location value.

        Returns
        -------
        str
            location value.
        """
        return self._location


    @location.setter
    def location(self, value: SurfaceGeographicCoordinates):
        """
        Sets the location value.

        Parameters
        ----------
        value
            new location value.
        """
        self._location = value


class GroundStationConjunction(GroundStation):
    """
    Class representing a GroundStationConjunction defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Parameters
    ----------
    identifier
        Ground station idenifier.
    name
        Ground station name.
    location
        Ground station location.
    conjunction_area
        Conjunction area.
    """
    def __init__(self,
                 identifier: str,
                 name: str,
                 location: SurfaceGeographicCoordinates,
                 conjunction_area: ConjunctionArea):

        super().__init__(identifier, name, location)

        self._conjunction_area = conjunction_area


    def xml_element(self) -> ET:
        """
        Produces the XML Element representation of this object.

        Returns
        -------
        ET
            XML Element represenation of this object.
        """

        xml_element = super().xml_element()

        xml_element.append(self._conjunction_area.xml_element())

        return xml_element


    @property
    def conjunction_area(self) -> ConjunctionArea:
        """
        Gets the conjunction_area value.

        Returns
        -------
        str
            conjunction_area value.
        """
        return self._conjunction_area


    @conjunction_area.setter
    def conjunction_area(self, value: ConjunctionArea):
        """
        Sets the conjunction_area value.

        Parameters
        ----------
        value
            new conjunction_area value.
        """
        self._conjunction_area = value


class GroundStationCondition(Condition):
    """
    Class representing a GroundStationCondition defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Parameters
    ----------
    ground_station
        1 to 4 GroundStations.
    coordinate_system
        Ground station coordinates system.
    trace_type
        Trace type.

    Raises
    ------
    ValueError
        If number of ground stations is out of range.
    """
    def __init__(self,
                 ground_station: List[GroundStationConjunction],
                 coordinate_system: TraceCoordinateSystem,
                 trace_type: TraceType):

        super().__init__('GroundStation')

        if not ground_station or len(ground_station) > 4:
            raise ValueError('len(ground_station) must be > 0 and < 5')

        self._ground_station = ground_station
        self._coordinate_system = coordinate_system
        self._trace_type = trace_type


    def xml_element(self) -> ET:
        """
        Produces the XML Element representation of this object.

        Returns
        -------
        ET
            XML Element represenation of this object.
        """

        xml_element = super().xml_element()

        for ground_station in self._ground_station:
            xml_element.append(ground_station.xml_element())

        builder = ET.TreeBuilder()
        builder.start('CoordinateSystem', {
            'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
            'xsi:type': 'TraceCoordinateSystem'
        })
        builder.data(self._coordinate_system.value)
        builder.end('CoordinateSystem')
        xml_element.append(builder.close())

        builder = ET.TreeBuilder()
        builder.start('TraceType', {})
        builder.data(self._trace_type.value)
        builder.end('TraceType')
        xml_element.append(builder.close())

        return xml_element


    @property
    def ground_station(self) -> GroundStationConjunction:
        """
        Gets the ground_station value.

        Returns
        -------
        str
            ground_station value.
        """
        return self._ground_station


    @ground_station.setter
    def ground_station(self, value: GroundStationConjunction):
        """
        Sets the ground_station value.

        Parameters
        ----------
        value
            new ground_station value.
        """
        self._ground_station = value


    @property
    def coordinate_system(self) -> CoordinateSystem:
        """
        Gets the coordinate_system value.

        Returns
        -------
        str
            coordinate_system value.
        """
        return self._coordinate_system


    @coordinate_system.setter
    def coordinate_system(self, value: CoordinateSystem):
        """
        Sets the coordinate_system value.

        Parameters
        ----------
        value
            new coordinate_system value.
        """
        self._coordinate_system = value


    @property
    def trace_type(self) -> TraceType:
        """
        Gets the trace_type value.

        Returns
        -------
        str
            trace_type value.
        """
        return self._trace_type


    @trace_type.setter
    def trace_type(self, value: TraceType):
        """
        Sets the trace_type value.

        Parameters
        ----------
        value
            new trace_type value.
        """
        self._trace_type = value


class LeadSatelliteCondition(Condition):
    """
    Class representing a LeadSatelliteCondition defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Parameters
    ----------
    satellite
        Satellites.
    conjunction_area
        Conjunction area.
    trace_type
        Trace type.
    """
    def __init__(self,
                 satellite: List[Satellite],
                 conjunction_area: ConjunctionArea,
                 trace_type: TraceType):

        super().__init__('LeadSatellite')

        self._satellite = satellite
        self._conjunction_area = conjunction_area
        self._trace_type = trace_type


    def xml_element(self) -> ET:
        """
        Produces the XML Element representation of this object.

        Returns
        -------
        ET
            XML Element represenation of this object.
        """

        xml_element = super().xml_element()

        for sat in self._satellite:
            xml_element.append(sat.xml_element())

        xml_element.append(self._conjunction_area.xml_element())

        builder = ET.TreeBuilder()
        builder.start('TraceType', {})
        builder.data(self._trace_type.value)
        builder.end('TraceType')
        xml_element.append(builder.close())

        return xml_element


    @property
    def conjunction_area(self) -> ConjunctionArea:
        """
        Gets the conjunction_area value.

        Returns
        -------
        str
            conjunction_area value.
        """
        return self._conjunction_area


    @conjunction_area.setter
    def conjunction_area(self, value: ConjunctionArea):
        """
        Sets the conjunction_area value.

        Parameters
        ----------
        value
            new conjunction_area value.
        """
        self._conjunction_area = value


    @property
    def trace_type(self) -> TraceType:
        """
        Gets the trace_type value.

        Returns
        -------
        str
            trace_type value.
        """
        return self._trace_type


    @trace_type.setter
    def trace_type(self, value: TraceType):
        """
        Sets the trace_type value.

        Parameters
        ----------
        value
            new trace_type value.
        """
        self._trace_type = value


class RegionCondition(Condition):
    """
    Class representing a RegionCondition defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Parameters
    ----------
    condition_operator
        Operator for combining region conditions.
    space_regions
        Space regions.
    radial_trace_regions
        Radial trace regions.
    b_field_trace_regions
        Magnetic field trace regions.
    """
    def __init__(self,
                 condition_operator: ConditionOperator,
                 space_regions: SpaceRegionsFilterOptions,
                 radial_trace_regions: TraceRegions,
                 b_field_trace_regions: TraceRegions):

        super().__init__('Region')

        self._condition_operator = condition_operator
        self._space_regions = space_regions
        self._radial_trace_regions = radial_trace_regions
        self._b_field_trace_regions = b_field_trace_regions


    def xml_element(self) -> ET:
        """
        Produces the XML Element representation of this object.

        Returns
        -------
        ET
            XML Element represenation of this object.
        """

        xml_element = super().xml_element()

        builder = ET.TreeBuilder()
        builder.start('ConditionOperator', {})
        builder.data(self._condition_operator.value)
        builder.end('ConditionOperator')
        xml_element.append(builder.close())

        if self._space_regions is not None:
            xml_element.append(self._space_regions.xml_element())
        if self._radial_trace_regions is not None:
            xml_element.append(\
                self._radial_trace_regions.xml_element(\
                    'RadialTraceRegions'))
        if self._b_field_trace_regions is not None:
            xml_element.append(\
                self._b_field_trace_regions.xml_element(\
                    'BFieldTraceRegions'))

        return xml_element


    @property
    def condition_operator(self) -> ConditionOperator:
        """
        Gets the condition_operator value.

        Returns
        -------
        str
            condition_operator value.
        """
        return self._condition_operator


    @condition_operator.setter
    def condition_operator(self, value: ConditionOperator):
        """
        Sets the condition_operator value.

        Parameters
        ----------
        value
            new condition_operator value.
        """
        self._condition_operator = value


    @property
    def space_regions(self) -> SpaceRegionsFilterOptions:
        """
        Gets the space_regions value.

        Returns
        -------
        str
            space_regions value.
        """
        return self._space_regions


    @space_regions.setter
    def space_regions(self, value: SpaceRegionsFilterOptions):
        """
        Sets the space_regions value.

        Parameters
        ----------
        value
            new space_regions value.
        """
        self._space_regions = value


    @property
    def radial_trace_regions(self) -> TraceRegions:
        """
        Gets the radial_trace_regions value.

        Returns
        -------
        str
            radial_trace_regions value.
        """
        return self._radial_trace_regions


    @radial_trace_regions.setter
    def radial_trace_regions(self, value: TraceRegions):
        """
        Sets the radial_trace_regions value.

        Parameters
        ----------
        value
            new radial_trace_regions value.
        """
        self._radial_trace_regions = value


    @property
    def b_field_trace_regions(self) -> TraceRegions:
        """
        Gets the b_field_trace_regions value.

        Returns
        -------
        str
            b_field_trace_regions value.
        """
        return self._b_field_trace_regions


    @b_field_trace_regions.setter
    def b_field_trace_regions(self, value: TraceRegions):
        """
        Sets the b_field_trace_regions value.

        Parameters
        ----------
        value
            new b_field_trace_regions value.
        """
        self._b_field_trace_regions = value
