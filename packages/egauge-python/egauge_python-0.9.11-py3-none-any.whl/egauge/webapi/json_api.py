#
# Copyright (c) 2020-2025 eGauge Systems LLC
#       4805 Sterling Dr, Suite 1
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
"""This module provides helper methods for accessing JSON web services."""

import logging
import socket
from typing import Any

import requests

from egauge.loggers import ModuleLogger

from .error import Error

log = ModuleLogger.get(__name__)

JSONObject = dict[str, "JSONValue"]
JSONArray = list[Any]
JSONValue = None | bool | int | float | str | JSONArray | JSONObject


class JSONAPIError(Error):
    """Raised if for any JSON API errors.  The first argument to this
    exception is a textual description of the error which occurred.
    Additional arguments are dependent on the source of the error.

    """


class UnauthenticatedError(Error):
    """Raised when a request fails with HTTP status code 401."""


def _raw_response(kwargs: dict[Any, Any]) -> bool:
    """Check if `raw_response` in kwargs is present and, if so, return
    whether its value is True.

    Required arguments:

    kwargs -- The keyword arguments to be checked.

    """
    if "raw_response" in kwargs:
        raw_response = kwargs["raw_response"]
        del kwargs["raw_response"]
        return raw_response is True
    return False


def _check_status(
    resource: str,
    reply: requests.Response,
    method: str,
    data=None,
    kwargs=None,
):
    """Check status code of the reply.  Raises UnauthenticatedError if
    401 or JSONAPIError if any other status code outside the range of
    200..299.

    Required arguments:

    resource -- The URL the request was issued for.

    reply -- A requests.Response object.

    method -- The name of the HTTP method that resulted in the reply
        ("GET", "POUT", etc.).

    data -- The data passed in the request body.

    kwargs -- The keyword arguments passed to the requests method.

    """
    if reply.status_code == 401:
        raise UnauthenticatedError(reply)
    if reply.status_code < 200 or reply.status_code > 299:
        if log.getEffectiveLevel() <= logging.DEBUG:
            data_str = f", data: {data}. " if data else ""
            kwargs_str = f", kwargs: {kwargs}" if kwargs else ""
            log.debug(
                "HTTP %s %s => %s%s%s",
                method,
                resource,
                reply.status_code,
                data_str,
                kwargs_str,
            )
        raise JSONAPIError(
            "Unexpected HTTP status code.", reply.status_code, reply.content
        )


def _json(reply: requests.Response) -> JSONValue:
    """Convert a response body to a JSONValue.  If there is no
    response body, the response body is empty, or the response body is
    the string "null", None is returned.

    If the body cannot be JSON-decoded, exception JSONAPIError is
    raised with "Invalid JSON data." as the first argument and the
    reply.content as the second argument.

    In all other cases, the JSON-decoded value of the body is
    returned.

    Required arguments:

    reply -- The response object to convert to a JSON value.

    """
    if not reply.text:
        return None

    try:
        return reply.json()
    except requests.JSONDecodeError as e:
        raise JSONAPIError("Invalid JSON data.", reply.content) from e


def get(resource: str, **kwargs) -> JSONValue | requests.Response:
    """Issue an HTTP GET request and return the parsed JSON reply or
    None if there is no response body or the response body is empty
    (note that this is indistinguishable from a body containing the
    string "null", which also returns None).  If keyword argument
    `raw_response` is True, a requests.Response object is returned
    instead.

    Raises UnauthenticatedError if the reply has a status code of 401.

    Raises JSONAPIError if the request fails for any reason or if the
    reply does not have a status code in the range from 200 to 299 or
    401.

    Required arguments:

    resource -- The URL of the resource to issue the request to.

    Keyword arguments:

    raw_response -- If True, return a requests.Response object.

    All other keyword arguments are passed on to requests.get().

    """
    raw = _raw_response(kwargs)
    try:
        r = requests.get(resource, **kwargs)
    except (requests.exceptions.RequestException, socket.error) as e:
        raise JSONAPIError("requests.get exception.", e) from e
    _check_status(resource, r, "GET", kwargs)
    return r if raw else _json(r)


def patch(resource: str, json_data, **kwargs) -> JSONValue | requests.Response:
    """Issue an HTTP PATCH request and return the parsed JSON reply or
    None if there is no response body or the response body is empty
    (note that this is indistinguishable from a body containing the
    string "null", which also returns None).  If keyword argument
    `raw_response` is True, a requests.Response object is returned
    instead.

    Raises UnauthenticatedError if the reply has a status code of 401.

    Raises JSONAPIError if the request fails for any reason or if the
    reply does not have a status code in the range from 200 to 299 or
    401.

    Required arguments:

    resource -- The URL of the resource to issue the request to.

    json_data -- The data to JSON-encode and include in the request
        body.

    Keyword arguments:

    raw_response -- If True, return a requests.Response object.

    All other keyword arguments are passed on to requests.patch().

    """
    headers = kwargs.get("headers", {})
    headers["Content-Type"] = "application/json"
    kwargs["headers"] = headers
    raw = _raw_response(kwargs)
    try:
        r = requests.patch(resource, json=json_data, **kwargs)
    except (requests.exceptions.RequestException, socket.error) as e:
        raise JSONAPIError("requests.patch exception.", e) from e
    _check_status(resource, r, "PATCH", json_data, kwargs)
    return r if raw else _json(r)


def put(resource: str, json_data, **kwargs) -> JSONValue | requests.Response:
    """Issue an HTTP PUT request and return the parsed JSON reply or
    None if there is no response body or the response body is empty
    (note that this is indistinguishable from a body containing the
    string "null", which also returns None).  If keyword argument
    `raw_response` is True, a requests.Response object is returned
    instead.

    Raises UnauthenticatedError if the reply has a status code of 401.

    Raises JSONAPIError if the request fails for any reason or if the
    reply does not have a status code in the range from 200 to 299 or
    401.

    Required arguments:

    resource -- The URL of the resource to issue the request to.

    json_data -- The data to JSON-encode and include in the request
        body.

    Keyword arguments:

    raw_response -- If True, return a requests.Response object.

    All other keyword arguments are passed on to requests.put().

    """
    headers = kwargs.get("headers", {})
    headers["Content-Type"] = "application/json"
    kwargs["headers"] = headers
    raw = _raw_response(kwargs)
    try:
        r = requests.put(resource, json=json_data, **kwargs)
    except (requests.exceptions.RequestException, socket.error) as e:
        raise JSONAPIError("requests.put exception.", e) from e
    _check_status(resource, r, "PUT", json_data, kwargs)
    return r if raw else _json(r)


def post(resource: str, json_data, **kwargs) -> JSONValue | requests.Response:
    """Issue an HTTP POST request and return the parsed JSON reply or
    None if there is no response body or the response body is empty
    (note that this is indistinguishable from a body containing the
    string "null", which also returns None).  If keyword argument
    `raw_response` is True, a requests.Response object is returned
    instead.

    Raises UnauthenticatedError if the reply has a status code of 401.

    Raises JSONAPIError if the request fails for any reason or if the
    reply does not have a status code in the range from 200 to 299 or
    401.

    Required arguments:

    resource -- The URL of the resource to issue the request to.

    json_data -- The data to JSON-encode and include in the request
        body.

    Keyword arguments:

    raw_response -- If True, return a requests.Response object.

    All other keyword arguments are passed on to requests.post().

    """
    headers = kwargs.get("headers", {})
    headers["Content-Type"] = "application/json"
    kwargs["headers"] = headers
    raw = _raw_response(kwargs)
    try:
        r = requests.post(resource, json=json_data, **kwargs)
    except (requests.exceptions.RequestException, socket.error) as e:
        raise JSONAPIError("requests.post exception.", e) from e
    _check_status(resource, r, "POST", json_data, kwargs)
    return r if raw else _json(r)


def delete(resource: str, **kwargs) -> JSONValue | requests.Response:
    """Issue an HTTP DELETE request and return the parsed JSON reply
    or None if there is no response body or the response body is empty
    (note that this is indistinguishable from a body containing the
    string "null", which also returns None).  If keyword argument
    `raw_response` is True, a requests.Response object is returned
    instead.

    Raises UnauthenticatedError if the reply has a status code of 401.

    Raises JSONAPIError if the request fails for any reason or if the
    reply does not have a status code in the range from 200 to 299 or
    401.

    Required arguments:

    resource -- The URL of the resource to issue the request to.

    Keyword arguments:

    raw_response -- If True, return a requests.Response object.

    All other keyword arguments are passed on to requests.delete().

    """
    raw = _raw_response(kwargs)
    try:
        r = requests.delete(resource, **kwargs)
    except (requests.exceptions.RequestException, socket.error) as e:
        raise JSONAPIError("requests.delete exception.", e) from e
    _check_status(resource, r, "DELETE", kwargs=kwargs)
    return r if raw else _json(r)
