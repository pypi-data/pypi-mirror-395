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
# pylint: disable=import-error
from sscws.outputoptions import OutputOptions, RegionOptions
# pylint: enable=import-error



class TestOutputOptions(unittest.TestCase):
    """
    Class for unittest of OutputOptions class.
    """

    def __init__(self, *args, **kwargs):
        super(TestOutputOptions, self).__init__(*args, **kwargs)
        self.maxDiff = None


    def test_region_options(self):
        """
        Test RegionOptions class.
        """

        region_options = RegionOptions()
        region_options_xml_str = \
            ET.tostring(region_options.xml_element()).decode('utf-8')

        #print(region_options_xml_str)
        self.assertEqual(region_options_xml_str, '<RegionOptions><Spacecraft>false</Spacecraft><RadialTracedFootpoint>false</RadialTracedFootpoint><NorthBTracedFootpoint>false</NorthBTracedFootpoint><SouthBTracedFootpoint>false</SouthBTracedFootpoint></RegionOptions>')

        region_options = RegionOptions(True, True, True, True)
        region_options_xml_str = \
            ET.tostring(region_options.xml_element()).decode('utf-8')

        self.assertEqual(region_options_xml_str, '<RegionOptions><Spacecraft>true</Spacecraft><RadialTracedFootpoint>true</RadialTracedFootpoint><NorthBTracedFootpoint>true</NorthBTracedFootpoint><SouthBTracedFootpoint>true</SouthBTracedFootpoint></RegionOptions>')


#    def test_output_options(self):
#        """
#        Test OutputOptions class.
#        """
#
#        hemisphere_regions = OutputOptions(True, True)
#        hemisphere_regions_xml_str = \
#            ET.tostring(hemisphere_regions.xml_element('MagneticTraceRegions')).decode('utf-8')
#
#        #print(hemisphere_regions_xml_str)
#        self.assertEqual(hemisphere_regions_xml_str, '<MagneticTraceRegions><North>true</North><South>true</South></MagneticTraceRegions>')


if __name__ == '__main__':
    unittest.main()
