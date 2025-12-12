#
# Copyright (c) 2018-2022, 2024 eGauge Systems LLC
# 	1644 Conestoga St, Suite 2
# 	Boulder, CO 80301
# 	voice: 720-545-9767
# 	email: davidm@egauge.net
#
#  All rights reserved.
#
#  This code is the property of eGauge Systems LLC and may not be
#  copied, modified, or disclosed without any prior and written
#  permission from eGauge Systems LLC.
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
import argparse
import sys

from intelhex import IntelHex

import egauge.ctid as CTid

CTid_table_addr = 0x3C0  # table goes in last 64 bytes


def is_abbrev(abbrev: str, full: str) -> bool:
    if not abbrev:
        return False
    if len(abbrev) > len(full):
        return False
    return abbrev == full[0 : len(abbrev)]


def auto_int(x: str) -> int:
    """Accept base-prefixed decimal."""
    return int(x, 0)


def edge_mask(x: str) -> int:
    try:
        return int(x)
    except ValueError:
        pass
    if is_abbrev(x, "rising"):  # rising
        return 0x1
    if is_abbrev(x, "falling"):
        return 0x2
    if is_abbrev(x, "both"):
        return 0x3
    raise ValueError(
        'Edge mask must be one of "rising", "falling", or "both".'
    )


def cal_table_entry(string: str) -> tuple[float, float, float]:
    pair = string.split(":")
    if len(pair) != 2:
        raise argparse.ArgumentTypeError("missing `:'")
    idx = float(pair[0])
    if idx not in table.cal_table:
        allowed = ", ".join(f"{k:g}" for k in table.cal_table)
        raise argparse.ArgumentTypeError(
            f"Invalid index {idx} (must be one of {allowed})."
        )
    val = pair[1].split("/")
    if len(val) != 2:
        raise argparse.ArgumentTypeError("missing `/'")
    v_adj = float(val[0])
    p_adj = float(val[1])
    return (idx, v_adj, p_adj)


def hexdump(title: str, data: bytes):
    print(title + ":", end="")
    c = 0
    for b in data:
        if c % 8 == 0:
            print(f"\n 0x{c:08x}:", end="")
        print(f" 0x{b:02x}", end="")
        c += 1
    print("")


def main():
    global table
    table = CTid.Table()

    parser = argparse.ArgumentParser(
        description="Encode CTid parameters.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "program_template",
        help="Filename of the program template.",
        default=None,
    )
    parser.add_argument(
        "-d", "--debug", type=int, default=0, help="Debug level"
    )
    parser.add_argument(
        "-o",
        "--output-file",
        type=argparse.FileType("w"),
        default=sys.stdout,
    )
    #
    # Common information:
    #
    parser.add_argument(
        "-S",
        "--sensor-type",
        default="AC",
        choices=CTid.SENSOR_TYPE_NAME,
        help="Sensor-type.",
    )
    parser.add_argument(
        "-M",
        "--manufacturer",
        default="0",
        help="Manufacturer name or ID.",
    )
    parser.add_argument(
        "-m",
        "--model",
        default="",
        help="Model name (up to 4 characters).",
    )
    parser.add_argument(
        "-n",
        "--serial-number",
        type=auto_int,
        default=0,
        help="Serial number.",
    )
    parser.add_argument(
        "-r",
        "--r-source",
        type=float,
        default=0,
        help="Source resistance in Ohms.",
    )
    parser.add_argument(
        "-l",
        "--r-load",
        type=float,
        default=0,
        help="Rated load resistance in Ohms.",
    )
    parser.add_argument(
        "-V",
        "--table-version",
        type=int,
        default=None,
        help="Version of the CTid table to generate.",
    )
    #
    # CT Parameters:
    #
    parser.add_argument(
        "-a",
        "--calibration-entry",
        type=cal_table_entry,
        action="append",
        help="Calibration-entry of the form X:VA/PA, where "
        "X is the percentage of the rated current to which the "
        "entry applies, VA is the voltage-adjustment in %% and "
        "PA is the phase-adjustment in \u00b0.",
    )
    parser.add_argument(
        "-c",
        "--rated-current",
        type=float,
        default=100,
        help="Rated current of CT in Ampère.",
    )
    parser.add_argument(
        "-i",
        "--manufacturer-info",
        type=auto_int,
        default=0,
        help="Manufacturer-specific information.",
    )
    parser.add_argument(
        "-p",
        "--phase",
        type=float,
        default=0,
        help="Phase at rated current in \u00b0.",
    )
    parser.add_argument(
        "-s",
        "--size",
        type=float,
        default=0,
        help="Size of the sensor in millimeter.",
    )
    parser.add_argument(
        "-t",
        "--voltage-temp-coeff",
        type=float,
        default=0,
        help="Voltage temperature coefficient in ppm/\u00b0C.",
    )
    parser.add_argument(
        "-T",
        "--phase-temp-coeff",
        type=float,
        default=0,
        help="Phase temperature coefficient in m\u00b0/\u00b0C.",
    )
    parser.add_argument(
        "-v",
        "--rated-voltage",
        type=float,
        default=1 / 3.0,
        help="Rated voltage of CT in Volt.",
    )
    parser.add_argument(
        "-b",
        "--bias-voltage",
        type=float,
        default=0,
        help="Output voltage when no current is flowing through the CD.",
    )
    #
    # Linear Parameters:
    #
    parser.add_argument("--scale", type=float, default=None, help="Scale.")
    parser.add_argument("--offset", type=float, default=None, help="Offset.")
    parser.add_argument(
        "--delay", type=float, default=None, help="Signal delay in μs."
    )
    parser.add_argument(
        "--unit",
        type=int,
        default=0,
        help=f"Physical unit code (0..{len(CTid.SENSOR_UNITS) - 1}).",
    )
    #
    # NTC Temperature Parameters:
    #
    parser.add_argument(
        "--ntc-a", type=float, default=None, help="NTC A coefficient."
    )
    parser.add_argument(
        "--ntc-b", type=float, default=None, help="NTC B coefficient."
    )
    parser.add_argument(
        "--ntc-c", type=float, default=None, help="NTC C coefficient."
    )
    parser.add_argument(
        "--ntc-m", type=float, default=None, help="NTC parameter M."
    )
    parser.add_argument(
        "--ntc-n", type=float, default=None, help="NTC parameter N."
    )
    parser.add_argument(
        "--ntc-k", type=float, default=None, help="NTC parameter K."
    )
    #
    # Pulse Temperature Parameters:
    #
    parser.add_argument(
        "--threshold",
        type=float,
        default=None,
        help="Pulse threshold in Volts.",
    )
    parser.add_argument(
        "--hysteresis",
        type=float,
        default=None,
        help="Hysteresis for threhold in Volts.",
    )
    parser.add_argument(
        "--debounce-time",
        type=float,
        default=None,
        help="Debounce time for pulse in milli-seconds.",
    )
    parser.add_argument(
        "--edge-mask",
        type=edge_mask,
        default=None,
        help="Edge-mask.  May be an integer or one of "
        '"rising", "falling", or "both".',
    )

    args = parser.parse_args()

    table_version = args.table_version

    mfg_name = args.manufacturer
    try:
        mfg_id = CTid.get_mfg_id_for_name(mfg_name)
    except CTid.Error as e:
        print(
            f'{parser.prog}: "{mfg_name}" is invalid: {e}',
            file=sys.stderr,
        )
        sys.exit(1)

    type_name = args.sensor_type
    try:
        sensor_type = CTid.get_sensor_type_id(type_name)
    except CTid.Error as e:
        print(
            f'{parser.prog}: "{type_name}" is invalid: {e}',
            file=sys.stderr,
        )
        sys.exit(1)

    table.mfg_id = mfg_id
    table.model = args.model
    table.size = args.size
    table.serial_number = args.serial_number
    table.sensor_type = sensor_type
    table.r_source = args.r_source
    table.r_load = args.r_load
    # CT parameters:
    table.rated_current = args.rated_current
    table.voltage_at_rated_current = args.rated_voltage
    table.bias_voltage = args.bias_voltage
    table.phase_at_rated_current = args.phase
    table.voltage_temp_coeff = args.voltage_temp_coeff
    table.phase_temp_coeff = args.phase_temp_coeff
    if args.calibration_entry is not None:
        for idx, v_adj, p_adj in args.calibration_entry:
            table.cal_table[idx][0] = v_adj
            table.cal_table[idx][1] = p_adj

    # Voltage and temperature parameters:

    if args.scale is not None:
        table.scale = args.scale
    if args.offset is not None:
        table.offset = args.offset
    if args.delay is not None:
        table.delay = args.delay
    if args.unit is not None:
        table.sensor_unit = args.unit

    # NTC parameters:

    if args.ntc_a is not None:
        table.ntc_a = args.ntc_a
    if args.ntc_b is not None:
        table.ntc_b = args.ntc_b
    if args.ntc_c is not None:
        table.ntc_c = args.ntc_c
    if args.ntc_m is not None:
        table.ntc_m = args.ntc_m
    if args.ntc_n is not None:
        table.ntc_n = args.ntc_n
    if args.ntc_k is not None:
        table.ntc_k = args.ntc_k

    # Pulse parameters:

    if args.threshold is not None:
        table.threshold = args.threshold
    if args.hysteresis is not None:
        table.hysteresis = args.hysteresis
    if args.debounce_time is not None:
        table.debounce_time = args.debounce_time
    if args.edge_mask is not None:
        table.edge_mask = args.edge_mask

    table.mfg_info = int(args.manufacturer_info)

    if args.debug > 0:
        print("CTid params:\n\t", table)

    exception = None
    try:
        if table_version is not None:
            table_data = table.encode(table_version)
        else:
            table_data = table.encode()
    except CTid.Error as e:
        table_data = None
        exception = e
        if table_version is None and CTid.CTID_VERSION < 6:
            try:
                table_data = table.encode(version=5)
                print(f"{parser.prog}: using v5 encoding")
                exception = None
            except CTid.Error as e:
                exception = e
    if table_data is None:
        print(f"{parser.prog}: {exception}", file=sys.stderr)
        sys.exit(1)

    if args.debug > 0:
        hexdump("table", bytes((CTid.START_SYM,)) + table_data)

    bitstream = CTid.bitstuff(table_data)

    if args.debug > 0:
        hexdump("bit stream", bitstream)

    ihex = IntelHex(args.program_template)

    max_addr = max(ihex.todict().keys())
    if max_addr > CTid_table_addr:
        print(
            f"{parser.prog}: max address in program file "
            f"0x{max_addr:x} is >= table address 0x{CTid_table_addr:x}"
        )
        sys.exit(1)

    addr = CTid_table_addr
    ihex[addr] = len(bitstream)
    addr += 1
    for i, byte in enumerate(bitstream):
        ihex[addr + i] = byte

    ihex.write_hex_file(args.output_file)
