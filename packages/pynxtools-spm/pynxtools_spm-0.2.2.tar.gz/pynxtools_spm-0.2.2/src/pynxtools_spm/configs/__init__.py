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

import os
import json


pwd = os.path.dirname(__file__)


def load_default_config(config_type):
    """Load the default configuration file for a given config type."""

    nanonis_dat_generic_sts = os.path.join(
        pwd, "nanonis", "nanonis_dat_generic_sts.json"
    )
    nanonis_sxm_generic_stm = os.path.join(
        pwd, "nanonis", "nanonis_sxm_generic_stm.json"
    )
    nanonis_sxm_generic_afm = os.path.join(
        pwd, "nanonis", "nanonis_sxm_generic_afm.json"
    )
    omicron_sm4_stm = os.path.join(pwd, "omicron", "omicron_sm4_stm.json")

    config_file = None
    if config_type == "nanonis_dat_generic_sts":
        config_file = nanonis_dat_generic_sts
    elif config_type == "nanonis_sxm_generic_stm":
        config_file = nanonis_sxm_generic_stm
    elif config_type == "nanonis_sxm_generic_afm":
        config_file = nanonis_sxm_generic_afm
    elif config_type == "omicron_sm4_stm":
        config_file = omicron_sm4_stm
    if config_file is not None:
        with open(config_file, "r", encoding="utf-8") as f:
            return json.load(f)
