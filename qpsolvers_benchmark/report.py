#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Stéphane Caron
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Benchmark report generator.
"""

import datetime
import logging
import platform

from .utils import check_as_emoji
from .validator import Validator

try:
    import cpuinfo
except ImportError:
    cpuinfo = None
    logging.warn("Run ``pip install py-cpuinfo`` for a more CPU info")


class Report:
    def __init__(self, validator: Validator):
        """
        Initialize report written to file.

        Args:
            fname: File to write report to.
        """
        self.cpu_info = (
            platform.processor()
            if cpuinfo is None
            else cpuinfo.get_cpu_info()["brand_raw"]
        )
        self.datetime = str(datetime.datetime.now(datetime.timezone.utc))
        self.validator = validator

    def write(self, fname: str) -> None:
        with open(fname, "w") as output:
            output.write(
                f"""# Benchmark

- Date: {self.datetime}
- CPU: {self.cpu_info}

## Validation parameters

| Name | Value |
|------|-------|
"""
            )
            output.write(
                "\n".join(
                    [
                        f"| ``{name}`` | {value} |"
                        for name, value in self.validator.list_params()
                    ]
                )
            )
            output.write("\n\n")
            output.write(
                """## Results

| Problem | Solver | Found solution? | Primal |
|---------|--------|-----------------|--------|
"""
            )
            for result in self.results:
                problem = result["problem"]
                solver = result["solver"]
                found = check_as_emoji(result["found"])
                primal = check_as_emoji(result["primal"])
                output.write(
                    f"| {problem} | {solver} | {found} | {primal} |\n"
                )
