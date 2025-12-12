#!/usr/bin/env python3
"""
TODO: Add simple description of the module
"""
# -*- coding: utf-8 -*-
#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
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
#

# TODO use logger from pynxtools and if it is not available, use a default logger
# TODO: design the massage pattern
import logging

from pint import formatter

__all__ = ["SPM_LOGGER"]

SPM_LOGGER: logging.Logger = logging.getLogger("pynxtools_spm")
SPM_LOGGER.setLevel("WARNING")

__ch = logging.StreamHandler()
__ch.setLevel("WARNING")
__formatter = logging.Formatter("%(levelname)s - %(name)s - %(message)s")
__ch.setFormatter(__formatter)
SPM_LOGGER.addHandler(__ch)
