#
# Copyright (c) 2024-2025 eGauge Systems LLC
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
"""Module for monitoring the progress of slow operations (SLOPs).

Once a slow operation is started through WebAPI, it returns a token
which can be polled periodically to watch the progress of the
operation and detect when it has completed.

This module supports that paradigm through the `SLOPStatus.stream()`
class method which returns an iterator generating the sequence of
`SLOPStatus` objects describing the progress of the SLOP.

"""

import decimal
from enum import Enum
from typing import Any

from .device import Device


class Error(Exception):
    """Raised for errors detected by this module."""


class SLOPInfo(Enum):
    """Tags for the SLOPStatus.info property."""

    #
    # See egauge/priv-db-common.h:
    #
    DB_ADJUST = "ADJUST"
    DB_RESTORE = "RESTORE"
    DB_SKIP = "SKIP"
    DB_SPLIT = "SPLIT"
    DB_ZERO = "ZERO"
    #
    # See egauge/priv-update-common.h:
    #
    UPD_CHKSIG = "CHKSIG"
    UPD_DOWNLOAD_FW = "FW_DOWNLOAD"
    UPD_DOWNLOAD_KERNEL = "KERNEL_DOWNLOAD"
    UPD_DOWNLOAD_SKIN = "SKIN_DOWNLOAD"
    UPD_EXTRACT = "EXTRACT"
    UPD_FINALIZE = "FINALIZE"
    UPD_FLASH = "FLASH"
    UPD_INSTALL = "INSTALL"
    UPD_VALIDATE = "VALIDATE"


class SLOPError(Enum):
    """Tags for the SLOPStatus.error property."""

    #
    # See egauge/slop.h:
    #
    OOM = "OOM"
    CANCELED = "CANCELED"
    #
    # See egauge/priv-activate-common.h for details.
    #
    ACT_ALRT = "ALRT"
    ACT_PUSH = "PUSH"
    ACT_SRV = "SRV"
    #
    # See egauge/priv-db-common.h:
    #
    DB_BADHDR = "BADHDR"
    DB_BADREG = "BADREG"
    DB_BADTS = "BADTS"
    DB_FILE_INVAL = "FILE_INVAL"
    DB_FILE_READ_ERR = "FILE_READ_ERR"
    DB_INVAL_INT = "INVAL_INT"
    DB_IN_FUTURE = "IN_FUTURE"
    DB_LOCK_FAILED = "LOCK_FAILED"
    DB_MISSING_COMMA = "NOCOMMA"
    DB_MISSING_VERSION = "NOVERS"
    DB_NOT_A_NET_REG = "NOT_NET_REG"
    DB_NO_FIRST_ROW = "NO_FIRST_ROW"
    DB_NO_POS_REG = "NO_POS_REG"
    DB_NO_SECOND_ROW = "NO_SECOND_ROW"
    DB_READ_FAILED = "DB_READ_ERR"
    DB_WRITE_FAILED = "WRITE_FAILED"
    #
    # See egauge/test-email.c:
    #
    MAIL_TX_ERR = "MAIL_TX_ERR"
    #
    # See egauge/priv-update-common.h:
    #
    UPD_BADSIG = "BADSIG"
    UPD_DOWNLOAD_FAILED = "DOWNLOAD_FAILED"
    UPD_EXTRACT_FAILED = "EXTRACT_FAILED"
    UPD_FLASH_FAILED = "FLASH_FAILED"
    UPD_INCOMPATIBLE = "INCOMPATBILE"
    UPD_INSTALL_FAILED = "INSTALL_FAILED"
    UPD_INVALID_IMAGE = "INVALID_IMAGE"
    UPD_NO_IMAGE = "NO_IMAGE"
    UPD_NOT_NEWER = "NOT_NEWER"
    UPD_NOT_SUPPORTED = "NOT_SUPPORTED"


_ERR_MSG_TEMPLATE = {
    SLOPError.OOM.value: "Out of memory.",
    SLOPError.CANCELED.value: "Canceled.",
    SLOPError.ACT_SRV.value: "Server error.value: {0}",
    SLOPError.ACT_ALRT.value: "Alert activation.value: {0}",
    SLOPError.ACT_PUSH.value: "Push activation.value: {0}",
    SLOPError.DB_BADHDR.value: "Bad backup file header.value: `{0}'",
    SLOPError.DB_BADREG.value: "Invalid register name `{0}'",
    SLOPError.DB_BADTS.value: "Invalid timestamp `{0}'",
    SLOPError.DB_FILE_INVAL.value: "Backup file is invalid.",
    SLOPError.DB_FILE_READ_ERR.value: (
        "Read of backup file failed after {0} lines"
    ),
    SLOPError.DB_INVAL_INT.value: "Invalid value in backup file at line {0}",
    SLOPError.DB_IN_FUTURE.value: "Backup is in the future ({0}>{1})",
    SLOPError.DB_LOCK_FAILED.value: "Failed to acquire lock",
    SLOPError.DB_MISSING_COMMA.value: "Comma missing in backup file line {0}",
    SLOPError.DB_MISSING_VERSION.value: "Version missing from backup file",
    SLOPError.DB_NOT_A_NET_REG.value: "Register `{0}' is not a net register",
    SLOPError.DB_NO_FIRST_ROW.value: "Backup file has no data rows",
    SLOPError.DB_NO_POS_REG.value: (
        "Register `{0}' has no matching positive-only register"
    ),
    SLOPError.DB_NO_SECOND_ROW.value: "Backup file has no second data row",
    SLOPError.DB_READ_FAILED.value: "Failed to read db at {0}",
    SLOPError.DB_WRITE_FAILED.value: "Failed to write db at {0}",
    SLOPError.MAIL_TX_ERR.value: 'Failed to send email to "{0}"',
    SLOPError.UPD_BADSIG.value: "Invalid signature",
    SLOPError.UPD_DOWNLOAD_FAILED.value: "Download of {0} failed.value: {1}",
    SLOPError.UPD_EXTRACT_FAILED.value: "Extraction of {0} failed.value: {1}",
    SLOPError.UPD_FLASH_FAILED.value: "Flashing of parting {0} failed",
    SLOPError.UPD_INCOMPATIBLE.value: (
        'Image for "{0}" devices is not compatible with this "{1}" device.'
    ),
    SLOPError.UPD_INSTALL_FAILED.value: "Installation failed.value: {0}",
    SLOPError.UPD_INVALID_IMAGE.value: "Invalid image file",
    SLOPError.UPD_NO_IMAGE.value: "File {0} does not exist",
    SLOPError.UPD_NOT_NEWER.value: (
        "Available version {0} is not newer than existing version {1}"
    ),
    SLOPError.UPD_NOT_SUPPORTED.value: "Operation not supported",
}

_INFO_MSG_TEMPLATE = {
    SLOPInfo.DB_ADJUST.value: "Adjusting",
    SLOPInfo.DB_RESTORE.value: "Restoring",
    SLOPInfo.DB_SKIP.value: "Skipping",
    SLOPInfo.DB_SPLIT.value: "Splitting",
    SLOPInfo.DB_ZERO.value: "Zeroing",
    SLOPInfo.UPD_CHKSIG.value: "Checking signature of {0}",
    SLOPInfo.UPD_DOWNLOAD_FW.value: "Downloading firmware {0}",
    SLOPInfo.UPD_DOWNLOAD_KERNEL.value: "Downloading kernel {0}",
    SLOPInfo.UPD_DOWNLOAD_SKIN.value: "Downloading skin {0}",
    SLOPInfo.UPD_EXTRACT.value: "Extracting {0} files",
    SLOPInfo.UPD_FINALIZE.value: "Finishing up",
    SLOPInfo.UPD_FLASH.value: "Flashing partition {0}",
    SLOPInfo.UPD_INSTALL.value: "Installing version {0}",
    SLOPInfo.UPD_VALIDATE.value: "Validating bundle",
}


class SLOPStatusStream:
    def __init__(
        self, status_class: type["SLOPStatus"], dev: Device, token: str
    ):
        """Create a SLOPStatusStream object.

        Required arguments:

        status_class -- The SLOPStatus class to use to convert a
          /sys/status/TOKEN result to a SLOPStatus object.

        dev -- The WebAPI device to fetch the latest SLOP status from.

        token -- The token of the SLOP to monitor.

        """
        self.status_class = status_class
        self.dev = dev
        self.token = token

    def __iter__(self):
        return self

    def __next__(self) -> "SLOPStatus":
        if self.token is None:
            raise StopIteration

        result = self.dev.get(f"/sys/status/{self.token}").get("result", {})
        if not isinstance(result, dict):
            raise Error("unexpected status", result)

        status = self.status_class(result)
        if status.done:
            self.token = None
        return status


class SLOPStatus:
    """The current status of a slow-operation (SLOP)."""

    @classmethod
    def stream(cls, dev: Device, token: str):
        """Return an iterator to monitor the status of a SLOP.

        Required arguments:

        dev -- The WebAPI device to fetch the latest SLOP status from.

        token -- The token of the SLOP to monitor.

        """
        return SLOPStatusStream(cls, dev, token)

    def __init__(self, status: dict[str, Any]):
        """Create a SLOPStatus object from a /sys/status/TOKEN
        response.

        Required arguments:

        status -- The SLOP status response received from WebAPI.

        """
        self._status = status

    @property
    def done(self) -> bool:
        """True if the SLOP has finished execution, False otherwise."""
        val = self._status.get("done", False)
        if not isinstance(val, bool):
            raise Error('invalid "done" value', val)
        return val

    @property
    def error(self) -> str | None:
        """The error tag, if an error occured, `None` otherwise."""
        val = self._status.get("error", None)
        if val is None:
            return None
        if not isinstance(val, str):
            raise Error('invalid "error" value', val)
        return val

    @property
    def info(self) -> str | None:
        """The info tag, if available, `None` otherwise."""
        val = self._status.get("info", None)
        if val is None:
            return None
        if not isinstance(val, str):
            raise Error('invalid "info" value', val)
        return val

    @property
    def args(self) -> list:
        """The argument list for the current info or error message, if
        any, or an empty list otherwise.

        """
        return self._status.get("args", [])

    @property
    def progress(self) -> float | None:
        """The progress fraction, if available, `None` otherwise."""
        val = self._status.get("progress", None)
        if val is None:
            return None
        if not isinstance(val, float):
            raise Error('invalid "progress" value', val)
        return val

    @property
    def result(self) -> Any:
        """The result of the SLOP, if available, `None` otherwise."""
        return self._status.get("result")

    @property
    def ts(self) -> decimal.Decimal | None:
        """The timestamp of when the SLOP status was last updated, if
        available, `None` otherwise."""
        return self._status.get("ts")

    def error_message(self) -> str:
        """The human-readable error message derived from the error tag.

        Returns a human-readable error message or "No error." if the
        `error` property is `None`.

        """
        if self.error is None:
            return "No error."

        template = _ERR_MSG_TEMPLATE.get(self.error)
        if template is None:
            return f"Unknown error {self.error}"

        return template.format(*self._status.get("args", []))

    def info_message(self) -> str:
        """The human-readable info message derived from the info tag.

        Returns a human-readable info message or "No info." if the
        `info` property is `None`.

        """
        if self.info is None:
            return "No info."

        template = _INFO_MSG_TEMPLATE.get(self.info)
        if template is None:
            return f"Unknown info {self.info}."

        return template.format(*self._status.get("args", []))
