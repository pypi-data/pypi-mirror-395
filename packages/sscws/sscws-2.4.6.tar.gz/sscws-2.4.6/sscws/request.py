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
Module defining classes to represent the Request and its
sub-classes from
<https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.<br>

Copyright &copy; 2013-2023 United States Government as represented by the
National Aeronautics and Space Administration. No copyright is claimed in
the United States under Title 17, U.S.Code. All Other Rights Reserved.
"""

import xml.etree.ElementTree as ET
from typing import List
from abc import ABCMeta

from sscws import NS
from sscws.bfieldmodels import BFieldModel
from sscws.conjunctions import Condition, ConditionOperator, \
    ExecuteOptions, GroundStationCondition, LeadSatelliteCondition, \
    RegionCondition, ResultOptions, SatelliteCondition
from sscws.filteroptions import LocationFilterOptions, RegionFilterOptions
from sscws.formatoptions import FormatOptions
from sscws.outputoptions import OutputOptions
from sscws.timeinterval import TimeInterval


class Request(metaclass=ABCMeta):
    """
    Class representing a Request from
    <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Notes
    -----
    Although this class is essentially a dictionary, it was defined as a
    class to make certain that it matched the structure and key names
    of a Request from
    <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    It also needs to function as a base class for the concrete
    sub-classes of a Request.

    Parameters
    ----------
    description
        Textual description of this request.
    interval
        Time interval of this request
    b_field_model
        Magnetic field model.  If None, default is BFieldModel.
    """
    #@abstractmethod
    def __init__(self,
                 description: str,
                 interval: TimeInterval,
                 b_field_model: BFieldModel = None):

        self._description = description
        self._interval = interval
        if b_field_model is None:
            self._b_field_model = BFieldModel()
        else:
            self._b_field_model = b_field_model


    @property
    def description(self) -> str:
        """
        Gets the description value.

        Returns
        -------
        str
            description value.
        """
        return self._description


    @description.setter
    def description(self, value: str):
        """
        Sets the description value.

        Parameters
        ----------
        value
            description value.
        """
        self._description = value


    @property
    def interval(self) -> TimeInterval:
        """
        Gets the interval value.

        Returns
        -------
        str
            interval value.
        """
        return self._interval


    @interval.setter
    def interval(self, value: TimeInterval):
        """
        Sets the interval value.

        Parameters
        ----------
        value
            interval value.
        """
        self._interval = value


    @property
    def b_field_model(self) -> BFieldModel:
        """
        Gets the b_field_model value.

        Returns
        -------
        str
            b_field_model value.
        """
        return self._b_field_model


    @b_field_model.setter
    def b_field_model(self, value: BFieldModel):
        """
        Sets the b_field_model value.

        Parameters
        ----------
        value
            b_field_model value.
        """
        self._b_field_model = value


    def xml_element(self) -> ET:
        """
        Produces the XML Element representation of this object.

        Returns
        -------
        ET
            XML Element represenation of this object.
        """

        attrs = {'xmlns': NS}
        if isinstance(self, DataRequest):
            request_type = 'Data'
#        elif isinstance(self, GraphRequest):
#            request_type = 'Graph'
#        elif isinstance(self, KmlRequest):
#            request_type = 'Kml'
        elif isinstance(self, LocationRequest):
            request_type = 'Location'
#        elif isinstance(self, QueryRequest):
#            request_type = 'Query'
        else:
            request_type = ''
            attrs = {}

        builder = ET.TreeBuilder()
        builder.start(request_type + 'Request', attrs)
        builder.start('Description', {})
        builder.data(self._description)
        builder.end('Description')
        builder.end(request_type + 'Request')
        xml_element = builder.close()

        xml_element.append(self._interval.xml_element())
        xml_element.append(self._b_field_model.xml_element())

        return xml_element


class SatelliteSpecification:
    """
    Class representing a SatelliteSpecification from
    <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Parameters
    ----------
    identifier
        satellite identifier
    resolution_factor
        resolution factor
    """
    def __init__(self,
                 identifier: str,
                 resolution_factor: int):

        self._identifier = identifier
        self._resolution_factor = resolution_factor


    @property
    def identifier(self) -> str:
        """
        Gets the identifier value.

        Returns
        -------
        str
            identifier value.
        """
        return self._identifier


    @identifier.setter
    def identifier(self, value: str):
        """
        Sets the identifier value.

        Parameters
        ----------
        value
            identifier value.
        """
        self._identifier = value


    @property
    def resolution_factor(self) -> int:
        """
        Gets the resolution_factor value.

        Returns
        -------
        str
            resolution_factor value.
        """
        return self._resolution_factor


    @resolution_factor.setter
    def resolution_factor(self, value: int):
        """
        Sets the resolution_factor value.

        Parameters
        ----------
        value
            resolution_factor value.
        """
        self._resolution_factor = value


    def xml_element(self) -> ET:
        """
        Produces the XML Element representation of this object.

        Returns
        -------
        ET
            XML Element represenation of this object.
        """
        builder = ET.TreeBuilder()

        builder.start('Satellites', {})
        builder.start('Id', {})
        builder.data(self._identifier)
        builder.end('Id')
        builder.start('ResolutionFactor', {})
        builder.data(str(self._resolution_factor))
        builder.end('ResolutionFactor')
        builder.end('Satellites')

        return builder.close()


class LocationRequest(Request):
    """
    Class representing a LocationRequest from
    <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Parameters
    ----------
    description
        Description of request.
    interval
        Time interval of request.
    b_field_model
        Magnetic field model.  If None, default is
        InternalBFieldModel.IGRF and Tsyganenko89cBFieldModel().
    satellites
        array of SatelliteSpecifications
    """
    def __init__(self,
                 description: str,
                 interval: TimeInterval,
                 satellites: List[SatelliteSpecification],
                 b_field_model: BFieldModel = None):

        super().__init__(description, interval, b_field_model)

        self._satellites = satellites


    def xml_element(self) -> ET:
        """
        Produces the XML Element representation of this object.

        Returns
        -------
        ET
            XML Element represenation of this object.
        """
        xml_element = super().xml_element()

        for sat in self._satellites:
            xml_element.append(sat.xml_element())

        return xml_element


    @property
    def satellites(self) -> List[SatelliteSpecification]:
        """
        Gets the satellites value.

        Returns
        -------
        str
            satellites value.
        """
        return self._satellites


    @satellites.setter
    def satellites(self, value: List[SatelliteSpecification]):
        """
        Sets the satellites value.

        Parameters
        ----------
        value
            satellites value.
        """
        self._satellites = value


class DataRequest(LocationRequest):
    """
    Class representing a DataRequest from
    <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Parameters
    ----------
    description
        Description of request.
    interval
        Time interval of request.
    satellites
        Array of SatelliteSpecifications.
    b_field_model
        Magnetic field model.  If None, default is
        InternalBFieldModel.IGRF and Tsyganenko89cBFieldModel().
    output_options
        Output options.
    region_filter_options
        Region filter options.
    location_filter_options
        Location filter options.
    format_options
        Format options.
    """
    def __init__(self,
                 description: str,
                 interval: TimeInterval,
                 satellites: List[SatelliteSpecification],
                 b_field_model: BFieldModel = None,
                 output_options: OutputOptions = None,
                 region_filter_options: RegionFilterOptions = None,
                 location_filter_options: LocationFilterOptions = None,
                 format_options: FormatOptions = None
                 ):  # pylint: disable=too-many-arguments

        super().__init__(description,
                         interval, satellites, b_field_model)

        self._output_options = output_options
        self._region_filter_options = region_filter_options
        self._location_filter_options = location_filter_options
        self._format_options = format_options


    def xml_element(self) -> ET:
        """
        Produces the XML Element representation of this object.

        Returns
        -------
        ET
            XML Element represenation of this object.
        """
        xml_element = super().xml_element()

        if self._output_options is not None:
            xml_element.append(self._output_options.xml_element())
        if self._region_filter_options is not None:
            xml_element.append(self._region_filter_options.xml_element())
        if self._location_filter_options is not None:
            xml_element.append(self._location_filter_options.xml_element())
        if self._format_options is not None:
            xml_element.append(self._format_options.xml_element())


        return xml_element


    @property
    def output_options(self) -> OutputOptions:
        """
        Gets the output_options value.

        Returns
        -------
        str
            output_options value.
        """
        return self._output_options


    @output_options.setter
    def output_options(self, value: OutputOptions):
        """
        Sets the output_options value.

        Parameters
        ----------
        value
            output_options value.
        """
        self._output_options = value


    @property
    def region_filter_options(self) -> RegionFilterOptions:
        """
        Gets the region_filter_options value.

        Returns
        -------
        str
            region_filter_options value.
        """
        return self._region_filter_options


    @region_filter_options.setter
    def region_filter_options(self, value: RegionFilterOptions):
        """
        Sets the region_filter_options value.

        Parameters
        ----------
        value
            region_filter_options value.
        """
        self._region_filter_options = value


    @property
    def location_filter_options(self) -> LocationFilterOptions:
        """
        Gets the location_filter_options value.

        Returns
        -------
        str
            location_filter_options value.
        """
        return self._location_filter_options


    @location_filter_options.setter
    def location_filter_options(self, value: LocationFilterOptions):
        """
        Sets the location_filter_options value.

        Parameters
        ----------
        value
            location_filter_options value.
        """
        self._location_filter_options = value


    @property
    def format_options(self) -> FormatOptions:
        """
        Gets the format_options value.

        Returns
        -------
        str
            format_options value.
        """
        return self._format_options


    @format_options.setter
    def format_options(self, value: FormatOptions):
        """
        Sets the format_options value.

        Parameters
        ----------
        value
            format_options value.
        """
        self._format_options = value


class QueryRequest():
    """
    Class representing a QueryRequest from
    <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Parameters
    ----------
    description
        Description of request.
    interval
        Time interval of request.
    condition_operator
        Operator for combining conditions.
    conditions
        Query conditions.  Consists of a SatelliteCondition along with
        one of the following:<br>
        - GroundStationCondition (and optionally a RegionCondition)<br>
        - LeadSatelliteCondition (and optionally a RegionCondition)<br>
        - RegionCondition
    b_field_model
        Magnetic field model.  If None, default is
        InternalBFieldModel.IGRF and Tsyganenko89cBFieldModel().
    result_options
        Query result options

    Raises
    ------
        ValueError if the conditions are not as described above.
    """
    def __init__(self,
                 description: str,
                 interval: TimeInterval,
                 condition_operator: ConditionOperator,
                 conditions: List[Condition],
                 b_field_model: BFieldModel = None,
                 result_options: ResultOptions = None
                 ):  # pylint: disable=too-many-arguments

        self._request = Request(description, interval, b_field_model)

        self._condition_operator = condition_operator

        if conditions is None or len(conditions) > 9:
            raise ValueError('Number of conditions is < 1 or > 9')

        sat_cond = 0
        gs_cond = 0
        lead_sat_cond = 0
        region_cond = 0
        for condition in conditions:
            if isinstance(condition, SatelliteCondition):
                sat_cond += 1
            if isinstance(condition, GroundStationCondition):
                gs_cond += 1
            if isinstance(condition, LeadSatelliteCondition):
                lead_sat_cond += 1
            if isinstance(condition, RegionCondition):
                region_cond += 1

        if sat_cond != 1:
            raise ValueError('Exactly 1 SatelliteCondition is required')

        if gs_cond == 0 and lead_sat_cond == 0 and region_cond == 0:
            raise ValueError('At lease 1 GroundStationCondition, ' +
                             'LeadSatilliteCondition, or RegionCondition ' +
                             'is required')

        self._conditions = conditions

        if result_options is None:
            self._result_options = ResultOptions()
        else:
            self._result_options = result_options

        self._execute_options = ExecuteOptions()


    def xml_element(self) -> ET:
        """
        Produces the XML Element representation of this object.

        Returns
        -------
        ET
            XML Element represenation of this object.
        """
        xml_element = self._request.xml_element()

        xml_element.append(self._execute_options.xml_element())

        if self._result_options is not None:
            xml_element.append(self._result_options.xml_element())

        builder = ET.TreeBuilder()
        builder.start('ConditionOperator', {})
        builder.data(self._condition_operator.value)
        builder.end('ConditionOperator')
        xml_element.append(builder.close())

        for condition in self._conditions:
            xml_element.append(condition.xml_element())

        builder = ET.TreeBuilder()
        builder.start('QueryRequest', {'xmlns': NS})
        builder.end('QueryRequest')
        query_element = builder.close()

        query_element.append(xml_element)

        return query_element


    @property
    def execute_options(self) -> ExecuteOptions:
        """
        Gets the execute_options value.

        Returns
        -------
        str
            execute_options value.
        """
        return self._execute_options


    @execute_options.setter
    def execute_options(self, value: ExecuteOptions):
        """
        Sets the execute_options value.  Currently, the server ignores any
        value other than the default.

        Parameters
        ----------
        value
            execute_options value.
        """
        self._execute_options = value


    @property
    def result_options(self) -> ResultOptions:
        """
        Gets the result_options value.

        Returns
        -------
        str
            result_options value.
        """
        return self._result_options


    @result_options.setter
    def result_options(self, value: ResultOptions):
        """
        Sets the result_options value.

        Parameters
        ----------
        value
            result_options value.
        """
        self._result_options = value


    @property
    def condition_operator(self) -> ConditionOperator:
        """
        Gets the condition_operator value.

        Returns
        -------
        str
            condition_operator value.
        """
        return self._condition_operator


    @condition_operator.setter
    def condition_operator(self, value: ConditionOperator):
        """
        Sets the condition_operator value.

        Parameters
        ----------
        value
            condition_operator value.
        """
        self._condition_operator = value


    @property
    def conditions(self) -> List[Condition]:
        """
        Gets the conditions value.

        Returns
        -------
        str
            conditions value.
        """
        return self._conditions


    @conditions.setter
    def conditions(self, value: List[Condition]):
        """
        Sets the conditions value.

        Parameters
        ----------
        value
            conditions value.
        """
        self._conditions = value
