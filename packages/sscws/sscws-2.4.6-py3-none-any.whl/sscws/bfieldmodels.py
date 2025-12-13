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
Module defining classes to represent the BFieldModel and its
sub-classes from
<https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

Copyright &copy; 2013-2021 United States Government as represented by the
National Aeronautics and Space Administration. No copyright is claimed in
the United States under Title 17, U.S.Code. All Other Rights Reserved.
"""

import xml.etree.ElementTree as ET
from abc import ABCMeta
from enum import Enum



class InternalBFieldModel(Enum):
    """
    Enumerations representing the InternalBFieldModel defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    IGRF = 'IGRF'
    SIMPLE_DIPOLE = 'SimpleDipole'


class ExternalBFieldModelName(Enum):
    """
    Enumerations representing the name of ExternalBFieldModel defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    TSYGANENKO96 = 'Tsyganenko96BFieldModel'
    TSYGANENKO89C = 'Tsyganenko89cBFieldModel'
    TSYGANENKO87 = 'Tsyganenko87BFieldModel'


class ExternalBFieldModel(metaclass=ABCMeta):
    """
    Enumerations representing the ExternalBFieldModel defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Parameters
    ----------
    name
        B-field model name.
    """
    def __init__(self,
                 name: ExternalBFieldModelName):
        self._name = name


    def xml_element(self) -> ET:
        """
        Produces the XML Element representation of this object.

        Returns
        -------
        ET
            XML Element represenation of this object.
        """

        builder = ET.TreeBuilder()
        builder.start('ExternalBFieldModel', {
            'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
            'xsi:type': self._name.value
        })
        builder.end('ExternalBFieldModel')
        return builder.close()


    @property
    def name(self) -> str:
        """
        Gets the name value.

        Returns
        -------
        str
            name value.
        """
        return self._name


    @name.setter
    def name(self, value: str):
        """
        Sets the name value.

        Parameters
        ----------
        value
            name value.
        """
        self._name = value


class Tsyganenko96BFieldModel(ExternalBFieldModel):
    """
    Class representing the Tsyganenko96BFieldModel defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Parameters
    ----------
    solar_wind_pressure
        Solar wind pressure (nP).  If None, default is 2.1.
    dst_index
        Disturbance Storm Time (DST) index.  If None, default is -20.
    by_imf
        BY Interplanetary Magnetic Field (IMF).  If None, default
        is 0.0.
    bz_imf
        BZ Interplanetary Magnetic Field (IMF).  If None, default
        is 0.0.
    """
    def __init__(self,
                 solar_wind_pressure: float = None,
                 dst_index: int = None,
                 by_imf: float = None,
                 bz_imf: float = None):

        super().__init__(ExternalBFieldModelName.TSYGANENKO96)

        if solar_wind_pressure is None:
            self._solar_wind_pressure = 2.1
        else:
            self._solar_wind_pressure = solar_wind_pressure

        if dst_index is None:
            self._dst_index = -20
        else:
            self._dst_index = dst_index

        if by_imf is None:
            self._by_imf = 0.0
        else:
            self._by_imf = by_imf

        if bz_imf is None:
            self._bz_imf = 0.0
        else:
            self._bz_imf = bz_imf


    def xml_element(self) -> ET:
        """
        Produces the XML Element representation of this object.

        Returns
        -------
        ET
            XML Element represenation of this object.
        """

        xml_element = super().xml_element()

        builder = ET.TreeBuilder()
        builder.start('SolarWindPressure', {})
        builder.data(str(self._solar_wind_pressure))
        builder.end('SolarWindPressure')
        xml_element.append(builder.close())

        builder = ET.TreeBuilder()
        builder.start('DstIndex', {})
        builder.data(str(self._dst_index))
        builder.end('DstIndex')
        xml_element.append(builder.close())

        builder = ET.TreeBuilder()
        builder.start('ByImf', {})
        builder.data(str(self._by_imf))
        builder.end('ByImf')
        xml_element.append(builder.close())

        builder = ET.TreeBuilder()
        builder.start('BzImf', {})
        builder.data(str(self._bz_imf))
        builder.end('BzImf')
        xml_element.append(builder.close())

        return xml_element


class Tsyganenko87Kp(Enum):
    """
    Enumerations representing the Tsyganenko87Kp defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    KP_0_0 = 'KP0_0'
    KP_1_1_1 = 'KP1_1_1'
    KP_2_2_2 = 'KP2_2_2'
    KP_3_3_3 = 'KP3_3_3'
    KP_4_4_4 = 'KP4_4_4'
    KP_5 = 'KP5'


class Tsyganenko87BFieldModel(ExternalBFieldModel):
    """
    Class representing the Tsyganenko87BFieldModel defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Parameters
    ----------
    key_parameters
        Model key parameter values.  If None, default is
        Tsyganenko87Kp.KP_3_3_3.
    """
    def __init__(self,
                 key_parameters: Tsyganenko87Kp = None):

        super().__init__(ExternalBFieldModelName.TSYGANENKO87)

        if key_parameters is None:
            self._key_parameters = Tsyganenko87Kp.KP_3_3_3
        else:
            self._key_parameters = key_parameters


    def xml_element(self) -> ET:
        """
        Produces the XML Element representation of this object.

        Returns
        -------
        ET
            XML Element represenation of this object.
        """

        xml_element = super().xml_element()

        builder = ET.TreeBuilder()
        builder.start('KeyParameterValues', {})
        builder.data(self._key_parameters.value)
        builder.end('KeyParameterValues')

        xml_element.append(builder.close())

        return xml_element


class Tsyganenko89cKp(Enum):
    """
    Enumerations representing the Tsyganenko89cKp defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.
    """
    KP_0_0 = 'KP0_0'
    KP_1_1_1 = 'KP1_1_1'
    KP_2_2_2 = 'KP2_2_2'
    KP_3_3_3 = 'KP3_3_3'
    KP_4_4_4 = 'KP4_4_4'
    KP_5_5_5 = 'KP5_5_5'
    KP_6 = 'KP6'


class Tsyganenko89cBFieldModel(ExternalBFieldModel):
    """
    Class representing the Tsyganenko89cBFieldModel defined
    in <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Parameters
    ----------
    key_parameters
        Model key parameter values.  If None, default is
        Tsyganenko89cKp.KP_3_3_3.
    """
    def __init__(self,
                 key_parameters: Tsyganenko89cKp = None):

        super().__init__(ExternalBFieldModelName.TSYGANENKO89C)

        if key_parameters is None:
            self._key_parameters = Tsyganenko89cKp.KP_3_3_3
        else:
            self._key_parameters = key_parameters


    def xml_element(self) -> ET:
        """
        Produces the XML Element representation of this object.

        Returns
        -------
        ET
            XML Element represenation of this object.
        """

        xml_element = super().xml_element()

        builder = ET.TreeBuilder()
        builder.start('KeyParameterValues', {})
        builder.data(self._key_parameters.value)
        builder.end('KeyParameterValues')

        xml_element.append(builder.close())

        return xml_element


class BFieldModel:
    """
    Class representing a BFieldModel from
    <https://sscweb.gsfc.nasa.gov/WebServices/REST/SSC.xsd>.

    Parameters
    ----------
    internal
        Internal B field model.  If None, the default is
        InternalBFieldModel.IGRF.
    external
        External B field model.  If None, the default is
        Tsyganenko 89c with KP 3-,3,3+.
    trace_stop_altitude
        Stop altitude for downward tracing of field lines.  If None,
           the default is 100km.

    """
    def __init__(self,
                 internal: InternalBFieldModel = None,
                 external: ExternalBFieldModel = None,
                 trace_stop_altitude: int = None):

        if internal is None:
            self._internal = InternalBFieldModel.IGRF
        else:
            self._internal = internal

        if external is None:
            self._external = Tsyganenko89cBFieldModel()
        else:
            self._external = external

        if trace_stop_altitude is None:
            self._trace_stop_altitude = 100
        else:
            self._trace_stop_altitude = trace_stop_altitude


    @property
    def internal(self) -> InternalBFieldModel:
        """
        Gets the internal value.

        Returns
        -------
        InternalBFieldModel
            internal value.
        """
        return self._internal


    @internal.setter
    def internal(self, value: InternalBFieldModel):
        """
        Sets the internal value.

        Parameters
        ----------
        value
            internal value.
        """
        self._internal = value


    @property
    def external(self) -> ExternalBFieldModel:
        """
        Gets the external value.

        Returns
        -------
        ExternalBFieldModel
            external value.
        """
        return self._external


    @external.setter
    def external(self, value: ExternalBFieldModel):
        """
        Sets the external value.

        Parameters
        ----------
        value
            external value.
        """
        self._external = value


    @property
    def trace_stop_altitude(self) -> int:
        """
        Gets the trace_stop_altitude value.

        Returns
        -------
        int
            trace_stop_altitude value.
        """
        return self._trace_stop_altitude


    @trace_stop_altitude.setter
    def trace_stop_altitude(self, value: int):
        """
        Sets the trace_stop_altitude value.

        Parameters
        ----------
        value
            trace_stop_altitude value.
        """
        self._trace_stop_altitude = value


    def xml_element(self) -> ET:
        """
        Produces the XML Element representation of this object.

        Returns
        -------
        ET
            XML Element represenation of this object.
        """

        builder = ET.TreeBuilder()
        builder.start('BFieldModel', {})
        builder.start('InternalBFieldModel', {})
        builder.data(self._internal.value)
        builder.end('InternalBFieldModel')

        builder.start('TraceStopAltitude', {})
        builder.data(str(self._trace_stop_altitude))
        builder.end('TraceStopAltitude')

        builder.end('BFieldModel')

        xml_element = builder.close()
        xml_element.append(self._external.xml_element())

        return xml_element
