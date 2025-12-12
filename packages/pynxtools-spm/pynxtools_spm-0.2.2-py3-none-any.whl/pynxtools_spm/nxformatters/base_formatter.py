#!/usr/bin/env python3
"""
Base formatter for SPM data.
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

import datetime
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Union

import numpy as np
import yaml
from pynxtools.dataconverter.helpers import convert_data_dict_path_to_hdf5_path
from pynxtools.dataconverter.readers.utils import FlattenSettings, flatten_and_replace
from pynxtools.dataconverter.template import Template

from pynxtools_spm.nxformatters.helpers import (
    _get_data_unit_and_others,
    add_local_timezone,
    replace_variadic_name_part,
    to_intended_t,
)
from pynxtools_spm.parsers import SPMParser

if TYPE_CHECKING:
    from pint import Quantity


REPLACE_NESTED: Dict[str, str] = {}

CONVERT_DICT = {
    "Positioner_spm": "POSITIONER_SPM[positioner_spm]",
    "Temperature": "TEMPERATURE[temperature]",
    "Scan_control": "SCAN_CONTROL[scan_control]",
    "unit": "@units",
    "version": "@version",
    "default": "@default",
    "Sample": "SAMPLE[sample]",
    "History": "HISTORY[history]",
    "User": "USER[user]",
    "Data": "DATA[data]",
    "Source": "SOURCE[source]",
    "Mesh_scan": "mesh_SCAN[mesh_scan]",
    "Instrument": "INSTRUMENT[instrument]",
    "Note": "NOTE[note]",
    "Scan_environment": "SCAN_ENVIRONMENT[scan_environment]",
    "Sample_component": "SAMPLE_COMPONENT[sample_component]",
    "Sample_environment": "SAMPLE_ENVIRONMENT[sample_environment]",
    "model_version": "model/@version",
}

PINT_QUANTITY_MAPPING = {
    "[mass] * [length] ** 2 / [time] ** 3 / [current]": "voltage",
    "[mass] * [length] ** 2 / [current] / [time] ** 3": "voltage",
    "[length] ** 2 * [mass] / [time] ** 3 / [current]": "voltage",
    "[length] ** 2 * [mass] / [current] / [time] ** 3": "voltage",
    "[current]": "current",
}

REPEATEABLE_CONCEPTS = ("Sample_component",)


@dataclass
class NXdata:
    grp_name: Optional[str] = ""
    signal: Optional[str] = None
    auxiliary_signals: Optional[List[str]] = None
    title: Optional[str] = None


def write_multiple_concepts_instance(
    eln_dict: Dict, list_of_concept: tuple[str], convert_mapping: Dict[str, str]
):
    """Write multiple concepts for variadic name in eln dict if there are multiple
    instances are requested in eln archive.json file.
    """
    new_dict = {}
    if not isinstance(eln_dict, dict):
        return eln_dict
    for key, val in eln_dict.items():
        if key in list_of_concept:
            if key in convert_mapping:
                del convert_mapping[key]
            val = [val] if not isinstance(val, list) else val
            for i, item in enumerate(val, 1):
                new_key = f"{key.lower()}_{i}"
                convert_mapping.update({new_key: f"{key.upper()}[{new_key}]"})
                new_dict[new_key] = write_multiple_concepts_instance(
                    item, list_of_concept, convert_mapping
                )
        elif isinstance(val, dict):
            new_dict[key] = write_multiple_concepts_instance(
                val, list_of_concept, convert_mapping
            )
        else:
            new_dict[key] = val
    return new_dict


class SPMformatter(ABC):
    # Map function to deal specific group. Map key should be the same as it is
    # in config file
    _grp_to_func: dict[str, str] = {}  # Placeholder
    _axes: list[str] = []  # Placeholder

    # Class used to colleted data from several subgroups of ScanControl and reuse them
    # in the subgroups

    # TODO: only use unit for instead of y_start_unit, ...
    @dataclass
    class NXScanControl:  # TODO: Rename this class NXimageScanControl and create another class for BiasSpectroscopy
        # Put the class in the base_formatter.py under BaseFormatter class
        x_points: int
        y_points: int
        x_offset: Union[int, float]
        x_offset_unit: Union[str, "Quantity"]
        y_offset: Union[int, float]
        y_offset_unit: Union[str, "Quantity"]
        x_start: Union[int, float]
        x_start_unit: Union[str, "Quantity"]
        y_start: Union[int, float]
        y_start_unit: Union[str, "Quantity"]
        x_range: Union[int, float]
        x_range_unit: Union[str, "Quantity"]
        y_range: Union[int, float]
        y_range_unit: Union[str, "Quantity"]
        x_end: Union[int, float]
        x_end_unit: Union[str, "Quantity"]
        y_end: Union[int, float]
        y_end_unit: Union[str, "Quantity"]
        fast_axis: str  # lower case x, y
        slow_axis: str  # lower case x, y

    @dataclass
    class BiasSweep:
        """Storage to store data from bias_sweep and reuse them"""

        scan_offset_bias: float
        scan_offset_bias_unit: str
        scan_range_bias: float
        scan_range_bias_unit: str
        scan_start_bias: float
        scan_start_bias_unit: str
        scan_end_bias: float
        scan_end_bias_unit: str
        scan_points_bias: float
        scan_size_bias: float
        scan_size_bias_unit: str

    def __init__(
        self,
        template: Template,
        raw_file: Union[str, "Path"],
        eln_file: str | Path,
        config_file: Optional[
            Union[str, Path]
        ] = None,  # Incase it is not provided by users
        entry: Optional[str] = None,
    ):
        self.template: Template = template
        self.raw_file: Union[str, "Path"] = raw_file
        self.eln = self._get_eln_dict(eln_file)  # Placeholder
        self.raw_data: Dict = self.get_raw_data_dict()
        self.entry: str = entry
        self.config_dict = self._get_conf_dict(config_file) or None  # Placeholder

    @abstractmethod
    def _get_conf_dict(self, config_file: str | Path = None): ...

    def _get_eln_dict(self, eln_file: str | Path):
        with open(eln_file, mode="r", encoding="utf-8") as fl_obj:
            eln_dict: dict = yaml.safe_load(fl_obj)
            extended_eln: dict = write_multiple_concepts_instance(
                eln_dict=eln_dict,
                list_of_concept=REPEATEABLE_CONCEPTS,
                convert_mapping=CONVERT_DICT,
            )
            eln_dict = flatten_and_replace(
                FlattenSettings(extended_eln, CONVERT_DICT, REPLACE_NESTED)
            )
        return eln_dict

    def walk_though_config_nested_dict(
        self,
        config_dict: Dict,
        parent_path: str,
        use_custom_func_prior: bool = True,
        func_on_raw_key: Optional[Callable] = None,
    ):
        # This concept is just note where the group will be
        # handeld name of the function regestered in the self._grp_to_func
        # or somthing like that.
        if "#note" in config_dict:
            return
        for key, val in config_dict.items():
            if val is None or val == "":
                continue
            # Handle links
            if isinstance(val, str):
                self._resolve_link_in_config(val, f"{parent_path}/{key}")
            # Special case, will be handled in a specific function registered
            # in self._grp_to_func
            elif retrived_key := next(
                (k for k in self._grp_to_func.keys() if key.startswith(k)), None
            ):
                if not use_custom_func_prior:
                    self.walk_though_config_nested_dict(
                        config_dict=val,
                        parent_path=f"{parent_path}/{key}",
                        func_on_raw_key=func_on_raw_key,
                    )
                    # Fill special fields first
                    method = getattr(self, self._grp_to_func[retrived_key])
                    method(val, parent_path, key)
                else:
                    method = getattr(self, self._grp_to_func[retrived_key])
                    method(val, parent_path, key)
                    self.walk_though_config_nested_dict(
                        config_dict=val,
                        parent_path=f"{parent_path}/{key}",
                        func_on_raw_key=func_on_raw_key,
                    )

            # end dict of the definition path that has raw_path key
            # TODO: use self.template_data_and_other function here.
            elif isinstance(val, dict) and "raw_path" in val:
                if "#note" in val:
                    continue
                data, unit, other_attrs = _get_data_unit_and_others(
                    data_dict=self.raw_data,
                    end_dict=val,
                    func_on_raw_key=func_on_raw_key,
                )
                if data in ["", None]:
                    continue
                self.template[f"{parent_path}/{key}"] = to_intended_t(data)
                self.template[f"{parent_path}/{key}/@units"] = unit
                if other_attrs:
                    for k, v in other_attrs.items():
                        self.template[f"{parent_path}/{key}/@{k}"] = v
            # Handle to construct nxdata group that comes along as a dict
            elif (
                isinstance(val, dict)
                and ("title" in val or "grp_name" in val)
                and "data" in val
            ):
                _ = self._nxdata_grp_from_conf_description(
                    partial_conf_dict=val,
                    parent_path=parent_path,
                    group_name=key,
                )
            # variadic fields that would have several values according to the dimension as list
            elif isinstance(val, list) and isinstance(val[0], dict):
                for item in val:
                    # Handle to construct nxdata group
                    if (
                        isinstance(item, dict)
                        and ("title" in item or "grp_name" in item)
                        and "data" in item
                    ):
                        _ = self._nxdata_grp_from_conf_description(
                            partial_conf_dict=item,
                            parent_path=parent_path,
                            group_name=key,
                        )
                    # TODO: Add condition if dict contains `raw_path`
                    else:  # Handle fields and attributes
                        part_to_embed, path_dict = list(item.items())[0]
                        # Current only one item is valid
                        # with #note tag this will be handled in a specific function
                        if "#note" in path_dict:
                            continue
                        data, unit, other_attrs = _get_data_unit_and_others(
                            data_dict=self.raw_data,
                            end_dict=path_dict,
                            func_on_raw_key=func_on_raw_key,
                        )
                        if data in ["", None]:
                            continue
                        temp_key = f"{parent_path}/{replace_variadic_name_part(key, part_to_embed=part_to_embed)}"
                        self.template[temp_key] = to_intended_t(data)
                        if unit:
                            self.template[f"{temp_key}/@units"] = unit
                        if other_attrs:
                            for k, v in other_attrs.items():
                                self.template[f"{temp_key}/@{k}"] = v
            else:
                self.walk_though_config_nested_dict(
                    val, f"{parent_path}/{key}", func_on_raw_key=func_on_raw_key
                )

    def rearrange_data_according_to_axes(self, data, is_forward: Optional[bool] = None):
        """Rearrange array data according to the fast and slow axes.

        Implement this function in other base classes (e.g., NanonisBase) where it is needed.
        Parameters
        ----------
        data : np.ndarray
            Two dimensional array data from scan.
        is_forward : bool, optional
            Default scan direction.
        """

        return data

    def feed_data_unit_attr_to_template(
        self,
        data: Any,
        parent_path: str,
        fld_key: str,
        group_name: str = None,
        unit: str = None,
        other_attrs: dict = None,
    ):
        if group_name:
            parent_path = f"{parent_path}/{group_name}"
        self.template[f"{parent_path}/{fld_key}"] = to_intended_t(data)
        if unit:
            self.template[f"{parent_path}/{fld_key}/@units"] = unit
        if other_attrs:
            for k, v in other_attrs.items():
                self.template[f"{parent_path}/{group_name}/@{k}"] = v

    def get_raw_data_dict(self):
        return SPMParser().get_raw_data_dict(self.raw_file, eln=self.eln)

    @abstractmethod
    def get_nxformatted_template(self): ...

    def _format_template_from_eln(self):
        for key, val in self.eln.items():
            self.template[key] = to_intended_t(val)

    def _resolve_link_in_config(self, val: str, path: str = "/"):
        """Resolve the link in the config file.

        Internal Link to an object in the same nexus file can be defined in config file as:
        "concept_path" "@default_link:/ENTRY[entry]/INSTRUMENT[instrument]/cryo_shield_temp_sensor",
        INSTRUMENT[insturment] -> Class name [instance name]
        or
        "concept_path" "@default_link:/ENTRY[entry]/INSTRUMENT/cryo_shield_temp_sensor"
        INSTRUMENT -> Class name
        both are valid

        But,
        "concept_path" "@default_link:/ENTRY[entry]/instrument/cryo_shield_temp_sensor"
        instrument -> instance name
        is not valid

        External Link to an object in another file is defined as:
        "concept_path" "@default_link:/path/to/another:file.h5
        or,
        "concept_path" "@default_link:/path/to/another:file.nxs

        (Link to another has not been implemented yet)
        """

        if val.startswith("@default_link:"):
            val = val.split("@default_link:")[-1]

            classes = val.split("/")[1:]
            pattern = ""
            for part in classes:
                if not ("[" in part and "]" in part):
                    pattern += rf"/{part}(\[\w+\])?"
                else:
                    pattern = (
                        pattern + "/" + part.replace("[", r"\[").replace("]", r"\]")
                    )
            # pattern += "$"

            for tmp_k, tmp_v in self.template.items():
                m = re.match(pattern=pattern, string=tmp_k)
                if m and tmp_v not in ("", None):
                    self.template[f"{path}"] = {
                        "link": convert_data_dict_path_to_hdf5_path(m.group())
                    }
                    break

    def _handle_fields_with_modified_raw_data_key(
        self,
        partial_conf_dict: dict,
        parent_path: str,
        group_name: str,
        func_to_raw_key: Callable,
    ):
        # only field
        for fld_key, end_dct in partial_conf_dict.items():
            if not (isinstance(end_dct, dict) and "raw_path" in end_dct):
                continue

            mod_val_dct = {}
            # correct the active channel in the raw data key
            for tag, raw_str in end_dct.items():
                if tag == "note":
                    continue
                mod_vval = func_to_raw_key(raw_str)
                mod_val_dct[tag] = mod_vval
            data, unit, other_attrs = _get_data_unit_and_others(
                data_dict=self.raw_data, end_dict=mod_val_dct
            )
            self.feed_data_unit_attr_to_template(
                data=data,
                parent_path=parent_path,
                group_name=group_name,
                unit=unit,
                other_attrs=other_attrs,
                fld_key=fld_key,
            )

    def _handle_variadic_field_with_modified_raw_data_key(
        self,
        varidic_dct_li: list,
        parent_path: str,
        group_name: str,
        fld_to_modify,
        func_to_raw_key,
    ):
        for varidic_dct in varidic_dct_li:
            if not (isinstance(varidic_dct, dict)):
                continue
            part_to_embed, end_dict = list(varidic_dct.items())[0]
            if not (isinstance(end_dict, dict) and "raw_path" in end_dict):
                continue
            mod_fld = replace_variadic_name_part(fld_to_modify, part_to_embed)

            self._handle_fields_with_modified_raw_data_key(
                partial_conf_dict={mod_fld: end_dict},
                parent_path=parent_path,
                group_name=group_name,
                func_to_raw_key=func_to_raw_key,
            )

    # TODO move this function to the base_formatter.py
    def walk_through_config_by_modified_raw_data_key(
        self,
        partial_conf_dict: dict,
        parent_path: str,
        group_name: str,
        func_to_raw_key: Callable,
    ):
        for key, val in partial_conf_dict.items():
            # skips fields
            if isinstance(val, dict) and "raw_path" in val:
                self._handle_fields_with_modified_raw_data_key(
                    partial_conf_dict={key: val},
                    parent_path=parent_path,
                    group_name=group_name,
                    func_to_raw_key=func_to_raw_key,
                )
            elif isinstance(val, list):
                # Variadic fields
                if all(
                    "raw_path" in enddct
                    for vardict in val
                    for _, enddct in vardict.items()
                ):
                    # for var_fld_dct in val:
                    self._handle_variadic_field_with_modified_raw_data_key(
                        varidic_dct_li=val,
                        parent_path=parent_path,
                        group_name=group_name,
                        fld_to_modify=key,
                        func_to_raw_key=func_to_raw_key,
                    )
                # Handle vriadic group
                else:
                    for var_grp_nm_part, var_grp_dct in val:
                        mod_grp_name = replace_variadic_name_part(
                            name=group_name, part_to_embed=var_grp_nm_part
                        )
                        self.walk_through_config_by_modified_raw_data_key(
                            partial_conf_dict=var_grp_dct,
                            parent_path=parent_path,
                            group_name=mod_grp_name,
                            func_to_raw_key=func_to_raw_key,
                        )

            # Nested group
            elif isinstance(val, dict):
                self.walk_through_config_by_modified_raw_data_key(
                    partial_conf_dict=val,
                    parent_path=f"{parent_path}/{group_name}",
                    group_name=key,
                    func_to_raw_key=func_to_raw_key,
                )

    @abstractmethod
    def _construct_nxscan_controllers(
        self,
        partial_conf_dict,
        parent_path: str,
        group_name="scan_control",
        **kwarg,
    ): ...

    # TODO: Try to use decorator to ge the group name at some later stage
    def _nxdata_grp_from_conf_description(
        self,
        partial_conf_dict,
        parent_path: str,
        group_name: str,
        group_index=0,
        is_forward: Optional[bool] = None,
        rearrange_2d_data: bool = True,
    ):
        """Example NXdata dict descrioption from config
        partial_conf_dict = {
            "data": {
                "name": "temperature1(filter)",
                "raw_path": "/dat_mat_components/Temperature 1 [filt]/value",
                "@units": "/dat_mat_components/Temperature 1 [filt]/unit",
            },
            "0": {
                "name": "Bias Voltage",
                "raw_path": [
                    "/dat_mat_components/Bias calc/value",
                    "/dat_mat_components/Bias/value",
                ],
                "@units": [
                    "/dat_mat_components/Bias calc/unit",
                    "/dat_mat_components/Bias/unit",
                ],
                "axis_ind": 0,
            },
            "@any_attr": "Actual attr value",
            "any_field1": {
                "raw_path": "@defalut:Any field name",}.
            "any_field2": {
                "raw_path": "/path/in/data/dict",}.
            "grp_name": "temperature1(filter)",
        }
        To get the proper relation please visit:

        args:
        -----
            "parent_path" -> Parent path for NXdata group in nexus tree.
            "0" -> Index of the axis if "axis_ind" is not provided.
                    Here both are same. Name of the axis is denoted
                    by the name key.
            "title" -> Title of the main plot.
            "grp_name" -> Name of the NXdata group.
            is_forward -> Direction of the scan. Default is True.

        return:
        -------
            str: Name of the NXdata group.

        """
        grp_name_to_embed = partial_conf_dict.get("grp_name", f"data_{group_index}")
        if "grp_name" in partial_conf_dict:
            del partial_conf_dict["grp_name"]

        grp_name_to_embed_fit = grp_name_to_embed.replace(" ", "_").lower()
        nxdata_group = replace_variadic_name_part(group_name, grp_name_to_embed_fit)
        dt_path = f"{parent_path}/{nxdata_group}"
        data_dict = partial_conf_dict.get("data")
        data_fld_nm = data_dict.pop("name", "")
        fld_arr, d_unit, d_others = _get_data_unit_and_others(
            self.raw_data, end_dict=data_dict
        )
        if not isinstance(fld_arr, np.ndarray):
            return
        nxdata_axes = []
        nxdata_indices = []
        axdata_unit_other_list = []
        # Handle axes
        for key, val in partial_conf_dict.items():
            if key == "data":  # handled above
                continue
            if isinstance(val, dict):
                try:
                    index = int(key)
                except ValueError:
                    continue
                ax_nm = val.pop("name", "")
                ax_ind = val.pop("axis_ind", index)
                axdata_unit_other = _get_data_unit_and_others(
                    self.raw_data, end_dict=val
                )
                if isinstance(axdata_unit_other[0], np.ndarray):
                    nxdata_axes.append(ax_nm)
                    nxdata_indices.append(ax_ind)
                    axdata_unit_other_list.append(axdata_unit_other)

        # DATA field
        field_nm_fit = data_fld_nm.replace(" ", "_").lower()
        field_nm_variadic = f"DATA[{field_nm_fit}]"
        self.template[f"{dt_path}/title"] = f"Title Data Group {group_index}"
        if rearrange_2d_data and isinstance(fld_arr, np.ndarray) and fld_arr.ndim == 2:
            fld_arr = self.rearrange_data_according_to_axes(
                fld_arr, is_forward=is_forward
            )
        self.template[f"{dt_path}/{field_nm_variadic}"] = fld_arr
        self.template[f"{dt_path}/{field_nm_variadic}/@units"] = d_unit
        self.template[f"{dt_path}/{field_nm_variadic}/@long_name"] = (
            f"{data_fld_nm} ({d_unit})"
        )
        self.template[f"{dt_path}/@signal"] = field_nm_fit
        if d_others:
            for k, v in d_others.items():
                k = k.replace(" ", "_").lower()
                k = k[1:] if k.startswith("@") else k
                self.template[f"{dt_path}/{field_nm_variadic}/@{k}"] = v
        if not (len(nxdata_axes) == len(nxdata_indices) == len(axdata_unit_other_list)):
            return

        for ind, (index, axis) in enumerate(zip(nxdata_indices, nxdata_axes)):
            axis_fit = axis.replace(" ", "_").lower()
            axis_variadic = f"AXISNAME[{axis_fit}]"
            self.template[f"{dt_path}/@AXISNAME_indices[{axis_fit}_indices]"] = index
            self.template[f"{dt_path}/{axis_variadic}"] = axdata_unit_other_list[ind][0]
            unit = axdata_unit_other_list[ind][1]
            self.template[f"{dt_path}/{axis_variadic}/@units"] = unit
            self.template[f"{dt_path}/{axis_variadic}/@long_name"] = f"{axis} ({unit})"
            if axdata_unit_other_list[ind][2]:  # Other attributes
                for k, v in axdata_unit_other_list[ind][2].items():
                    k = k if k.startswith("@") else f"@{k}"
                    self.template[f"{dt_path}/{axis_variadic}/{k}"] = v

        self.template[f"{dt_path}/@axes"] = [
            ax.replace(" ", "_").lower() for ax in nxdata_axes
        ]
        # Read grp attributes from config file
        for key, val in partial_conf_dict.items():
            if key in ("grp_name",) or isinstance(val, dict) or key.startswith("#"):
                continue
            elif key.startswith("@"):
                self.template[f"{dt_path}/{key}"] = val
            # NXdata field, this part is not needed.
            elif isinstance(val, dict):
                data, unit_, other_attrs = _get_data_unit_and_others(
                    data_dict=self.raw_data, end_dict=val
                )
                self.template[f"{dt_path}/{key}"] = data
                if unit_:
                    self.template[f"{dt_path}/{key}/@units"] = unit_
                    if other_attrs:
                        self.template[f"{dt_path}/{key}/@{other_attrs}"] = other_attrs

        return nxdata_group

    def _handle_special_fields(self):
        """Handle special fields.

        Further curation the  special fields in template
        after the template is already populated with data.
        """
        field_to_type = {
            r"active_channel$": str,
            r"model/@version$": str,
            r"/model$": str,
            r"lockin_amplifier/(demodulated|modulation)_signal$": lambda input: input.lower(),
            r"lockin_amplifier/(hp|lp){1,}_filter_orderN\[\1_filter_order_[\w]*\]$": (
                lambda input: input if isinstance(input, (int, float)) else ""
            ),
        }

        def _format_datetime(parent_path, fld_key, fld_data):
            """Format start time"""

            # "day.month.year hour:minute:second" -> "day-month-year hour:minute:second"
            re_pattern = re.compile(
                r"(\d{1,2})\.(\d{1,2})\.(\d{4}) (\d{1,2}:\d{1,2}:\d{1,2})"
            )

            if not isinstance(fld_data, str):
                return
            match = re_pattern.match(fld_data.strip())

            if match:
                date_time_format = "%d-%m-%Y %H:%M:%S"
                # Convert to "day-month-year hour:minute:second" format
                date_str = datetime.datetime.strptime(
                    f"{match.group(1)}-{match.group(2)}-{match.group(3)} {match.group(4)}",
                    date_time_format,
                ).isoformat()
                self.template[f"{parent_path}/{fld_key}"] = date_str

            else:
                try:
                    datetime.datetime.fromisoformat(fld_data)
                except ValueError:
                    pass
                else:
                    self.template[f"{parent_path}/{fld_key}"] = fld_data

        for key, val in self.template.items():
            if key.endswith("start_time"):
                parent_path, key = key.rsplit("/", 1)
                _format_datetime(parent_path, key, val)
            elif key.endswith("end_time"):
                parent_path, key = key.rsplit("/", 1)
                _format_datetime(parent_path, key, val)

        for template_key, val in self.template.items():
            if m := re.search(pattern=r"(\w*date|time)$", string=template_key):
                try:
                    t_with_zone = add_local_timezone(val)
                    self.template[template_key] = t_with_zone
                except Exception:
                    # Only consider the time or date that follows ISO 8601
                    # or convertable with it
                    pass
            for key, typ in field_to_type.items():
                if re.search(pattern=rf"{key}", string=template_key):
                    self.template[template_key] = typ(val)

    def template_data_units_and_others(
        self,
        end_conf_dct: dict,
        parent_path: str,
        concept_key: str,
        part_to_embed: Optional[str],
    ):
        """
        Puts the data, unit, and other attributes into the template
        """
        data, unit, other_attrs = _get_data_unit_and_others(
            data_dict=self.raw_data, end_dict=end_conf_dct
        )
        if not isinstance(data, np.ndarray) and data in ["", None]:
            return
        temp_key = f"{parent_path}/{replace_variadic_name_part(concept_key, part_to_embed=part_to_embed)}"
        self.template[temp_key] = to_intended_t(data)
        self.template[f"{temp_key}/@units"] = unit
        if other_attrs:
            for k, v in other_attrs.items():
                self.template[f"{temp_key}/@{k}"] = v

    def put_scan_2d_region_field_in_template(self, parent_path, group_name):
        """Puts the scan region fields into the template"""
        self.template[f"{parent_path}/{group_name}/scan_start_x"] = (
            self.NXScanControl.x_start
        )
        self.template[f"{parent_path}/{group_name}/scan_start_x/@units"] = (
            self.NXScanControl.x_start_unit
        )
        self.template[f"{parent_path}/{group_name}/scan_start_y"] = (
            self.NXScanControl.y_start
        )
        self.template[f"{parent_path}/{group_name}/scan_start_y/@units"] = (
            self.NXScanControl.y_start_unit
        )
        self.template[f"{parent_path}/{group_name}/scan_end_x"] = (
            self.NXScanControl.x_end
        )
        self.template[f"{parent_path}/{group_name}/scan_end_x/@units"] = (
            self.NXScanControl.x_end_unit
        )
        self.template[f"{parent_path}/{group_name}/scan_end_y"] = (
            self.NXScanControl.y_end
        )
        self.template[f"{parent_path}/{group_name}/scan_end_y/@units"] = (
            self.NXScanControl.y_end_unit
        )
        self.template[f"{parent_path}/{group_name}/scan_range_x"] = (
            self.NXScanControl.x_range
        )
        self.template[f"{parent_path}/{group_name}/scan_range_x/@units"] = (
            self.NXScanControl.x_range_unit
        )
        self.template[f"{parent_path}/{group_name}/scan_range_y"] = (
            self.NXScanControl.y_range
        )
        self.template[f"{parent_path}/{group_name}/scan_range_y/@units"] = (
            self.NXScanControl.y_range_unit
        )
        self.template[f"{parent_path}/{group_name}/scan_offset_value_x"] = (
            self.NXScanControl.x_offset
        )
        self.template[f"{parent_path}/{group_name}/scan_offset_value_x/@units"] = (
            self.NXScanControl.x_offset_unit
        )
        self.template[f"{parent_path}/{group_name}/scan_offset_value_y"] = (
            self.NXScanControl.y_offset
        )
        self.template[f"{parent_path}/{group_name}/scan_offset_value_y/@units"] = (
            self.NXScanControl.y_offset_unit
        )
