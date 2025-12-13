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
Module defining classes to represent region classes from
<https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.<br>

Copyright &copy; 2013-2023 United States Government as represented by the
National Aeronautics and Space Administration. No copyright is claimed in
the United States under Title 17, U.S.Code. All Other Rights Reserved.
"""

# pylint: disable=duplicate-code

import xml.etree.ElementTree as ET
from enum import Enum


class FootpointRegion(Enum):
    """
    Enumerations representing the FootpointRegion defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    NOT_APPLICABLE = 'NotApplicable'
    NORTH_CUSP = 'NorthCusp'
    SOUTH_CUSP = 'SouthCusp'
    NORTH_CLEFT = 'NorthCleft'
    SOUTH_CLEFT = 'SouthCleft'
    NORTH_AURORAL_OVAL = 'NorthAuroralOval'
    SOUTH_AURORAL_OVAL = 'SouthAuroralOval'
    NORTH_POLAR_CAP = 'NorthPolarCap'
    SOUTH_POLAR_CAP = 'SouthPolarCap'
    NORTH_MID_LATITUDE = 'NorthMidLatitude'
    SOUTH_MID_LATITUDE = 'SouthMidLatitude'
    LOW_LATITUDE = 'LowLatitude'


    def __str__(self):
        return self.value


    # pylint: disable=too-many-return-statements
    @staticmethod
    def from_code(
            code: int
        ) -> 'FootpointRegion':
        """
        Produces the FootpointRegion Enum corresponding to the given code
        in an SSC CDF.

        Parameters
        ----------
        code
            FootpointRegion value from an SSC CDF.
        Returns
        -------
        FootpointRegion
            Corresponding to the given code.
        Raises
        ------
        ValueError
            If the given code is not a valid FootpointRegion code.
        """

        if code == 0:
            return FootpointRegion.NOT_APPLICABLE
        if code == 1:
            return FootpointRegion.NORTH_CUSP
        if code == 2:
            return FootpointRegion.SOUTH_CUSP
        if code == 3:
            return FootpointRegion.NORTH_CLEFT
        if code == 4:
            return FootpointRegion.SOUTH_CLEFT
        if code == 5:
            return FootpointRegion.NORTH_AURORAL_OVAL
        if code == 6:
            return FootpointRegion.SOUTH_AURORAL_OVAL
        if code == 7:
            return FootpointRegion.NORTH_POLAR_CAP
        if code == 8:
            return FootpointRegion.SOUTH_POLAR_CAP
        if code == 9:
            return FootpointRegion.NORTH_MID_LATITUDE
        if code == 10:
            return FootpointRegion.SOUTH_MID_LATITUDE
        if code == 11:
            return FootpointRegion.LOW_LATITUDE
        raise ValueError('unrecognized FootpointRegion code ' + code)
    # pylint: enable=too-many-return-statements


class Hemisphere(Enum):
    """
    Enumerations representing the Hemisphere defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    SOUTH = 'South'
    NORTH = 'North'

    @classmethod
    def from_identifier(
        cls,
        identifier: str) -> 'Hemisphere':
        """
        Get the Enum corresponding to the given identifier value.

        Parameters
        ----------
        cls
            class.
        identifier
            Enum value corresponding to a Hemisphere.
        Returns
        -------
        Hemisphere
            Enum corresponding to the given identifier value.
        Raises
        ------
        ValueError
            If the given identifier does not correspond to any
            Hemisphere value.
        """

        for member in cls:
            #if member.name == identifier or member.value == identifier:
            if identifier in (member.name, member.value):
                return member
        raise ValueError('Invalid Hemisphere identifier ' + identifier)


class HemisphereRegions:
    """
    Class representing a HemisphereRegions from
    <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Parameters
    ----------
    north
        Northern hemisphere region.
    south
        Southern hemisphere region.
    """
    def __init__(self,
                 north: bool,
                 south: bool):

        self._north = north
        self._south = south


    @property
    def north(self) -> bool:
        """
        Gets the north value.

        Returns
        -------
        str
            north value.
        """
        return self._north


    @north.setter
    def north(self, value: bool):
        """
        Sets the north value.

        Parameters
        ----------
        value
            north value.
        """
        self._north = value


    @property
    def south(self) -> bool:
        """
        Gets the south value.

        Returns
        -------
        str
            south value.
        """
        return self._south


    @south.setter
    def south(self, value: bool):
        """
        Sets the south value.

        Parameters
        ----------
        value
            south value.
        """
        self._south = value


    def xml_element(self,
                    name: str) -> ET:
        """
        Produces the XML Element representation of this object.

        Parameters
        ----------
        name
            Name of Region.

        Returns
        -------
        ET
            XML Element represenation of this object.
        """
        builder = ET.TreeBuilder()

        builder.start(name, {})
        builder.start('North', {})
        builder.data(str(self._north).lower())
        builder.end('North')
        builder.start('South', {})
        builder.data(str(self._south).lower())
        builder.end('South')
        builder.end(name)

        return builder.close()


class SpaceRegion(Enum):
    """
    Enumerations representing the SpaceRegion defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    INTERPLANETARY_MEDIUM = 'InterplanetaryMedium'
    DAYSIDE_MAGNETOSHEATH = 'DaysideMagnetosheath'
    NIGHTSIDE_MAGNETOSHEATH = 'NightsideMagnetosheath'
    DAYSIDE_MAGNETOSPHERE = 'DaysideMagnetosphere'
    NIGHTSIDE_MAGNETOSPHERE = 'NightsideMagnetosphere'
    PLASMA_SHEET = 'PlasmaSheet'
    TAIL_LOBE = 'TailLobe'
    LOW_LATITUDE_BOUNDARY_LAYER = 'LowLatitudeBoundaryLayer'
    HIGH_LATITUDE_BOUNDARY_LAYER = 'HighLatitudeBoundaryLayer'
    DAYSIDE_PLASMASPHERE = 'DaysidePlasmasphere'
    NIGHTSIDE_PLASMASPHERE = 'NightsidePlasmasphere'


    def __str__(self):
        return self.value

    # pylint: disable=too-many-return-statements
    @staticmethod
    def from_code(
            code: int
        ) -> 'SpaceRegion':
        """
        Produces the SpaceRegion Enum corresponding to the given code
        in an SSC CDF.

        Parameters
        ----------
        code
            SpaceRegion value from an SSC CDF.
        Returns
        -------
        SpaceRegion
            Corresponding to the given code.
        Raises
        ------
        ValueError
            If the given code is not a valid SpaceRegion code.
        """

        if code == 1:
            return SpaceRegion.INTERPLANETARY_MEDIUM
        if code == 2:
            return SpaceRegion.DAYSIDE_MAGNETOSHEATH
        if code == 3:
            return SpaceRegion.NIGHTSIDE_MAGNETOSHEATH
        if code == 4:
            return SpaceRegion.DAYSIDE_MAGNETOSPHERE
        if code == 5:
            return SpaceRegion.NIGHTSIDE_MAGNETOSPHERE
        if code == 6:
            return SpaceRegion.PLASMA_SHEET
        if code == 7:
            return SpaceRegion.TAIL_LOBE
        if code == 8:
            return SpaceRegion.LOW_LATITUDE_BOUNDARY_LAYER
        if code == 9:
            return SpaceRegion.HIGH_LATITUDE_BOUNDARY_LAYER
        if code == 10:
            return SpaceRegion.DAYSIDE_PLASMASPHERE
        if code == 11:
            return SpaceRegion.NIGHTSIDE_PLASMASPHERE
        raise ValueError('unrecognized SpaceRegion code ' + code)
    # pylint: enable=too-many-return-statements


class SpaceRegionType(Enum):
    """
    Enumerations representing the SpaceRegionType defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    INTERPLANETARY_MEDIUM = 'InterplanetaryMedium'
    DAYSIDE_MAGNETOSHEATH = 'DaysideMagnetosheath'
    NIGHTSIDE_MAGNETOSHEATH = 'NightsideMagnetosheath'
    DAYSIDE_MAGNETOSPHERE = 'DaysideMagnetosphere'
    NIGHTSIDE_MAGNETOSPHERE = 'NightsideMagnetosphere'
    PLASMA_SHEET = 'PlasmaSheet'
    TAIL_LOBE = 'TailLobe'
    LOW_LATITUDE_BOUNDARY_LAYER = 'LowLatitudeBoundaryLayer'
    HIGH_LATITUDE_BOUNDARY_LAYER = 'HighLatitudeBoundaryLayer'
    DAYSIDE_PLASMASPHERE = 'DaysidePlasmasphere'
    NIGHTSIDE_PLASMASPHERE = 'NightsidePlasmasphere'
