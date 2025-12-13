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

import unittest
from datetime import datetime, timezone

from context import sscws  # pylint: disable=unused-import

from sscws.timeinterval import TimeInterval  # pylint: disable=import-error



class TestTimeInterval(unittest.TestCase):
    """
    Class for unittest of TimeInterval class.
    """

    def __init__(self, *args, **kwargs):
        super(TestTimeInterval, self).__init__(*args, **kwargs)


    def test_get_datetime_exceptions(self):
        """
        Test for get_datetime function exceptions.
        """

        with self.assertRaises(ValueError):
            TimeInterval.get_datetime(123)

        with self.assertRaises(ValueError):
            TimeInterval.get_datetime('bad_datetime')


    def test_get_datetimes_exceptions(self):
        """
        Test for get_datetime function.
        """

        with self.assertRaises(ValueError):
            TimeInterval.get_datetimes('2020-01-01T00:00:00Z', 123)

        with self.assertRaises(ValueError):
            TimeInterval.get_datetimes('2020-01-01T00:00:00Z', 'bad_datetime')


    def test_time_interval_init_exceptions(self):
        """
        Test for TimeInterval construtor exception.
        """

        self.assertEqual(TimeInterval.get_datetime('2019-01-01T00:00:00Z'),
                         datetime(2019, 1, 1, 0, 0, 0, 0, timezone.utc))


    def test_time_interval_eq(self):
        """
        Test for TimeInterval equality operator.
        """

        t_1 = TimeInterval('20190101T000000Z', '2019-01-02T00:00:00Z')
        t_2 = TimeInterval(datetime(2019, 1, 1, 0, 0, 0, 0, timezone.utc),
                           datetime(2019, 1, 2, 0, 0, 0, 0, timezone.utc))

        self.assertEqual(t_1, t_2)


    def test_time_interval_basic_iso_format(self):
        """
        Test TimeInterval.basic_iso_format().
        """

        self.assertEqual(
            TimeInterval.basic_iso_format(
                datetime(2019, 1, 1, 0, 0, 0, 0, timezone.utc)),
            '20190101T000000Z')


    def test_time_interval_str(self):
        """
        Test TimeInterval.str().
        """

        t_1 = TimeInterval(datetime(2019, 1, 1, 0, 0, 0, 0, timezone.utc),
                           datetime(2019, 1, 2, 0, 0, 0, 0, timezone.utc))

        self.assertEqual(str(t_1),
                         '2019-01-01T00:00:00+00:00 2019-01-02T00:00:00+00:00')


    def test_time_interval_get_datetime(self):
        """
        Test TimeInterval get_datetime.
        """

        t_0 = datetime(2019, 1, 1, 0, 0, 0, 0) # no timezone
        t_1 = datetime(2019, 1, 1, 0, 0, 0, 0, timezone.utc)
        t_2 = TimeInterval.get_datetime(t_0)
        utc_offset = t_2 - t_1

        #print('t_2: ', t_2.strftime('%Y-%m-%d %H:%M:%S %Z'))

        # get_datetime should adjust timezone to utc
        self.assertEqual(t_2.tzinfo, timezone.utc)
        self.assertEqual(t_2, t_1 + utc_offset)


    def test_time_interval_properties(self):
        """
        Test TimeInterval properties.
        """

        t_1 = TimeInterval(datetime(2019, 1, 1, 0, 0, 0, 0, timezone.utc),
                           datetime(2019, 1, 2, 0, 0, 0, 0, timezone.utc))

        t_1.start = datetime(2020, 1, 1, 0, 0, 0, 0, timezone.utc)
        t_1.end = datetime(2020, 1, 2, 0, 0, 0, 0, timezone.utc)

        self.assertEqual(t_1.start, datetime(2020, 1, 1, 0, 0, 0, 0, timezone.utc))
        self.assertEqual(t_1.end, datetime(2020, 1, 2, 0, 0, 0, 0, timezone.utc))


if __name__ == '__main__':
    unittest.main()
