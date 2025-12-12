#
# Copyright (c) 2025 eGauge Systems LLC
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
import json
import logging
import logging.config
import sys
from json import JSONDecodeError
from pathlib import Path
from typing import Any


class ModuleLogger:
    logging_config: dict[str, Any] | None = None

    @classmethod
    def get(cls, module_name: str) -> logging.Logger:
        if cls.logging_config is None:
            config_egauge = Path.home() / ".config/egauge"
            prog_name = Path(sys.argv[0]).stem

            cfg_path = config_egauge / "logging" / (prog_name + ".json")
            if not cfg_path.exists():
                cfg_path = config_egauge / "logging.json"
                if not cfg_path.exists():
                    cfg_path = None

            if cfg_path:
                with open(cfg_path, encoding="utf-8") as f:
                    try:
                        cls.logging_config = json.load(f)
                        if cls.logging_config:
                            logging.config.dictConfig(cls.logging_config)
                    except (
                        JSONDecodeError,
                        ValueError,
                        TypeError,
                        AttributeError,
                        ImportError,
                    ) as e:
                        log = logging.getLogger(__name__)
                        log.error("%s: %s", cfg_path, e)
                        # don't try loading it again:
                        cls.logging_config = {}

        return logging.getLogger(module_name)
