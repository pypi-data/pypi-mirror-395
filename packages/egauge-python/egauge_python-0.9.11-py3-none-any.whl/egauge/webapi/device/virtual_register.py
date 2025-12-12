#
# Copyright (c) 2022-2024 eGauge Systems LLC
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
import re
from dataclasses import dataclass
from enum import Enum, auto
from types import SimpleNamespace
from typing import Any, Callable, Generic, NoReturn, TypeVar

from ..error import Error

ID_PATTERN = re.compile(r"[A-Z]+")
NUMBER_PATTERN = re.compile(r"(\d+)")

# When evaluating a virtual register formula, the register values are
# looked up by id, which could be the register name and integer index
# or really anything else that's convenient for the user.  The
# translation from register name to register id is accomplished by the
# `compile_reg` function argument below.
RegId = TypeVar("RegId")


class VirtRegError(Error):
    """Exception raised due to any errors in this module."""


class Operator(Enum):
    REG = auto()  # value of a register
    MIN = auto()  # deprecated MIN(reg,c)
    MAX = auto()  # deprecated MAX(reg,c)


@dataclass
class Addend(Generic[RegId]):
    op: Operator
    reg: RegId
    const = 0
    negate: bool = False  # true if addend should be subtracted

    def __str__(self):
        reg = f"reg[{self.reg}]"
        if self.op == Operator.REG:
            val = reg
        elif self.op == Operator.MIN:
            val = f"MIN({reg},{self.const})"
        elif self.op == Operator.MAX:
            val = f"MAX({reg},{self.const})"
        else:
            raise VirtRegError(f'Operator "{self.op}" is unknown.')
        return ("-" if self.negate else "+") + val


def _default_compile_reg(reg: str) -> str:
    """By default, use the register name as the register id."""
    return reg


class VirtualRegister(Generic[RegId]):
    """Objects of this class are a parsed version of the virtual register
    formula.  Since these formulas need to work both for rates and
    cumulative values, only addition and subtraction are supported.
    For historical reasons, we continue to support the MIN/MAX
    operators, even though they don't work properly for cumulate
    value.  The should not be used on new meters."""

    def __init__(
        self,
        formula: str,
        compile_reg: Callable[[str], RegId] = _default_compile_reg,
    ):
        """Compile a formula to a virtual register calculator.

        Required arguments:

        formula -- The virtual register formula to compile.

        compile_reg -- An optional callback that can be used to
            translate a register name to a register id (default
            `None`).  If `None`, the register name is used as the
            register id.

        """
        self._phys_regs = []
        self._addends = self._compile(formula, compile_reg)

    def __str__(self):
        """Returns a human-readable representation of the virtual
        register's formula."""
        return " ".join([str(a) for a in self._addends])

    def calc(self, get: Callable[[RegId], Any]) -> Any:
        """Calculate the value of a virtual register and return it.

        The returned value has the same type as is returned by the
        `get` function.  It may be `float` or `int`.  The distinction
        matters here because not all 64-bit integers can be
        represented accurately as a double-precision IEEE754
        floating-point number and vice versa.  If you are considering
        replacing `Any` with a generic type instead, read this
        cautionary tale first: https://tinyurl.com/5bp2yrb2 It would
        be nice if we could just use `numbers.Real` instead of `Any`,
        but that has all kinds of issues, too.

        Required arguments:

        get -- A callback that must return the value of the physical
            register id passed as its first and only argument.

        """
        total = 0
        for a in self._addends:
            val = get(a.reg)
            if a.op == Operator.REG:
                pass
            elif a.op == Operator.MIN:
                if a.const < val:
                    val = a.const
            elif a.op == Operator.MAX:
                if a.const > val:
                    val = a.const
            if a.negate:
                val = -val
            total += val
        return total

    @property
    def phys_regs(self) -> list[str]:
        """Get the list of physical registers the virtual register
        depends on.

        """
        return self._phys_regs

    def _compile(
        self,
        formula: str,
        compile_reg: Callable[[str], RegId] = _default_compile_reg,
    ) -> list[Addend[RegId]]:
        """Compile a virtual register formula to the equivalent list
        of addends.

        Virtual register are limited to sums/differences of physical
        register values.

        For backwards-compatibility, an addend may also consist of a
        MAX() or MIN() function call.  Those functions never worked
        correctly for calculating cumulative values, so they're
        deprecated.  Unfortunately, old devices may still use them.

        EBNF for a register formula:

          formula = ['+'|'-'] addend { ('+'|'-') addend}* .
          addend = regname | func .
          regname = QUOTED_STRING .
          formula = ('MIN'|'MAX') '(' regname ',' number ')' .
          number = [0-9]+ .

        Required arguments:

        formula -- The virtual register formula to translate.

        compile_reg -- An optional callback that can be used to
            translate a register name to a register id (default
            `None`).  If `None`, the register name is used as the
            register id.

        """

        def error(reason: str) -> NoReturn:
            raise VirtRegError(f"{reason} (rest: '{formula[state.idx :]}')")

        def whitespace():
            while state.idx < len(formula) and formula[state.idx] in [
                " ",
                "\t",
            ]:
                state.idx += 1

        def peek() -> str:
            if state.idx >= len(formula):
                return ""
            return formula[state.idx]

        def getch() -> str:
            if state.idx >= len(formula):
                return ""
            state.idx += 1
            return formula[state.idx - 1]

        def match(what: str) -> bool:
            whitespace()
            if peek() == what:
                state.idx += 1
                return True
            return False

        def regname() -> Addend[RegId]:
            if not match('"'):
                return error('Expected opening quote (")')
            name = ""
            while True:
                ch = getch()
                if ch == "\\":
                    ch = getch()
                elif not ch or ch == '"':
                    break
                name += ch
            if not name:
                return error("Register name must not be empty")

            if ch != '"':  # dont use match: no whitespace allowed
                return error('Expected closing quote (")')
            state.phys_regs[name] = True
            return Addend(op=Operator.REG, reg=compile_reg(name))

        def number() -> int:
            whitespace()
            m = NUMBER_PATTERN.match(formula[state.idx :])
            if not m:
                return error("Expected number")
            t = m.group()
            state.idx += len(t)
            return int(t)

        def func() -> Addend[RegId]:
            """Parse:

            (MIN|MAX) '(' regname ',' number ')'

            """
            m = ID_PATTERN.match(formula[state.idx :])
            if not isinstance(m, re.Match):
                error("Expected function id")

            name = m.group()
            if name == "MAX":
                op = Operator.MAX
            elif name == "MIN":
                op = Operator.MIN
            else:
                error("Expected MIN or MAX")
            state.idx += len(name)

            if not match("("):
                error('Expected "("')

            a = regname()

            if not match(","):
                error('Expected ","')

            a.const = number()

            if not match(")"):
                error('Expected ")"')

            a.op = op
            return a

        def addend():
            whitespace()
            if state.idx >= len(formula):
                return

            negate = False
            if match("-"):
                negate = True
            elif match("+"):
                pass
            elif state.addends:
                error('Expected "+" or "-"')

            whitespace()

            if peek() == '"':
                a = regname()
            else:
                a = func()
            a.negate = negate
            state.addends.append(a)

        # with the above local functions, the rest is easy:

        state = SimpleNamespace(idx=0, addends=[], phys_regs={})
        while state.idx < len(formula):
            addend()
        self._phys_regs = list(state.phys_regs.keys())
        return state.addends


def test():
    regmap = {"Grid": 0, "Solar": 1}

    for formula in [
        "",
        '"Solar"+"Solar"',
        ' - "Grid"	',
        '+"Grid"',
        '"Grid"+MAX("Solar",0)',
    ]:
        try:
            virt = VirtualRegister(formula, lambda reg: regmap[reg])
        except VirtRegError as e:
            print("Error: Compile failed for formula:", formula)
            print("\t", e)
            continue
        print(
            "formula:",
            formula,
            ">>> compiled: ",
            virt,
            "phys_regs",
            virt.phys_regs,
        )

    virt = VirtualRegister("")
    if virt.calc(lambda reg: 1 / 0) != 0:
        raise VirtRegError("Expected 0")

    virt = VirtualRegister('"Grid"+MAX("Solar",0)')
    if virt.calc(lambda reg: {"Grid": 10, "Solar": 20}[reg]) != 30:
        raise VirtRegError("Expected 30")
    if virt.calc(lambda reg: {"Grid": 10, "Solar": -20}[reg]) != 10:
        raise VirtRegError("Expected 10")
    if virt.calc(lambda reg: {"Grid": -10, "Solar": -20}[reg]) != -10:
        raise VirtRegError("Expected 10")
    print("Success!")
