#
# Copyright (c) 2016-2017, 2019-2022, 2024-2025 eGauge Systems LLC
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

from egauge.loggers import ModuleLogger

log = ModuleLogger.get(__name__)

_START_SYM_ZC_COUNT = 16  # number of zero-crossings in start-symbol
_CLK_FREQ = 480  # nominal clock frequency of CTid carrier
_CLK_TOL = 50  # clock tolerance in %

_MAX_CLK_FREQ = math.ceil(_CLK_FREQ * (1.0 + (_CLK_TOL / 100)))
_MIN_CLK_FREQ = math.floor(_CLK_FREQ * (1.0 - (_CLK_TOL / 100)))
_MIN_CLK_PERIOD = 1e6 / _MAX_CLK_FREQ  # min. period in microseconds
_MAX_CLK_PERIOD = 1e6 / _MIN_CLK_FREQ  # max. period in microseconds

_START_SYM_MAX_DURATION = _START_SYM_ZC_COUNT / 2 * _MAX_CLK_PERIOD


def time_diff(l: float, r: float) -> float:
    return l - r


def is_zero_crossing(curr: float, prev: float, mean: float) -> bool:
    return (prev < mean) != (curr < mean)


class Window:
    def __init__(self, sampling_freq: float):
        self.sample_period = 1e6 / sampling_freq  # period in microseconds
        self.avg_len = math.ceil(_START_SYM_MAX_DURATION / self.sample_period)
        window_len = 2 * self.avg_len

        self.tolerance = 0.0
        self.count = 0  # number of valid samples
        self.avg_count = 0  # number of averaged samples
        self.sum = 0  # sum of the valid samples
        self.mean = 0  # mean value of valid samples
        self.wr = 0  # index of next sample to be written
        self.prev_polarity = 0  # previous polarity
        self.ts: list[float] = [0] * window_len
        self.val: list[float] = [0] * window_len

    def enter_sample(self, ts: float, val: float):
        if self.avg_count < self.avg_len:
            self.avg_count += 1
        else:
            idx = self.wr + self.avg_len
            if idx >= len(self.val):
                idx -= len(self.val)
            self.sum -= self.val[idx]
        if self.count < len(self.val):
            self.count += 1
        self.sum += val
        self.val[self.wr] = val
        self.ts[self.wr] = ts
        self.wr = (self.wr + 1) % len(self.val)
        self.mean = self.sum / self.avg_count

    def at_zero_crossing(self) -> bool:
        curr_val = self.val[(self.wr + len(self.val) - 1) % len(self.val)]
        curr_pol = curr_val >= self.mean
        prev_pol = self.prev_polarity
        self.prev_polarity = curr_pol
        return curr_pol != prev_pol

    def at_start_symbol(self) -> float | None:
        if self.count < 1:
            return None

        curr = (self.wr + len(self.val) - 1) % len(self.val)
        prev_val = self.val[curr]
        self.prev_polarity = prev_val >= self.mean
        end_ts = self.ts[curr]
        start_ts = end_ts - _START_SYM_MAX_DURATION
        total = 0
        avg_count = 0

        # See if we can find 16 zero-crossings within _START_SYM_MAX_DURATION:
        first_ts = 0
        zc_ts = []
        i = 1
        while i < self.count:
            curr = (curr + len(self.val) - 1) % len(self.val)
            curr_ts = self.ts[curr]
            curr_val = self.val[curr]

            if time_diff(start_ts, curr_ts) > _MAX_CLK_PERIOD:
                return None

            total += curr_val
            avg_count += 1

            if not is_zero_crossing(curr_val, prev_val, self.mean):
                continue  # keep looking for zero-crossing
            prev_val = curr_val
            zc_ts.append(curr_ts)
            if len(zc_ts) >= _START_SYM_ZC_COUNT:
                first_ts = curr_ts
                break

            i += 1

        if len(zc_ts) < _START_SYM_ZC_COUNT:
            return None

        mean = total / avg_count

        # Verify that there were no zero-crossings for
        # _START_SYM_MAX_DURATION before the first edge of the
        # start-symbol
        while i < self.count:
            curr = (curr + len(self.val) - 1) % len(self.val)
            curr_ts = self.ts[curr]
            curr_val = self.val[curr]

            if is_zero_crossing(curr_val, prev_val, mean):
                return None
            if time_diff(first_ts, curr_ts) >= _START_SYM_MAX_DURATION:
                break
            prev_val = curr_val

            i += 1

        # Calculate average period based on the 7 full bit times the
        # 16 zero-crossings cover (clock periods may be asymmetric):
        period = time_diff(zc_ts[1], zc_ts[_START_SYM_ZC_COUNT - 1]) / (
            _START_SYM_ZC_COUNT / 2 - 1
        )
        if period < _MIN_CLK_PERIOD or period > _MAX_CLK_PERIOD:
            return None

        self.tolerance = max(period / 4, 1.2 * self.sample_period)

        # Verify that each bit has the expected period:
        curr_ts = end_ts
        for i in range(0, _START_SYM_ZC_COUNT, 2):
            dt = time_diff(curr_ts, zc_ts[i + 1])
            if abs(dt - period) > self.tolerance:
                return None
            curr_ts = zc_ts[i + 1]

        # Now that we confirmed a start-symbol, commit to its mean value:
        self.sum = total
        self.avg_count = avg_count
        self.mean = mean
        return period


class ByteDecoder:
    def __init__(self):
        self.num_bits = 0
        self.val = 0
        self.edge_count = 0
        self.run_length = 0
        self.start_ts = None
        self.decoded_byte = 0

    def reset(self):
        self.__init__()

    def timed_out(self, period: float, now: float) -> bool:
        if self.start_ts is None:
            return False
        return time_diff(now, self.start_ts) > 4 * period

    def update(self, period: float, tolerance: float, ts: float) -> bool:
        if self.start_ts is None:
            self.start_ts = ts
            return False

        if time_diff(ts, self.start_ts + period - tolerance) < 0:
            # got what looks like a 1-edge
            self.edge_count += 1
            return False

        bit = self.edge_count & 1
        log.debug(
            "bit %d at 0x%08x (edge_count %d, start_ts 0x%08x)",
            bit,
            ts,
            self.edge_count,
            self.start_ts,
        )

        self.edge_count = 0
        self.start_ts = ts
        if self.run_length >= 7:
            # drop stuffer bit...
            self.run_length = 0
            return False

        if bit:
            self.run_length += 1
        else:
            self.run_length = 0

        self.val = (self.val << 1) | bit
        self.num_bits += 1

        if self.num_bits < 8:
            return False
        self.decoded_byte = self.val
        self.val = 0
        self.num_bits = 0
        return True

    def get_byte(self) -> int:
        return self.decoded_byte


class Decoder:
    """Decode a sequence of equidistant sample values that represent a
    differential Manchester-encoded signal into a byte stream.

    """

    def __init__(self, sampling_freq: float):
        """Create a waveform decoder for data sampled at a given
        frequency.

        Required arguments:

        sampling_freq -- The sampling frequency in Hertz.

        """
        self.w = Window(sampling_freq)
        self.bd = ByteDecoder()
        self.period = None

    def add_sample(self, timestamp: float, value: float) -> int:
        """Enter a sample value for a given timestamp.

        Returns -1 when a new start-symbol was detected, 0 when more
        data is needed, and 1 if a complete byte has been decoded.

        Required arguments:

        timestamp -- The time in microseconds at which the sample
            value was acquired.

        value -- The value of the sample.

        """
        self.w.enter_sample(timestamp, value)

        if self.period is None:
            self.period = self.w.at_start_symbol()
            if self.period is None:
                return 0
            self.bd.reset()
            return -1  # got a new start-symbol

        if self.bd.timed_out(self.period, timestamp):
            # check if implied last edge finishes a byte, if so, return it:
            ret = self.bd.update(self.period, self.w.tolerance, timestamp)
            self.period = None
            return 1 if ret else 0

        if not self.w.at_zero_crossing():
            return 0

        log.debug("zero-crossing at 0x%08x (mean %d)", timestamp, self.w.mean)
        return self.bd.update(self.period, self.w.tolerance, timestamp)

    def get_byte(self) -> int:
        """After Decoder.add_samples() returns 1, this returns the
        most recently decoded byte.

        """
        return self.bd.get_byte()
