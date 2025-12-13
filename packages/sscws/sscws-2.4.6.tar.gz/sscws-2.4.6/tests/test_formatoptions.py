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
from sscws.formatoptions import FormatOptions
# pylint: enable=import-error



class TestFormatOptions(unittest.TestCase):
    """
    Class for unittest of FormatOptions class.
    """

    def __init__(self, *args, **kwargs):
        super(TestFormatOptions, self).__init__(*args, **kwargs)
        self.maxDiff = None



    def test_format_options(self):
        """
        Test FormatOptions class.
        """

        format_options = FormatOptions()
        format_options_xml_str = \
            ET.tostring(format_options.xml_element()).decode('utf-8')

        #print(format_options_xml_str)
        self.assertEqual(format_options_xml_str, '<FormatOptions><DateFormat>yyyy_ddd</DateFormat><TimeFormat>hh_hhhh</TimeFormat><DistanceFormat>IntegerKm</DistanceFormat><DistanceDigits>1</DistanceDigits><DegreeFormat>Decimal</DegreeFormat><DegreeDigits>1</DegreeDigits><LatLonFormat>Lat90Lon360</LatLonFormat><Cdf>false</Cdf><LinesPerPage>55</LinesPerPage></FormatOptions>')


if __name__ == '__main__':
    unittest.main()
