#!/usr/bin/env python3
"""
Parse raw data of STS experiment from Nanonis dat file.
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

import logging
import os
from typing import Dict, Optional, Tuple, Union, Any

import numpy as np


import pynxtools_spm.parsers.helpers as phs

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

UNIT_MAP = {
    "on/off": None,
    "off": False,
    "on": True,
    "off/on": None,
    "ON/OFF": None,
    "OFF": False,
    "ON": True,
    "OFF/ON": None,
    "On/Off": None,
    "Off": False,
    "On": True,
    "Off/On": None,
}

# Type aliases
NestedDict_t = Dict[str, Union[int, str, float, "NestedDict_t"]]


# pylint: disable=invalid-name
class DatGenericNanonis:
    """This class collect and store data fo Bias spectroscopy of SPM experiment.

    The class splits the data and store in into nested python dictionary as follows.
       E.g.
        bais_data = {data_field_name:{value: value_for_data_field_of_any_data_typeS,
                                      unit: unit name,
                                      date: ---,
                                      time: ---}
                    }
    """

    def __init__(self, file_name: str) -> None:
        """Innitialize object level variables."""
        # Note: If get some information about machines or vendors which makes
        # the data file distinguished collecte them.
        self.bias_spect_dict: NestedDict_t = {}
        self.raw_file: str = file_name
        self.extract_and_store_from_dat_file()

    # pylint: disable=too-many-arguments
    def check_and_write_unit(
        self, dct, key_or_line, unit_separators, end_of_seperators, value=None
    ):
        """Check and write unit.

        Parameters
        ----------
        dct : dict

        key_or_line : _type_
            The dict that tracks full nested paths and unit at deepest nest.
        unit_separators : list
            List of separator chars
        end_of_seperators : list
            List of end separator chars
        value : dict, optional
            dict to store dict
        """
        for sep_unit, end_sep in zip(unit_separators, end_of_seperators):
            if sep_unit in key_or_line:
                key, unit = key_or_line.split(sep_unit, 1)
                unit = unit.split(end_sep)[0]
                if key_or_line in dct:
                    del dct[key_or_line]
                # Replace some unit that are not part of standard e.g. on/off
                if UNIT_MAP.get(unit):
                    unit = UNIT_MAP[unit]
                if isinstance(value, dict):
                    value["unit"] = unit
                else:
                    value: NestedDict_t = {}
                    value["unit"] = unit
                dct[key] = value
                break

    def retrive_key_recursively(
        self, line_to_analyse: str, dict_to_store: NestedDict_t, key_seperators: list
    ) -> None:
        """Store metadata path in recursive manner because the path is separated by chars.

        Parameters
        ----------
        line_to_analyse : str
            Line with metadata path where each part of path is separated by chars from
            key_separated chars.
        dict_to_store : NestedDict_t
            Dict to store metadata path part in nested form
        key_separators : list
            List of chars separating metadata path.
        """
        unit_separators = [" ("]
        end_of_seperators = [")"]

        line_to_analyse = line_to_analyse.strip()
        for k_sep in key_seperators:
            new_dict: NestedDict_t = {}
            if k_sep in line_to_analyse:
                key, rest = line_to_analyse.split(k_sep, 1)
                key = key.strip()
                if key in dict_to_store:
                    new_dict = dict_to_store[key]  # type: ignore
                else:
                    new_dict = {}
                dict_to_store[key] = new_dict
                # check if key contains any unit inside bracket '()'
                self.check_and_write_unit(
                    dict_to_store, key, unit_separators, end_of_seperators, new_dict
                )
                self.retrive_key_recursively(rest, new_dict, key_seperators)
                return

        for sep_unit in unit_separators:
            if sep_unit in line_to_analyse:
                self.check_and_write_unit(
                    dict_to_store, line_to_analyse, unit_separators, end_of_seperators
                )
                return

        dict_to_store["value"] = line_to_analyse.strip()
        return

    def check_matrix_data_block_has_started(
        self, line_to_analyse: str
    ) -> Tuple[bool, list]:
        """_summary_

        Parameters
        ----------
        line_to_analyse : str
            Line to check whether matrix data has started.

        Returns
        -------
            Bool flag: Flag for matarix data found
            value list: List of row values if the matrix has found.
        """
        wd_list = line_to_analyse.split()
        int_list = []
        if not wd_list:
            return False, []
        for word in wd_list:
            try:
                float_n = float(word)
                int_list.append(float_n)
            except ValueError:
                return False, []
        return True, int_list

    def check_metadata_and_unit(self, key_and_unit: str):
        """Check for metadata and unit.

        Parameters
        ----------
        key_and_unit : str
            String to check key, metadata and unit
        """
        metadata = ""
        key: str
        unit: Any
        key, unit = key_and_unit.split("(")
        unit, rest = unit.split(")", 1)
        # Some units have extra info e.g. Current (A) [filt]
        if "[" in rest:
            metadata = rest.split("[")[-1].split("]")[0]
        if UNIT_MAP.get(unit):
            unit = UNIT_MAP[unit]
        return key, unit, metadata

    def extract_and_store_from_dat_file(self) -> None:
        """Extract data from data file and store them into object level nested dictionary."""

        key_seperators = [">", "\t"]
        is_matrix_data_found = False
        one_d_numpy_array = np.empty(0)

        def dismentle_matrix_into_dict_key_value_list(
            column_string, one_d_np_array, dict_to_store
        ):
            column_keys = column_string.split("\t")
            np_2d_array = one_d_np_array.reshape(-1, len(column_keys))
            dat_mat_comp = "dat_mat_components"
            dict_to_store[dat_mat_comp] = {}
            for ind, key_and_unit in enumerate(column_keys):
                if "(" in key_and_unit:
                    key, unit, data_stage = self.check_metadata_and_unit(key_and_unit)
                    # data_stage could be 'filt' or something like this
                    if data_stage:
                        dict_to_store[dat_mat_comp][f"{key.strip()} [{data_stage}]"] = {
                            "unit": unit,
                            "value": np_2d_array[:, ind],
                            "metadata": data_stage,
                        }
                    else:
                        dict_to_store[dat_mat_comp][key.strip()] = {
                            "unit": unit,
                            "value": np_2d_array[:, ind],
                        }
                else:
                    dict_to_store[dat_mat_comp][key.strip()] = {
                        "value": list(np_2d_array[:, ind])
                    }

        with open(self.raw_file, mode="r", encoding="utf-8") as file_obj:
            lines = file_obj.readlines()
            # last two lines for getting matrix data block that comes at the end of the file
            last_line: str
            for ind, line in enumerate(lines):
                if ind == 0:
                    last_line = line
                    continue
                is_mat_data, data_list = self.check_matrix_data_block_has_started(line)
                if is_mat_data:
                    is_matrix_data_found = True
                    one_d_numpy_array = np.append(one_d_numpy_array, data_list)
                    is_mat_data = False
                elif (not is_mat_data) and is_matrix_data_found:
                    is_matrix_data_found = False
                    dismentle_matrix_into_dict_key_value_list(
                        last_line, one_d_numpy_array, self.bias_spect_dict
                    )
                    last_line = line
                else:
                    self.retrive_key_recursively(
                        last_line, self.bias_spect_dict, key_seperators
                    )
                    last_line = line

            if (not is_mat_data) and is_matrix_data_found:
                is_matrix_data_found = False
                dismentle_matrix_into_dict_key_value_list(
                    last_line, one_d_numpy_array, self.bias_spect_dict
                )

    def parse(self):
        flattened_dict = {}
        # DatGenericNanonis to give slash separated path
        phs.nested_path_to_slash_separated_path(
            self.bias_spect_dict, flattened_dict=flattened_dict
        )
        return flattened_dict
