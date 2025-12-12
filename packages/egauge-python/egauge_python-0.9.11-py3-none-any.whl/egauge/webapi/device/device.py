#
# Copyright (c) 2020, 2022-2024 eGauge Systems LLC
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
"""Module to provide access to a device's JSON WebAPI."""

from dataclasses import dataclass

from .. import json_api
from ..auth import JWTAuth
from ..error import Error
from ..json_api import JSONAPIError
from .virtual_register import VirtualRegister


class DeviceError(Error):
    """Raised if for device related errors."""


@dataclass
class ChannelInfo:
    chan: int  # the channel number
    unit: str  # the physical unit of the channel data


@dataclass
class RegInfo:
    idx: int
    tc: str
    formula: VirtualRegister | None


def _json_obj(reply) -> dict:
    """Convert a JSON API response to an object.

    Raises JSONAPIError("Reply is not a JSON object.") if the response
    is not an object.

    Raises JSONAPIError("WebAPI error: {err}") if the response
    contains a member of name "error".  {err} is the value of that
    member.

    """
    if not isinstance(reply, dict):
        raise JSONAPIError("Reply is not a JSON object.", reply)

    err = reply.get("error")
    if err:
        raise JSONAPIError(f"WebAPI error: {err}")

    return reply


class Device:
    """This class provides access to an eGauge device's JSON WebAPI.
    See "Web API Design" document for details."""

    def __init__(
        self,
        dev_uri: str,
        auth: JWTAuth | None = None,
        verify: bool | str = True,
    ):
        """Return a device object that can be used to access the meter
        which supports WebAPI.

        Required arguments:

        dev_uri -- The device URI of the meter such as
            "http://eGaugeHQ.egauge.io".

        Keyword arguments:

        auth -- An authentication object that provides the credentials
            to access the device (default None).

        verify -- If False, certificate verification is disabled.  It
            may also be a string in which case it must be the path of
            a file that holds the CA bundle to use (default True).

        """
        self.dev_uri = dev_uri
        self.api_uri = dev_uri + "/api"
        self.auth = auth
        self._reg_info = None  # cached register info
        self._chan_info = None  # cached channel info
        self._verify = verify

    def __str__(self) -> str:
        """Returns the device URI of the meter."""
        return self.dev_uri

    def get(self, resource: str, **kwargs) -> dict:
        """Issue GET request to a WebAPI resource and return the
        resulting response object.

        Raises JSONAPIError if the request fails for any reason.

        Required arguments:

        resource -- URI of the resource to access.

        Keyword arguments:

        Any keyword arguments are passed on to requests.get().

        """
        if "verify" not in kwargs:
            kwargs["verify"] = self._verify
        return _json_obj(
            json_api.get(self.api_uri + resource, auth=self.auth, **kwargs)
        )

    def put(self, resource: str, json_data, **kwargs) -> dict:
        """Issue a PUT request to a WebAPI resource and return the
        resulting response object.

        Raises JSONAPIError if the request fails for any reason.

        Required arguments:

        resource -- URI of the resource to access.

        json_data -- The data to JSON-encode and pass in the request
            body.

        Keyword arguments:

        Any keyword arguments are passed on to requests.get().

        """
        if "verify" not in kwargs:
            kwargs["verify"] = self._verify
        return _json_obj(
            json_api.put(
                self.api_uri + resource, json_data, auth=self.auth, **kwargs
            )
        )

    def post(self, resource, json_data, **kwargs) -> dict:
        """Issue a POST request to a WebAPI resource and return the
        resulting response object.

        Raises JSONAPIError if the request fails for any reason.

        Required arguments:

        resource -- URI of the resource to access.

        json_data -- The data to JSON-encode and pass in the request
            body.

        Keyword arguments:

        Any keyword arguments are passed on to requests.get().

        """
        if "verify" not in kwargs:
            kwargs["verify"] = self._verify
        return _json_obj(
            json_api.post(
                self.api_uri + resource, json_data, auth=self.auth, **kwargs
            )
        )

    def delete(self, resource: str, **kwargs):
        """Issue a DELETE request to a WebAPI resource and return the
        resulting response object.

        Raises JSONAPIError if the request fails for any reason.

        Required arguments:

        resource -- URI of the resource to access.

        Keyword arguments:

        Any keyword arguments are passed on to requests.get().

        """
        if "verify" not in kwargs:
            kwargs["verify"] = self._verify
        return _json_obj(
            json_api.delete(self.api_uri + resource, auth=self.auth, **kwargs)
        )

    def _fetch_reg_info(self) -> dict[str, RegInfo]:
        """Fetch register info, including type and virtual register
        formulas.

        """
        reply = self.get("/register", params={"virtual": "formula"})
        regs = reply.get("registers")
        if not isinstance(regs, list):
            raise DeviceError("Failed to fetch register info.", reply)
        reg_info = {}
        for reg in regs:
            formula = reg.get("formula")
            vreg = VirtualRegister(formula) if formula else None
            ri = RegInfo(reg["idx"], reg["type"], vreg)
            reg_info[reg["name"]] = ri
        return reg_info

    def reg_idx(self, regname: str) -> int:
        """Return the register index of a register. The returned
        information is cached in the device object since it is
        relatively expensive to acquire. If the meter configuration
        changes, this information must be flushed with a call to
        Device.clear_cache().

        Required arguments:

        regname -- The name of the register whose index to return.

        """
        if self._reg_info is None:
            self._reg_info = self._fetch_reg_info()
        return self._reg_info[regname].idx

    def reg_type(self, regname: str) -> str:
        """Return the type code of a register. The returned
        information is cached in the device object since it is
        relatively expensive to acquire. If the meter configuration
        changes, this information must be flushed with a call to
        Device.clear_cache().

        Required arguments:

        regname -- The name of the register whose index to return.

        """
        if self._reg_info is None:
            self._reg_info = self._fetch_reg_info()
        return self._reg_info[regname].tc

    def reg_virtuals(self) -> list[str]:
        """Return the list of virtual register names. The returned
        information is cached in the device object since it is
        relatively expensive to acquire. If the meter configuration
        changes, this information must be flushed with a call to
        Device.clear_cache().

        Required arguments:

        regname -- The name of the register whose index to return.

        """
        if self._reg_info is None:
            self._reg_info = self._fetch_reg_info()
        virts = []
        for reg, ri in self._reg_info.items():
            if ri.formula:
                virts.append(reg)
        return virts

    def reg_formula(self, regname: str) -> VirtualRegister | None:
        """Return the VirtualRegister object of a register or None if
        the named register is not a virtual register. The returned
        information is cached in the device object since it is
        relatively expensive to acquire. If the meter configuration
        changes, this information must be flushed with a call to
        Device.clear_cache().

        Required arguments:

        regname -- The name of the register whose VirtualRegister
            object to return.

        """
        if self._reg_info is None:
            self._reg_info = self._fetch_reg_info()
        return self._reg_info[regname].formula

    def _fetch_chan_info(self) -> dict[str, ChannelInfo]:
        """Fetch channel info from /capture."""
        reply = self.get("/capture", params={"i": ""})
        if reply is None or "channels" not in reply:
            raise DeviceError("Failed to get channel info.", reply)

        channels = reply["channels"]
        if not isinstance(channels, dict):
            raise DeviceError("Invalid channel info.", channels)

        chan_info = {}
        for chan, info in channels.items():
            ci = ChannelInfo(chan=int(chan), unit=info.get("unit"))
            chan_info[info["name"]] = ci
        return chan_info

    def channel_info(self) -> dict[str, ChannelInfo]:
        """Get the channel info as provided by /api/cap?i. The
        returned information is cached in the device object since it
        is relatively expensive to acquire. If the meter configuration
        changes, this information must be flushed with a call to
        Device.clear_cache().

        """
        if self._chan_info is None:
            self._chan_info = self._fetch_chan_info()
        return self._chan_info

    def clear_cache(self):
        """Clear the cached contents for this device object."""
        self._reg_info = None
        self._chan_info = None

    def is_up(self, timeout: float = 1) -> bool:
        """Check if the device is up and running.

        This method attempts to read /sys/time.  If a valid response
        is received within the specified timeout, True is returned,
        otherwise False is returned.

        Keyword arguments:

        timeout -- The maximum number of seconds to wait for a
            response (default 1).

        """
        try:
            self.get("/sys/time", timeout=timeout)
        except json_api.JSONAPIError:
            return False
        return True
