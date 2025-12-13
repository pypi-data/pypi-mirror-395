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
# Copyright (c) 2013-2020 United States Government as represented by
# the National Aeronautics and Space Administration. No copyright is
# claimed in the United States under Title 17, U.S.Code. All Other
# Rights Reserved.
#

"""
Module defining classes to represent the mapping classes from
<https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.<br>

Copyright &copy; 2013-2020 United States Government as represented by the
National Aeronautics and Space Administration. No copyright is claimed in
the United States under Title 17, U.S.Code. All Other Rights Reserved.
"""

from enum import Enum


class MapProjection(Enum):
    """
    Enumerations representing the MapProjection defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    AZIMUTHAL = 'Azimuthal'
    CYLINDRICAL = 'Cylindrical'
    MERCATOR = 'Mercator'
    MOLLEWEIDE = 'Molleweide'
    ORTHOGRAPHIC = 'Othographic'
    STEREOGRAPHIC = 'Stereographic'


class MapProjectionTrace(Enum):
    """
    Enumerations representing the MapProjectionTrace defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    B_FIELD_NORTH = 'BFieldNorth'
    B_FIELD_SOUTH = 'BFieldSouth'
    RADIAL = 'Radial'


class MapRegion(Enum):
    """
    Enumerations representing the MapRegion defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    NORTH_CUSP = 'NorthCusp'
    SOUTH_CUSP = 'SouthCusp'
    NORTH_CLEFT = 'NorthCleft'
    SOUTH_CLEFT = 'SouthCleft'
    NORTH_AURORAL_OVAL = 'NorthAuroralOval'
    SOUTH_AURORAL_OVAL = 'SouthOuroralOval'
    NORTH_POLAR_CAP = 'NorthPolarCap'
    SOUTH_POLAR_CAP = 'SouthPolarCap'
    NORTH_MID_LATITUDE = 'NorthMidLatitude'
    SOUTH_MID_LATITUDE = 'SouthMidLatitude'
    LOW_LATITUDE = 'LowLatitude'
    NONE = 'None'


class PolarMapOrientation(Enum):
    """
    Enumerations representing the PolarMapOrientation defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    EQUATORIAL = 'Equatorial'
    NORTH_POLE = 'NorthPole'
    SOUTH_POLE = 'SouthPole'
