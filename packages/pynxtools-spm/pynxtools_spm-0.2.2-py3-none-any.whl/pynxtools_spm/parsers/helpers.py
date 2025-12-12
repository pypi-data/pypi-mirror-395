#!/usr/bin/env python
"""
TODO: Add simple description of the module
"""


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

import numpy as np
from typing import Dict, Any

UNIT_TO_SKIP = ["on/off", "off", "on", "off/on"]


def nested_path_to_slash_separated_path(
    nested_dict: dict, flattened_dict: dict, parent_path=""
):
    """Convert nested dict into slash separeted path upto certain level."""
    separator = "/"

    for key, val in nested_dict.items():
        path = parent_path + separator + key
        if isinstance(val, dict):
            nested_path_to_slash_separated_path(val, flattened_dict, path)
        else:
            flattened_dict[path] = val


def has_separator_char(key, sep_char_li):
    """
    Check string or key whether the separator char provided in
    'Separator Char List' exist or not.
    """
    bool_k = [x in sep_char_li for x in key]
    return np.any(bool_k)


def get_nested_dict_from_concatenated_key(
    data_dict, dict_to_map_path=None, sep_chars=None
):
    """
    Create nested dict. If key are concateneted with '_', '>' split the key and
    construct nested dict. For example, {'x1': {'x2': {'x3': {'x4': {'x5': 3}}}}
    from 'x1_x2_x3_x4>x5:3'
    """
    if dict_to_map_path is not None:
        spreaded_dict = dict_to_map_path
    else:
        spreaded_dict: Dict[str, Any] = {}
    if sep_chars is None:
        sep_chars = ["_", ">"]
    for d_key, d_val in data_dict.items():
        if has_separator_char(d_key, sep_chars):
            # Find out which separator char exist there
            for k_c in d_key:
                if k_c in sep_chars:
                    sep_char = k_c
                    break
            l_key, r_key = d_key.split(sep_char, 1)
            if not has_separator_char(r_key, sep_chars):
                if l_key not in spreaded_dict:
                    spreaded_dict[l_key]: Dict[str, Any] = {}
                spreaded_dict[l_key][r_key] = d_val
            else:
                if l_key in spreaded_dict:
                    spreaded_dict[l_key] = get_nested_dict_from_concatenated_key(
                        {r_key: d_val},
                        dict_to_map_path=spreaded_dict[l_key],
                        sep_chars=sep_chars,
                    )
                else:
                    spreaded_dict[l_key]: Dict[str, Any] = {}
                    spreaded_dict[l_key] = get_nested_dict_from_concatenated_key(
                        {r_key: d_val},
                        dict_to_map_path=spreaded_dict[l_key],
                        sep_chars=sep_chars,
                    )
        else:
            spreaded_dict[d_key] = d_val

    return spreaded_dict


# TODO only one from get_nested_dict_from_concatenated_key and transfer_plain_config_to_nested_config
# can bve kept.
def transfer_plain_config_to_nested_config(template, nested_dict):
    def split_each_key(key, final_val, nested_dict):
        parts = key.split("/", 1)
        if len(parts) < 2:
            parts.append("")
        k1, rest = parts
        k1_val = nested_dict.get(k1, None)
        if k1_val is None and rest != "":
            nested_dict[k1] = dict()
            split_each_key(rest, final_val, nested_dict[k1])
        elif rest == "":
            nested_dict[k1] = final_val
        elif isinstance(k1_val, dict):
            split_each_key(rest, final_val, k1_val)

    for key, value in template.items():
        _, rest = key.split("/", 1)
        split_each_key(key=rest, final_val=value, nested_dict=nested_dict)


# def nested_path_to_slash_separated_path(
#     nested_dict: dict, flattened_dict: dict, parent_path=""
# ):
#     """Convert nested dict into slash separeted path upto certain level."""
#     start = "/"

#     for key, val in nested_dict.items():
#         path = parent_path + start + key
#         if isinstance(val, dict):
#             nested_path_to_slash_separated_path(val, flattened_dict, path)
#         else:
#             flattened_dict[path] = val
