#!/usr/bin/env python3
#
# Copyright (c) 2016-2017, 2024 eGauge Systems LLC
#
# See LICENSE file for details.
#
"""This program is a simple demonstration of how the ctid.Decoder()
can be used to decode the CTid info from a waveform consisting of a
series of timestamped samples.  The data is read from
`examples/data/test-ctid-decoder.raw`, which contains data sampled at
8kHz.

"""

import pickle
import sys
from pathlib import Path

from egauge import ctid


def fmt_ts(timestamp: float) -> str:
    """Format a timestamp in a human-readable format.

    Required arguments:

    timestamp -- A timestamp measured in microseconds.

    """
    sec = 1e-6 * timestamp
    return f"{sec:.3f} sec"


def decode(
    sample_rate: float, ts_list: list[float], values: list[float]
) -> ctid.Table | None:
    """Decode a series of samples and convert them to a CTid table.

    Returns a ctid.Table object as soon as the first CTid table has
    been successfully decoded or None if no CTid table was found.

    Required arguments:

    sampling_rate -- The average frequency at which the samples were
        acquired.  This is used to properly size the decoding window
        size.  Assuming a sufficient number of samples, this could be
        inferred from `ts_list`.

    ts_list -- The list of timestamps, measured in microseconds.

    values -- The list of sample values.  This must be the same length
        as `ts_list`.

    """
    table_data = b""
    decoder = ctid.Decoder(sample_rate)
    for i, val in enumerate(values):
        ts = ts_list[i]
        ret = decoder.add_sample(ts, val)
        if ret < 0:
            print(f"found start symbol at {fmt_ts(ts)}")
            table_data = b""
        elif ret > 0:
            byte = decoder.get_byte()
            idx = len(table_data)
            print(f"decoded byte {idx:2}: 0x{byte:02x} at {fmt_ts(ts)}")
            table_data += byte.to_bytes(1)
            try:
                table = ctid.Table(table_data)
                return table
            except ctid.CRCError as e:
                print(f"Error: {e}")
                decoder = ctid.Decoder(sample_rate)
                table_data = b""
            except ctid.Error:
                pass  # need more data
    return None


input_path = Path(__file__).parent / "data" / "test-ctid-decoder.raw"

with open(input_path, "rb") as f:
    (freq, ts, samples) = pickle.load(f)

print(f"decoding data (sampling rate {freq:.1f} Hz)...")

table = decode(freq, ts, samples)

if table is None:
    print("Sorry, no CTid table detected...", file=sys.stderr)
    sys.exit(1)

print(f"Received: {table}")
