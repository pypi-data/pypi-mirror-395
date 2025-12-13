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
# Copyright (c) 2013-2021 United States Government as represented by
# the National Aeronautics and Space Administration. No copyright is
# claimed in the United States under Title 17, U.S.Code. All Other
# Rights Reserved.
#

"""
Module defining classes to represent the output format option classes from
<https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.<br>

Copyright &copy; 2013-2021 United States Government as represented by the
National Aeronautics and Space Administration. No copyright is claimed in
the United States under Title 17, U.S.Code. All Other Rights Reserved.
"""

import xml.etree.ElementTree as ET
from enum import Enum


class DateFormat(Enum):
    """
    Enumerations representing the DateFormat defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    YYYY_DDD = 'yyyy_ddd'
    YY_MM_DD = 'yy_mm_dd'
    YY_MMM_DD = 'yy_Mmm_dd'
    YY_CMMM_DD = 'yy_CMMM_dd'


class DegreeFormat(Enum):
    """
    Enumerations representing the DegreeFormat defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    DECIMAL = 'Decimal'
    MINUTES = 'Minutes'
    MINUTES_SECONDS = 'MinutesSeconds'


class DistanceFormat(Enum):
    """
    Enumerations representing the DistanceFormat defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    RE = 'Re'
    KM = 'Km'
    INTEGER_KM = 'IntegerKm'
    SCIENTFIC_NOTATION_KM = 'ScientificNotationKm'


class LatLonFormat(Enum):
    """
    Enumerations representing the LatLonFormat defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    LAT_90_LON_360 = 'Lat90Lon360'
    LAT_90_LON_180 = 'Lat90Lon180'
    LAT_90_SN_LON_180_WE = 'Lat90SnLon180We'


class TimeFormat(Enum):
    """
    Enumerations representing the TimeFormat defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    HH_HHHH = 'hh_hhhh'
    HH_MM_SS = 'hh_mm_ss'
    HH_MM = 'hh_mm'


class FormatOptions:  # pylint: disable=too-many-instance-attributes
    """
    Class representing a FormatOptions type from
    <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Parameters
    ----------
    date_format
        Date format option.  If None, default is DateFormat.YYYY_DDD.
    time_format
        Time format option.  If None, default is TimeForamt.HH_HHHH.
    distance_format
        Distance format option.  If None, default is
        DistanceForamt.INTEGER_KM.
    distance_digits
        Distance digits option.  If None, default is 1.
    degree_format
        Degree format option.  If None, default is DegreeFormat.DECIMAL.
    degree_digits
        Degree digits option.  If None, default is 1.
    lat_lon_format
        Latitude/Longitude format option.  If None, default is
        LatLonFormat.LAT_90_LON_360.
    cdf
        CDF option.  If None, default is False.
    lines_per_page
        Lines per page option.  If None, default is 55.
    """
    def __init__(
            self,
            date_format: DateFormat = None,
            time_format: TimeFormat = None,
            distance_format: DistanceFormat = None,
            distance_digits: int = None,
            degree_format: DegreeFormat = None,
            degree_digits: DegreeFormat = None,
            lat_lon_format: LatLonFormat = None,
            cdf: bool = None,
            lines_per_page: int = None
        ):  # pylint: disable=too-many-arguments,too-many-branches

        if date_format is None:
            self._date_format = DateFormat.YYYY_DDD
        else:
            self._date_format = date_format

        if time_format is None:
            self._time_format = TimeFormat.HH_HHHH
        else:
            self._time_format = time_format

        if distance_format is None:
            self._distance_format = DistanceFormat.INTEGER_KM
        else:
            self._distance_format = distance_format

        if distance_digits is None:
            self._distance_digits = 1
        else:
            self._distance_digits = distance_digits

        if degree_format is None:
            self._degree_format = DegreeFormat.DECIMAL
        else:
            self._degree_format = degree_format

        if degree_digits is None:
            self._degree_digits = 1
        else:
            self._degree_digits = degree_digits

        if lat_lon_format is None:
            self._lat_lon_format = LatLonFormat.LAT_90_LON_360
        else:
            self._lat_lon_format = lat_lon_format

        if cdf is None:
            self._cdf = False
        else:
            self._cdf = cdf

        if lines_per_page is None:
            self._lines_per_page = 55
        else:
            self._lines_per_page = lines_per_page


    @property
    def date_format(self) -> DateFormat:
        """
        Gets the date_format value.

        Returns
        -------
        str
            date_format value.
        """
        return self._date_format


    @date_format.setter
    def date_format(self, value: DateFormat):
        """
        Sets the date_format value.

        Parameters
        ----------
        value
            date_format value.
        """
        self._date_format = value


    @property
    def time_format(self) -> TimeFormat:
        """
        Gets the time_format value.

        Returns
        -------
        str
            time_format value.
        """
        return self._time_format


    @time_format.setter
    def time_format(self, value: TimeFormat):
        """
        Sets the time_format value.

        Parameters
        ----------
        value
            time_format value.
        """
        self._time_format = value


    @property
    def distance_format(self) -> DistanceFormat:
        """
        Gets the distance_format value.

        Returns
        -------
        str
            distance_format value.
        """
        return self._distance_format


    @distance_format.setter
    def distance_format(self, value: DistanceFormat):
        """
        Sets the distance_format value.

        Parameters
        ----------
        value
            distance_format value.
        """
        self._distance_format = value


    @property
    def distance_digits(self) -> int:
        """
        Gets the distance_digits value.

        Returns
        -------
        str
            distance_digits value.
        """
        return self._distance_digits


    @distance_digits.setter
    def distance_digits(self, value: int):
        """
        Sets the distance_digits value.

        Parameters
        ----------
        value
            distance_digits value.
        """
        self._distance_digits = value


    @property
    def degree_format(self) -> DegreeFormat:
        """
        Gets the degree_format value.

        Returns
        -------
        str
            degree_format value.
        """
        return self._degree_format


    @degree_format.setter
    def degree_format(self, value: DegreeFormat):
        """
        Sets the degree_format value.

        Parameters
        ----------
        value
            degree_format value.
        """
        self._degree_format = value


    @property
    def degree_digits(self) -> int:
        """
        Gets the degree_digits value.

        Returns
        -------
        str
            degree_digits value.
        """
        return self._degree_digits


    @degree_digits.setter
    def degree_digits(self, value: int):
        """
        Sets the degree_digits value.

        Parameters
        ----------
        value
            degree_digits value.
        """
        self._degree_digits = value


    @property
    def lat_lon_format(self) -> LatLonFormat:
        """
        Gets the lat_lon_format value.

        Returns
        -------
        str
            lat_lon_format value.
        """
        return self._lat_lon_format


    @lat_lon_format.setter
    def lat_lon_format(self, value: LatLonFormat):
        """
        Sets the lat_lon_format value.

        Parameters
        ----------
        value
            lat_lon_format value.
        """
        self._lat_lon_format = value


    @property
    def cdf(self) -> bool:
        """
        Gets the cdf value.

        Returns
        -------
        str
            cdf value.
        """
        return self._cdf


    @cdf.setter
    def cdf(self, value: bool):
        """
        Sets the cdf value.

        Parameters
        ----------
        value
            cdf value.
        """
        self._cdf = value


    @property
    def lines_per_page(self) -> int:
        """
        Gets the lines_per_page value.

        Returns
        -------
        str
            lines_per_page value.
        """
        return self._lines_per_page


    @lines_per_page.setter
    def lines_per_page(self, value: int):
        """
        Sets the lines_per_page value.

        Parameters
        ----------
        value
            lines_per_page value.
        """
        self._lines_per_page = value


    def xml_element(self) -> ET:
        """
        Produces the XML Element representation of this object.

        Returns
        -------
        ET
            XML Element represenation of this object.
        """

        builder = ET.TreeBuilder()
        builder.start('FormatOptions', {})
        builder.start('DateFormat', {})
        builder.data(self._date_format.value)
        builder.end('DateFormat')
        builder.start('TimeFormat', {})
        builder.data(self._time_format.value)
        builder.end('TimeFormat')
        builder.start('DistanceFormat', {})
        builder.data(self._distance_format.value)
        builder.end('DistanceFormat')
        builder.start('DistanceDigits', {})
        builder.data(str(self._distance_digits))
        builder.end('DistanceDigits')
        builder.start('DegreeFormat', {})
        builder.data(self._degree_format.value)
        builder.end('DegreeFormat')
        builder.start('DegreeDigits', {})
        builder.data(str(self._degree_digits))
        builder.end('DegreeDigits')
        builder.start('LatLonFormat', {})
        builder.data(self._lat_lon_format.value)
        builder.end('LatLonFormat')
        builder.start('Cdf', {})
        builder.data(str(self._cdf).lower())
        builder.end('Cdf')
        builder.start('LinesPerPage', {})
        builder.data(str(self._lines_per_page))
        builder.end('LinesPerPage')
        builder.end('FormatOptions')

        return builder.close()


class CdfFormatOptions(FormatOptions):

    """
    Convenience class representing a FormatOptions object specifying
    CDF format results.
    """
    def __init__(self):
        super().__init__(None, None, DistanceFormat.KM, None, None, None,
                         None, True, None)
