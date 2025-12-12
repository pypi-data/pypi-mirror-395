"""
A short description on STS reader which also suitable for file from STM .
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

import json
from typing import Dict, Union, Tuple, Any, Optional
import numpy as np
import yaml
import copy

from pynxtools.dataconverter.readers.base.reader import BaseReader
from pynxtools.dataconverter.template import Template
from pynxtools import get_nexus_version

from pynxtools_spm.nxformatters.base_formatter import SPMformatter

# For flatened key-value pair from nested dict.
REPLACE_NESTED: Dict[str, str] = {}


def manually_filter_data_type(template):
    """Check for the data with key type and fix it"""
    nexus_key_to_dt = {
        "/ENTRY[entry]/INSTRUMENT[instrument]/ENVIRONMENT[environment]/current_sensor/current_gain": float,
        "rcs_fabrication/model": str,
        "hardware/mode": str,
        "hardware/model/@version": str,
    }
    template_copy = copy.deepcopy(template)
    for key, val in template_copy.items():
        for manual_key, dt in nexus_key_to_dt.items():
            if key.endswith(manual_key):
                try:
                    template[key] = dt(val)
                except (ValueError, TypeError):
                    print(
                        f"Warning: Could not convert data {val} for field {key} to {dt}"
                    )
                    del template[key]


# pylint: disable=invalid-name, too-few-public-methods
class SPMReader(BaseReader):
    """Reader for XPS."""

    supported_nxdls = ["NXspm", "NXsts", "NXstm", "NXafm"]

    def read(
        self,
        template: dict = None,
        file_paths: Tuple[str] = None,
        objects: Tuple[Any] = None,
    ):
        """
        General read menthod to prepare the template.
        """
        filled_template: Union[Dict, None] = Template()
        eln_file: str = None
        config_file: Optional[str] = None
        data_file: Optional[str] = ""
        experirment_technique: Optional[str] = None
        raw_file_ext: Optional[str] = None

        for file in file_paths:
            ext = file.rsplit(".", 1)[-1]
            fl_obj: object
            if ext in ["sxm", "dat", "sm4"]:
                data_file = file
                raw_file_ext = ext
            if ext == "json":
                config_file = file
            if ext in ["yaml", "yml"]:
                eln_file = file
                with open(file, mode="r", encoding="utf-8") as fl_obj:
                    eln_dict = yaml.safe_load(fl_obj)
                    experirment_technique = eln_dict.get("experiment_technique")
                    # TODO get defition name
                if experirment_technique is None:
                    raise ValueError("Experiment technique is not defined in ELN file.")
        if not eln_file:
            raise ValueError("ELN file is required for the reader to work.")
        if not data_file:
            raise ValueError("Data file is required for the reader to work.")

        formater_obj: Optional[SPMformatter] = None
        # Get callable object that has parser inside
        if experirment_technique == "STM" and raw_file_ext == "sxm":
            from pynxtools_spm.nxformatters.nanonis.nanonis_sxm_stm import (
                NanonisSxmSTM,
            )

            formater_obj = NanonisSxmSTM(
                template=template,
                raw_file=data_file,
                eln_file=eln_file,
                config_file=config_file,
            )
            # nss.get_nxformatted_template()
        elif experirment_technique == "STM" and raw_file_ext == "sm4":
            from pynxtools_spm.nxformatters.omicron.omicron_sm4_stm import (
                OmicronSM4STM,
            )

            formater_obj = OmicronSM4STM(
                template=template,
                raw_file=data_file,
                eln_file=eln_file,
                config_file=config_file,
            )
            # oss.get_nxformatted_template()
        elif experirment_technique == "AFM" and raw_file_ext == "sxm":
            from pynxtools_spm.nxformatters.nanonis.nanonis_sxm_afm import NanonisSxmAFM

            formater_obj = NanonisSxmAFM(
                template=template,
                raw_file=data_file,
                eln_file=eln_file,
                config_file=config_file,
            )
            # nsa.get_nxformatted_template()
        elif experirment_technique == "STS" and raw_file_ext == "dat":
            from pynxtools_spm.nxformatters.nanonis.nanonis_dat_sts import NanonisDatSTS

            formater_obj = NanonisDatSTS(
                template=template,
                raw_file=data_file,
                eln_file=eln_file,
                config_file=config_file,
            )
            # nds.get_nxformatted_template()

        if not formater_obj:
            raise ValueError(
                f"IncorrectExperiment: Incorect experiment technique ({experirment_technique}) or file extension ({raw_file_ext}) are given"
            )
        formater_obj.get_nxformatted_template()
        # manually_remove the empty data
        for key, val in template.items():
            if isinstance(val, np.ndarray):
                filled_template[key] = val
                continue
            elif val in (None, ""):
                continue

            filled_template[key] = val
        # Set nexus def version
        filled_template["/ENTRY[entry]/definition/@version"] = get_nexus_version()
        if not filled_template.keys():
            raise ValueError(
                "Reader could not read anything! Check for input files and the"
                " corresponding extention."
            )
        manually_filter_data_type(filled_template)
        return filled_template


READER = SPMReader
