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

from sscws.bfieldmodels import *        # pylint: disable=import-error



class TestTsyganenko96BFieldModel(unittest.TestCase):
    """
    Class for unittest of Tsyganenko96BFieldModel class.
    """

    def __init__(self, *args, **kwargs):
        super(TestTsyganenko96BFieldModel, self).__init__(*args, **kwargs)
        self.maxDiff = None


    def test_tsyganenko96(self):
        """
        Test tsyganenko96 class.
        """

        tsyganenko96_1 = Tsyganenko96BFieldModel()
        tsyganenko96_2 = Tsyganenko96BFieldModel(2.0, -10, 0.1, 0.2)
        tsyganenko96_1_xml_str = \
            ET.tostring(tsyganenko96_1.xml_element()).decode('utf-8')
        tsyganenko96_2_xml_str = \
            ET.tostring(tsyganenko96_2.xml_element()).decode('utf-8')

        self.assertEqual(tsyganenko96_1_xml_str, '<ExternalBFieldModel xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="Tsyganenko96BFieldModel"><SolarWindPressure>2.1</SolarWindPressure><DstIndex>-20</DstIndex><ByImf>0.0</ByImf><BzImf>0.0</BzImf></ExternalBFieldModel>')
        self.assertEqual(tsyganenko96_2_xml_str, '<ExternalBFieldModel xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="Tsyganenko96BFieldModel"><SolarWindPressure>2.0</SolarWindPressure><DstIndex>-10</DstIndex><ByImf>0.1</ByImf><BzImf>0.2</BzImf></ExternalBFieldModel>')

    def test_tsyganenko87(self):
        """
        Test tsyganenko87 class.
        """

        tsyganenko87_1 = Tsyganenko87BFieldModel()
        tsyganenko87_2 = Tsyganenko87BFieldModel(Tsyganenko87Kp.KP_4_4_4)
        tsyganenko87_1_xml_str = \
            ET.tostring(tsyganenko87_1.xml_element()).decode('utf-8')
        tsyganenko87_2_xml_str = \
            ET.tostring(tsyganenko87_2.xml_element()).decode('utf-8')

        self.assertEqual(tsyganenko87_1_xml_str, '<ExternalBFieldModel xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="Tsyganenko87BFieldModel"><KeyParameterValues>KP3_3_3</KeyParameterValues></ExternalBFieldModel>')
        self.assertEqual(tsyganenko87_2_xml_str, '<ExternalBFieldModel xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="Tsyganenko87BFieldModel"><KeyParameterValues>KP4_4_4</KeyParameterValues></ExternalBFieldModel>')

    def test_tsyganenko89c(self):
        """
        Test tsyganenko89c class.
        """

        tsyganenko89c_1 = Tsyganenko89cBFieldModel()
        tsyganenko89c_2 = Tsyganenko89cBFieldModel(Tsyganenko89cKp.KP_4_4_4)
        tsyganenko89c_1_xml_str = \
            ET.tostring(tsyganenko89c_1.xml_element()).decode('utf-8')
        tsyganenko89c_2_xml_str = \
            ET.tostring(tsyganenko89c_2.xml_element()).decode('utf-8')

        self.assertEqual(tsyganenko89c_1_xml_str, '<ExternalBFieldModel xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="Tsyganenko89cBFieldModel"><KeyParameterValues>KP3_3_3</KeyParameterValues></ExternalBFieldModel>')
        self.assertEqual(tsyganenko89c_2_xml_str, '<ExternalBFieldModel xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="Tsyganenko89cBFieldModel"><KeyParameterValues>KP4_4_4</KeyParameterValues></ExternalBFieldModel>')

    def test_bfieldmodel(self):
        """
        Test bfieldmodel class.
        """

        b_field_model_1 = BFieldModel()
        b_field_model_2 = BFieldModel(InternalBFieldModel.SIMPLE_DIPOLE,
                              Tsyganenko96BFieldModel(), 111)

        b_field_model_1_xml_str = \
            ET.tostring(b_field_model_1.xml_element()).decode('utf-8')
        b_field_model_2_xml_str = \
            ET.tostring(b_field_model_2.xml_element()).decode('utf-8')

        self.assertEqual(b_field_model_1_xml_str, '<BFieldModel><InternalBFieldModel>IGRF</InternalBFieldModel><TraceStopAltitude>100</TraceStopAltitude><ExternalBFieldModel xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="Tsyganenko89cBFieldModel"><KeyParameterValues>KP3_3_3</KeyParameterValues></ExternalBFieldModel></BFieldModel>')
        self.assertEqual(b_field_model_2_xml_str, '<BFieldModel><InternalBFieldModel>SimpleDipole</InternalBFieldModel><TraceStopAltitude>111</TraceStopAltitude><ExternalBFieldModel xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="Tsyganenko96BFieldModel"><SolarWindPressure>2.1</SolarWindPressure><DstIndex>-20</DstIndex><ByImf>0.0</ByImf><BzImf>0.0</BzImf></ExternalBFieldModel></BFieldModel>')


if __name__ == '__main__':
    unittest.main()
