#
# Copyright (c) 2020-2021, 2024 eGauge Systems LLC
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
"""This module provides access to the eGauge WebAPI's /api/ctid
service."""

import datetime
import os
import secrets
import time
from collections.abc import Sequence

from egauge import ctid, webapi

from ..error import Error

SCAN_TIMEOUT = 2.5  # scan timeout in seconds

Polarity = str  # must be one of "+" or "-"


def ctid_info_to_table(reply: dict) -> ctid.Table:
    """Convert a ctid reply to a ctid.Table object.

    Required arguments:

    reply -- A response returned by WebAPI endpoint `/ctid/N`, where
        `N` is a sensor port number.

    """
    t = ctid.Table()
    t.version = reply.get("version", 0)
    t.mfg_id = reply.get("mfgid", 0)
    t.model = reply.get("model", "unknown")
    t.serial_number = reply.get("sn", 0)
    t.sensor_type = reply.get("k", ctid.SENSOR_TYPE_AC)
    t.r_source = reply.get("rsrc", 0)
    t.r_load = reply.get("rload", 0)

    params = reply.get("params", {})
    t.size = params.get("size")
    t.rated_current = params.get("i")
    t.voltage_at_rated_current = params.get("v")
    t.phase_at_rated_current = params.get("a")
    t.voltage_temp_coeff = params.get("tv")
    t.phase_temp_coeff = params.get("ta")
    t.cal_table = {}
    cal_table = params.get("cal", {})
    for l_str in cal_table:
        l = float(l_str)
        t.cal_table[l] = [
            cal_table[l_str].get("v", 0),
            cal_table[l_str].get("a", 0),
        ]
    t.bias_voltage = params.get("bias_voltage", 0)
    t.scale = params.get("scale")
    t.offset = params.get("offset")
    t.delay = params.get("delay")
    t.threshold = params.get("threshold")
    t.hysteresis = params.get("hysteresis")
    t.debounce_time = params.get("debounce_time")
    t.edge_mask = params.get("edge_mask")
    t.ntc_a = params.get("ntc_a")
    t.ntc_b = params.get("ntc_b")
    t.ntc_c = params.get("ntc_c")
    t.ntc_m = params.get("ntc_m")
    t.ntc_n = params.get("ntc_n")
    t.ntc_k = params.get("ntc_k")
    return t


class CTidInfoError(Error):
    """This is used for any errors raised by this module."""


class PortInfo:
    """Encapsulates the port number on which a CTid table was read,
    the polarity which is was read with, and the table itself.

    """

    def __init__(
        self, port: int, polarity: Polarity | None, table: ctid.Table | None
    ):
        self.port = port
        self.polarity = polarity
        self.table = table

    def port_name(self) -> str:
        """Return the canonical port name."""
        return "S%d" % self.port

    def short_mfg_name(self) -> str:
        """Return the short (concise) name of the manufacturer of the sensor
        or `-' if unknown.

        """
        if self.table is None or self.table.mfg_id is None:
            return "-"
        return ctid.mfg_short_name(self.table.mfg_id) or "-"

    def model_name(self) -> str:
        """Return the model name of the sensor attached to the port.  If
        unknown `-' is returned.

        """
        if self.table is None or self.table.model is None:
            return "-"
        return self.table.model

    def mfg_model_name(self) -> str:
        """Return a "fully qualified" model name, which consists of
        the short version of the manufacter's name, a dash, and the
        model name.

        """
        return "%s-%s" % (self.short_mfg_name(), self.model_name())

    def sn(self) -> int | None:
        """Return the serial number or None if unknown."""
        if self.table is None or not isinstance(self.table.serial_number, int):
            return None
        return self.table.serial_number

    def serial_number(self) -> str:
        """Return the serial number of the sensor attached to the port as a
        decimal string.  If unknown, '-' is returned.

        """
        if self.table is None or self.table.serial_number is None:
            return "-"
        return str(self.table.serial_number)

    def unique_name(self) -> str:
        """Return a sensor's unique name, which is a string consisting of the
        manufacturer's short name, the model name, and the serial
        number, all separated by dashes..

        """
        return f"{self.mfg_model_name()}-{self.serial_number()}"

    def sensor_type(self) -> int | None:
        """Return the sensor type of the sensor attached to the port or None
        if unknown.

        """
        if self.table is None or self.table.sensor_type is None:
            return None
        return self.table.sensor_type

    def sensor_type_name(self) -> str:
        """Return the name of the sensor type of the sensor attached to the
        port or '-' if unknown.

        """
        st = self.sensor_type()
        if st is None:
            return "-"
        return ctid.get_sensor_type_name(st) or "-"

    def as_dict(self) -> dict | None:
        """Return CTid info as a serializable dictionary."""
        if self.table is None:
            return None
        params = {}
        p = {
            "port": self.port,
            "polarity": self.polarity,
            "version": self.table.version,
            "mfgid": self.table.mfg_id,
            "model": self.table.model,
            "sn": self.table.serial_number,
            "k": self.table.sensor_type,
            "rsrc": self.table.r_source,
            "rload": self.table.r_load,
            "params": params,
        }
        if self.table.sensor_type in [
            ctid.SENSOR_TYPE_AC,
            ctid.SENSOR_TYPE_DC,
            ctid.SENSOR_TYPE_RC,
        ]:
            params["size"] = self.table.size
            params["i"] = self.table.rated_current
            params["v"] = self.table.voltage_at_rated_current
            params["a"] = self.table.phase_at_rated_current
            params["tv"] = self.table.voltage_temp_coeff
            params["ta"] = self.table.phase_temp_coeff
            params["bias_voltage"] = self.table.bias_voltage
            cal_table = {}
            for l, row in self.table.cal_table.items():
                cal_table[l] = {"v": row[0], "a": row[1]}
            params["cal"] = cal_table
        elif self.table.sensor_type == ctid.SENSOR_TYPE_VOLTAGE:
            params["scale"] = self.table.scale
            params["offset"] = self.table.offset
            params["delay"] = self.table.delay
        elif self.table.sensor_type == ctid.SENSOR_TYPE_TEMP_LINEAR:
            params["scale"] = self.table.scale
            params["offset"] = self.table.offset
        elif self.table.sensor_type == ctid.SENSOR_TYPE_TEMP_NTC:
            params["ntc_a"] = self.table.ntc_a
            params["ntc_b"] = self.table.ntc_b
            params["ntc_c"] = self.table.ntc_c
            params["ntc_m"] = self.table.ntc_m
            params["ntc_n"] = self.table.ntc_n
            params["ntc_k"] = self.table.ntc_k
        elif self.table.sensor_type == ctid.SENSOR_TYPE_PULSE:
            params["threshold"] = self.table.threshold
            params["hysteresis"] = self.table.hysteresis
            params["debounce_time"] = self.table.debounce_time
            params["edge_mask"] = self.table.edge_mask
        return p

    def __str__(self) -> str:
        return (
            f"(port={self.port},polarity={self.polarity},table={self.table})"
        )


class CTidInfo:
    def __init__(self, dev):
        """A CTidInfo object provides to access the WebAPI CTid
        service of a meter. The service allows reading CTid info from
        a particular port, scanning a port, flashing the attached
        sensor's indicator LED, or iterating over all the ports with
        CTid information.

        """
        self.dev = dev
        self.tid = None
        self.info = None
        self.index = 0
        self.polarity = None
        self.port_number = None

    def _make_tid(self):
        """Create a random transaction id and store it in `self.tid`."""
        self.tid = secrets.randbits(32)
        if self.tid < 1:
            self.tid += 1

    def stop(self):
        """Stop pending CTid operation, if any."""
        if self.tid is not None:
            self.dev.post("/ctid/stop", {})
        self.tid = None

    def scan_start(self, port_number: int, polarity: Polarity):
        """Initiate a CTid scan.

        Raises CTidInfoError on errors.

        Required arguments:

        port_number -- The number of the port to scan.  Number 1 is
            the first port.  The maximum port number depends on the
            meter.

        polarity -- The polarity with which to scan the port.  "+"
            indicates normal polarity, "-" indicates reversed
            polarity.

        """
        if port_number < 1:
            raise CTidInfoError("Invalid port number.", port_number)
        if self.tid is not None:
            self.stop()
        self._make_tid()
        self.polarity = polarity
        self.port_number = port_number
        data = {"op": "scan", "tid": self.tid, "polarity": polarity}
        resource = "/ctid/%d" % port_number
        last_e = None
        for _ in range(3):
            try:
                reply = self.dev.post(resource, data)
                if reply.get("status") == "OK":
                    return
            except Error as e:
                last_e = e
        raise CTidInfoError(
            "Failed to initiate CTid scan", port_number, polarity
        ) from last_e

    def scan_result(self) -> PortInfo | None:
        """Get the result of a port scan.

        This attempts to read the result from a CTid scan initiated
        with a call to CTidInfo.scan_start().  If the result is not
        available yet, None is returned.  In that case, the caller
        should wait a little and then retry the request again for up
        to SCAN_TIMEOUT seconds.

        The the result is available, a CTidInfo.PortInfo object is
        returned.

        Raises CTidInfoError on errors.

        """
        if not isinstance(self.port_number, int):
            raise CTidInfoError("CTidInfo.scan_start() must be called first.")

        if not isinstance(self.polarity, Polarity):
            raise CTidInfoError(f"Invalid polarity {self.polarity}.")

        resource = "/ctid/%d" % self.port_number
        reply = self.dev.get(resource, params={"tid": self.tid})
        if (
            reply.get("port") == self.port_number
            and reply.get("tid") == self.tid
        ):
            return PortInfo(
                self.port_number, self.polarity, ctid_info_to_table(reply)
            )
        return None

    def scan(
        self,
        port_number: int,
        polarity: Polarity | None = None,
        timeout: float = SCAN_TIMEOUT,
    ):
        """Synchronously scan the CTid information of a port.

        This is a convenience method which calls CTidInfo.scan_start()
        followed by repeated calls to CTidInfo.scan_result() until the
        scan is complete or the operation times out.  If no CTid info
        could be read from the port, the returned PortInfo's table
        property will be `None`.

        Required arguments:

        port_number -- The port to scan.  Number 1 is the first port.

        Keyword arguments:

        polarity -- The polarity with which to scan the port.  "+"
            indicates normal polarity, "-" indicates reversed
            polarity.  If None, a scan is first attempted with normal
            polarity and if that times out, a scan is attempted with
            reversed polarity (default None).

        timeout -- The maximum time in seconds to wait for the
            operation to complete (default SCAN_TIMEOUT = 2.5
            seconds).

        Raises CTidInfoError on errors.

        """
        polarity_list = ["+", "-"] if polarity is None else [polarity]
        for pol in polarity_list:
            self.scan_start(port_number, pol)

            start_time = datetime.datetime.now()
            while True:
                time.sleep(0.25)
                result = self.scan_result()
                if result is not None:
                    return result
                elapsed = (
                    datetime.datetime.now() - start_time
                ).total_seconds()
                if elapsed > timeout:
                    break
            self.stop()
        return PortInfo(port_number, None, None)

    def flash(self, port_number: int, polarity: Polarity = "-"):
        """Start flashing (blinking) the indicator LED of a
        CTid-enabled sensor.

        Flashing will continue until CTidInfo.stop() is called or
        until a timeout occurs after about 30 minutes.

        Required arguments:

        port_number -- The port number of the sensor to flash.

        Keywoard arguments:

        polarity -- The polarity to use for flashing the LED.  This
            defaults to negative polarity since, with a correctly
            wired sensor, that will result in the LED flashing at
            about 2 Hz.  If the sensor wiring is reversed, the LED
            will still flash, albeit slower.

        Raises CTidInfoError on errors.

        """
        if port_number < 1:
            raise CTidInfoError("Invalid port number.", port_number)
        if self.tid is not None:
            self.stop()
        self._make_tid()
        data = {"op": "flash", "tid": self.tid, "polarity": polarity}
        resource = "/ctid/%d" % port_number
        for _ in range(3):
            try:
                reply = self.dev.post(resource, data)
                if reply.get("status") == "OK":
                    break
            except Error:
                pass

    def delete(self, port_number: int):
        """Delete the CTid information stored for a port.

        Note that this only deletes the CTid information that the
        meter has saved (cached) in its storage - it does not delete
        any information from the sensor itself.

        Required arguments:

        port_number -- The number of the port whose CTid info is to be
            deleted.

        Raises CTidInfoError on errors.

        """
        if port_number < 1:
            raise CTidInfoError("Invalid port number.", port_number)
        resource = "/ctid/%d" % port_number
        reply = self.dev.delete(resource)
        if reply is None or reply.get("status") != "OK":
            reason = reply.get("error") if reply is not None else "timed out"
            raise CTidInfoError(
                "Failed to delete CTid info.", port_number, reason
            )

    def get(self, port_number: int) -> PortInfo | None:
        """Get the CTid information stored for a given port.

        If no information is stored, None is returned.

        port_number -- The number of the port whose CTid info is to be
            returned.

        """
        if port_number < 1:
            raise CTidInfoError("Invalid port number.", port_number)
        resource = "/ctid/%d" % port_number
        reply = self.dev.get(resource)
        if reply is None:
            raise CTidInfoError("Failed to read CTid info.", port_number)
        if not reply:
            return None
        if reply.get("port") != port_number:
            raise CTidInfoError(
                "CTid info has incorrect port number.",
                reply.get("port"),
                port_number,
            )
        return PortInfo(
            port_number, reply.get("polarity"), ctid_info_to_table(reply)
        )

    def put(self, port_info: PortInfo | Sequence[PortInfo]):
        """Store CTid info for a given port to the meter.

        Note that this only stores the info on the meter - it does not
        affect the info stored in the CTid-enabled sensors themselves.

        Required arguments:

        port_info -- The port info to store on the meter.  If a list,
            the meter will first delete the CTid info of all ports and
            then save the CTidInfo given in the PortInfo list.

        Raises CTidInfoError on errors.

        """
        if isinstance(port_info, PortInfo):
            resource = f"/ctid/{port_info.port}"
            data = port_info.as_dict()
        else:
            resource = "/ctid"
            data = {"info": [pi.as_dict() for pi in port_info]}
        reply = self.dev.put(resource, json_data=data)
        if reply is None:
            raise CTidInfoError("PUT of CTid info failed.")
        if reply.get("status") != "OK":
            raise CTidInfoError("Failure saving CTid info.", data, reply)

    def __iter__(self):
        """Iterate over all available CTid information."""
        reply = self.dev.get("/ctid")
        self.info = reply.get("info", [])
        self.index = 0
        return self

    def __next__(self):
        if self.info is None or self.index >= len(self.info):
            raise StopIteration
        info = self.info[self.index]
        t = ctid_info_to_table(info)
        self.index += 1
        return PortInfo(info["port"], info["polarity"], t)


def test():
    from . import device

    dut = os.getenv("EGDEV") or "http://1608050004.lan"
    usr = os.getenv("EGUSR") or "owner"
    pwd = os.getenv("EGPWD") or "default"
    ctid_info = CTidInfo(device.Device(dut, auth=webapi.JWTAuth(usr, pwd)))
    print("SCANNING")
    port_info = ctid_info.scan(port_number=3)
    print("  port_info[%d]" % port_info.port, port_info.table)
    print("-" * 40)
    print("ITERATING")
    for t in ctid_info:
        print("  port %d%s:" % (t.port, t.polarity), t.table)

    print("DELETING")
    ctid_info.delete(port_number=3)
    port_info = ctid_info.get(port_number=3)
    if port_info is None:
        print("  no CTid info for port 3")
    else:
        print("  port_info[%d]" % port_info.port, port_info.table)

    print("FLASHING")
    ctid_info.flash(port_number=3)
    time.sleep(5)
    ctid_info.stop()
