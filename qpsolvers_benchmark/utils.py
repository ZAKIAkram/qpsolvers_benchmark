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
Utility functions.
"""

import platform
import logging

try:
    import cpuinfo
except ImportError:
    cpuinfo = None
    logging.warn("Run ``pip install py-cpuinfo`` for more accurate CPU info")


def bool_as_emoji(b: bool):
    return "\U00002714" if b else "\U0000274C"


def get_cpu_info():
    return (
        platform.processor()
        if cpuinfo is None
        else cpuinfo.get_cpu_info()["brand_raw"]
    )