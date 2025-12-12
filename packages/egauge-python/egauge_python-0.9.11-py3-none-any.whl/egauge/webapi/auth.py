#
# Copyright (c) 2020-2022, 2024-2025 eGauge Systems LLC
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
"""This module provides support additional requests auth services, in
particular for JWT-token based authentication (JWTAuth) and for plain
token-based authentication (TokenAuth).

"""

import hashlib
import os
import secrets
import types
from functools import wraps
from pathlib import Path
from urllib.parse import urlparse

import requests
from requests.auth import AuthBase

from egauge.loggers import ModuleLogger

from . import json_api

# The name of the optional environment variable storing a token:
ENV_EGAUGE_API_TOKEN = "EGAUGE_API_TOKEN"

MAX_RETRIES = 10

log = ModuleLogger.get(__name__)


def _decorate_public_metaclass(decorator):
    """Return a metaclass which will decorate all public methods of a
    class with the DECORATOR function.

    """

    class MetaClass(type):
        def __new__(mcs, class_name, bases, class_dict, **kwargs):
            if bases:
                decorated_class = bases[0]
                for attr_name, attr in decorated_class.__dict__.items():
                    if isinstance(attr, types.FunctionType):
                        if attr_name[0] == "_":
                            continue
                        attr = decorator(attr)
                    class_dict[attr_name] = attr
            return type.__new__(mcs, class_name, bases, class_dict, **kwargs)

    return MetaClass


def decorate_public(cls, decorator):
    """Return a subclass of CLS in which all public methods of CLS are
    decorated with function DECORATOR.  Methods whose name start with
    an underscore ('_') are considered private, all other methods are
    considered public.

    """

    # pylint: disable=unused-variable
    def wrapper(method):
        @wraps(method)
        def wrapped(*args, **kwargs):
            return decorator(method, *args, *kwargs)

        return wrapped

    class DecoratedClass(cls, metaclass=_decorate_public_metaclass(wrapper)):
        # pylint: disable=too-few-public-methods
        pass

    return DecoratedClass


class JWTAuth(AuthBase):
    """Implements the eGauge device WebAPI's JWT-based authentication
    scheme.  Digest login is used so the password is never sent over
    the HTTP connection.

    """

    def __init__(self, username: str, password: str):
        self.bearer_token: str | None = None
        self.username = username
        self.password = password

    def __call__(self, r):
        if self.bearer_token:
            self.add_auth_header(r)
        r.register_hook("response", self.handle_response)
        return r

    def __eq__(self, other):
        return self.username == getattr(
            other, "username", None
        ) and self.password == getattr(other, "password", None)

    def add_auth_header(
        self, req: requests.Request | requests.PreparedRequest
    ):
        """If we have a bearer-token, add an HTTP Authorization header
        to a request.

        Required arguments:

        req -- The request to which to add an Authorization header.

        """
        if self.bearer_token:
            req.headers["Authorization"] = "Bearer " + self.bearer_token

    def handle_401(self, r, **kwargs):
        """Called when server responds with 401 Unauthorized."""
        log.debug("handle_401: auth request received for %s", r.request.url)

        try:
            auth_request = r.json()
        except ValueError:
            log.debug("handle_401: auth request is not valid JSON")
            return r

        realm = auth_request["rlm"]
        server_nonce = auth_request["nnc"]

        client_nonce = f"{secrets.randbits(64):x}"

        content = self.username + ":" + realm + ":" + self.password
        ha1 = hashlib.md5(content.encode("utf-8")).hexdigest()

        content = ha1 + ":" + server_nonce + ":" + client_nonce
        ha2 = hashlib.md5(content.encode("utf-8")).hexdigest()

        data = {
            "rlm": realm,
            "usr": self.username,
            "nnc": server_nonce,
            "cnnc": client_nonce,
            "hash": ha2,
        }

        url = urlparse(r.request.url)
        login_uri = url.scheme + "://" + url.netloc + "/api/auth/login"
        verify = kwargs.get("verify", True)
        auth_r = json_api.post(
            login_uri, data, timeout=60, verify=verify, raw_response=True
        )

        # to keep pyright happy (shouldn't be possible):
        if not isinstance(auth_r, requests.Response):
            log.debug("handle_401: login attempt failed")
            return r

        if auth_r.status_code != 200:
            log.debug(
                "handle_401: login response status %d", auth_r.status_code
            )
            return auth_r

        try:
            auth_reply = auth_r.json()
        except requests.JSONDecodeError:
            log.debug("handle_401: login response is invalid")
            return auth_r

        if not isinstance(auth_reply, dict):
            log.debug("handle_401: login reply is not a dict")
            return r

        err = auth_reply.get("error")
        if err:
            if err != "Nonce expired.":
                log.debug("handle_401: login reply error: %s", err)
                return auth_r
            log.debug("handle_401: server nonce expired - retrying")
            # if the server nonce expired, retry the original request
            # without a token so we get a fresh auth required response:
            token = None
        else:
            token = auth_reply.get("jwt")
            if not isinstance(token, str):
                log.debug(
                    "handle_401: token in auth reply is not a string: %s",
                    token,
                )
                return r

        self.bearer_token = token

        prep = r.request.copy()
        self.add_auth_header(prep)
        _r = r.connection.send(prep, **kwargs)
        _r.history.append(r)
        _r.request = prep
        return _r

    def handle_response(self, r, **kwargs):
        """Called when a server response is received."""
        if r.status_code == 401:
            for i in range(MAX_RETRIES):
                r = self.handle_401(r, **kwargs)
                if r.status_code != 401:
                    break
                log.debug("handle_response: auth attempt %d failed", i + 1)
        log.debug("handle_response: returning status %d", r.status_code)
        return r


class TokenAuth(AuthBase):
    """Implements the eGauge web services' token-based authentication
    scheme.  This sends the password to the server, so it must not be
    used unless the underlying transport is encrypted!

    """

    def __init__(
        self,
        username=None,
        password=None,
        ask=None,
        token_service_url="https://api.egauge.net/v1/api-token-auth/",
    ):
        self.username = username
        self.password = password
        self.ask_credentials = ask
        self.token_file = None
        self.token_service_url = token_service_url
        self.token = os.environ.get(ENV_EGAUGE_API_TOKEN)
        if self.token is None:
            self.token_file = Path.home() / ".cache" / "egauge" / "api_token"
            self.token = None
            try:
                with open(self.token_file, "r", encoding="utf-8") as f:
                    self.token = f.read().rstrip()
            except IOError:
                pass

            # try old token file:
            if self.token is None:
                old_token_file = Path.home() / ".egauge_api_token"
                try:
                    with open(old_token_file, "r", encoding="utf-8") as f:
                        self.token = f.read().rstrip()
                    old_token_file.unlink(missing_ok=True)
                    self._save_token()
                except IOError:
                    pass

            if not isinstance(self.token, str) or len(self.token) < 32:
                self.token = None

    def __call__(self, r):
        self.add_auth_header(r)
        r.register_hook("response", self.handle_response)
        return r

    def __eq__(self, other):
        return self.username == getattr(
            other, "username", None
        ) and self.password == getattr(other, "password", None)

    def add_auth_header(
        self, req: requests.Request | requests.PreparedRequest
    ):
        """If we have a token, add an HTTP Authorization header to a
        request.

        Required arguments:

        req -- The request to which to add an Authorization header.

        """
        if self.token:
            req.headers["Authorization"] = "Token " + self.token

    def handle_401(self, r, **kwargs):
        """Called when server responds with 401 Unauthorized."""
        usr = self.username
        pwd = self.password

        if usr is None or pwd is None:
            if self.ask_credentials is None:
                return r

            credentials = self.ask_credentials()
            if credentials is None:
                return r
            [usr, pwd] = credentials

        creds = {"username": usr, "password": pwd}
        verify = kwargs.get("verify", True)
        auth_reply = requests.post(
            self.token_service_url, json=creds, timeout=60, verify=verify
        ).json()

        if not isinstance(auth_reply, dict):
            return r

        token = auth_reply.get("token")
        if not isinstance(token, str) or not token:
            return r

        self.token = auth_reply["token"]

        if self.token_file is None:
            # the original token came for the os.environ
            os.environ[ENV_EGAUGE_API_TOKEN] = self.token
        else:
            self._save_token()

        prep = r.request.copy()
        self.add_auth_header(prep)
        _r = r.connection.send(prep, **kwargs)
        _r.history.append(r)
        _r.request = prep
        return _r

    def handle_response(self, r, **kwargs):
        """Called when a server response is received."""
        if r.status_code == 401:
            for _ in range(MAX_RETRIES):
                r = self.handle_401(r, **kwargs)
                if r.status_code != 401:
                    break
        return r

    def _save_token(self):
        if self.token_file is None or self.token is None:
            return

        self.token_file.parent.mkdir(parents=True, exist_ok=True)
        try:
            fd = os.open(self.token_file, os.O_CREAT | os.O_WRONLY, 0o600)
            os.write(fd, (self.token + "\n").encode("utf-8"))
            os.close(fd)
        except IOError:
            pass
