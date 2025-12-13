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
# Copyright (c) 2025 United States Government as represented by
# the National Aeronautics and Space Administration. No copyright is
# claimed in the United States under Title 17, U.S.Code. All Other
# Rights Reserved.
#

"""
Module for unittest of the Cdf class.<br>

Copyright &copy; 2025 United States Government as represented by the
National Aeronautics and Space Administration. No copyright is claimed in
the United States under Title 17, U.S.Code. All Other Rights Reserved.
"""

#import xml.etree.ElementTree as ET
import unittest
#from datetime import datetime, timezone

from context import sscws  # pylint: disable=unused-import

from sscws.cdf import Cdf     # pylint: disable=import-error
from sscws.coordinates import CoordinateSystem



class TestCdf(unittest.TestCase):
    """
    Class for unittest of Cdf class.
    """

    def __init__(self, *args, **kwargs):
        super(TestCdf, self).__init__(*args, **kwargs)
        self.maxDiff = None


    def test_cdf(self):
        """
        Test Cdf class.
        """

        cdf = Cdf();
        # simple SSC WS result file
        cdf.open('tests/cluster1_20250408075651_1770126.cdf')
        sat_data = cdf.get_satellite_data()

        #print(sat_data)
        self.assertTrue(sat_data is not None)
        self.assertTrue('Id' in sat_data)
        self.assertEqual(sat_data['Id'], 'cluster1')
        self.assertTrue('Coordinates' in sat_data)
        coords = sat_data['Coordinates'][0]
        self.assertEqual(coords['CoordinateSystem'], CoordinateSystem.GSE)
        x = coords['X']
        #print(x)
        y = coords['Y']
        z = coords['Z']
        self.assertTrue('Time' in sat_data)
        time = sat_data['Time']
        


if __name__ == '__main__':
    unittest.main()
