#
# Copyright (c) 2020, 2024-2025 eGauge Systems LLC
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
"""This module provides access to the eGauge Serial Number web
service.

"""

import urllib.parse

import requests

from egauge.loggers import ModuleLogger

from .. import json_api
from ..auth import TokenAuth
from ..error import Error
from ..json_api import JSONObject, JSONValue

log = ModuleLogger.get(__name__)


class SerialNumberError(Error):
    """Raised for Serial Number API errors."""


class SerialNumber:
    def __init__(self, auth: TokenAuth | None = None):
        """Create an object providing access to the serial-number
        service.

        Keyword arguments:

        auth -- An authentication object which can provide the
            credentials required to access the serial-number service.

        """
        self.api_uri = "https://api.egauge.net/v1/serial-numbers/"
        self.auth = auth

    def _get(self, resource: str, **kwargs) -> JSONValue | requests.Response:
        """Issue an HTTP GET request for a serial-number resource
        and return the reply.

        Required arguments:

        resource -- The URI of the resource to get.

        Keyword arguments are passed on to requests.get().

        """
        reply = json_api.get(self.api_uri + resource, auth=self.auth, **kwargs)
        log.debug("get[%s] = %s", resource, reply)
        return reply

    def _post(
        self, resource: str, json_data, **kwargs
    ) -> JSONValue | requests.Response:
        """Issue an HTTP POST request to serial-number resource and
        return the reply.

        Required arguments:

        resource -- The URI of the resource to post to.

        Keyword arguments are passed on to requests.get().

        """
        reply = json_api.post(
            self.api_uri + resource, json_data, auth=self.auth, **kwargs
        )
        log.debug("post[%s] = %s", resource, reply)
        return reply

    def allocate(self, model_name: str, serial: int | None = None) -> int:
        """Allocate the next available serial-number for a model and
        return it.

        Required arguments:

        model_name -- The model name for which to allocate a serial
            number.  Typically, this should be prefixed by the
            manufacturer's name to ensure uniqueness.  For example,
            for eGauge model ETN100, the model name would be
            "eGauge-ETN100".  Once allocated, a serial-number cannot
            be freed again, so care should be taken to use all
            allocated numbers.

        Keyword arguments:

        serial -- If specified, allocate that specific serial-number,
            if it is avaiable, or fail otherwise.  Depending on model
            name, the serial-number API service may reject attempts to
            allocate specific serial numbers.

        On error, exception SerialNumberError is raised.

        """
        data: JSONObject = {"name": model_name}
        if serial is not None:
            data["serial"] = serial
        reply = self._post("models/allocate/", json_data=data)
        if not isinstance(reply, dict):
            raise SerialNumberError(
                f"Unexpected response allocating SN for {model_name}.", reply
            )
        if "serial" not in reply:
            log.error(
                "Failed to allocate SN: model=%s, reply=%s.", model_name, reply
            )
            if "errors" in reply:
                raise SerialNumberError(
                    "Error during SN allocation.", model_name, reply["errors"]
                )
            raise SerialNumberError("SN allocation failed.", model_name)
        sn = reply["serial"]
        if not isinstance(sn, int):
            raise SerialNumberError(f'SN "{sn}" is not an integer.')
        return sn

    def get_models(self) -> list[dict]:
        """Get a list of all model names registered in the database.
        Each object in the list has members `id` (internal database id
        of the model), `name` (the model name), and `max_sn` (the
        maximum serial-number).

        On error, exception SerialNumberError is raised.

        """

        # For better or worse, this end point returns a list on
        # success but a dictionary in failure:

        reply = self._get("models/")

        if isinstance(reply, dict):
            err = reply.get("detail")
            if err:
                raise SerialNumberError(f"Error fetching SN models: {err}")

        if not isinstance(reply, list):
            raise SerialNumberError(
                "Unexpected response from SN models.", reply
            )
        return reply

    def create_model(self, model_name: str, max_sn: int) -> bool:
        """Create a new model.

        Returns True if the model was created successfully, False
        otherwise.

        Required arguments:

        model_name -- The name of the model to create.

        max_sn -- The maximum serial number that may be allocated.

        """
        data = {"name": model_name, "max_sn": max_sn}
        reply = self._post("models/", data)
        if not isinstance(reply, dict) or "name" not in reply:
            return False
        return reply["name"] == model_name

    def get_devices(
        self, model_name: str | None = None, dev_filter: str | None = None
    ) -> list[dict]:
        """Get a list of devices.

        Keyword arguments:

        model_name -- If specified, only devices with that model name
            are returned.

        dev_filter -- If specified, only devices matching the filter
            are returned.

        """
        resource = "devices/"
        if model_name is not None:
            quoted_model = urllib.parse.quote(model_name, safe="")
            resource += quoted_model + "/"

        if dev_filter is not None:
            resource += "?" + dev_filter

        reply = self._get(resource)
        if not isinstance(reply, list):
            raise SerialNumberError(
                "Failed to get metadata.", model_name, dev_filter
            )
        return reply

    def get_metadata(self, model_name: str, sn: int) -> dict:
        """Get the JSON-blob metadata for a device.

        On error, exception SerialNumberError is raised.

        Required arguments:

        model_name -- The model name of the device.

        sn -- The serial number of the device.

        """
        quoted_model = urllib.parse.quote(model_name, safe="")
        resource = f"devices/{quoted_model}/{sn}/"
        reply = self._get(resource)
        if not isinstance(reply, dict):
            raise SerialNumberError(
                "Failed to get serial number record.", model_name, sn
            )

        metadata = reply.get("metadata")
        if not isinstance(metadata, dict):
            log.warning("no metadata exists for SN %s.", sn)
            return {}

        return metadata

    def set_metadata(self, model_name: str, sn: int, meta: dict):
        """Set the metadata for a device.

        Using methods get_metadata() and set_metadata() to update
        portions of the metadata is not atomic.  Higher-level
        synchronization (such as a ResourceLock) can be used to ensure
        atomicity of such updates.

        Required arguments:

        model_name -- The model name of the device.

        sn -- The serial number of the device.

        meta -- The meta data to associated with the device.  This
            must be serializable with json.dumps().

        On error, exception SerialNumberError is raised.

        """
        quoted_model = urllib.parse.quote(model_name, safe="")
        resource = "devices/%s/%s/" % (quoted_model, sn)
        reply = self._post(resource, json_data={"metadata": meta})
        if not isinstance(reply, dict):
            raise SerialNumberError("Failed to set metadata.", model_name, sn)
        if "errors" in reply:
            raise SerialNumberError(
                "Failed to save metadata.", model_name, sn, reply["errors"]
            )
