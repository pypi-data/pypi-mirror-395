"""
A parser for files from stm experiment into a simple dict.
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

import logging
import os
import re

import numpy as np
import pynxtools_spm.parsers.helpers as phs
import pynxtools_spm.parsers.nanonispy as nap
from pynxtools_spm.parsers.base_parser import SPMBase
from pynxtools_spm.parsers.helpers import (
    UNIT_TO_SKIP,
    nested_path_to_slash_separated_path,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")


# some Global variables to reduce the run time
SCAN_SIDE = None


class SxmGenericNanonis(SPMBase):
    """Specific class for stm reader from nanonis company."""

    def convert_key_to_unit_and_entity(
        self, key, val, start_bracket="", end_bracket=""
    ):
        """
        Split key into 'key' and 'key/@units' if key is designed as somthing like this 'key(A)'.
        """
        if start_bracket and end_bracket:
            if start_bracket in key and end_bracket in key:
                tmp_l_part, tmp_r_part = key.rsplit(start_bracket)
                unit = tmp_r_part.rsplit(end_bracket)[0]
                full_key = tmp_l_part.strip()
                if unit in UNIT_TO_SKIP:
                    unit = ""
                return [(full_key, val), (f"{full_key}/@unit", unit)]

            # In case if value contain name and unit e.g. /.../demodulated_signal: 'current(A)'
            if start_bracket in val and end_bracket in val:
                unit_parts = val.rsplit(start_bracket)
                # Assume that val does not have any key but decriptive text,
                # e.g. Current (A);Bias (V);
                if len(unit_parts) > 2:
                    return [(key, val)]
                tmp_l_part, tmp_r_part = unit_parts
                unit = tmp_r_part.rsplit(end_bracket)[0]
                val = tmp_l_part.strip()
                if unit in UNIT_TO_SKIP:
                    unit = ""
                return [(key, val), (f"{key}/@unit", unit)]

        return []

    def __get_raw_metadata_and_signal(self, file_name):
        """
        Retun metadata plain dict and signal
        Convert header part (that contains metadata) of a file with 'sxm' extension into
        plain dict.
        """
        scan_file = nap.read.Scan(file_name)
        header_end_byte = scan_file.start_byte()
        h_part = scan_file.read_raw_header(header_end_byte)
        while True:
            # Ignore all starting chars of string h_part except Alphabat
            if not re.match("[a-zA-Z]", h_part):
                h_part = h_part[1:]
            else:
                break

        h_comp_iter = iter(re.split("\n:|:\n", h_part))
        return dict(zip(h_comp_iter, h_comp_iter)), scan_file.signals

    def __get_aligned_scan_metadata_dict(self, prepend_part, text):
        """Scan metadata from descriptive text.

        Parameters
        ----------
        text : str
            descriptive text that contains scan metadata.

        Return
        ------
        dict
            A dictionary that contains scan metadata.
        """
        scan_metadata_dict = {}
        lines = text.split("\n")
        header = lines[0].split("\t")

        for line in lines[1:]:
            if line == "":
                continue
            parts = line.split("\t")
            startting = prepend_part + "/" + parts[2]
            for meta_tag, value in zip(header[1:], parts[1:]):
                scan_metadata_dict[startting + "/" + meta_tag] = value
        return scan_metadata_dict

    def __get_nested_metadata_dict_and_signal(self):
        """
        Get meradata and signal from spm file.
        """
        metadata_dict, signal = self.__get_raw_metadata_and_signal(self.file_path)
        nesteded_matadata_dict = phs.get_nested_dict_from_concatenated_key(
            metadata_dict
        )
        # Convert nested (dict) path to signal into slash_separated path to signal
        temp_flattened_dict_sig = {}
        nested_path_to_slash_separated_path(signal, temp_flattened_dict_sig)
        temp_flattened_dict = {}
        nested_path_to_slash_separated_path(nesteded_matadata_dict, temp_flattened_dict)
        flattened_dict = {}
        scan_metadata_dict = None

        for key, val in temp_flattened_dict.items():
            # list of tuples of (data path, data) and (unit path/unit and unit value)
            tuple_li = self.convert_key_to_unit_and_entity(
                key, val, start_bracket="(", end_bracket=")"
            )
            if tuple_li:
                for tup in tuple_li:
                    flattened_dict[tup[0]] = tup[1]
            else:
                flattened_dict[key] = val
            # Alingment of scan data with info, e.g.
            # /DATA/INFO : 	Channel	Name	Unit	Direction	Calibration	Offset
            # 14	Z	m	both	-3.484E-9	0.000E+0
            # 3	Input_4	V	both	1.000E+0	0.000E+0
            # 0	Current	A	both	-1.000E-10	-8.014E-13
            # 16	Phase	deg	both	1.800E+1	0.000E+0
            # 17	Amplitude	m	both	4.235E-11	0.000E+0
            # 18	Frequency_Shift	Hz	both	3.815E+0	0.000E+0
            # 19	Excitation	V	both	1.000E-2	0.000E+0
            # 20	LIX_1_omega	A	both	1.000E+0	0.000E+0
            # 21	LIY_1_omega	A	both	1.000E+0	0.000E+0
            if key == "/DATA/INFO":
                scan_metadata_dict = self.__get_aligned_scan_metadata_dict(
                    "/DATA/INFO", text=val
                )

        if scan_metadata_dict:
            flattened_dict.update(scan_metadata_dict)
        flattened_dict.update(temp_flattened_dict_sig)
        return flattened_dict

    def parse(self):
        return self.__get_nested_metadata_dict_and_signal()


def get_stm_raw_file_info(raw_file):
    """Parse the raw_file into a organised dictionary. It helps users as well as developers
    to understand how the reader works and modify the config file."""

    base_name = os.path.basename(raw_file)
    raw_name = base_name.rsplit(".")[0]
    data_dict = SxmGenericNanonis(raw_file).__get_nested_metadata_dict_and_signal()
    temp_file = f"{raw_name}.txt"
    with open(temp_file, mode="w", encoding="utf-8") as txt_f:
        for key, val in data_dict.items():
            txt_f.write(f"{key} : {val}\n")
    logging.info(" %s has been created to investigate raw data structure.", temp_file)
