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
# Copyright (c) 2018-2023 United States Government as represented by
# the National Aeronautics and Space Administration. No copyright is
# claimed in the United States under Title 17, U.S.Code. All Other
# Rights Reserved.
#


"""
Module defining a class to represent the TimeInterval class from
<https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.<br>

Copyright &copy; 2018-2023 United States Government as represented by the
National Aeronautics and Space Administration. No copyright is claimed in
the United States under Title 17, U.S.Code. All Other Rights Reserved.
"""


import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from typing import Tuple, Union
import dateutil.parser




class TimeInterval:
    """
    A class representing a TimeInterval class from
    <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Parameters
    ----------
    start
        Start time of interval.
    end
        End time of interval.

    Notes
    -----
    Since SSC, and satellite position information in general, uses UTC,
    the resulting start and end properties have a UTC timezone.  If
    the given values' timezone is not UTC, the start/end values are
    adjusted to UTC.  If the given value has no timezone (is naive) a
    UTC value is set.

    Raises
    ------
    ValueError
        If the given start/end datetime values are invalid.
    """
    def __init__(self,
                 start: Union[datetime, str],
                 end: Union[datetime, str]):

        self._start = TimeInterval.get_datetime(start)
        self._end = TimeInterval.get_datetime(end)


    @property
    def start(self) -> datetime:
        """
        Gets the start value.

        Returns
        -------
        datetime
            start value.
        """
        return self._start


    @start.setter
    def start(self, value: Union[datetime, str]):
        """
        Sets the start value.

        Parameters
        ----------
        value
            start datetime value.
        """
        self._start = TimeInterval.get_datetime(value)


    @property
    def end(self) -> datetime:
        """
        Gets the end value.

        Returns
        -------
        datetime
            end value.
        """
        return self._end


    @end.setter
    def end(self, value: Union[datetime, str]):
        """
        Sets the _end value.

        Parameters
        ----------
        value
            end datetime value.
        """
        self._end = TimeInterval.get_datetime(value)


    def xml_element(self) -> ET:
        """
        Produces the XML Element representation of this object.

        Returns
        -------
        ET
            XML Element represenation of this object.
        """
        builder = ET.TreeBuilder()

        builder.start('TimeInterval', {})
        builder.start('Start', {})
        builder.data(self._start.isoformat())
        builder.end('Start')
        builder.start('End', {})
        builder.data(self._end.isoformat())
        builder.end('End')
        builder.end('TimeInterval')

        return builder.close()


    def __str__(self):
        return self._start.isoformat() + ' ' + self._end.isoformat()


    def __eq__(self, other):
        return self._start == other.start and self._end == other.end


    @staticmethod
    def get_datetime(value: Union[datetime, str]) -> datetime:
        """
        Produces a datetime representation of the given value.  The
        returned datetime always has a timezone of timezone.utc.  If
        the given value's timezone is not utc, the return value is
        adjusted to utc.  If the given value has no timezone (is naive)
        a utc value is set.

        Parameters
        ----------
        value
            value to convert to a datetime.
        Returns
        -------
        datetime
            datetime representation of the given value in the UTC
            timezone.
        Raises
        ------
        ValueError
            If the given value is not a valid datetime value.
        """
        if isinstance(value, datetime):
            datetime_value = value
        elif isinstance(value, str):
            datetime_value = dateutil.parser.parse(value)
        else:
            raise ValueError('unrecognized datetime value')

        if datetime_value.tzinfo is None or \
           datetime_value.tzinfo.utcoffset(None) is None:
            return datetime_value.replace(tzinfo=timezone.utc)

        return datetime_value.astimezone(timezone.utc)


    @staticmethod
    def get_datetimes(
            start: Union[datetime, str],
            end: Union[datetime, str]
        ) -> Tuple[datetime, datetime]:
        """
        Produces a datetime representation of the given values.

        Parameters
        ----------
        start
            start value to convert to a datetime.
        end
            end value to convert to a datetime.
        Returns
        -------
        Tuple
            [0] datetime representation of the given start value.
            [1] datetime representation of the given end value.
        Raises
        ------
        ValueError
            If either of the given values is not a valid datetime value.
        """
        try:
            start_datetime = TimeInterval.get_datetime(start)
        except ValueError as exc:
            raise ValueError('unrecognized start datetime value') from exc

        try:
            end_datetime = TimeInterval.get_datetime(end)
        except ValueError as exc:
            raise ValueError('unrecognized end datetime value') from exc

        return start_datetime, end_datetime


    @staticmethod
    def basic_iso_format(value: datetime) -> str:
        """
        Produces the basic (minimal) ISO 8601 format of the given
        datetime.

        Parameters
        ----------
        value
            datetime value to convert to string.
        Returns
        -------
        str
            Basic ISO 8601 format time string.
        """
        return value.isoformat().replace('+00:00', 'Z').translate(
            {ord(i):None for i in ':-'})
