#
# Copyright (c) 2024 eGauge Systems LLC
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
import typing
from pathlib import Path

from intelhex import IntelHex

from . import ctid

# the default (ATtiny10) address at which the CTid table is stored:
CTID_TABLE_ADDR = 0x3C0


def intel_hex_encode(
    program_image: Path | str | typing.IO | dict | IntelHex,
    table: ctid.Table,
    table_addr: int = CTID_TABLE_ADDR,
    ctid_version: int = ctid.CTID_VERSION,
) -> bytes:
    """Encode a program image and a CTid table into an Intel hex
    formatted file and return it as a byte stream.

    This raises ctid.Error if there is a problem.

    Required arguments:

    program_image -- The program image to encode the CTid table into.

    table -- The CTid table to encode.

    Keyword arguments:

    table_addr -- The base address at which to store the CTid table.
        It is an error if the program_image already has content at the
        addresses to be occupied by the CTid table (default 0x3c0).

    ctid_version -- The CTid specification version to use when encoding
        the table (default ctid.CTID_VERSION).

    """
    bitstream = ctid.bitstuff(table.encode(ctid_version))
    bitstream_len = len(bitstream)

    if bitstream_len > 255:
        raise ctid.Error("CTid table too large", bitstream_len, 255)

    if isinstance(program_image, Path):
        program_image = str(program_image)

    ihex = IntelHex(program_image)

    max_addr = ihex.maxaddr()
    if max_addr is None:
        raise ctid.Error("program image is empty")

    if max_addr >= table_addr:
        raise ctid.Error(
            "CTid table overlaps program image", max_addr, table_addr
        )

    # the byte at table_addr stores the bitstream length:
    ihex[table_addr] = bitstream_len

    for i, byte in enumerate(bitstream):
        ihex[table_addr + 1 + i] = byte

    return ihex.tobinstr()
