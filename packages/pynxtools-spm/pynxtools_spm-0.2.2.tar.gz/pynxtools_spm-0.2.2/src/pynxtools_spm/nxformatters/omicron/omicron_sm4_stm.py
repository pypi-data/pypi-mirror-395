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

from typing import TYPE_CHECKING, Optional, Any, Callable
import re
import datetime
from pathlib import Path
import numpy as np

from pynxtools.dataconverter.helpers import convert_data_dict_path_to_hdf5_path

from pynxtools_spm import SPM_LOGGER
from pynxtools_spm.nxformatters.omicron.omicron_base import OmicronBase
from pynxtools_spm.configs import load_default_config
import pynxtools_spm.nxformatters.helpers as fhs
from pynxtools_spm.nxformatters.helpers import (
    _get_data_unit_and_others,
)
from pynxtools_spm.nxformatters.helpers import replace_variadic_name_part


if TYPE_CHECKING:
    from pynxtools.dataconverter.template import Template


class OmicronSM4STM(OmicronBase):
    """
    Formatter for Omicron SM4 STM data.
    """

    _grp_to_func = {
        "lockin_amplifier": "_construct_lockin_amplifier_grp",
        "SPM_SCAN_CONTROL[": "_construct_nxscan_controllers",
    }
    _scan_list: list[str] = []

    _scan_tag_raw_data: dict[str, Any] = {}
    _scan_tag_to_data_group: dict[str, Any] = {}

    def __init__(
        self,
        template: "Template",
        raw_file: str | Path,
        eln_file: str | Path,
        config_file: str | Path = None,  # Incase it is not provided by users
        entry: Optional[str] = None,
    ):
        super().__init__(template, raw_file, eln_file, config_file, entry)

    def get_nxformatted_template(self):
        self.walk_though_config_nested_dict(self.config_dict, parent_path="")
        self._format_template_from_eln()
        self._handle_special_fields()

    def _get_conf_dict(self, config_file=None):
        if config_file is not None:
            return fhs.read_config_file(config_file)
        else:
            return load_default_config("omicron_sm4_stm")

    @staticmethod
    def find_active_channel(raw_dt_dct: dict = None, key: str = None):
        """
        Find active channel from a bunch of available channels.
        """
        if not (raw_dt_dct or key):
            raise ValueError(
                "NoInputData: Unable to find the active channels due to lack of input data."
            )

        def search_pattern(key_: str) -> Optional[re.Match[str]]:
            return re.search(r"RHK_CH(\d*)Drive_MasterOscillator", key_, flags=re.A)

        if key is not None:
            search_result = search_pattern(key)
            if search_result:
                return search_result.groups()[0]

        # Get the active channel
        for key_, val in raw_dt_dct.items():
            search_result = search_pattern(key_)
            # expect val a string representation of a number
            if search_result:
                try:
                    _ = int(val)
                    return search_result.groups()[0]
                except (ValueError, TypeError):
                    SPM_LOGGER.warning("No active channel is found")
        return

    @staticmethod
    def get_key_with(active_chnl=None, key=None):
        """Get key with active channel."""

        if not active_chnl:
            return key

        repl = rf"RHK_CH{active_chnl}Drive"

        return re.sub(pattern=r"RHK_CH[0-9]*Drive", repl=repl, string=key)

    def _construct_lockin_amplifier_grp(
        self,
        partial_conf_dict: dict,
        parent_path: str = "",
        group_name: Optional[str] = None,
    ):
        """Construct the lockin amplifier group."""
        # TODO: Make the active channel object level variable
        actv_chnl = self.find_active_channel(raw_dt_dct=self.raw_data)
        self.walk_through_config_by_modified_raw_data_key(
            partial_conf_dict=partial_conf_dict,
            parent_path=parent_path,
            group_name=group_name,
            func_to_raw_key=lambda k: self.get_key_with(active_chnl=actv_chnl, key=k),
        )

    def _construct_scan_pattern_grp(
        self,
        partial_conf_dict: dict,
        parent_path: str,
        group_name: Optional[str],
        scan_tag: str,
        func_on_raw_key: Callable,
    ):
        """Constructs Scan Pattern group from the scan environment group."""
        # Store full raw_data_dict and fill scan_region group according to the scan name
        raw_data = self.raw_data
        self.raw_data = self._scan_tag_raw_data[scan_tag]
        for key, val in partial_conf_dict.items():
            if re.match(r"^scan_points[\w]+", string=key):
                # If scan_points list of variadic fields
                if isinstance(val, list):
                    for li_elm in val:
                        part_to_embed, end_dct = list(li_elm.items())[0]
                        fld_key = replace_variadic_name_part(
                            name=key, part_to_embed=part_to_embed
                        )
                        data, _, other_attrs = _get_data_unit_and_others(
                            data_dict=self.raw_data,
                            end_dict=end_dct,
                            func_on_raw_key=func_on_raw_key,
                        )
                        if part_to_embed.endswith("x"):
                            self.NXScanControl.x_points = data
                            self.template[f"{parent_path}/{group_name}/{fld_key}"] = (
                                data
                            )
                        elif part_to_embed.endswith("y"):
                            self.NXScanControl.y_points = data
                            self.template[f"{parent_path}/{group_name}/{fld_key}"] = (
                                data
                            )

                elif isinstance(val, dict) and "raw_path" in val:
                    data, _, other_attrs = _get_data_unit_and_others(
                        data_dict=raw_data, end_dict=val
                    )
                    if key.endswith("x"):
                        self.NXScanControl.x_points = data
                        self.template[f"{parent_path}/{group_name}/{key}"] = data
                    elif key.endswith("y"):
                        self.NXScanControl.y_points = data
                        self.template[f"{parent_path}/{group_name}/{key}"] = data
                continue

            # step_size would be handled later.
            if not re.match(pattern=r"step_size[\w]+\[", string=key):
                self.walk_though_config_nested_dict(
                    config_dict={key: val},
                    parent_path=f"{parent_path}/{group_name}",
                    func_on_raw_key=func_on_raw_key,
                )

        for key, val in partial_conf_dict.items():
            if isinstance(val, list) and re.match(
                pattern=r"step_size[A-Y]{1}\[", string=key
            ):
                for li_elm in val:
                    part_to_embed, end_dct = list(li_elm.items())[0]
                    fld_key = replace_variadic_name_part(
                        name=key, part_to_embed=part_to_embed
                    )
                    data, unit, other_attrs = _get_data_unit_and_others(
                        data_dict=self.raw_data,
                        end_dict=end_dct,
                        func_on_raw_key=func_on_raw_key,
                    )
                    if data:
                        self.feed_data_unit_attr_to_template(
                            data=data,
                            parent_path=parent_path,
                            group_name=group_name,
                            fld_key=fld_key,
                            unit=unit,
                            other_attrs=other_attrs,
                        )

                    else:
                        if (
                            self.NXScanControl.x_points
                            and self.NXScanControl.x_range
                            and part_to_embed.endswith("x")
                        ):
                            self.template[f"{parent_path}/{group_name}/{fld_key}"] = (
                                self.NXScanControl.x_range / self.NXScanControl.x_points
                            )
                            self.template[
                                f"{parent_path}/{group_name}/{fld_key}/@units"
                            ] = self.NXScanControl.x_start_unit
                        elif (
                            self.NXScanControl.y_points
                            and self.NXScanControl.y_range
                            and part_to_embed.endswith("y")
                        ):
                            self.template[f"{parent_path}/{group_name}/{fld_key}"] = (
                                self.NXScanControl.y_range / self.NXScanControl.y_points
                            )
                            self.template[
                                f"{parent_path}/{group_name}/{fld_key}/@units"
                            ] = self.NXScanControl.y_start_unit

        self.raw_data = raw_data

    def _construct_scan_region_grp(
        self,
        partial_conf_dict: dict,
        parent_path: str,
        group_name: Optional[str],
        scan_tag: str,
        func_on_raw_key: Callable,
    ):
        """Constructs Scan Region group from the scan control group."""
        x_arr = None
        y_arr = None

        # Store full raw_data_dict and fill scan_region group according to the scan name
        raw_data = self.raw_data
        self.raw_data = self._scan_tag_raw_data[scan_tag]
        # Calculate the start of the x_axis and y_axis from the coordinate matrix.
        for k, v in self.raw_data.items():
            m = re.match(
                pattern=rf"/{scan_tag}/[\w/]*coords/[\w]+(x|y)", string=k, flags=re.I
            )
            if m and m.groups()[0] == "x":
                x_arr = v
            elif m and m.groups()[0] == "y":
                y_arr = v

        if isinstance(x_arr, np.ndarray):
            self.NXScanControl.x_end = x_arr[-1]
            self.NXScanControl.x_start = x_arr[0]
            self.NXScanControl.x_range = (
                self.NXScanControl.x_end - self.NXScanControl.x_start
            )
            self.NXScanControl.x_start_unit = "m"
        if isinstance(y_arr, np.ndarray):
            self.NXScanControl.y_end = y_arr[-1]
            self.NXScanControl.y_start = y_arr[0]
            self.NXScanControl.y_range = (
                self.NXScanControl.y_end - self.NXScanControl.y_start
            )
            self.NXScanControl.y_start_unit = "m"

        # handle fields
        for key, val in partial_conf_dict.items():
            if (
                re.match(pattern=r"scan_range[\w]{1}", string=key, flags=re.I)
                and "raw_path" in val
            ):
                self.template[
                    f"{parent_path}/{group_name}/{replace_variadic_name_part(key, part_to_embed='x')}"
                ] = self.NXScanControl.x_range
                # TODO collect unit from raw data dict
                self.template[
                    f"{parent_path}/{group_name}/{replace_variadic_name_part(key, part_to_embed='x')}/@units"
                ] = self.NXScanControl.x_start_unit
                self.template[
                    f"{parent_path}/{group_name}/{replace_variadic_name_part(key, part_to_embed='y')}"
                ] = self.NXScanControl.y_range
                self.template[
                    f"{parent_path}/{group_name}/{replace_variadic_name_part(key, part_to_embed='y')}/@units"
                ] = self.NXScanControl.y_start_unit
            elif (
                re.match(pattern=r"scan_start[\w]{1}", string=key, flags=re.I)
                and "raw_path" in val
            ):
                self.template[
                    f"{parent_path}/{group_name}/{replace_variadic_name_part(key, part_to_embed='x')}"
                ] = self.NXScanControl.x_start
                # TODO collect unit from raw data dict
                self.template[
                    f"{parent_path}/{group_name}/{replace_variadic_name_part(key, part_to_embed='x')}/@units"
                ] = self.NXScanControl.x_start_unit
                self.template[
                    f"{parent_path}/{group_name}/{replace_variadic_name_part(key, part_to_embed='y')}"
                ] = self.NXScanControl.y_start
                self.template[
                    f"{parent_path}/{group_name}/{replace_variadic_name_part(key, part_to_embed='y')}/@units"
                ] = self.NXScanControl.y_start_unit
            elif (
                re.match(pattern=r"scan_end[\w]{1}", string=key, flags=re.I)
                and "raw_path" in val
            ):
                self.template[
                    f"{parent_path}/{group_name}/{replace_variadic_name_part(key, part_to_embed='x')}"
                ] = self.NXScanControl.x_end
                # TODO collect unit from raw data dict
                self.template[
                    f"{parent_path}/{group_name}/{replace_variadic_name_part(key, part_to_embed='x')}/@units"
                ] = self.NXScanControl.x_start_unit
                self.template[
                    f"{parent_path}/{group_name}/{replace_variadic_name_part(key, part_to_embed='y')}"
                ] = self.NXScanControl.y_end
                self.template[
                    f"{parent_path}/{group_name}/{replace_variadic_name_part(key, part_to_embed='y')}/@units"
                ] = self.NXScanControl.y_start_unit

            # single field or nested groups or variadic fields
            else:
                self.walk_though_config_nested_dict(
                    config_dict={key: val},
                    parent_path=f"{parent_path}/{group_name}",
                    func_on_raw_key=func_on_raw_key,
                )

        # set back the original raw_data dict
        self.raw_data = raw_data

    def _construct_nxscan_controllers(
        self,
        partial_conf_dict: dict,
        parent_path: str,
        group_name: Optional[str] = None,
        **kwarg,
    ):
        """Specialization of the generic function to create NXscan controller
        in scan environment group."""

        # Modify the raw_data key according to the scan_tag: Topography_Backward, Current_Forward
        def func_on_raw_key_with(scan_tag, k, all_tags: list):
            return re.sub(
                pattern=rf"^/({'|'.join(all_tags)})/",
                repl=rf"/{scan_tag}/",
                string=k,
                flags=re.I,
            )

        for key, val in self.raw_data.items():
            m = re.match(
                pattern=r"/(?=topography|current|backward|forward)([\w]+)/",
                string=key,
                flags=re.I,
            )
            if m:
                scan_tag = m.groups()[0]
                if scan_tag not in self._scan_tag_raw_data:
                    self._scan_tag_raw_data[scan_tag] = {}

                self._scan_tag_raw_data[scan_tag][key] = val

                if scan_tag not in self._scan_list:
                    self._scan_list.append(scan_tag)

        m = re.search(
            pattern=r"^(SPM_SCAN_CONTROL\[[_\w]*)([*]+)([_\w]*\])$",
            string=group_name,
        )

        if not m:
            raise ValueError(
                "UnavailableGroup: Scan controller group has not been found in config file."
            )

        groups = m.groups()
        for scan_tag in self._scan_list:
            # modify group name according to the scan_tag
            group_name_mod = group_name.replace(groups[1], scan_tag.lower())
            parent_path_mod = f"{parent_path}/{group_name_mod}"

            func_on_raw_key = lambda k: func_on_raw_key_with(
                scan_tag=scan_tag, k=k, all_tags=self._scan_list
            )

            # Data from scan_region group will be used later
            for key, val in partial_conf_dict.items():
                if re.match(pattern=r"^scan_region$", string=rf"{key}", flags=re.I):
                    self._construct_scan_region_grp(
                        partial_conf_dict=val,
                        parent_path=parent_path_mod,
                        group_name=key,
                        scan_tag=scan_tag,
                        func_on_raw_key=func_on_raw_key,
                    )

            for key, val in partial_conf_dict.items():
                if re.match(
                    pattern=r"^meshSCAN\[mesh_scan\]$", string=rf"{key}", flags=re.I
                ):
                    self._construct_scan_pattern_grp(
                        partial_conf_dict=val,
                        parent_path=parent_path_mod,
                        group_name=key,
                        scan_tag=scan_tag,
                        func_on_raw_key=func_on_raw_key,
                    )

                elif isinstance(val, dict) and "raw_path" in val:
                    if "#note" in val:
                        continue
                    self.walk_though_config_nested_dict(
                        config_dict={key: val},
                        parent_path=parent_path_mod,
                        func_on_raw_key=func_on_raw_key,
                    )

    def _handle_special_fields(self):
        """Handle special fields in the template."""
        super()._handle_special_fields()
        template_key = ""
        config_dict = self.config_dict
        template_links = {}
        completed_field = []
        completed_group = []
        end_time_str = "end_time"
        start_time_str = "start_time"

        # end time
        for template_key, val in self.template.items():
            # Construct end_time
            if end_time_str not in completed_field and re.match(
                pattern=rf"/ENTRY\[\w+\]/{start_time_str}$", string=template_key
            ):
                self.template[template_key] = fhs.add_local_timezone(val)
                end_time_k = template_key.replace(start_time_str, end_time_str)
                end_dct = None
                for k in end_time_k.split("/")[1:]:
                    end_dct = config_dict.get(k, None)
                    config_dict = end_dct
                if isinstance(end_dct, dict) and "raw_path" in end_dct:
                    data, _, _ = _get_data_unit_and_others(
                        data_dict=self.raw_data, end_dict=end_dct
                    )
                    start_time = val
                    if start_time not in ["", None]:
                        try:
                            end_time = datetime.datetime.fromisoformat(
                                start_time
                            ) + datetime.timedelta(float(data))
                            end_time = datetime.datetime.isoformat(end_time)
                            self.template[end_time_k] = fhs.add_local_timezone(end_time)
                            completed_field.append(end_time_str)
                        except (ValueError, TypeError):
                            pass
            # TODO add a logger for all ecceptions
            elif m := re.match(
                pattern=r"(/ENTRY\[\w+\]/INSTRUMENT\[\w+\]/SCAN_ENVIRONMENT\[\w+\]/SPM_SCAN_CONTROL\[(\w+)\]/meshSCAN\[\w+\])",
                string=template_key,
            ):
                groups = m.groups()
                scn_ctl_grp = groups[1]
                full_match = groups[0]

                if scn_ctl_grp in completed_group:
                    continue

                for scan_tag in self._scan_list:
                    if scan_tag.lower() in scn_ctl_grp:
                        template_links[f"{full_match}/DATA[scan_data]"] = (
                            self._scan_tag_to_data_group[scan_tag]
                        )
                        completed_group.append(scn_ctl_grp)

        for template_key, link in template_links.items():
            self.template[template_key] = {
                "link": convert_data_dict_path_to_hdf5_path(link)
            }

    def _nxdata_grp_from_conf_description(
        self,
        partial_conf_dict,
        parent_path,
        group_name,
        group_index=0,
        is_forward=None,
        rearrange_2d_data=True,
    ):
        """Specialization of the generic function to create NXdata group from plot description
        in config file."""
        # conf_dict is an end dict of nxdata group
        conf_dict = partial_conf_dict.copy()

        group_name = super()._nxdata_grp_from_conf_description(
            partial_conf_dict,
            parent_path,
            group_name,
            group_index,
            is_forward,
            rearrange_2d_data=rearrange_2d_data,
        )
        if not group_name:
            return
        # Find the scan name from the given raw path "raw_path"
        # the scan tag comes in the name of scan_control
        for key, val in conf_dict.items():
            if key == "data":
                raw_path = val.get("raw_path")
                scan_tag = re.match(
                    rf"/({'|'.join(self._scan_list)})/", string=raw_path
                )
                scan_tag = scan_tag.groups()[0] if scan_tag else None
                if not scan_tag:
                    continue
                self._scan_tag_to_data_group[scan_tag] = f"{parent_path}/{group_name}"
