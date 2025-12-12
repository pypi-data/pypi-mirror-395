#
# Copyright (c) 2020-2021, 2023, 2024 eGauge Systems LLC
#       1644 Conestoga St, Suite 2
#       Boulder, CO 80301
#       voice: 720-545-9767
#       email: davidm@egauge.net
#
# All rights reserved.
#
# MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
import decimal
import json

from ..error import Error
from .device import Device
from .register_row import RegisterRow
from .register_type import RegisterType


class LocalError(Error):
    """All errors in this module raise this exception."""


def sensor_port_name(index: int) -> str:
    """Get the canonical sensor port name for a port number.

    Required arguments:

    index -- The index of the sensor port whose name to return.  It
        must be in the range from 0..NUM_PORTS-1, where NUM_PORTS is
        the number of sensor ports supported by the meter.

    """
    sensor = index + 1
    return f"S{sensor}"


class Local:
    """Fetch data from /api/local."""

    # Sensor parameter spec strings:
    #   For l=...:
    SPEC_L1 = "L1"
    SPEC_L2 = "L2"
    SPEC_L3 = "L3"
    SPEC_L1_L2 = "L12"
    SPEC_L2_L3 = "L23"
    SPEC_L3_L1 = "L31"
    SPEC_LDC = "Ldc"
    SPEC_D1 = "D1"
    SPEC_D2 = "D2"
    SPEC_D3 = "D3"

    # Sensor names as they appear in the output:
    NAME_L1 = "L1"
    NAME_L2 = "L2"
    NAME_L3 = "L3"
    NAME_L1_L2 = "L1-L2"
    NAME_L2_L3 = "L2-L3"
    NAME_L3_L1 = "L3-L1"
    NAME_LDC = "Ldc"
    NAME_D1 = "D1"
    NAME_D2 = "D2"
    NAME_D3 = "D3"
    NAME_TEMP_PCB = "Tpcb"
    NAME_HUMID_PCB = "Hpcb"

    METRIC_RATE = "rate"
    METRIC_CUMUL = "cumul"
    METRIC_TYPE = "type"

    MEASUREMENT_NORMAL = "n"
    MEASUREMENT_MEAN = "m"
    MEASUREMENT_FREQ = "f"

    SECTION_VALUES = "values"
    SECTION_ENERGY = "energy"
    SECTION_APPARENT = "apparent"

    def __init__(self, dev: Device, params, **kwargs):
        self.raw = dev.get("/local", params=params, **kwargs)

    def ts(self) -> decimal.Decimal | None:
        """Return the timestamp of the local data in seconds since the
        Unix epoch.

        """
        if self.raw is None:
            return None
        return decimal.Decimal(self.raw["ts"])

    def type_code(self, sensor_name: str) -> str | None:
        """Return the type-code of a sensor.

        Required arguments:

        sensor_name -- The name of the sensor whose type-code to
        return.

        """
        if self.raw is None:
            return None
        try:
            return self.raw["values"][sensor_name]["type"]
        except KeyError:
            pass
        return None

    def rate(
        self,
        sensor_name: str,
        measurement: str = MEASUREMENT_NORMAL,
        section: str = SECTION_VALUES,
    ) -> float | None:
        """Return the rate of change value of a sensor.

        Required arguments:

        sensor_name -- The name of the sensor whose rate to return.

        Keyword arguments:

        measurement -- The measurement that should be returned for the
            sensor (default MEASUREMENT_NORMAL).  The mean (average)
            value can be requested with MEASUREMENT_MEAN or the
            frequency at which the sensor's value crosses zero can be
            requested with MEASUREMENT_FREQ.  If the requested value
            is unavailable, 'None' is returned.

        section -- The section to return the rate from (default
            SECTION_VALUES).  Can be one of SECTION_VALUES,
            SECTION_ENERGY, or SECTION_APPARENT.

        """
        if self.raw is None:
            return None
        try:
            m = self.raw[section][sensor_name]["rate"]
            if section == Local.SECTION_VALUES:
                return m[measurement]
            return m
        except KeyError:
            pass
        return None

    def cumul(
        self,
        sensor_name: str,
        measurement: str = MEASUREMENT_NORMAL,
        section: str = SECTION_VALUES,
    ) -> int | None:
        """Return the cumulative value of a sensor.

        Required arguments:

        sensor_name -- The name of the sensor whose rate to return.

        Keyword arguments:

        measurement -- The measurement that should be returned for the
            sensor (default MEASUREMENT_NORMAL).  The mean (average)
            value can be requested with MEASUREMENT_MEAN or the
            frequency at which the sensor's value crosses zero can be
            requested with MEASUREMENT_FREQ.  If the requested value
            is unavailable, 'None' is returned.

        section -- The section to return the rate from (default
            SECTION_VALUES).  Can be one of SECTION_VALUES,
            SECTION_ENERGY, or SECTION_APPARENT.

        """
        if self.raw is None:
            return None
        try:
            m = self.raw[section][sensor_name]["cumul"]
            if section == Local.SECTION_VALUES:
                return int(m[measurement])
            return int(m)
        except KeyError:
            pass
        return None

    def row(
        self,
        metric: str = METRIC_CUMUL,
        measurement: str = MEASUREMENT_NORMAL,
        section: str = SECTION_VALUES,
    ):
        """Return a timestamped row of register data.

        Keyword arguments:

        metric -- The metric to return (default METRIC_CUMUL).  May be
            one of METRIC_RATE or METRIC_CUMUL.

        measurement -- The measurement that should be returned for the
            sensor (default MEASUREMENT_NORMAL).  The mean (average)
            value can be requested with MEASUREMENT_MEAN or the
            frequency at which the sensor's value crosses zero can be
            requested with MEASUREMENT_FREQ.  If the requested value
            is unavailable, 'None' is returned.

        section -- The section to return the rate from (default
            SECTION_VALUES).  Can be one of SECTION_VALUES,
            SECTION_ENERGY, or SECTION_APPARENT.

        """
        if metric not in [Local.METRIC_RATE, Local.METRIC_CUMUL]:
            raise LocalError(
                "Metric must be one of METRIC_RATE or METRIC_CUMUL", metric
            )

        if self.raw is None:
            return None
        regs = {}
        type_codes = {}
        is_diff = True
        if metric == Local.METRIC_CUMUL:
            is_diff = False
        for key, metrics in self.raw[section].items():
            if metric not in metrics:
                continue
            val = metrics[metric]
            if section == Local.SECTION_VALUES:
                val = val[measurement]
            if metric == Local.METRIC_CUMUL:
                val = int(val)  # convert from decimal string to integer
            regs[key] = val
            if section == Local.SECTION_ENERGY:
                # this assumes the sensor pairs measure voltage and current:
                tc = RegisterType.POWER.value
            elif section == Local.SECTION_APPARENT:
                # this assumes the sensor pairs measure voltage and current:
                tc = RegisterType.APPARENT_POWER.value
            elif measurement == Local.MEASUREMENT_FREQ:
                tc = RegisterType.FREQ.value
            elif Local.METRIC_TYPE in metrics:
                tc = metrics[Local.METRIC_TYPE]
            else:
                raise LocalError(f"Internal error: unknown section {section}")

            regs[key] = val
            type_codes[key] = tc
        return RegisterRow(self.ts(), regs, type_codes, is_diff)

    def __str__(self) -> str:
        """Return the raw data of the object as a JSON-encoded
        string."""
        return json.dumps(self.raw)
