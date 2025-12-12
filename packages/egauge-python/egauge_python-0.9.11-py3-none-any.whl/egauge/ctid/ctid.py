# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017, 2019-2025 eGauge Systems LLC
# 	4805 Sterling Dr, Suite 1
# 	Boulder, CO 80301
# 	voice: 720-545-9767
# 	email: davidm@egauge.net
#
#  All rights reserved.
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
import math
import struct

import crcmod
from deprecated import deprecated

from .bit_stuffer import BitStuffer

CTID_VERSION = 5  # latest version of CTid Specification this code supports
START_SYM = 0xFF

SENSOR_TYPE_AC = 0x0  # AC-only sensor
SENSOR_TYPE_DC = 0x1  # DC-capable sensor
SENSOR_TYPE_RC = 0x2  # differential-output sensor ("Rogowski Coil"...)
SENSOR_TYPE_VOLTAGE = 0x3  # DEPRECATED -- use SENSOR_TYPE_LINEAR instead
SENSOR_TYPE_LINEAR = 0x3
SENSOR_TYPE_TEMP_LINEAR = 0x4
SENSOR_TYPE_TEMP_NTC = 0x5
SENSOR_TYPE_PULSE = 0x6

# List of registered manufacturer IDs:
_MFG_ID = {
    0x0000: ["eGauge Systems LLC", "eGauge"],
    0x0001: ["Magnelab, Inc.", "Magnelab"],
    0x0002: ["Continental Control Systems LLC", "CCS"],
    0x0003: ["J&D Electronics", "J&D"],
    0x0004: ["Accuenergy, Inc.", "Accuenergy"],
}

# For backwards-compatibility:
MFG_ID = {}
for key, value in _MFG_ID.items():
    MFG_ID[key] = value[0]

SENSOR_TYPE_NAME = ["AC", "DC", "RC", "linear", "temp", "NTC", "pulse"]

SENSOR_UNITS = (
    ("V", "voltage"),
    ("A", "current"),
    ("Ah", "charge"),
    ("W", "power"),
    ("var", "reactive power"),
    ("VA", "apparent power"),
    ("Hz", "frequency"),
    ("Ω", "resistance"),
    ("°", "angle"),
    ("°C", "temperature"),
    ("%RH", "humidity"),
    ("Pa", "pressure"),
    ("g", "mass"),
    ("m/s", "velocity"),
    ("g/s", "mass flow"),
    ("m^3/s", "volumetric flow"),
    ("%", "percentage"),
    ("ppm", "parts-per-million"),
    ("", "air quality"),
    ("", "number"),
)

crc8_rohc = crcmod.predefined.mkCrcFun("crc-8-rohc")
crc16_modbus = crcmod.predefined.mkCrcFun("modbus")

# Max. mantissa value for float12 format:
F12_MAX_MANTISSA = 0x1FF


class CRCError(Exception):
    """Exception raised in case of a CRC error.  Property `expected`
    holds the expected CRC value, `got` holds the received CRC.

    """

    def __init__(self, expected, got):
        super().__init__()
        self.expected = expected
        self.got = got

    def __str__(self):
        return f"Expected CRC {self.expected:#x} but got {self.got:#x}"


class Error(Exception):
    """This is raised for errors other than CRCErrors."""


def get_mfg_id_for_name(name: str) -> int:
    """Get the manufacturer id for the given name.

    Raises Error if the passed string is not unique or if the passed
    string is neither a recognized name or a valid number.

    Required arguments:

    name -- The name of the manufacturer for which to return the id.
        This may be a prefix of the full name, as long as the prefix
        is unique.  Alternatively, name may also be a decimal integer
        string or a hexdecimal string with prefix 0x.

    """
    match = None
    for key, value in MFG_ID.items():
        if len(value) >= len(name):
            if value.startswith(name):
                if match is None:
                    match = key
                else:
                    raise Error(
                        "Name is ambiguous. Please specify more letters."
                    )
    if match is not None:
        return match

    try:
        return int(name, 0)
    except ValueError as e:
        raise Error("Neither a name nor a valid number.") from e


def get_sensor_type_id(name_or_number: str) -> int:
    """Convert a string to a sensor type id.

    Raises Error if the passed string is neither a recognized sensor
    type name nor a valid number string.

    Required arguments:

    name_or_number -- The string to convert to a sensor type id.  The
        string may be one of the names listed in
        `ctid.SENSOR_TYPE_NAME` (the comparison ignores case) or it
        may be a number representing the integer id of the sensor
        type.  The number string should be in decimal, unless it
        starts with "0x", in which case it must be in hexadecimal.

    """
    lc_name = name_or_number.lower()
    for i, name in enumerate(SENSOR_TYPE_NAME):
        if name.lower() == lc_name:
            return i

    try:
        return int(name_or_number, 0)
    except ValueError as e:
        raise Error("Neither a sensor type name nor a valid number.") from e


def get_sensor_type_name(sensor_type: int) -> str | None:
    if sensor_type < 0 or sensor_type >= len(SENSOR_TYPE_NAME):
        return None
    return SENSOR_TYPE_NAME[sensor_type]


def get_sensor_unit(unit_code: int) -> str:
    if 0 <= unit_code < len(SENSOR_UNITS):
        return SENSOR_UNITS[unit_code][0]
    return "?"


def get_sensor_unit_desc(unit_code: int) -> str:
    if 0 <= unit_code < len(SENSOR_UNITS):
        return SENSOR_UNITS[unit_code][1]
    return "?"


def mfg_name(ident: int) -> str | None:
    """Get the manufacturer name for a given manufacturer id.

    Returns None if the specified id is unknown.

    Required arguments:

    ident -- The id of the manufacturer whose name to return.

    """
    if ident in _MFG_ID:
        return _MFG_ID[ident][0]
    return None


def mfg_short_name(ident: int) -> str | None:
    """Get the short version of a manufacturer's name for a given
    manufacturer id.

    Returns None if the specified id is unknown.

    Required arguments:

    ident -- The id of the manufacturer whose short name to return.

    """
    if ident in _MFG_ID:
        return _MFG_ID[ident][1]
    return None


@deprecated(version="0.0", reason="Use CTid.mfg_name() instead")
def get_mfg_id(ident: int):
    return mfg_name(ident)


def s10(val: int) -> int:
    """Convert 10 bit unsigned integer to a signed 9-bit integer.

    Required arguments:

    val -- The integer to convert.

    """
    if not 0 <= val < 1024:
        raise ValueError
    if val < 512:
        return val
    return val - 1024


def fix(
    val: float,
    num_bits: int,
    is_signed: bool,
    name: str,
    unit: str | None,
    scale: float,
):
    f = round(val / scale)
    limit = 1 << num_bits
    min_val = -(limit / 2) if is_signed else 0
    max_val = +(limit / 2 - 1) if is_signed else limit - 1
    if f < min_val or f > max_val:
        unit_str = (" " + unit) if unit is not None else ""
        prec = -int(math.log10(scale))
        val_str = f"{val:.{prec}f}"
        min_str = f"{min_val * scale:.{prec}f}"
        max_str = f"{max_val * scale:.{prec}f}"
        raise Error(
            f"{name} {val_str}{unit_str} outside of range "
            f"from {min_str} to {max_str}{unit_str}."
        )
    return f


def unfix(val: int, scale: float) -> float:
    return val * scale


def float12(val: float, name: str, unit: str) -> int:
    """Encode a floating point value in the range from 0 to 1e7 to the
    12-bit float format.

    Required arguments:

    val -- The floating point value to convert.

    name -- The name of the CTid parameters being converted.

    unit -- The physical unit of the CTid parameter being converted.
    """
    if val < 0 or val > 1e7:
        raise Error(
            f"{name} {val}{unit} outside of range from 0 to 10,000,000{unit}"
        )
    exp = math.log10(val) if val >= 1.0 else 0
    exp = int(math.ceil(exp))
    mantissa = int(round((val / math.pow(10, exp)) * F12_MAX_MANTISSA))
    return (mantissa << 3) | exp


def unfloat12(val: int) -> float:
    """Decode a 12-bit integer to a floating point value in the range
    from 0 to 1e7.

    Required arguments:

    val -- The integer value to decode.

    """
    mantissa = (val >> 3) & F12_MAX_MANTISSA
    exp = val & 0x7
    return mantissa / float(F12_MAX_MANTISSA) * math.pow(10, exp)


def decimal16(val: float, name: str, unit: str) -> int:
    """Encode a decimal value with a 11-bit signed mantissa and a
    power-of-ten exponent from -16..15 as a 16-bit integer.
    This covers the range from -1024e15 to +1023e15.

    Required arguments:

    val -- The floating point value to convert.

    name -- The name of the CTid parameters being converted.

    unit -- The physical unit of the CTid parameter being converted.

    """
    mantissa = 0
    exp = 0

    if val != 0.0:
        # Determine exponent that gives us an mantissa in the range
        # from -1024..-103 or 103..1023:
        while exp > -16 and -102.4 <= val <= 102.3:
            val *= 10.0
            exp -= 1
        mantissa = round(val)
        while mantissa < -1024 or mantissa > 1023:
            mantissa /= 10.0
            exp += 1
        if exp > 15:
            raise Error(
                f"{name} {val}{unit} outside of range "
                f"from -1024e15..1023e15{unit}"
            )
        mantissa = int(mantissa)
    return ((mantissa & 0x7FF) << 5) | (exp & 0x1F)


def undecimal16(val: int) -> float:
    """Decode 16-bit integer to a floating number number.

    Required arguments:

    val -- The integer value to decode.

    """
    mantissa = (val >> 5) & 0x7FF
    if mantissa >= 0x400:
        mantissa -= 0x800
    exp = val & 0x1F
    if exp >= 0x10:
        exp -= 0x20
    return mantissa * math.pow(10, exp)


def check_table_data(raw_data: bytes):
    version = struct.unpack_from(">B", raw_data)[0]
    if version <= 1:
        length = 30
        if len(raw_data) < length + 1:  # excluding start symbol
            raise Error("Insufficient table data")
        exp_crc = crc8_rohc(raw_data[:length])
        got_crc = struct.unpack_from(">B", raw_data[length:])[0]
        if exp_crc != got_crc:
            raise CRCError(exp_crc, got_crc)
    elif version <= 3:
        length = 33
        if len(raw_data) < length + 2:  # excluding start symbol
            raise Error("Insufficient table data")
        exp_crc = crc16_modbus(raw_data[:length])
        got_crc = struct.unpack_from(">H", raw_data[length:])[0]
        if exp_crc != got_crc:
            raise CRCError(exp_crc, got_crc)
    else:
        length = 43
        if len(raw_data) < length + 2:  # excluding start symbol
            raise Error("Insufficient table data")
        exp_crc = crc16_modbus(raw_data[:length])
        got_crc = struct.unpack_from(">H", raw_data[length:])[0]
        if exp_crc != got_crc:
            raise CRCError(exp_crc, got_crc)
    return raw_data[:length]


class Table:
    """Objects of this class can be used to hold the contents of a
    CTid table in a Python-native format.  Use method Table.encode()
    to convert the table to a sequence of bytes, encoded as per CTid
    specification or decode a sequence of bytes with method
    Table.decode().

    """

    def __init__(self, data: bytes | None = None):
        if data is not None:
            data = check_table_data(data)

        self.encoding = False
        self.version = CTID_VERSION
        self.mfg_id = 0
        self.model = ""
        self.serial_number: int = 0
        self.sensor_type = SENSOR_TYPE_AC
        self.r_source: float = 0
        self.r_load: float = 0  # undefined

        self.size: float = 0
        self.rated_current: float = 0
        self.voltage_at_rated_current: float = 0
        self.phase_at_rated_current: float = 0
        self.voltage_temp_coeff: float = 0
        self.phase_temp_coeff: float = 0
        self.cal_table = {1.5: [0, 0], 5: [0, 0], 15: [0, 0], 50: [0, 0]}
        self.bias_voltage: float = 0
        self.reserved = 0
        self.mfg_info = 0
        self.scale: float = 0
        self.offset: float = 0
        self.delay: float = 0
        self.sensor_unit: int = 0
        self.threshold: float = 0
        self.hysteresis: float = 0
        self.debounce_time: int = 0
        self.edge_mask: int = 0
        self.ntc_a: float = 0
        self.ntc_b: float = 0
        self.ntc_c: float = 0
        self.ntc_m: float = 0
        self.ntc_n: float = 0
        self.ntc_k: float = 0

        # internal data:
        self._raw_data = b""
        self._raw_offset = 0

        if data is not None:
            self.decode(data)

    def __str__(self) -> str:
        mfg_id_str = get_mfg_id(self.mfg_id)
        if mfg_id_str is not None:
            mfg_id_str = '"' + mfg_id_str + '"'
        else:
            mfg_id_str = f"{self.mfg_id:#04x}"

        sensor_type_str = get_sensor_type_name(self.sensor_type)
        if sensor_type_str is not None:
            sensor_type_str = '"' + sensor_type_str + '"'
        else:
            sensor_type_str = f"{self.sensor_type:#1x}"

        ret = (
            f"CTid version={self.version:d}, sensor_type={sensor_type_str}, "
            f'mfg_id={mfg_id_str}, model="{self.model}", '
        )
        if (
            self.sensor_type >= SENSOR_TYPE_AC
            and self.sensor_type <= SENSOR_TYPE_RC
        ):
            rows = []
            for lvl, val in self.cal_table.items():
                rows.append(f"{repr(lvl)}%: {val[0]:+.2f}%/{val[1]:+.2f}°")
            ret += (
                f"size={self.size:.1f}mm, "
                f"serial={self.serial_number}, "
                f"current={self.rated_current:.1f}A, "
                f"voltage={self.voltage_at_rated_current:.6f}V, "
                f"bias={1e3 * self.bias_voltage:.3f}mV, "
                f"phase={self.phase_at_rated_current:.2f}°, "
                f"voltage_temp_coeff={self.voltage_temp_coeff:.0f}ppm/°C, "
                f"phase_temp_coeff={self.phase_temp_coeff:.1f}m°/°C, "
                f"reserved={self.reserved:#02x}, "
                f"mfg_info={self.mfg_info:#02x}, "
                f"Rs={self.r_source:g}, "
                f"Rl={self.r_load:g}, "
                "cal={" + ", ".join(rows) + "}"
            )
        elif self.sensor_type == SENSOR_TYPE_LINEAR:
            unit = get_sensor_unit(self.sensor_unit)
            ret += (
                f"scale={self.scale:g}{unit}/V "
                f"offset={self.offset:g}{unit} "
                f"delay={self.delay:g}μs"
            )
        elif self.sensor_type == SENSOR_TYPE_TEMP_LINEAR:
            ret += f"scale={self.scale:g}°C/V offset={self.offset:g}°C"
        elif self.sensor_type == SENSOR_TYPE_TEMP_NTC:
            ret += (
                f"A={self.ntc_a:g} "
                f"B={self.ntc_b:g} "
                f"C={self.ntc_c:g} "
                f"M={self.ntc_m:g} "
                f"N={self.ntc_n:g} "
                f"K={self.ntc_k:g}"
            )
        elif self.sensor_type == SENSOR_TYPE_PULSE:
            ret += (
                f"threshold={self.threshold:g}±{self.hysteresis:g}V "
                f"debounce={self.debounce_time:d}ms "
                f"edge={self.edge_mask:#x}"
            )
        else:
            pass
        ret += "}"
        return ret

    def m_u2(self, name: str, scale: float = 1, unit: str | None = None):
        fmt = ">B"
        if self.encoding:
            val = fix(getattr(self, name), 2, False, name, unit, scale)
            self._raw_data += struct.pack(fmt, val << 6)
        else:
            val = struct.unpack_from(fmt, self._raw_data, self._raw_offset)[0]
            self._raw_offset += struct.calcsize(fmt)
            setattr(self, name, unfix(val >> 6, scale))

    def m_u8(self, name: str, scale: float = 1, unit: str | None = None):
        fmt = ">B"
        if self.encoding:
            val = fix(getattr(self, name), 8, False, name, unit, scale)
            self._raw_data += struct.pack(fmt, val)
        else:
            val = struct.unpack_from(fmt, self._raw_data, self._raw_offset)[0]
            self._raw_offset += struct.calcsize(fmt)
            setattr(self, name, unfix(val, scale))

    def m_s8(
        self,
        name: str,
        scale: float = 1,
        unit: str | None = None,
        idx1: float | None = None,
        idx2: int | None = None,
    ):
        fmt = ">b"
        if self.encoding:
            if idx1 is not None and idx2 is not None:
                val = fix(
                    getattr(self, name)[idx1][idx2], 8, True, name, unit, scale
                )
            else:
                val = fix(getattr(self, name), 8, True, name, unit, scale)
            self._raw_data += struct.pack(fmt, val)
        else:
            val = struct.unpack_from(fmt, self._raw_data, self._raw_offset)[0]
            self._raw_offset += struct.calcsize(fmt)
            if idx1 is not None and idx2 is not None:
                t = getattr(self, name)
                t[idx1][idx2] = unfix(val, scale)
            else:
                setattr(self, name, unfix(val, scale))

    def m_4s10(self, name: str, levels: list[float]):
        """Pack/unpack four signed 10-bit words into/from 5 unsigned bytes.

        Required arguments:

        name -- The name of the CTid parameter being packed/unpacked


        levels -- The signal levels (in percent) by which the table is
            indexed.

        """
        fmt = 5 * "B"
        t = getattr(self, name)
        if self.encoding:
            v0 = fix(t[levels[0]][0], 10, True, name, "%", 0.01)
            v1 = fix(t[levels[0]][1], 10, True, name, "°", 0.01)
            v2 = fix(t[levels[1]][0], 10, True, name, "%", 0.01)
            v3 = fix(t[levels[1]][1], 10, True, name, "°", 0.01)
            bs = (
                (v0 >> 2) & 0xFF,
                ((v0 & 0x03) << 6) | ((v1 >> 4) & 0x3F),
                ((v1 & 0x0F) << 4) | ((v2 >> 6) & 0x0F),
                ((v2 & 0x3F) << 2) | ((v3 >> 8) & 0x03),
                (v3 & 0xFF),
            )
            self._raw_data += struct.pack(fmt, *bs)
        else:
            bs = struct.unpack_from(fmt, self._raw_data, self._raw_offset)
            self._raw_offset += struct.calcsize(fmt)
            v0 = s10((bs[0] << 2) | ((bs[1] >> 6) & 0x03))
            v1 = s10(((bs[1] & 0x3F) << 4) | ((bs[2] >> 4) & 0x0F))
            v2 = s10(((bs[2] & 0x0F) << 6) | ((bs[3] >> 2) & 0x3F))
            v3 = s10(((bs[3] & 0x03) << 8) | bs[4])
            t[levels[0]][0] = unfix(v0, 0.01)
            t[levels[0]][1] = unfix(v1, 0.01)
            t[levels[1]][0] = unfix(v2, 0.01)
            t[levels[1]][1] = unfix(v3, 0.01)

    def m_u16(self, name: str, scale: float = 1, unit: str | None = None):
        fmt = ">H"
        if self.encoding:
            val = fix(getattr(self, name), 16, False, name, unit, scale)
            self._raw_data += struct.pack(fmt, val)
        else:
            val = struct.unpack_from(fmt, self._raw_data, self._raw_offset)[0]
            self._raw_offset += struct.calcsize(fmt)
            setattr(self, name, unfix(val, scale))

    def m_s16(self, name: str, scale: float = 1, unit: str | None = None):
        fmt = ">h"
        if self.encoding:
            val = fix(getattr(self, name), 16, True, name, unit, scale)
            self._raw_data += struct.pack(fmt, val)
        else:
            val = struct.unpack_from(fmt, self._raw_data, self._raw_offset)[0]
            self._raw_offset += struct.calcsize(fmt)
            setattr(self, name, unfix(val, scale))

    def m_d16(self, name: str, unit: str):
        fmt = ">H"
        if self.encoding:
            val = getattr(self, name)
            self._raw_data += struct.pack(fmt, decimal16(val, name, unit))
        else:
            val = struct.unpack_from(fmt, self._raw_data, self._raw_offset)[0]
            self._raw_offset += struct.calcsize(fmt)
            setattr(self, name, undecimal16(val))

    def m_s12(self, name: str, scale: float = 1, unit: str | None = None):
        fmt = ">H"
        if self.encoding:
            s12 = fix(getattr(self, name), 12, True, name, unit, scale)
            if s12 < 0:
                s12 &= 0xFFF
            self._raw_data += struct.pack(fmt, s12 << 4)
        else:
            u16 = struct.unpack_from(fmt, self._raw_data, self._raw_offset)[0]
            self._raw_offset += struct.calcsize(fmt)
            s12 = (u16 >> 4) & 0x0FFF
            if s12 >= 0x800:
                s12 -= 0x1000
            setattr(self, name, unfix(s12, scale))

    def m_u4_s12(
        self,
        name4: str,
        scale4: float,
        unit4: str | None,
        name12: str,
        scale12: float = 1,
        unit12: str | None = None,
    ):
        fmt = ">H"
        if self.encoding:
            u4 = fix(getattr(self, name4), 4, False, name4, unit4, scale4)
            s12 = fix(getattr(self, name12), 12, True, name12, unit12, scale12)
            if s12 < 0:
                s12 &= 0xFFF
            self._raw_data += struct.pack(fmt, (u4 << 12) | s12)
        else:
            u16 = struct.unpack_from(fmt, self._raw_data, self._raw_offset)[0]
            self._raw_offset += struct.calcsize(fmt)
            setattr(self, name4, unfix((u16 >> 12) & 0xF, scale4))
            s12 = u16 & 0x0FFF
            if s12 >= 0x800:
                s12 -= 0x1000
            setattr(self, name12, unfix(s12, scale12))

    def m_f12_f12(self, name1: str, unit1: str, name2: str, unit2: str):
        fmt = ">BH"
        if self.encoding:
            f1 = float12(getattr(self, name1), name1, unit1)
            f2 = float12(getattr(self, name2), name2, unit2)
            u24 = (f1 << 12) | f2
            self._raw_data += struct.pack(fmt, u24 >> 16, u24 & 0xFFFF)
        else:
            val = struct.unpack_from(fmt, self._raw_data, self._raw_offset)
            u24 = (val[0] << 16) | val[1]
            self._raw_offset += struct.calcsize(fmt)
            setattr(self, name1, round(unfloat12((u24 >> 12) & 0xFFF)))
            setattr(self, name2, round(unfloat12((u24 >> 0) & 0xFFF)))

    def m_u24(self, name: str, scale: float = 1, unit: str | None = None):
        fmt = ">BH"
        if self.encoding:
            val = fix(getattr(self, name), 24, False, name, unit, scale)
            self._raw_data += struct.pack(
                fmt, (val >> 16) & 0xFF, val & 0xFFFF
            )
        else:
            val = struct.unpack_from(fmt, self._raw_data, self._raw_offset)
            val = (val[0] << 16) | val[1]
            self._raw_offset += struct.calcsize(fmt)
            setattr(self, name, unfix(val, scale))

    def m_f32(self, name: str):
        fmt = ">f"
        if self.encoding:
            self._raw_data += struct.pack(fmt, getattr(self, name))
        else:
            val = struct.unpack_from(fmt, self._raw_data, self._raw_offset)
            self._raw_offset += struct.calcsize(fmt)
            setattr(self, name, val[0])

    def m_utf8_4(self, name: str):
        if self.encoding:
            val = getattr(self, name).encode("utf-8")
            if len(val) > 4:
                raise Error(
                    f"{name} `{getattr(self, name)}' is {len(val)} bytes "
                    "long in UTF-8 but only up to 4 bytes are allowed."
                )
            while len(val) < 4:
                val += b"\0"
            self._raw_data += val
        else:
            raw = b""
            for i in range(self._raw_offset, self._raw_offset + 4):
                if self._raw_data[i] == 0:
                    break
                raw += bytearray((self._raw_data[i],))
            self._raw_offset += 4
            setattr(self, name, raw.decode())

    def m_utf8_8(self, name: str):
        if self.encoding:
            val = getattr(self, name).encode("utf-8")
            if len(val) > 8:
                raise Error(
                    f"{name} `{getattr(self, name)}' is {len(val)} bytes "
                    "long in UTF-8 but only up to 8 bytes are allowed."
                )
            while len(val) < 8:
                val += b"\0"
            self._raw_data += val
        else:
            raw = b""
            for i in range(self._raw_offset, self._raw_offset + 8):
                if self._raw_data[i] == 0:
                    break
                raw += bytearray((self._raw_data[i],))
            self._raw_offset += 8
            setattr(self, name, raw.decode())

    def marshall_params_ct(self):
        """Current Transducer Parameters"""
        self.m_u16("rated_current", 0.1, "A")
        self.m_u16("voltage_at_rated_current", 10e-6, "V")
        self.m_u16("size", 0.1, "mm")
        self.m_s12("phase_at_rated_current", 0.01, "°")
        self.m_s8("voltage_temp_coeff", 5, "ppm/°C")
        self.m_s8("phase_temp_coeff", 0.5, "m°/°C")
        if self.version >= 5:
            keys = list(self.cal_table.keys())
            if len(keys) != 4:
                raise Error(f"Cal table has {len(keys)} rows; expected 4.")
            self.m_4s10("cal_table", keys[0:2])
            self.m_4s10("cal_table", keys[2:4])
        else:
            for k in sorted(self.cal_table.keys()):
                self.m_s8("cal_table", 0.02, "%", idx1=k, idx2=0)
                self.m_s8("cal_table", 0.02, "\u00b0", idx1=k, idx2=1)
        self.m_s16("bias_voltage", 1e-6, "V")

    def marshall_params_basic_linear(self):
        """Basic linear Parameters (for linear temp. and generic linear
        sensors)."""
        self.m_f32("scale")
        self.m_f32("offset")

    def marshall_params_linear(self):
        """Linear Parameters."""
        self.marshall_params_basic_linear()
        self.m_s16("delay", 0.01, "μs")
        self.m_u16("sensor_unit")

    def marshall_params_ntc(self):
        """NTC Parameters."""
        self.m_f32("ntc_a")
        self.m_f32("ntc_b")
        self.m_f32("ntc_c")
        self.m_f32("ntc_m")
        if self.version == 3:
            self.m_d16("ntc_r1", "Ω")
        else:
            self.m_f32("ntc_n")
            self.m_f32("ntc_k")

    def marshall_params_pulse(self):
        """Pulse Parameters."""
        self.m_u16("threshold", 10e-6, "V")
        self.m_u16("hysteresis", 10e-6, "V")
        self.m_u8("debounce_time")
        self.m_u2("edge_mask")

    def marshall_params(self):
        if (
            self.sensor_type >= SENSOR_TYPE_AC
            and self.sensor_type <= SENSOR_TYPE_RC
        ):
            self.marshall_params_ct()
        elif self.sensor_type == SENSOR_TYPE_LINEAR:
            self.marshall_params_linear()
        elif self.sensor_type == SENSOR_TYPE_TEMP_LINEAR:
            self.marshall_params_basic_linear()
        elif self.sensor_type == SENSOR_TYPE_TEMP_NTC:
            self.marshall_params_ntc()
        elif self.sensor_type == SENSOR_TYPE_PULSE:
            self.marshall_params_pulse()

        max_size = 43 if self.version >= 4 else 33

        if len(self._raw_data) < max_size:
            self._raw_data += (max_size - len(self._raw_data)) * b"\0"
        elif len(self._raw_data) > max_size:
            raise Error("CTid table too big", len(self._raw_data), max_size)

    def marshall(self):
        self.m_u8("version")
        self.m_u16("mfg_id")
        if self.version >= 4:
            # v4 or newer
            self.m_utf8_8("model")
            self.m_u8("reserved")
            self.m_u24("serial_number")
            self.m_u8("sensor_type")
            self.m_f12_f12("r_source", "Ω", "r_load", "Ω")
            self.marshall_params()
        else:
            self.m_utf8_4("model")
            if self.version == 3:
                # v3
                self.m_u24("serial_number")
                self.m_u8("sensor_type")
                self.m_f12_f12("r_source", "Ω", "r_load", "Ω")
                self.m_u8("reserved")
                self.marshall_params()
            else:
                # v1 or v2
                self.m_u16("size", 0.1, "mm")
                self.m_u24("serial_number")
                self.m_u16("rated_current", 0.1, "A")
                self.m_u16("voltage_at_rated_current", 10e-6, "V")
                self.m_u4_s12(
                    "sensor_type",
                    1,
                    None,
                    "phase_at_rated_current",
                    0.01,
                    "°",
                )
                self.m_s8("voltage_temp_coeff", 5, "ppm/°C")
                self.m_s8("phase_temp_coeff", 0.5, "m°/°C")
                for k in sorted(self.cal_table.keys()):
                    self.m_s8("cal_table", 0.02, "%", idx1=k, idx2=0)
                    self.m_s8("cal_table", 0.02, "°", idx1=k, idx2=1)
                self.m_u8("reserved")
                self.m_u8("mfg_info")
                if self.version > 1:
                    self.m_f12_f12("r_source", "Ω", "r_load", "Ω")

    def encode(self, version: int = CTID_VERSION):
        """Encode the table contents and store it as a sequence of
        bytes in property `raw_data`.

        Keyword arguments:

        version -- The version of the CTid specification according to
            which to produce the table (default latest version).

        """
        self.encoding = True
        self._raw_data = b""
        self._raw_offset = 0
        self.version = version
        if version < 2 and (self.r_source != 0.0 or self.r_load != 0.0):
            raise Error(
                "Unable to encode r_source and r_load in "
                f"CTid table version {version}."
            )
        try:
            self.marshall()
        except KeyError as e:
            raise Error("Required parameter missing from CTid table.") from e
        except struct.error as e:
            raise Error("CTid table parameter has an invalid value.") from e
        if self.version == 1:
            # v1 used an 8-bit CRC
            self._raw_data += struct.pack(">B", crc8_rohc(self._raw_data))
            assert len(self._raw_data) == 31  # excluding start symbol
        else:
            self._raw_data += struct.pack(">H", crc16_modbus(self._raw_data))
            if self.version < 4:
                # v2-3
                assert len(self._raw_data) == 35  # excluding start symbol
            else:
                # v4 and on...
                assert len(self._raw_data) == 45  # excluding start symbol
        return self._raw_data

    def decode(self, raw_data: bytes):
        """Load the table from a sequence of bytes.

        Required arguments:

        raw_data -- The byte sequence to decode.  Note: the
            start-symbol and the CRC must not be part of this data.
            The CRC should already have been confirmed to be correct
            before calling this method.

        """
        self.encoding = False
        self._raw_data = raw_data
        self._raw_offset = 0
        self.marshall()


def bitstuff(data: bytes) -> bytes:
    """Get the bit-stuffed version of the data, prefixed with the
    start symbol.

    Required arguments:

    data -- The data bytes to bit-stuff.

    """
    bs = BitStuffer(bytes((START_SYM,)))
    for b in data:
        bs.append(b)
    return bs.get_output()


def unstuff(bitstream: bytes) -> bytearray:
    """Remove the start-symbol and the bit-stuffing from the
    bitstream.

    Required arguments:

    bitstream -- The bitstream to unstuff.

    """
    if bitstream[0] != START_SYM:
        raise Error("Bitstream missing start symbol.", bitstream[0], START_SYM)

    data = bytearray()
    run_length = 0
    byte = 0x00
    num_bits = 0
    for b in bitstream[1:]:
        mask = 0x80
        while mask != 0:
            if run_length >= 7:
                # drop a stuffer bit
                run_length = 0
            else:
                if b & mask:
                    byte |= 1 << (7 - num_bits)
                    run_length += 1
                else:
                    run_length = 0
                num_bits += 1
                if num_bits >= 8:
                    data.append(byte)
                    byte = 0
                    num_bits = 0
            mask >>= 1
    return data
