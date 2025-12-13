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
Module defining classes to represent tracing classes from
<https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.<br>

Copyright &copy; 2013-2023 United States Government as represented by the
National Aeronautics and Space Administration. No copyright is claimed in
the United States under Title 17, U.S.Code. All Other Rights Reserved.
"""

# pylint: disable=duplicate-code

import xml.etree.ElementTree as ET
from enum import Enum

from sscws.regions import HemisphereRegions


class BFieldTraceDirection(Enum):
    """
    Enumerations representing the BFieldTraceDirection defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    SAME_HEMISPHERE = 'SameHemisphere'
    OPPOSITE_HEMISPHERE = 'OppositeHemisphere'
    NORTH_HEMISPHERE = 'NorthHemisphere'
    SOUTH_HEMISPHERE = 'SouthHemisphere'
    EITHER_HEMISPHERE = 'EitherHemisphere'


class TraceCoordinateSystem(Enum):
    """
    Enumerations representing the TraceCoordinateSystem defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    GEO = 'Geo'
    GM = 'Gm'


class TraceType(Enum):
    """
    Enumerations representing the TraceType defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    B_FIELD = 'BField'
    RADIAL = 'Radial'


class TraceRegions:
    """
    Class representing a TraceRegions from
    <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Parameters
    ----------
    cusp
        Cusp region.
    cleft
        Cleft region.
    auroral_oval
        Auroral Oval region.
    polar_cap
        Polar Cap region.
    mid_latitude
        Mid-Latitude region.
    low_latitude
        Low-Latitude region.
    """
    def __init__(self,
                 cusp: HemisphereRegions = None,
                 cleft: HemisphereRegions = None,
                 auroral_oval: HemisphereRegions = None,
                 polar_cap: HemisphereRegions = None,
                 mid_latitude: HemisphereRegions = None,
                 low_latitude: bool = None,
                 ):  # pylint: disable=too-many-arguments

        self._cusp = cusp
        self._cleft = cleft
        self._auroral_oval = auroral_oval
        self._polar_cap = polar_cap
        self._mid_latitude = mid_latitude
        self._low_latitude = low_latitude


    @property
    def cusp(self) -> HemisphereRegions:
        """
        Gets the cusp value.

        Returns
        -------
        str
            cusp value.
        """
        return self._cusp


    @cusp.setter
    def cusp(self, value: HemisphereRegions):
        """
        Sets the cusp value.

        Parameters
        ----------
        value
            cusp value.
        """
        self._cusp = value


    @property
    def cleft(self) -> HemisphereRegions:
        """
        Gets the cleft value.

        Returns
        -------
        str
            cleft value.
        """
        return self._cleft


    @cleft.setter
    def cleft(self, value: HemisphereRegions):
        """
        Sets the cleft value.

        Parameters
        ----------
        value
            cleft value.
        """
        self._cleft = value


    @property
    def auroral_oval(self) -> HemisphereRegions:
        """
        Gets the auroral_oval value.

        Returns
        -------
        str
            auroral_oval value.
        """
        return self._auroral_oval


    @auroral_oval.setter
    def auroral_oval(self, value: HemisphereRegions):
        """
        Sets the auroral_oval value.

        Parameters
        ----------
        value
            auroral_oval value.
        """
        self._auroral_oval = value


    @property
    def polar_cap(self) -> HemisphereRegions:
        """
        Gets the polar_cap value.

        Returns
        -------
        str
            polar_cap value.
        """
        return self._polar_cap


    @polar_cap.setter
    def polar_cap(self, value: HemisphereRegions):
        """
        Sets the polar_cap value.

        Parameters
        ----------
        value
            polar_cap value.
        """
        self._polar_cap = value


    @property
    def mid_latitude(self) -> HemisphereRegions:
        """
        Gets the mid_latitude value.

        Returns
        -------
        str
            mid_latitude value.
        """
        return self._mid_latitude


    @mid_latitude.setter
    def mid_latitude(self, value: HemisphereRegions):
        """
        Sets the mid_latitude value.

        Parameters
        ----------
        value
            mid_latitude value.
        """
        self._mid_latitude = value


    @property
    def low_latitude(self) -> bool:
        """
        Gets the low_latitude value.

        Returns
        -------
        str
            low_latitude value.
        """
        return self._low_latitude


    @low_latitude.setter
    def low_latitude(self, value: bool):
        """
        Sets the low_latitude value.

        Parameters
        ----------
        value
            low_latitude value.
        """
        self._low_latitude = value


    def xml_element(self,
                    name: str) -> ET:
        """
        Produces the XML Element representation of this object.

        Parameters
        ----------
        name
            Name of this TraceRegion.

        Returns
        -------
        ET
            XML Element represenation of this object.
        """

        builder = ET.TreeBuilder()
        builder.start(name, {})
        builder.end(name)
        xml_element = builder.close()

        xml_element.append(self._cusp.xml_element('Cusp'))
        xml_element.append(self._cleft.xml_element('Cleft'))
        xml_element.append(self._auroral_oval.xml_element('AuroralOval'))
        xml_element.append(self._polar_cap.xml_element('PolarCap'))
        xml_element.append(self._mid_latitude.xml_element('MidLatitude'))
        builder = ET.TreeBuilder()
        builder.start('LowLatitude', {})
        builder.data(str(self._low_latitude).lower())
        builder.end('LowLatitude')
        xml_element.append(builder.close())

        return xml_element
