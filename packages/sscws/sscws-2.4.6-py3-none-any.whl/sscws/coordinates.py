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
Module defining classes to represent the coordinate related classes from
<https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.<br>

Copyright &copy; 2013-2021 United States Government as represented by the
National Aeronautics and Space Administration. No copyright is claimed in
the United States under Title 17, U.S.Code. All Other Rights Reserved.
"""

import xml.etree.ElementTree as ET
from enum import Enum
from abc import ABCMeta


class CoordinateSystem(Enum):
    """
    Enumerations representing the CoordinateSystem type defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    GEO = 'Geo'
    GM = 'Gm'
    GSE = 'Gse'
    GSM = 'Gsm'
    SM = 'Sm'
    GEI_TOD = 'GeiTod'
    GEI_J_2000 = 'GeiJ2000'

    @classmethod
    def from_identifier(
        cls,
        identifier: str
        ) -> 'CoordinateSystem':
        """
        Gets the Enum corresponding to the given identifier value.

        Parameters
        ----------
        cls
            class.
        identifier
            Enum value corresponding to a CoordinateSystem.
        Returns
        -------
        CoordinateSystem
            Enum corresponding to the given identifier value.
        Raises
        ------
        ValueError
            If the given identifier does not correspond to any
            CoordinateSystem value.
        """

        for member in cls:
            #if member.name == identifier or member.value == identifier:
            if identifier in (member.name, member.value):
                return member
        raise ValueError('Invalid CoordinateSystem identifier ' +
                         identifier)


class CoordinateSystemType(Enum):
    """
    Enumerations representing the CoordinateSystemType defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    SPHERICAL = 'Spherical'
    CARTESIAN = 'Cartesian'


class CoordinateComponent(Enum):
    """
    Enumerations representing the CoordinateComponent defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    X = 'X'
    Y = 'Y'
    Z = 'Z'
    LAT = 'Lat'
    LON = 'Lon'
    LOCAL_TIME = 'Local_Time'


class ProjectionCoordinateSystem(Enum):
    """
    Enumerations representing the ProjectionCoordinateSystem defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    GEO = 'Geo'
    GM = 'Gm'
    SM = 'Sm'


class Coordinates(metaclass=ABCMeta):
    """
    Class representing a Coordinates defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Parameters
    ----------
    sub_type
        Sub-type name.
    """
    def __init__(self,
                 sub_type: str):

        self._sub_type = sub_type


    def xml_element(self,
                    name: str = None) -> ET:
        """
        Produces the XML Element representation of this object.

        Parameters
        ----------
        name
            Element name.  If None, use class sub-type.

        Returns
        -------
        ET
            XML Element represenation of this object.
        """

        if name is not None:
            element_name = name
        else:
            element_name = self._sub_type + 'Coordinates'

        builder = ET.TreeBuilder()
        builder.start(element_name, {})
        builder.end(element_name)
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


class SurfaceGeographicCoordinates(Coordinates):
    """
    Class representing an SurfaceGeographicCoordinates from
    <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Parameters
    ----------
    latitude
        Latitude.
    longitude
        Longitude.

    Raises
    ------
    ValueError
        If the given latitude/longitude values are invalid.
    """
    def __init__(self,
                 latitude: float,
                 longitude: float,
                 sub_type: str = None):

        super().__init__('SurfaceGeographic')

        if sub_type is not None:
            self._sub_type = sub_type

        if latitude < -90.0 or latitude > 90.0:
            raise ValueError('invalid latitude')
        if longitude < -180.0 or longitude > 360.0:
            raise ValueError('invalid longitude')

        self._latitude = latitude
        self._longitude = longitude


    @property
    def latitude(self) -> float:
        """
        Gets the latitude value.

        Returns
        -------
        bool
            latitude value.
        """
        return self._latitude


    @latitude.setter
    def latitude(self, value: float):
        """
        Sets the latitude value.

        Parameters
        ----------
        value
            new latitude value.
        """
        self._latitude = value


    @property
    def longitude(self) -> float:
        """
        Gets the longitude value.

        Returns
        -------
        str
            longitude value.
        """
        return self._longitude


    @longitude.setter
    def longitude(self, value: float):
        """
        Sets the longitude value.

        Parameters
        ----------
        value
            new longitude value.
        """
        self._longitude = value


    def xml_element(self,
                    name: str = None) -> ET:
        """
        Produces the XML Element representation of this object.

        Parameters
        ----------
        name
            Element name.  If None, use class sub-type.

        Returns
        -------
        ET
            XML Element represenation of this object.
        """
        xml_element = super().xml_element(name)

        builder = ET.TreeBuilder()
        builder.start('Latitude', {})
        builder.data(str(self._latitude))
        builder.end('Latitude')
        xml_element.append(builder.close())

        builder = ET.TreeBuilder()
        builder.start('Longitude', {})
        builder.data(str(self._longitude))
        builder.end('Longitude')
        xml_element.append(builder.close())

        return xml_element


class AltitudeGeographicCoordinates(SurfaceGeographicCoordinates):
    """
    Class representing an AltitudeGeographicCoordinates from
    <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Parameters
    ----------
    latitude
        Latitude.
    longitude
        Longitude.
    altitude
        Altitude.

    Raises
    ------
    ValueError
        If the given latitude/longitude values are invalid.
    """
    def __init__(self,
                 latitude: float,
                 longitude: float,
                 altitude: float):

        super().__init__(latitude, longitude, 'AltitudeGeographic')

        self._altitude = altitude


    @property
    def altitude(self) -> float:
        """
        Gets the altitude value.

        Returns
        -------
        bool
            altitude value.
        """
        return self._altitude


    @altitude.setter
    def altitude(self, value: float):
        """
        Sets the altitude value.

        Parameters
        ----------
        value
            new altitude value.
        """
        self._altitude = value


    def xml_element(self,
                    name: str = None) -> ET:
        """
        Produces the XML Element representation of this object.

        Parameters
        ----------
        name
            Element name.  If None, use class sub-type.

        Returns
        -------
        ET
            XML Element represenation of this object.
        """
        xml_element = super().xml_element(name)

        builder = ET.TreeBuilder()
        builder.start('Altitude', {})
        builder.data(str(self._altitude))
        builder.end('Altitude')
        xml_element.append(builder.close())

        return xml_element
