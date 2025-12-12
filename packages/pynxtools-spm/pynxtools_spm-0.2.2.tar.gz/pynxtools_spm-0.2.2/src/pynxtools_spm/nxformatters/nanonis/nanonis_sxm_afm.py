#!/usr/bin/env python3
"""
A formatter that formats the STM (Scanning Tunneling Microscopy) experiment's raw data
to NeXus application definition NXstm.
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

from __future__ import annotations
from typing import Optional, Union, TYPE_CHECKING
from pathlib import Path
import numpy as np

from pynxtools_spm.nxformatters.nanonis.nanonis_sxm_stm import NanonisSxmSTM
from pynxtools_spm.nxformatters.nanonis.nanonis_base import NanonisBase
from pynxtools_spm.configs import load_default_config
import pynxtools_spm.nxformatters.helpers as fhs

if TYPE_CHECKING:
    from pynxtools.dataconverter.template import Template


# TODO: Try to replace the upper version group, field and attributes
# with search method from regrex (e.g. SCAN_DATA[...]). This will help
# to search the group and field of overwritten name.

# TODO: add test to check if user example config file is the same as given default
# config file with this package.
# TODO: Check why link to NXdata does not work
# # Create links for NXdata in entry level
# entry = parent_path.split("/")[1]
# self.template[f"/{entry}/{field_nm}"] = {
#     "link": get_link_compatible_key(f"{parent_path}/{group_name}")
# }


class NanonisSxmAFM(NanonisSxmSTM, NanonisBase):
    """Formatter for Nanonis SPM data in SXM file format for AFM."""

    _grp_to_func = {
        "SPM_SCAN_CONTROL[spm_scan_control]": "_construct_nxscan_controllers",
        "start_time": "_set_start_end_time",
        "end_time": "_set_start_end_time",
    }
    _axes = ["x", "y", "z"]

    def __init__(
        self,
        template: "Template",
        raw_file: Union[str, "Path"],
        eln_file: str | Path,
        config_file: str = None,  # Incase it is not provided by users
        entry: Optional[str] = None,
    ):
        super().__init__(template, raw_file, eln_file, config_file, entry)
        # # self.config_dict: Dict = self._get_conf_dict(config_file)
        # self.nanonis_sxm_stm = NanonisSxmSTM(self.template, self.raw_file, eln_file)
        # # Use AFM specific config file and the resulting dict
        # self.nanonis_sxm_stm.config_dict = self.config_dict

    def get_nxformatted_template(self):
        self.walk_though_config_nested_dict(self.config_dict, "")
        self._format_template_from_eln()
        self._handle_special_fields()

    def _get_conf_dict(self, config_file: str | Path = None):
        if config_file is not None:
            return fhs.read_config_file(config_file)
        else:
            # return _nanonis_afm_sxm_generic_5e
            return load_default_config("nanonis_sxm_generic_afm")

    def construct_scan_pattern_grp(
        self,
        partial_conf_dict,
        parent_path: str,
        group_name="scan_mesh",
    ):
        """To construct the scan pattern like scan_mesh, scan_spiral (group) etc."""
        # The config file for afm is exactly the same as for stm
        NanonisSxmSTM.construct_scan_pattern_grp(
            self,
            partial_conf_dict=partial_conf_dict,
            parent_path=parent_path,
            group_name=group_name,
        )

    def construct_scan_region_grp(
        self,
        partial_conf_dict,
        parent_path: str,
        group_name="scan_region",
    ):
        """To construct the scan region like scan_region."""
        # The config file for afm is exactly the same as for stm
        NanonisSxmSTM.construct_scan_region_grp(
            self,
            partial_conf_dict=partial_conf_dict,
            parent_path=parent_path,
            group_name=group_name,
        )

    def construct_single_scan_data_grp(self, parent_path, plot_data_info, group_name):
        """To construct the scan data like scan_data."""
        # The config file for afm is exactly the same as for stm
        NanonisSxmSTM.construct_single_scan_data_grp(
            self,
            parent_path=parent_path,
            plot_data_info=plot_data_info,
            group_name=group_name,
        )

    def construct_scan_data_grps(
        self,
        partial_conf_dict,
        parent_path: str,
        group_name="SCAN_DATA[scan_data]",
    ):
        """To construct the scan data like scan_data."""

        # The config file for afm is exactly the same as for stm
        NanonisSxmSTM.construct_scan_data_grps(
            self,
            partial_conf_dict=partial_conf_dict,
            parent_path=parent_path,
            group_name=group_name,
        )

    def _construct_nxscan_controllers(
        self,
        partial_conf_dict,
        parent_path: str,
        group_name="scan_control",
        **kwarg,
    ):
        """To construct the scan control like scan_control."""
        # The config file for afm is exactly the same as for stm
        NanonisSxmSTM._construct_nxscan_controllers(
            self,
            partial_conf_dict=partial_conf_dict,
            parent_path=parent_path,
            group_name=group_name,
        )

    def _nxdata_grp_from_conf_description(
        self,
        partial_conf_dict,
        parent_path,
        group_name,
        group_index=0,
        is_forward: Optional[bool] = None,
        rearrange_2d_data: bool = True,
    ):
        """Specialization of the generic function to create NXdata group from plot description
        in config file."""
        if (
            is_forward is None
            and "data" in partial_conf_dict
            and "raw_path" in partial_conf_dict["data"]
        ):
            is_forward = (
                True
                if "forward" in partial_conf_dict.get("data").get("raw_path").lower()
                else False
            )
        else:
            return

        nxdata_group_nm = NanonisBase._nxdata_grp_from_conf_description(
            self,
            partial_conf_dict,
            parent_path,
            group_name,
            group_index,
            is_forward,
            rearrange_2d_data=rearrange_2d_data,
        )
        if nxdata_group_nm is None:
            return None
        if "0" not in partial_conf_dict:
            axis_x = "x"
            axis_y = "y"
            self.template[f"{parent_path}/{nxdata_group_nm}/@axes"] = [
                axis_y,
                axis_x,
            ]
            self.template[
                f"{parent_path}/{nxdata_group_nm}/@AXISNAME_indices[{axis_x}_indices]"
            ] = 0
            self.template[f"{parent_path}/{nxdata_group_nm}/AXISNAME[{axis_x}]"] = (
                np.linspace(
                    self.NXScanControl.x_start,
                    self.NXScanControl.x_end,
                    int(self.NXScanControl.x_points),
                )
            )
            self.template[
                f"{parent_path}/{nxdata_group_nm}/AXISNAME[{axis_x}]/@units"
            ] = self.NXScanControl.x_start_unit

            self.template[
                f"{parent_path}/{nxdata_group_nm}/@AXISNAME_indices[{axis_y}_indices]"
            ] = 1
            self.template[f"{parent_path}/{nxdata_group_nm}/AXISNAME[{axis_y}]"] = (
                np.linspace(
                    self.NXScanControl.y_end,
                    self.NXScanControl.y_start,
                    int(self.NXScanControl.y_points),
                )
            )
            self.template[
                f"{parent_path}/{nxdata_group_nm}/AXISNAME[{axis_y}]/@units"
            ] = self.NXScanControl.y_start_unit
        return nxdata_group_nm
