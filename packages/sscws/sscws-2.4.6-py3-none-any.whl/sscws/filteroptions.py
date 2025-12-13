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
# Copyright (c) 2013-2023 United States Government as represented by
# the National Aeronautics and Space Administration. No copyright is
# claimed in the United States under Title 17, U.S.Code. All Other
# Rights Reserved.
#

"""
Module defining classes to related to filter options from
<https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.<br>

Copyright &copy; 2013-2023 United States Government as represented by the
National Aeronautics and Space Administration. No copyright is claimed in
the United States under Title 17, U.S.Code. All Other Rights Reserved.
"""

# pylint: disable=too-many-lines

import xml.etree.ElementTree as ET

from sscws.outputoptions import LocationFilter



class RegionFilterOptions:
    """
    Class representing a RegionFilterOptions from
    <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Parameters
    ----------
    space_regions
        Specifies the space region filter options.
    radial_trace_regions
        Specifies the radial trace region filter options.
    magnetic_trace_regions
        Specifies the magnetic trace region filter options.
    """
    def __init__(self,
                 space_regions: bool = None,
                 radial_trace_regions: bool = None,
                 magnetic_trace_regions: bool = None):

        self._space_regions = space_regions
        self._radial_trace_regions = radial_trace_regions
        self._magnetic_trace_regions = magnetic_trace_regions


    @property
    def space_regions(self) -> bool:
        """
        Gets the space_regions value.

        Returns
        -------
        bool
            space_regions value.
        """
        return self._space_regions


    @space_regions.setter
    def space_regions(self, value: bool):
        """
        Sets the space_regions value.

        Parameters
        ----------
        value
            space_regions value.
        """
        self._space_regions = value


    @property
    def radial_trace_regions(self) -> bool:
        """
        Gets the radial_trace_regions value.

        Returns
        -------
        bool
            radial_trace_regions value.
        """
        return self._radial_trace_regions


    @radial_trace_regions.setter
    def radial_trace_regions(self, value: bool):
        """
        Sets the radial_trace_regions value.

        Parameters
        ----------
        value
            radial_trace_regions value.
        """
        self._radial_trace_regions = value


    @property
    def magnetic_trace_regions(self) -> bool:
        """
        Gets the magnetic_trace_regions value.

        Returns
        -------
        bool
            magnetic_trace_regions value.
        """
        return self._magnetic_trace_regions


    @magnetic_trace_regions.setter
    def magnetic_trace_regions(self, value: bool):
        """
        Sets the magnetic_trace_regions value.

        Parameters
        ----------
        value
            magnetic_trace_regions value.
        """
        self._magnetic_trace_regions = value



    def xml_element(self) -> ET:
        """
        Produces the XML Element representation of this object.

        Returns
        -------
        ET
            XML Element represenation of this object.
        """
        builder = ET.TreeBuilder()

        builder.start('RegionFilterOptions', {})
        builder.end('RegionFilterOptions')

        xml_element = builder.close()

        if self._space_regions is not None:
            xml_element.append(
                self._space_regions.xml_element())
        if self._radial_trace_regions is not None:
            xml_element.append(
                self._radial_trace_regions.xml_element(
                    'RadialTraceRegions'))
        if self._magnetic_trace_regions is not None:
            xml_element.append(
                self._magnetic_trace_regions.xml_element(
                    'MagneticTraceRegions'))

        return xml_element


class LocationFilterOptions:  # pylint: disable=too-many-instance-attributes
    """
    Class representing a LocationFilterOptions from
    <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Parameters
    ----------
    all_filters
        Coordinate options.
    distance_from_center_of_earth
        All location filters flag.
    magnetic_field_strength
        Minimum/Maximum number of points.
    distance_from_neutral_sheet
        Region options.
    distance_from_bow_shock
        Value options.
    distance_from_magnetopause
        Distance-from magnetopause options.
    dipole_l_value
        Dipole L value options.
    dipole_invariant_latitude
        Dipole invariant latitude options.
    """
    def __init__(self,
                 all_filters: bool = None,
                 distance_from_center_of_earth: LocationFilter = None,
                 magnetic_field_strength: LocationFilter = None,
                 distance_from_neutral_sheet: LocationFilter = None,
                 distance_from_bow_shock: LocationFilter = None,
                 distance_from_magnetopause: LocationFilter = None,
                 dipole_l_value: LocationFilter = None,
                 dipole_invariant_latitude: LocationFilter = None
                 ):  # pylint: disable=too-many-arguments

        if all_filters is None:
            self._all_filters = True
        else:
            self._all_filters = all_filters

        if distance_from_center_of_earth is not None:
            self._distance_from_center_of_earth = \
                distance_from_center_of_earth

        if magnetic_field_strength is not None:
            self._magnetic_field_strength = magnetic_field_strength

        if distance_from_neutral_sheet is not None:
            self._distance_from_neutral_sheet = distance_from_neutral_sheet

        if distance_from_bow_shock is not None:
            self._distance_from_bow_shock = distance_from_bow_shock

        if distance_from_magnetopause is not None:
            self._distance_from_magnetopause = distance_from_magnetopause

        if dipole_l_value is not None:
            self._dipole_l_value = dipole_l_value

        if dipole_invariant_latitude is not None:
            self._dipole_invariant_latitude = dipole_invariant_latitude


    @property
    def all_filters(self) -> bool:
        """
        Gets the all_filters value.

        Returns
        -------
        str
            all_filters value.
        """
        return self._all_filters


    @all_filters.setter
    def all_filters(self, value: bool):
        """
        Sets the all_filters value.

        Parameters
        ----------
        value
            all_filters value.
        """
        self._all_filters = value


    @property
    def distance_from_center_of_earth(self) -> LocationFilter:
        """
        Gets the distance_from_center_of_earth value.

        Returns
        -------
        str
            distance_from_center_of_earth value.
        """
        return self._distance_from_center_of_earth


    @distance_from_center_of_earth.setter
    def distance_from_center_of_earth(self, value: LocationFilter):
        """
        Sets the distance_from_center_of_earth value.

        Parameters
        ----------
        value
            distance_from_center_of_earth value.
        """
        self._distance_from_center_of_earth = value


    @property
    def magnetic_field_strength(self) -> LocationFilter:
        """
        Gets the magnetic_field_strength value.

        Returns
        -------
        str
            magnetic_field_strength value.
        """
        return self._magnetic_field_strength


    @magnetic_field_strength.setter
    def magnetic_field_strength(self, value: LocationFilter):
        """
        Sets the magnetic_field_strength value.

        Parameters
        ----------
        value
            magnetic_field_strength value.
        """
        self._magnetic_field_strength = value


    @property
    def distance_from_neutral_sheet(self) -> LocationFilter:
        """
        Gets the distance_from_neutral_sheet value.

        Returns
        -------
        str
            distance_from_neutral_sheet value.
        """
        return self._distance_from_neutral_sheet


    @distance_from_neutral_sheet.setter
    def distance_from_neutral_sheet(self, value: LocationFilter):
        """
        Sets the distance_from_neutral_sheet value.

        Parameters
        ----------
        value
            distance_from_neutral_sheet value.
        """
        self._distance_from_neutral_sheet = value


    @property
    def distance_from_bow_shock(self) -> LocationFilter:
        """
        Gets the distance_from_bow_shock value.

        Returns
        -------
        str
            distance_from_bow_shock value.
        """
        return self._distance_from_bow_shock


    @distance_from_bow_shock.setter
    def distance_from_bow_shock(self, value: LocationFilter):
        """
        Sets the distance_from_bow_shock value.

        Parameters
        ----------
        value
            distance_from_bow_shock value.
        """
        self._distance_from_bow_shock = value


    @property
    def distance_from_magnetopause(self) -> LocationFilter:
        """
        Gets the distance_from_magnetopause value.

        Returns
        -------
        str
            distance_from_magnetopause value.
        """
        return self._distance_from_magnetopause


    @distance_from_magnetopause.setter
    def distance_from_magnetopause(self, value: LocationFilter):
        """
        Sets the distance_from_magnetopause value.

        Parameters
        ----------
        value
            distance_from_magnetopause value.
        """
        self._distance_from_magnetopause = value


    @property
    def dipole_l_value(self) -> LocationFilter:
        """
        Gets the dipole_l_value value.

        Returns
        -------
        str
            dipole_l_value value.
        """
        return self._dipole_l_value


    @dipole_l_value.setter
    def dipole_l_value(self, value: LocationFilter):
        """
        Sets the dipole_l_value value.

        Parameters
        ----------
        value
            dipole_l_value value.
        """
        self._dipole_l_value = value


    def xml_element(self) -> ET:
        """
        Produces the XML Element representation of this object.

        Returns
        -------
        ET
            XML Element represenation of this object.
        """

        builder = ET.TreeBuilder()
        builder.start('LocationFilterOptions', {})
        builder.start('AllFilters', {})
        builder.data(str(self._all_filters).lower())
        builder.end('AllFilters')
        xml_element = builder.close()

        if self._distance_from_center_of_earth is not None:
            xml_element.append(
                self._distance_from_center_of_earth.xml_element(
                    'DistanceFromCenterOfEarth'))
        if self._magnetic_field_strength is not None:
            xml_element.append(
                self._magnetic_field_strength.xml_element(
                    'MagneticFieldStrength'))
        if self._distance_from_neutral_sheet is not None:
            xml_element.append(
                self._distance_from_neutral_sheet.xml_element(
                    'DistanceFromNeutralSheet'))
        if self._distance_from_bow_shock is not None:
            xml_element.append(
                self._distance_from_bow_shock.xml_element(
                    'DistanceFromBowShock'))
        if self._distance_from_magnetopause is not None:
            xml_element.append(
                self._distance_from_magnetopause.xml_element(
                    'DistanceFromMagnetopause'))
        if self._dipole_l_value is not None:
            xml_element.append(
                self._dipole_l_value.xml_element('DipoleLValue'))
        if self._dipole_invariant_latitude is not None:
            xml_element.append(
                self._dipole_invariant_latitude.xml_element(
                    'DipoleInvariantLatitude'))

        return xml_element


class SpaceRegionsFilterOptions:  # pylint: disable=too-many-instance-attributes
    """
    Class representing a SpaceRegionsFilterOptions from
    <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Parameters
    ----------
    interplanetary_medium
        Specifies whether the interplanetary medium region filter is
        to be applied.  If None, default is False.
    dayside_magnetosheath
        Specifies whether the dayside magnetosheath region filter is
        to be applied.  If None, default is False.
    nightside_magnetosheath
        Specifies whether the nightside magnetosheath region filter is
        to be applied.  If None, default is False.
    dayside_magnetosphere
        Specifies whether the dayside magnetosphere region filter is
        to be applied.  If None, default is False.
    nightside_magnetosphere
        Specifies whether the nightside magnetosphere region filter is
        to be applied.  If None, default is False.
    plasma_sheet
        Specifies whether the plasma sheet region filter is to be
        applied.  If None, default is False.
    tail_lobe
        Specifies whether the tail lobe region filter is to be applied.
        If None, default is False.
    high_latitude_boundary_layer
        Specifies whether the high latitude boundary layer region
        filter is to be applied.  If None, default is False.
    low_latitude_boundary_layer
        Specifies whether the low latitude boundary layer region
        filter is to be applied.  If None, default is False.
    dayside_plasmasphere
        Specifies whether the dayside plasmasphere region
        filter is to be applied.  If None, default is False.
    nightside_plasmasphere
        Specifies whether the nightside plasmasphere region
        filter is to be applied.  If None, default is False.
    """
    def __init__(self,
                 interplanetary_medium: bool = None,
                 dayside_magnetosheath: bool = None,
                 nightside_magnetosheath: bool = None,
                 dayside_magnetosphere: bool = None,
                 nightside_magnetosphere: bool = None,
                 plasma_sheet: bool = None,
                 tail_lobe: bool = None,
                 high_latitude_boundary_layer: bool = None,
                 low_latitude_boundary_layer: bool = None,
                 dayside_plasmasphere: bool = None,
                 nightside_plasmasphere: bool = None
                 ):  # pylint: disable=too-many-arguments,too-many-branches

        if interplanetary_medium is None:
            self._interplanetary_medium = False
        else:
            self._interplanetary_medium = interplanetary_medium
        if dayside_magnetosheath is None:
            self._dayside_magnetosheath = False
        else:
            self._dayside_magnetosheath = dayside_magnetosheath
        if nightside_magnetosheath is None:
            self._nightside_magnetosheath = False
        else:
            self._nightside_magnetosheath = nightside_magnetosheath
        if dayside_magnetosphere is None:
            self._dayside_magnetosphere = False
        else:
            self._dayside_magnetosphere = dayside_magnetosphere
        if nightside_magnetosphere is None:
            self._nightside_magnetosphere = False
        else:
            self._nightside_magnetosphere = nightside_magnetosphere
        if plasma_sheet is None:
            self._plasma_sheet = False
        else:
            self._plasma_sheet = plasma_sheet
        if tail_lobe is None:
            self._tail_lobe = False
        else:
            self._tail_lobe = tail_lobe
        if high_latitude_boundary_layer is None:
            self._high_latitude_boundary_layer = False
        else:
            self._high_latitude_boundary_layer = high_latitude_boundary_layer
        if low_latitude_boundary_layer is None:
            self._low_latitude_boundary_layer = False
        else:
            self._low_latitude_boundary_layer = low_latitude_boundary_layer
        if dayside_plasmasphere is None:
            self._dayside_plasmasphere = False
        else:
            self._dayside_plasmasphere = dayside_plasmasphere
        if nightside_plasmasphere is None:
            self._nightside_plasmasphere = False
        else:
            self._nightside_plasmasphere = nightside_plasmasphere


    @property
    def interplanetary_medium(self) -> bool:
        """
        Gets the interplanetary_medium value.

        Returns
        -------
        bool
            interplanetary_medium value.
        """
        return self._interplanetary_medium


    @interplanetary_medium.setter
    def interplanetary_medium(self, value: bool):
        """
        Sets the interplanetary_medium value.

        Parameters
        ----------
        value
            interplanetary_medium value.
        """
        self._interplanetary_medium = value


    @property
    def dayside_magnetosheath(self) -> bool:
        """
        Gets the dayside_magnetosheath value.

        Returns
        -------
        bool
            dayside_magnetosheath value.
        """
        return self._dayside_magnetosheath


    @dayside_magnetosheath.setter
    def dayside_magnetosheath(self, value: bool):
        """
        Sets the dayside_magnetosheath value.

        Parameters
        ----------
        value
            dayside_magnetosheath value.
        """
        self._dayside_magnetosheath = value


    @property
    def nightside_magnetosheath(self) -> bool:
        """
        Gets the nightside_magnetosheath value.

        Returns
        -------
        bool
            nightside_magnetosheath value.
        """
        return self._nightside_magnetosheath


    @nightside_magnetosheath.setter
    def nightside_magnetosheath(self, value: bool):
        """
        Sets the nightside_magnetosheath value.

        Parameters
        ----------
        value
            nightside_magnetosheath value.
        """
        self._nightside_magnetosheath = value


    @property
    def dayside_magnetosphere(self) -> bool:
        """
        Gets the dayside_magnetosphere value.

        Returns
        -------
        bool
            dayside_magnetosphere value.
        """
        return self._dayside_magnetosphere


    @dayside_magnetosphere.setter
    def dayside_magnetosphere(self, value: bool):
        """
        Sets the dayside_magnetosphere value.

        Parameters
        ----------
        value
            dayside_magnetosphere value.
        """
        self._dayside_magnetosphere = value


    @property
    def nightside_magnetosphere(self) -> bool:
        """
        Gets the nightside_magnetosphere value.

        Returns
        -------
        bool
            nightside_magnetosphere value.
        """
        return self._nightside_magnetosphere


    @nightside_magnetosphere.setter
    def nightside_magnetosphere(self, value: bool):
        """
        Sets the nightside_magnetosphere value.

        Parameters
        ----------
        value
            nightside_magnetosphere value.
        """
        self._nightside_magnetosphere = value


    @property
    def plasma_sheet(self) -> bool:
        """
        Gets the plasma_sheet value.

        Returns
        -------
        bool
            plasma_sheet value.
        """
        return self._plasma_sheet


    @plasma_sheet.setter
    def plasma_sheet(self, value: bool):
        """
        Sets the plasma_sheet value.

        Parameters
        ----------
        value
            plasma_sheet value.
        """
        self._plasma_sheet = value


    @property
    def tail_lobe(self) -> bool:
        """
        Gets the tail_lobe value.

        Returns
        -------
        bool
            tail_lobe value.
        """
        return self._tail_lobe


    @tail_lobe.setter
    def tail_lobe(self, value: bool):
        """
        Sets the tail_lobe value.

        Parameters
        ----------
        value
            tail_lobe value.
        """
        self._tail_lobe = value


    @property
    def high_latitude_boundary_layer(self) -> bool:
        """
        Gets the high_latitude_boundary_layer value.

        Returns
        -------
        bool
            high_latitude_boundary_layer value.
        """
        return self._high_latitude_boundary_layer


    @high_latitude_boundary_layer.setter
    def high_latitude_boundary_layer(self, value: bool):
        """
        Sets the high_latitude_boundary_layer value.

        Parameters
        ----------
        value
            high_latitude_boundary_layer value.
        """
        self._high_latitude_boundary_layer = value


    @property
    def low_latitude_boundary_layer(self) -> bool:
        """
        Gets the low_latitude_boundary_layer value.

        Returns
        -------
        bool
            low_latitude_boundary_layer value.
        """
        return self._low_latitude_boundary_layer


    @low_latitude_boundary_layer.setter
    def low_latitude_boundary_layer(self, value: bool):
        """
        Sets the low_latitude_boundary_layer value.

        Parameters
        ----------
        value
            low_latitude_boundary_layer value.
        """
        self._low_latitude_boundary_layer = value


    @property
    def dayside_plasmasphere(self) -> bool:
        """
        Gets the dayside_plasmasphere value.

        Returns
        -------
        bool
            dayside_plasmasphere value.
        """
        return self._dayside_plasmasphere


    @dayside_plasmasphere.setter
    def dayside_plasmasphere(self, value: bool):
        """
        Sets the dayside_plasmasphere value.

        Parameters
        ----------
        value
            dayside_plasmasphere value.
        """
        self._dayside_plasmasphere = value


    @property
    def nightside_plasmasphere(self) -> bool:
        """
        Gets the nightside_plasmasphere value.

        Returns
        -------
        bool
            nightside_plasmasphere value.
        """
        return self._nightside_plasmasphere


    @nightside_plasmasphere.setter
    def nightside_plasmasphere(self, value: bool):
        """
        Sets the nightside_plasmasphere value.

        Parameters
        ----------
        value
            nightside_plasmasphere value.
        """
        self._nightside_plasmasphere = value


    def xml_element(self) -> ET:
        """
        Produces the XML Element representation of this object.

        Returns
        -------
        ET
            XML Element represenation of this object.
        """

        builder = ET.TreeBuilder()
        builder.start('SpaceRegions', {})
        builder.start('InterplanetaryMedium', {})
        builder.data(str(self._interplanetary_medium).lower())
        builder.end('InterplanetaryMedium')

        builder.start('DaysideMagnetosheath', {})
        builder.data(str(self._dayside_magnetosheath).lower())
        builder.end('DaysideMagnetosheath')

        builder.start('NightsideMagnetosheath', {})
        builder.data(str(self._nightside_magnetosheath).lower())
        builder.end('NightsideMagnetosheath')

        builder.start('DaysideMagnetosphere', {})
        builder.data(str(self._dayside_magnetosphere).lower())
        builder.end('DaysideMagnetosphere')

        builder.start('NightsideMagnetosphere', {})
        builder.data(str(self._nightside_magnetosphere).lower())
        builder.end('NightsideMagnetosphere')

        builder.start('PlasmaSheet', {})
        builder.data(str(self._plasma_sheet).lower())
        builder.end('PlasmaSheet')

        builder.start('TailLobe', {})
        builder.data(str(self._tail_lobe).lower())
        builder.end('TailLobe')

        builder.start('HighLatitudeBoundaryLayer', {})
        builder.data(str(self._high_latitude_boundary_layer).lower())
        builder.end('HighLatitudeBoundaryLayer')

        builder.start('LowLatitudeBoundaryLayer', {})
        builder.data(str(self._low_latitude_boundary_layer).lower())
        builder.end('LowLatitudeBoundaryLayer')

        builder.start('DaysidePlasmasphere', {})
        builder.data(str(self._dayside_plasmasphere).lower())
        builder.end('DaysidePlasmasphere')

        builder.start('NightsidePlasmasphere', {})
        builder.data(str(self._nightside_plasmasphere).lower())
        builder.end('NightsidePlasmasphere')
        builder.end('SpaceRegions')

        return builder.close()


class MappedRegionFilterOptions:
    """
    Class representing a MappedRegionFilterOptions from
    <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Parameters
    ----------
    cusp
        Cusp region.
    cleft
        Cleft region.
    auroral_oval
        Auroral Oval region.
    polar_cap
        Polar Cap region.
    mid_latitude
        Mid-Latitude region.
    low_latitude
        Low-Latitude region.
    """
    def __init__(self,
                 cusp: LocationFilter = None,
                 cleft: LocationFilter = None,
                 auroral_oval: LocationFilter = None,
                 polar_cap: LocationFilter = None,
                 mid_latitude: LocationFilter = None,
                 low_latitude: bool = None,
                 ):  # pylint: disable=too-many-arguments

        self._cusp = cusp
        self._cleft = cleft
        self._auroral_oval = auroral_oval
        self._polar_cap = polar_cap
        self._mid_latitude = mid_latitude
        self._low_latitude = low_latitude


    @property
    def cusp(self) -> LocationFilter:
        """
        Gets the cusp value.

        Returns
        -------
        str
            cusp value.
        """
        return self._cusp


    @cusp.setter
    def cusp(self, value: LocationFilter):
        """
        Sets the cusp value.

        Parameters
        ----------
        value
            cusp value.
        """
        self._cusp = value


    @property
    def cleft(self) -> LocationFilter:
        """
        Gets the cleft value.

        Returns
        -------
        str
            cleft value.
        """
        return self._cleft


    @cleft.setter
    def cleft(self, value: LocationFilter):
        """
        Sets the cleft value.

        Parameters
        ----------
        value
            cleft value.
        """
        self._cleft = value


    @property
    def auroral_oval(self) -> LocationFilter:
        """
        Gets the auroral_oval value.

        Returns
        -------
        str
            auroral_oval value.
        """
        return self._auroral_oval


    @auroral_oval.setter
    def auroral_oval(self, value: LocationFilter):
        """
        Sets the auroral_oval value.

        Parameters
        ----------
        value
            auroral_oval value.
        """
        self._auroral_oval = value


    @property
    def polar_cap(self) -> LocationFilter:
        """
        Gets the polar_cap value.

        Returns
        -------
        str
            polar_cap value.
        """
        return self._polar_cap


    @polar_cap.setter
    def polar_cap(self, value: LocationFilter):
        """
        Sets the polar_cap value.

        Parameters
        ----------
        value
            polar_cap value.
        """
        self._polar_cap = value


    @property
    def mid_latitude(self) -> LocationFilter:
        """
        Gets the mid_latitude value.

        Returns
        -------
        str
            mid_latitude value.
        """
        return self._mid_latitude


    @mid_latitude.setter
    def mid_latitude(self, value: LocationFilter):
        """
        Sets the mid_latitude value.

        Parameters
        ----------
        value
            mid_latitude value.
        """
        self._mid_latitude = value


    @property
    def low_latitude(self) -> bool:
        """
        Gets the low_latitude value.

        Returns
        -------
        str
            low_latitude value.
        """
        return self._low_latitude


    @low_latitude.setter
    def low_latitude(self, value: bool):
        """
        Sets the low_latitude value.

        Parameters
        ----------
        value
            low_latitude value.
        """
        self._low_latitude = value


    def xml_element(self,
                    name: str) -> ET:
        """
        Produces the XML Element representation of this object.

        Parameters
        ----------
        name
            Name of this TraceRegion.

        Returns
        -------
        ET
            XML Element represenation of this object.
        """

        builder = ET.TreeBuilder()
        builder.start(name, {})
        builder.end(name)
        xml_element = builder.close()

        if self._cusp is not None:
            xml_element.append(
                self._cusp.xml_element(
                    'Cusp'))
        if self._cleft is not None:
            xml_element.append(
                self._cleft.xml_element(
                    'Cleft'))
        if self._auroral_oval is not None:
            xml_element.append(
                self._auroral_oval.xml_element(
                    'AuroralOval'))
        if self._polar_cap is not None:
            xml_element.append(
                self._polar_cap.xml_element(
                    'PolarCap'))
        if self._mid_latitude is not None:
            xml_element.append(
                self._mid_latitude.xml_element(
                    'MidLatitude'))
        if self._low_latitude is not None:
            builder = ET.TreeBuilder()
            builder.start('LowLatitude', {})
            builder.data(str(self._low_latitude).lower())
            builder.end('LowLatitude')
            xml_element.append(builder.close())

        return xml_element
