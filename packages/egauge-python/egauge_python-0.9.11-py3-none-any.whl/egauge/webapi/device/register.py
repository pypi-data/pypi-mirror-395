#
# Copyright (c) 2020, 2022, 2024 eGauge Systems LLC
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
"""This module provides access to the eGauge WebAPI's /api/register
service."""

import decimal
import json

from deprecated import deprecated

from ..error import Error
from ..json_api import JSONAPIError
from .device import Device
from .physical_quantity import PhysicalQuantity
from .register_row import RegisterRow
from .virtual_register import VirtualRegister


class RegisterError(Error):
    """Raised if for any register related errors."""


def regnames_to_ranges(dev, regs):
    """Convert a list of register names to a register-ranges string."""
    indices = set()
    for name in regs:
        formula = dev.reg_formula(name)
        if formula is None:
            indices.add(dev.reg_idx(name))
        else:
            for phys_reg in formula.phys_regs:
                indices.add(dev.reg_idx(phys_reg))
    indices = sorted(list(indices))

    ranges = []
    idx = 0
    while idx < len(indices):
        start = stop = indices[idx]
        idx += 1
        while idx < len(indices) and indices[idx] == stop + 1:
            stop = indices[idx]
            idx += 1
        if start == stop:
            ranges.append(str(start))
        else:
            ranges.append(str(start) + ":" + str(stop))
    if len(ranges) < 1:
        return None
    return "+".join(ranges)


class Register:
    def __init__(
        self,
        dev: Device,
        params: dict | None = None,
        regs: list[str] | None = None,
        **kwargs,
    ):
        """Fetch register data from a meter.

        Required arguments:

        dev -- The device object to use to access the meter.

        Keywoard arguments:

        params -- A dictionary of query parameters that specify the
            data to return (default `None`).

        regs -- The list of registers to return (default `None`).  If
            `None`, all registers are returned.  Otherwise,
            data is returned only for the named registers.

        Additional keyword arguments are passed along to the
            requests.get() method.

        """
        self.dev = dev
        # maps regname to index in "register"/"row" arrays:
        self.regorder = None
        self.iter_range_idx = 0
        self.iter_row_idx = 0
        self.iter_ts = decimal.Decimal(0)
        if params is None:
            params = {}
        self._requested_regs = regs
        if regs is not None:
            reg_ranges = regnames_to_ranges(dev, regs)
            if reg_ranges is not None:
                params["reg"] = reg_ranges
        try:
            self.raw = self.dev.get("/register", params=params, **kwargs)
        except JSONAPIError as e:
            raise RegisterError("failed to read registers: {e}", params) from e

    def _create_regorder(self) -> dict[str, int]:
        """Create a dictionary mapping a register name to the index
        within the `registers' and `row' arrays which contain the info
        for that particular name.

        """
        regorder = {}
        for index, reg in enumerate(self.raw["registers"]):
            regorder[reg["name"]] = index
        return regorder

    def ts(self) -> decimal.Decimal | None:
        """Return the timestamp of the register rates.

        The returned value is seconds since the Unix epoch.

        """
        if self.raw is None:
            return None
        return decimal.Decimal(self.raw["ts"])

    @property
    def regs(self) -> list[str]:
        """Return the list of available register names."""
        if self._requested_regs:
            return self._requested_regs

        if self.regorder is None:
            self.regorder = self._create_regorder()

        return list(self.regorder.keys()) + self.dev.reg_virtuals()

    def have(self, reg):
        """Check if a register is available (known).

        Returns True if the register is known, False otherwise.


        Required arguments:

        reg -- The name of the register to check for.

        """
        return reg in self.regs

    def _rate(self, reg: str) -> float | None:
        if self.raw is None:
            return None

        row = self.raw["registers"]
        formula = self.dev.reg_formula(reg)
        if isinstance(formula, VirtualRegister):
            return formula.calc(lambda reg: self._row_rate(row, reg))
        return self._row_rate(row, reg)

    def _row_rate(self, row: list[dict], reg: str) -> float:
        if self.regorder is None:
            self.regorder = self._create_regorder()

        idx = self.regorder[reg]
        return row[idx]["rate"]

    @deprecated(version="0.7.0", reason="use pq_rate() instead")
    def rate(self, reg: str) -> float | None:
        return self._rate(reg)

    def pq_rate(self, reg: str) -> PhysicalQuantity | None:
        """Return the rate of change value of a register.

        Returns `None` if the rate is unknown.

        Required arguments:

        reg -- The name of the register whose rate value to return.

        """
        rate = self._rate(reg)
        if rate is None:
            return None
        return PhysicalQuantity(
            rate, self.type_code(reg), is_cumul=False
        ).to_preferred()

    def type_code(self, reg) -> str:
        """Return the type-code of a register.

        Required arguments:

        reg -- The name of the register whose type-code to return.

        """
        return self.dev.reg_type(reg)

    @deprecated(version="0.7.0", reason="use Device.reg_formula() instead")
    def formula(self, reg: str) -> str | None:
        if self.raw is None:
            return None
        if self.regorder is None:
            self.regorder = self._create_regorder()
        return self.raw["registers"][self.regorder[reg]]["formula"]

    def index(self, reg: str) -> int | None:
        """Return the register index of a register.

        Required arguments:

        reg -- The name of the register whose index to return.

        """
        if self.raw is None:
            return None
        if self.regorder is None:
            self.regorder = self._create_regorder()
        return self.raw["registers"][self.regorder[reg]]["idx"]

    def database_id(self, reg: str) -> int | None:
        """Return the database-id of a register.

        Returns `None` if the register is unknown.

        Required arguments:

        reg -- The name of the register whose database id to return.

        """
        if self.raw is None:
            return None
        if self.regorder is None:
            self.regorder = self._create_regorder()
        return self.raw["registers"][self.regorder[reg]]["did"]

    def _make_row(
        self, ts: decimal.Decimal, cumul_list: list[str]
    ) -> RegisterRow:
        """Convert a "rows" array to a RegisterRow()."""
        row = RegisterRow(ts)

        # first, fill in the physical registers:
        phys = {}
        for idx, cumul in enumerate(cumul_list):
            ri = self.raw["registers"][idx]
            reg = ri["name"]
            cumul = int(cumul)
            phys[reg] = cumul
            if self._requested_regs and reg not in self._requested_regs:
                continue
            row.regs[reg] = cumul
            row.type_codes[reg] = self.type_code(reg)

        # second, fill in virtual registers (if any):
        for reg in self.dev.reg_virtuals():
            if self._requested_regs and reg not in self._requested_regs:
                continue
            formula = self.dev.reg_formula(reg)
            if not isinstance(formula, VirtualRegister):
                raise RegisterError(
                    f"Formula for virtual register {reg} is missing."
                )
            row.regs[reg] = formula.calc(lambda reg: phys[reg])
            row.type_codes[reg] = self.type_code(reg)
        return row

    def __getitem__(self, index: int) -> RegisterRow:
        """Return the n-th row of cumulative register values as a
        RegisterRow.

        """
        range_idx = 0
        while True:
            curr_range = self.raw["ranges"][range_idx]
            ts = decimal.Decimal(curr_range["ts"])
            if index < len(curr_range["rows"]):
                ts -= index * decimal.Decimal(str(curr_range["delta"]))
                return self._make_row(ts, curr_range["rows"][index])
            range_idx += 1
            index -= len(curr_range["rows"])

    def __iter__(self):
        """Iterate over cumulative register values.

        Each iteration returns one row of data as a RegisterRow.

        """
        if self.raw is None:
            return None
        self.iter_range_idx = 0
        self.iter_row_idx = 0
        return self

    def __next__(self) -> RegisterRow:
        if (
            not isinstance(self.raw, dict)
            or "ranges" not in self.raw
            or self.iter_range_idx >= len(self.raw["ranges"])
        ):
            raise StopIteration
        curr_range = self.raw["ranges"][self.iter_range_idx]

        if self.iter_row_idx == 0:
            self.iter_ts = decimal.Decimal(curr_range["ts"])

        row = self._make_row(
            self.iter_ts, curr_range["rows"][self.iter_row_idx]
        )

        self.iter_ts -= decimal.Decimal(str(curr_range["delta"]))
        self.iter_row_idx += 1
        if self.iter_row_idx >= len(curr_range["rows"]):
            self.iter_row_idx = 0
            self.iter_range_idx += 1
        return row

    def __str__(self) -> str:
        """Returns the raw register data as a JSON-encoded string."""
        return json.dumps(self.raw)
