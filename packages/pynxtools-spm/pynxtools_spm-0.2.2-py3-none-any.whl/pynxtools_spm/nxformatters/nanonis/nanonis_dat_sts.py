#!/usr/bin/env python3
"""
A formatter that formats the STS (Scanning Tunneling Spectroscopy) experiment's raw data
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

from typing import Any, Dict, Union, Optional
from dataclasses import dataclass
from pathlib import Path
from pint import UnitRegistry
import numpy as np
from pynxtools.dataconverter.template import Template
from pynxtools_spm.configs import load_default_config
import pynxtools_spm.nxformatters.helpers as fhs
from pynxtools_spm.nxformatters.helpers import (
    _get_data_unit_and_others,
)
from pynxtools_spm.nxformatters.base_formatter import (
    PINT_QUANTITY_MAPPING,
)
from pynxtools_spm.nxformatters.nanonis.nanonis_base import NanonisBase
from pynxtools_spm.nxformatters.helpers import (
    cal_dy_by_dx,
    get_actual_from_variadic_name,
)

ureg: UnitRegistry = UnitRegistry()


class NanonisDatSTS(NanonisBase):
    """Formatter for Nanonis STS data with .dat extension"""

    _grp_to_func = {
        "BIAS_SWEEP[bias_sweep]": "_construct_bias_sweep_grp",
    }
    _axes = ["x", "y", "z"]
    links_to_concepts: Dict[str, Any] = {}

    @dataclass
    class TmpConceptsVal:
        """Temporary storage for concept values to use later"""

        flip_number: int = None

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
        raw_file: str | Path,
        eln_file: str | Path,
        config_file: Optional[Union[str, Path]] = None,
        entry: Optional[str] = None,
    ):
        super().__init__(template, raw_file, eln_file, config_file, entry)

    def _get_conf_dict(self, config_file: str | Path = None):
        if config_file:
            return fhs.read_config_file(config_file)
        return load_default_config("nanonis_dat_generic_sts")

    def get_nxformatted_template(self):
        self.walk_though_config_nested_dict(self.config_dict, "")
        self._format_template_from_eln()
        self._handle_special_fields()

    def _construct_nxscan_controllers(
        self,
        partial_conf_dict,
        parent_path: str,
        group_name="scan_control",
        **kwarg,
    ):
        pass

    def _construct_linear_sweep_grp(self, partial_conf_dict, parent_path, group_name):
        """Constructs the linear_sweep group under the group tree
        BIAS_SPECTROSCOPY[bias_spectroscopy]:
            bias_seep:
                linear_sweep: {...}
        """
        scan_points = "scan_points_bias"
        step_size = "step_size_bias"
        copy_partial_conf_dict = partial_conf_dict.copy()
        for key, _ in partial_conf_dict.items():
            if scan_points == key:
                data, _, _ = _get_data_unit_and_others(
                    data_dict=self.raw_data,
                    partial_conf_dict=partial_conf_dict,
                    concept_field=scan_points,
                )
                self.template[f"{parent_path}/{group_name}/{scan_points}"] = data
                self.BiasSweep.scan_points_bias = data
                del copy_partial_conf_dict[key]
        self.BiasSweep.scan_size_bias = (
            self.BiasSweep.scan_end_bias - self.BiasSweep.scan_start_bias
        ) / self.BiasSweep.scan_points_bias
        self.BiasSweep.scan_size_bias_unit = self.BiasSweep.scan_end_bias_unit

        self.template[f"{parent_path}/{group_name}/{step_size}"] = (
            self.BiasSweep.scan_size_bias
        )
        self.template[f"{parent_path}/{group_name}/{step_size}/@units"] = (
            self.BiasSweep.scan_size_bias_unit
        )
        self.walk_though_config_nested_dict(
            config_dict=copy_partial_conf_dict,
            parent_path=f"{parent_path}/{group_name}",
        )

    def _construct_scan_region_grp_in_bias_spec(
        self, partial_conf_dict, parent_path, group_name
    ):
        """Constructs the scan_region group under the group tree
        SPM_BIAS_SPECTROSCOPY[bias_spectroscopy]:
            BIAS_SWEEP[bias_sweep]:
                scan_region: {...}
        """
        bias_start = "scan_start_bias"
        bias_end = "scan_end_bias"
        partial_conf_dict_copy = partial_conf_dict.copy()
        for key, _ in partial_conf_dict.items():
            if bias_start == key:
                data, unit, _ = _get_data_unit_and_others(
                    data_dict=self.raw_data,
                    partial_conf_dict=partial_conf_dict,
                    concept_field=bias_start,
                )
                self.template[f"{parent_path}/{group_name}/{bias_start}"] = data
                self.template[f"{parent_path}/{group_name}/{bias_start}/@units"] = unit
                self.BiasSweep.scan_start_bias = data
                self.BiasSweep.scan_start_bias_unit = unit
                del partial_conf_dict_copy[key]
            elif bias_end == key:
                data, unit, _ = _get_data_unit_and_others(
                    data_dict=self.raw_data,
                    partial_conf_dict=partial_conf_dict,
                    concept_field=bias_end,
                )
                self.template[f"{parent_path}/{group_name}/{bias_end}"] = data
                self.template[f"{parent_path}/{group_name}/{bias_end}/@units"] = unit
                self.BiasSweep.scan_end_bias = data
                self.BiasSweep.scan_end_bias_unit = unit
                del partial_conf_dict_copy[key]
        self.walk_though_config_nested_dict(
            config_dict=partial_conf_dict_copy,
            parent_path=f"{parent_path}/{group_name}",
        )

    def _construct_bias_sweep_grp(self, partial_conf_dict, parent_path, group_name):
        """Constructs the bias_sweep group under the group tree
        BIAS_SPECTROSCOPY[bias_spectroscopy]:
            BIAS_SWEEP[bias_sweep]: {...}
        """
        scan_region = "scan_region"
        linear_sweep = "linear_sweep"
        scan_region_dict = partial_conf_dict.get(scan_region, None)
        if not scan_region_dict:
            return
        self._construct_scan_region_grp_in_bias_spec(
            partial_conf_dict=scan_region_dict,
            parent_path=f"{parent_path}/{group_name}",
            group_name=scan_region,
        )
        linear_sweep_dict = partial_conf_dict.get(linear_sweep, None)
        if not linear_sweep_dict:
            return
        self._construct_linear_sweep_grp(
            partial_conf_dict=linear_sweep_dict,
            parent_path=f"{parent_path}/{group_name}",
            group_name=linear_sweep,
        )

    def _construct_di_dv_grp(self, iv_dict, parent_path, group_name):
        """Constructs the dI/dV group under the group tree"""
        try:
            di_by_dv = cal_dy_by_dx(iv_dict["current_fld"], iv_dict["voltage_fld"])
        except (KeyError, ValueError, ZeroDivisionError):
            return

        if not (
            np.shape(di_by_dv)
            == np.shape(iv_dict["voltage_fld"])
            == np.shape(iv_dict["current_fld"])
        ):
            return
        fld_nm = "dI_by_dV"
        self.template[f"{parent_path}/{group_name}/DATA[{fld_nm}]"] = di_by_dv
        self.template[f"{parent_path}/{group_name}/DATA[{fld_nm}]/@units"] = str(
            ureg(iv_dict["current_unit"] + "/" + iv_dict["voltage_unit"]).units
        )

        self.template[f"{parent_path}/{group_name}/@signal"] = fld_nm
        axis = iv_dict["voltage_fld_name"]
        self.template[f"{parent_path}/{group_name}/@axes"] = [axis]
        self.template[
            f"{parent_path}/{group_name}/@AXISNAME_indices[{axis}_indices]"
        ] = 0
        self.template[f"{parent_path}/{group_name}/AXISNAME[{axis}]"] = iv_dict[
            "voltage_fld"
        ]

        self.template[f"{parent_path}/{group_name}/AXISNAME[{axis}]/@units"] = iv_dict[
            "voltage_unit"
        ]
        self.template[f"{parent_path}/{group_name}/title"] = "dI by dV (Conductance)"

    def _nxdata_grp_from_conf_description(
        self,
        partial_conf_dict,
        parent_path,
        group_name,
        group_index=0,
        is_forward=None,
        rearrange_2d_data=True,
    ):
        """Constructs the NXdata group from the configuration description."""
        group_name = super()._nxdata_grp_from_conf_description(
            partial_conf_dict,
            parent_path,
            group_name,
            group_index,
            is_forward,
            rearrange_2d_data,
        )

        if group_name is None:
            return
        curnt_volt = {
            "current_fld": "",
            "current_unit": "",
            "current_fld_name": "",
            "voltage_fld": "",
            "voltage_unit": "",
            "voltage_fld_name": "",
        }
        current_field_to_data = {}
        current = False
        voltage = False
        for key, val in self.template.items():
            # Find out current field
            if key.startswith(parent_path + "/" + group_name):
                if key.endswith("@units"):
                    current = (
                        PINT_QUANTITY_MAPPING.get(str(ureg(val).dimensionality))
                        == "current"
                        or current
                    )
                    if current and not curnt_volt["current_unit"]:
                        curnt_volt["current_unit"] = val
                        curnt_volt["current_fld"] = self.template[key[0:-7]]
                        curnt_volt["current_fld_name"] = get_actual_from_variadic_name(
                            key[0:-7].split("/")[-1]
                        )

                        current_field_to_data[key[0:-7]] = self.template[key[0:-7]]

                    voltage = (
                        PINT_QUANTITY_MAPPING.get(str(ureg(val).dimensionality))
                        == "voltage"
                        or voltage
                    )
                    if voltage and not curnt_volt["voltage_unit"]:
                        curnt_volt["voltage_unit"] = val
                        curnt_volt["voltage_fld"] = self.template[key[0:-7]]
                        curnt_volt["voltage_fld_name"] = get_actual_from_variadic_name(
                            key[0:-7].split("/")[-1]
                        )
        # check if group is current group and calculatre dI/dV
        if current and voltage:
            try:
                # Fix it currently it is unable to get data from eln
                self.TmpConceptsVal.flip_number = (
                    self.TmpConceptsVal.flip_number
                    or next(
                        filter(
                            lambda x: x[0].endswith("flip_sign"),
                            self.eln.items(),
                        )
                    )[1]
                )
            except StopIteration:
                pass
            flip_number = self.TmpConceptsVal.flip_number or 1

            if flip_number is None:
                raise ValueError(
                    "Flip number for lockin current must be suplied via eln."
                )
            if len(current_field_to_data) != 1:
                raise ValueError("Each group can have only one current field.")
            current_field, value = list(current_field_to_data.items())[0]
            self.template[current_field] = flip_number * value
            group_name_grad = (
                f"{group_name[0:-1]}_grad]"
                if group_name[-1] == "]"
                else f"{group_name}_grad"
            )
            self._construct_di_dv_grp(curnt_volt, parent_path, group_name_grad)

        return group_name

    def _handle_special_fields(self):
        """Handle special fields in the template."""
        super()._handle_special_fields()
