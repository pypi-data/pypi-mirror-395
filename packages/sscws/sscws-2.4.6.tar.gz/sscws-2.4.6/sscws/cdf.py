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
# Copyright (c) 2023-2025 United States Government as represented by
# the National Aeronautics and Space Administration. No copyright is
# claimed in the United States under Title 17, U.S.Code. All Other
# Rights Reserved.
#


"""
Module defining a class to represent a Common Data Format (CDF)
<https://cdf.gsfc.nasa.gov/> produced by the Satellite Situation
Center (SSC) <https://sscweb.gsfc.nasa.gov>.  This module is specialized
for SSC CDF files.  It should not be used for more general CDF files.
<br>

Copyright &copy; 2023-2025 United States Government as represented by the
National Aeronautics and Space Administration. No copyright is claimed in
the United States under Title 17, U.S.Code. All Other Rights Reserved.
"""


import re
#from datetime import datetime, timezone
from typing import Dict, List

import numpy as np

#try:
import cdflib
#except ImportError as error:
#    # cdflib >= 1.0 which requires numpy >= 1.20 which requires python >= 3.8
#    from cdflib.dataclasses import (
#        AEDR,
#        VDR,
#        ADRInfo,
#        AttData,
#        CDFInfo,
#        CDRInfo,
#        GDRInfo,
#        VDRInfo,
#    )
#    import dataclasses
#    from cdflib.dataclass import VDRInfo
#    import cdflib.dataclasses.VDRInfo

from sscws.coordinates import CoordinateSystem
from sscws.regions import Hemisphere, FootpointRegion, SpaceRegion


#
# Regular expression pattern to identify CDF variables containing
# X, Y, and Z coordinate values.  The cature group contains the
# coordinate system identifier.
#
XYZ_PATTERN = re.compile(r"XYZ_(TOD|J2000|GEO|GM|GSE|GSM|SM)")

#
# Regular expression pattern to identify CDF variables containing
# component (X, Y, Z, lat, lon, or local-time) values.  The first
# capture group contains the coordinate system identifer.  The
# second capture group contains the component identifer.
#
COMPONENT_PATTERN = re.compile(
            r"(TOD|J2000|GEO|GM|GSE|GSM|SM)_(X|Y|Z|LAT|LON|LCT_T)")

#
# Regular expression pattern to identify CDF variables containing
# B Trace values (North/South, GEO/GM, lat/lon/arc-length).  The
# first capture group contains the North/South hemisphere value.
# The second capture group contains the coordinate system
# identifier.  The third capture group contains the component
# identifier.
#
B_TRACE_PATTERN = re.compile(
            r"(North|South)Btrace_(GEO|GM)_(LAT|LON|ARCLEN)")

#
# Regular expression pattern to capture the B Trace stop altitude
# value contained in the TEXT global attribute entries.  The
# first capture group contains the stop altitude value.
#
B_TRACE_STOP_ALTITUDE_PATTERN = re.compile(
            r"\s+Stop trace altitude \(km\):\s+(\d+\.\d+)")




class Cdf:
    """
    A class representing a CDF file produced by
    <https://sscweb.gsfc.nasa.gov/>.  Note that this class is specialized
    for SSC CDF files.  It should not be used for more general CDF files.
    This class only supports reading the file and does not support 
    writing to the CDF file.
    """
    def __init__(self):
        self._filename = None
        self._cdf = None
        self._info = None
        self._global_attributes = None


    @property
    def filename(self) -> str:
        """
        Gets the filename value.

        Returns
        -------
        str
            filename value.
        """
        return self._filename


    def open(
            self,
            name: str
        ) -> None:
        """
        Opens the specified file for reading.

        Parameters
        ----------
        name
            Name of CDF file to open.

        Raises
        ------
        FileNotFound
            If the specified file is not found.
        """
        self._filename = name
        self._cdf = cdflib.cdfread.CDF(name)
        self._info = self._cdf.cdf_info()
        self._global_attributes = self._cdf.globalattsget()


    def get_variable_names(
            self
        ) -> List[str]:
        """
        Gets the variable names (both r and z variables).

        Returns
        -------
        List
            A list of the variable names.
        """

        try:
            return self._info['rVariables'] + self._info['zVariables']
        except TypeError:
            # cdflib >= 1.0
            return self._info.rVariables + self._info.zVariables


    def get_variable_info(
            self,
            name: str
        ): # -> VDRInfo:
        """
        Gets information about the specified variable.

        Parameters
        ----------
        name
            Name of variable.
        Returns
        -------
        VDRInfo
            Information about the specified variable.
        """
        return self._cdf.varinq(name)


    def get_variable_data(
            self,
            name: str,
            startrec: int,
            endrec: int
        ) -> np.ndarray:
        """
        Gets the specified variable's data.

        Parameters
        ----------
        name
            Name of variable.
        startrec
            Index of the first record to get.
        endrec
            Index of the last record to get.  All records from startrec
            ot endrec inclusive are fetched.
        Returns
        -------
        np.ndarray
            The specified variable's data from startrec to endrec
            inclusive.
        """
        return self._cdf.varget(name, startrec = startrec, endrec = endrec)


    def get_text_attributes(
            self
        ): # -> AttData
        """
        Gets the value of the TEXT global attribute entries.

        Returns
        -------
        AttData
            Value of the TEXT global attribute entries.
        """
        return self._global_attributes['TEXT']


    def get_b_trace_stop_altitude(
            self
        ) -> float:
        """
        Gets the B-field trace stop altitude value.

        Returns
        -------
        float
            B-field trace stop altitude value.  NaN if not found.
        """
        for value in self.get_text_attributes():
            match = B_TRACE_STOP_ALTITUDE_PATTERN.match(value)
            if match:
                return float(match.groups()[0])

        return float('NaN')


    def get_source_name(
            self
        ) -> str:
        """
        Gets the value of the Source_name global attribute.

        Returns
        -------
        str
            Value of the Source_name global attribute.
        """
        name = self._global_attributes['Source_name']

        if isinstance(name, list):    # cdflib >= 1.0
            name = name[0]

        return name


    def get_satellite_name(
            self
        ) -> str:
        """
        Gets the name of the satellite whose location data is in
        this file.

        Returns
        -------
        str
            Name of satellite whose location data is in this file.
        """
        return self.get_source_name()


    def get_coordinate_data(
            self
        ) -> List[Dict]:
        """
        Gets coordinate data.

        Returns
        -------
        List[Dict]
            Coordinate data.
        """

        coordinate_data = {}

        for name in self.get_variable_names():
            var_info = self.get_variable_info(name)
            try:
                last_rec = var_info['Last_Rec']
            except TypeError:
                # cdflib >= 1.0
                last_rec = var_info.Last_Rec
            data = self.get_variable_data(name, 0, last_rec)

            matcher = XYZ_PATTERN.match(name)

            if matcher:
                coord_system = matcher.group(1)

                #print(name, ' VDRInfo: ', var_info)
                #print('data = ', data)

                coordinate_data[coord_system] = {
                    'CoordinateSystem': CoordinateSystem.from_identifier(coord_system),
                    'X': data[:,0],
                    'Y': data[:,1],
                    'Z': data[:,2]
                }
            else:
                matcher = COMPONENT_PATTERN.match(name)

                if matcher:
                    coord_system = matcher.group(1)
                    component = matcher.group(2)

                    coordinate_data[coord_system] = {
                        'CoordinateSystem': CoordinateSystem.from_identifier(coord_system),
                        component: data
                    }
        results = []
        for value in coordinate_data.values():
            results.append(value)

        return results


    def get_time(
            self
        ) -> List[np.datetime64]:
        """
        Get the time values.

        Returns
        -------
        List[np.datetime64]
            Time values.
        """

        name = 'Epoch'
        var_info = self.get_variable_info(name)
        try:
            last_rec = var_info['Last_Rec']
        except TypeError:
            # cdflib >= 1.0
            last_rec = var_info.Last_Rec
        epoch = self.get_variable_data(name, 0, last_rec)

        datetimes = cdflib.cdfepoch.to_datetime(epoch)

        return datetimes

        # fix timezone (https://github.com/MAVENSDC/cdflib/issues/224)
        #tz_datetimes = np.empty(len(datetimes), dtype=object)
        #for i in range(len(datetimes)):
        #    tz_datetimes[i] = datetimes[i].replace(tzinfo=timezone.utc)
        #return tz_datetimes


    def get_b_trace_data(
            self
        ) -> List[Dict]:
        """
        Gets the B-field trace data.

        Returns
        -------
        List[Dict]
            B-field trace data.
        """

        b_trace_data = {}

        for name in self.get_variable_names():
            var_info = self.get_variable_info(name)
            try:
                last_rec = var_info['Last_Rec']
            except TypeError:
                # cdflib >= 1.0
                last_rec = var_info.Last_Rec
            data = self.get_variable_data(name, 0, last_rec)

            matcher = B_TRACE_PATTERN.match(name)

            if matcher:
                hemisphere = matcher.group(1)
                coord_system = matcher.group(2)
                component = matcher.group(3)
                if component == 'LAT':
                    component = 'Latitude'
                if component == 'LON':
                    component = 'Longitude'
                if component == 'LCT_T':
                    component = 'LocalTime'
                if component == 'ARCLEN':
                    component = 'ArcLength'

                key = coord_system + hemisphere

                if key not in b_trace_data:

                    b_trace_data[key] = {
                        'CoordinateSystem': CoordinateSystem.from_identifier(coord_system),
                        'Hemisphere': Hemisphere.from_identifier(hemisphere)
                    }
                b_trace_data[key][component] = data

        results = []
        for key, value in b_trace_data.items():
            results.append(value)

        return results


    def get_value(
            self,
            name: str
        ) -> np.ndarray:
        """
        Gets all of the specified variable's data.

        Parameters
        ----------
        name
            Name of variable.
        Returns
        -------
        np.ndarray
            All of the specified variable's data.
        """

        var_info = self.get_variable_info(name)
        try:
            last_rec = var_info['Last_Rec']
        except TypeError:
            # cdflib >= 1.0
            last_rec = var_info.Last_Rec
        return self.get_variable_data(name, 0, last_rec)


    def get_spacecraft_region(
            self
        ) -> List['SpaceRegion']:
        """
        Gets the spacecraft region information.

        Returns
        -------
        List[SpaceRegion]
            Spacecraft region information.
        """

        regions = []

        try:
            region_codes = self.get_value('SPACECRAFT_REGIONS')
        except ValueError:
            return regions

        for region_code in region_codes:
            regions.append(SpaceRegion.from_code(region_code))

        return regions


    def get_footpoint_regions(
            self,
            name: str
        ) -> List[FootpointRegion]:
        """
        Gets the trace footpoint region information.

        Returns
        -------
        List[FootpointRegion]
            Trace footpoint region information.
        """

        regions = []

        try:
            region_codes = self.get_value(name + 'TRACED_REGIONS')
        except ValueError:
            return regions

        for region_code in region_codes:
            regions.append(FootpointRegion.from_code(region_code))

        return regions


    def get_b_gse_component(
            self,
            name: str
        ) -> np.ndarray:
        """
        Gets all of the specified B-field GSE component data.

        Parameters
        ----------
        name
            Name of component (X, Y, or Z).
        Returns
        -------
        np.ndarray
            All of the specified B-field GSE component data.
        """

        return self.get_value('MAG_' + name)


    def get_satellite_data(
            self
        ) -> Dict:
        """
        Gets the SatelliteData from this CDF.

        Returns
        -------
        Dict
            The SatelliteData from this CDF.
        """
        var_names = self.get_variable_names()
        data = {}
        data['Id'] = self.get_satellite_name().lower()
        data['Coordinates'] = self.get_coordinate_data()
        data['Time'] = self.get_time()
        b_trace_data = self.get_b_trace_data()
        if len(b_trace_data) > 0:
            data['BTraceData'] = b_trace_data

        if 'RADIUS' in var_names:
            data['RadialLength'] = self.get_value('RADIUS')
        if 'MAG_STRTH' in var_names:
            data['MagneticStrength'] = self.get_value('MAG_STRTH')
        if 'DNEUTS' in var_names:
            data['NeutralSheetDistance'] = self.get_value('DNEUTS')

        if 'BOW_SHOCK' in var_names:
            data['BowShockDistance'] = self.get_value('BOW_SHOCK')
        if 'MAG_PAUSE' in var_names:
            data['MagnetoPauseDistance'] = self.get_value('MAG_PAUSE')
        if 'L_VALUE' in var_names:
            data['DipoleLValue'] = self.get_value('L_VALUE')
        if 'INVAR_LAT' in var_names:
            data['DipoleInvariantLatitude'] = self.get_value('INVAR_LAT')
        sc_region = self.get_spacecraft_region()
        if len(sc_region) > 0:
            data['SpacecraftRegion'] = sc_region
        if 'RADIAL_TRACED_REGIONS' in var_names:
            data['RadialTracedFootpointRegions'] = \
                self.get_footpoint_regions('RADIAL_')
        if 'MAG_X' in var_names:
            data['BGseX'] = self.get_b_gse_component('X')
        if 'MAG_Y' in var_names:
            data['BGseY'] = self.get_b_gse_component('Y')
        if 'MAG_Z' in var_names:
            data['BGseZ'] = self.get_b_gse_component('Z')
        if 'NORTH_B_TRACED_REGIONS' in var_names:
            data['NorthBTracedFootpointRegions'] = \
                self.get_footpoint_regions('NORTH_B')
        if 'SOUTH_B_TRACED_REGIONS' in var_names:
            data['SouthBTracedFootpointRegions'] = \
                self.get_footpoint_regions('SOUTH_B')

        return data
