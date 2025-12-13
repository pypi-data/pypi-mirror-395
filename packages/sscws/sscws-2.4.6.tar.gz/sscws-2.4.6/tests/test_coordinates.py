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

from context import sscws  # pylint: disable=unused-import

# pylint: disable=import-error
from sscws.coordinates import SurfaceGeographicCoordinates, \
    AltitudeGeographicCoordinates
# pylint: enable=import-error



#pylint: disable=line-too-long
class TestSurfaceGeographicCoordinates(unittest.TestCase):
    """
    Class for unittest of SurfaceGeographicCoordinates class.
    """

    def __init__(self, *args, **kwargs):
        super(TestSurfaceGeographicCoordinates, self).__init__(*args, **kwargs)
        self.maxDiff = None


    def test_surface_geographic_coordinates(self):
        """
        Test SurfaceGeographicCoordinates class.
        """

        sgc = SurfaceGeographicCoordinates(0.0, 0.0)
        sgc_xml_str = \
            ET.tostring(sgc.xml_element()).decode('utf-8')

        #print(sgc_xml_str)
        self.assertEqual(sgc_xml_str, '<SurfaceGeographicCoordinates><Latitude>0.0</Latitude><Longitude>0.0</Longitude></SurfaceGeographicCoordinates>')


    def test_surface_geographic_coordinates_exceptions(self):

        with self.assertRaises(ValueError):
            SurfaceGeographicCoordinates(-91.0, 0.0)

        with self.assertRaises(ValueError):
            SurfaceGeographicCoordinates(91.0, 0.0)

        with self.assertRaises(ValueError):
            SurfaceGeographicCoordinates(0.0, -181.0)

        with self.assertRaises(ValueError):
            SurfaceGeographicCoordinates(0.0, 361.0)


class TestAltitudeGeographicCoordinates(unittest.TestCase):
    """
    Class for unittest of AltitudeGeographicCoordinates class.
    """

    def __init__(self, *args, **kwargs):
        super(TestAltitudeGeographicCoordinates, self).__init__(*args, **kwargs)
        self.maxDiff = None


    def test_surface_geographic_coordinates(self):
        """
        Test AltitudeGeographicCoordinates class.
        """

        sgc = AltitudeGeographicCoordinates(0.0, 0.0, 0.0)
        sgc_xml_str = \
            ET.tostring(sgc.xml_element()).decode('utf-8')

        #print(sgc_xml_str)
        self.assertEqual(sgc_xml_str, '<AltitudeGeographicCoordinates><Latitude>0.0</Latitude><Longitude>0.0</Longitude><Altitude>0.0</Altitude></AltitudeGeographicCoordinates>')



if __name__ == '__main__':
    unittest.main()
