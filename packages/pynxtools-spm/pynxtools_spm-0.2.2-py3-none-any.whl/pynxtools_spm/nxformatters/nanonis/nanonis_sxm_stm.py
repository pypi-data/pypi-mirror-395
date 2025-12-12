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

from typing import TYPE_CHECKING, Optional, Any, Callable
from pathlib import Path
import re
import datetime
import numpy as np

from pynxtools_spm.nxformatters.nanonis.nanonis_base import NanonisBase
from pynxtools_spm.nxformatters.nanonis.nanonis_dat_sts import NanonisDatSTS
from pynxtools_spm.nxformatters.helpers import (
    _get_data_unit_and_others,
    _SCIENTIFIC_NUM_PATTERN,
    to_intended_t,
)
from pynxtools_spm.configs import load_default_config
import pynxtools_spm.nxformatters.helpers as fhs


if TYPE_CHECKING:
    from pynxtools.dataconverter.template import Template


# TODO: add test to check if user example config file is the same as given default
# config file with this package.
# TODO: Check why link to NXdata does not work
# # Create links for NXdata in entry level
# entry = parent_path.split("/")[1]
# self.template[f"/{entry}/{field_nm}"] = {
#     "link": get_link_compatible_key(f"{parent_path}/{group_name}")
# }


# TODO: Add tests for both config files with described NXdata
# and without described NXdata (for stm and afm)

gbl_scan_ranges: list[float] = []


class NanonisSxmSTM(NanonisBase):
    """Formatter for Nanonis STM data in SXM file format."""

    _grp_to_func = {
        "SPM_SCAN_CONTROL[spm_scan_control]": "_construct_nxscan_controllers",
        "start_time": "_set_start_end_time",
        "end_time": "_set_start_end_time",
        "BIAS_SWEEP[bias_sweep]": "_construct_bias_sweep_grp",
        # "DATA[data]": "construct_scan_data_grps",
    }
    _axes = ["x", "y", "z"]

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
        self.walk_though_config_nested_dict(self.config_dict, "")
        self._format_template_from_eln()
        self._handle_special_fields()

    def _get_conf_dict(self, config_file: str | Path = None):
        if config_file is not None:
            return fhs.read_config_file(config_file)
        else:
            return load_default_config("nanonis_sxm_generic_stm")

    def construct_scan_pattern_grp(
        self,
        partial_conf_dict,
        parent_path: str,
        group_name="scan_mesh",
    ):
        """To construct the scan pattern like scan_mesh, scan_spiral (group) etc."""
        # Scanner speed
        forward_speed_k = "forward_speedN[forward_speed_n]"
        forward_speed, unit, _ = _get_data_unit_and_others(
            data_dict=self.raw_data,
            partial_conf_dict=partial_conf_dict,
            concept_field=forward_speed_k,
        )
        fast_axis = (
            self.NXScanControl.fast_axis[1:]
            if self.NXScanControl.fast_axis.startswith("-")  # -ve direction
            else self.NXScanControl.fast_axis
        )
        # TODO: chech fast_axis contains - sign and remove it
        self.template[
            f"{parent_path}/{group_name}/forward_speedN[forward_speed_{fast_axis}]"
        ] = to_intended_t(forward_speed)
        self.template[
            f"{parent_path}/{group_name}/forward_speedN[forward_speed_{fast_axis}]/@units"
        ] = unit
        backward_speed_k = "backward_speedN[backward_speed_n]"
        backward_speed, unit, _ = _get_data_unit_and_others(
            data_dict=self.raw_data,
            partial_conf_dict=partial_conf_dict,
            concept_field=backward_speed_k,
        )
        self.template[
            f"{parent_path}/{group_name}/backward_speedN[backward_speed_{fast_axis}]"
        ] = to_intended_t(backward_speed)
        self.template[
            f"{parent_path}/{group_name}/backward_speedN[backward_speed_{fast_axis}]/@units"
        ] = unit

        # scan_point fields
        scan_point = "scan_pointsN[scan_points_n]"

        scan_points, unit, _ = _get_data_unit_and_others(
            data_dict=self.raw_data,
            partial_conf_dict=partial_conf_dict,  # dict that contains concept field
            concept_field=scan_point,
        )
        gbl_scan_points = re.findall(_SCIENTIFIC_NUM_PATTERN, scan_points)
        if gbl_scan_points:
            gbl_scan_points = [float(x) for x in gbl_scan_points]
        for ind, point in enumerate(gbl_scan_points):
            self.template[
                f"{parent_path}/{group_name}/scan_pointsN[scan_points_{self._axes[ind]}]"
            ] = point
            if self._axes[ind] == "x":
                self.NXScanControl.x_points = point
            elif self._axes[ind] == "y":
                self.NXScanControl.y_points = point

        # step_size
        if len(gbl_scan_points) == len(gbl_scan_ranges):
            for ind, (rng, pnt) in enumerate(zip(gbl_scan_ranges, gbl_scan_points)):
                stp_s = f"{parent_path}/{group_name}/step_sizeN[step_size_{self._axes[ind]}]"
                self.template[stp_s] = rng / pnt
                self.template[stp_s + "/@units"] = self.NXScanControl.x_range_unit

        # scan_data group
        scan_data = "SCAN_DATA[scan_data]"
        if partial_conf_dict.get(scan_data):
            self.construct_scan_data_grps(
                partial_conf_dict=partial_conf_dict[scan_data],
                parent_path=f"{parent_path}/{group_name}",
                group_name=scan_data,
            )

    def _construct_bias_sweep_grp(
        self, partial_conf_dict, parent_path, group_name="bias_sweep"
    ):
        sts_bias_sweep = getattr(NanonisDatSTS, "_construct_bias_sweep_grp")

        def _construct_scan_region_grp_in_bias_spec(
            self, partial_conf_dict, parent_path, group_name
        ):
            getattr(NanonisDatSTS, "_construct_scan_region_grp_in_bias_spec")(
                self, partial_conf_dict, parent_path, group_name
            )

        NanonisSxmSTM._construct_scan_region_grp_in_bias_spec = (
            _construct_scan_region_grp_in_bias_spec
        )

        def _construct_linear_sweep_grp(
            self, partial_conf_dict, parent_path, group_name
        ):
            getattr(NanonisDatSTS, "_construct_linear_sweep_grp")(
                self, partial_conf_dict, parent_path, group_name
            )

        NanonisSxmSTM._construct_linear_sweep_grp = _construct_linear_sweep_grp

        if isinstance(sts_bias_sweep, Callable):
            sts_bias_sweep(self, partial_conf_dict, parent_path, group_name)

    def construct_scan_region_grp(
        self,
        partial_conf_dict,
        parent_path: str,
        group_name="scan_region",
    ):
        """Constaruct region group from scan_control group sitting in scan_environment group."""
        scan_offset = "scan_offset_valueN[scan_offset_value_n]"

        scan_offsets, unit, _ = _get_data_unit_and_others(
            data_dict=self.raw_data,
            partial_conf_dict=partial_conf_dict,
            concept_field=scan_offset,
        )
        # TODO add a check it scan_start is provided by config dict
        scan_offsets = to_intended_t(re.findall(_SCIENTIFIC_NUM_PATTERN, scan_offsets))
        for ind, offset in enumerate(scan_offsets):
            # off_key = f"{parent_path}/{group_name}/scan_offset_valueN[scan_offset_value_{self._axes[ind]}]"
            # self.template[off_key] = offset
            # self.template[f"{off_key}/@units"] = unit
            if self._axes[ind] == "x":
                self.NXScanControl.x_offset = offset  # type: ignore
                self.NXScanControl.x_offset_unit = unit
                self.NXScanControl.x_start = offset  # type: ignore
                self.NXScanControl.x_start_unit = unit
            elif self._axes[ind] == "y":
                self.NXScanControl.y_offset = offset  # type: ignore
                self.NXScanControl.y_offset_unit = unit
                self.NXScanControl.y_start = offset  # type: ignore
                self.NXScanControl.y_start_unit = unit

        # Scan Angle
        scan_angle = "scan_angleN[scan_angle_n]"

        scan_angles, unit, _ = _get_data_unit_and_others(
            data_dict=self.raw_data,
            partial_conf_dict=partial_conf_dict,
            concept_field=scan_angle,
        )
        if isinstance(scan_angles, str):
            scan_angles = to_intended_t(
                re.findall(_SCIENTIFIC_NUM_PATTERN, scan_angles)
            )
        elif isinstance(scan_angles, (int, float)):
            scan_angles = [scan_angles]
        for ind, angle in enumerate(scan_angles):
            ang_key = (
                f"{parent_path}/{group_name}/scan_angleN[scan_angle_{self._axes[ind]}]"
            )
            self.template[ang_key] = angle
            self.template[f"{ang_key}/@units"] = unit

        # scan range
        scan_range = "scan_rangeN[scan_range_n]"
        scan_ranges, unit, _ = _get_data_unit_and_others(
            data_dict=self.raw_data,
            partial_conf_dict=partial_conf_dict,
            concept_field=scan_range,
        )
        global gbl_scan_ranges
        gbl_scan_ranges = re.findall(_SCIENTIFIC_NUM_PATTERN, scan_ranges)
        if gbl_scan_ranges:
            gbl_scan_ranges = [float(x) for x in gbl_scan_ranges]
        for ind, rng in enumerate(gbl_scan_ranges):
            if self._axes[ind] == "x":
                self.NXScanControl.x_range = rng
                self.NXScanControl.x_range_unit = unit
                if self.NXScanControl.x_start not in (None, ""):
                    self.NXScanControl.x_end = rng + self.NXScanControl.x_start
                    self.NXScanControl.x_end_unit = unit
            elif self._axes[ind] == "y":
                self.NXScanControl.y_range = rng
                self.NXScanControl.y_range_unit = unit
                if self.NXScanControl.y_start not in (None, ""):
                    self.NXScanControl.y_end = rng + self.NXScanControl.y_start
                    self.NXScanControl.y_end_unit = unit

        self.put_scan_2d_region_field_in_template(parent_path, group_name)

    def construct_single_scan_data_grp(self, parent_path, plot_data_info, group_name):
        """Construct single NXdata group for a single scan data."""

        raw_key = plot_data_info["data_path"]
        axes = ["x", "y"]
        field_nm = raw_key[1:].replace("/", "_").lower()
        # Replace group name with field name

        # Group 1 captures the content inside square brackets
        pattern1 = r".*?\[([a-z0-9_]+)\]"

        # Check for Pattern 1 first (find lowercase content inside square brackets)
        match1 = re.search(pattern1, group_name)
        if match1:
            part_to_be_replaced = match1.group(1)
            group_name = group_name.replace(part_to_be_replaced, field_nm)
        self.template[f"{parent_path}/{group_name}/@signal"] = field_nm
        self.template[f"{parent_path}/{group_name}/@axes"] = axes
        title = raw_key[1:].replace("/", " ").upper()
        self.template[f"{parent_path}/{group_name}/title"] = title

        # data field
        f_data = to_intended_t(self.raw_data[raw_key])
        self.template[f"{parent_path}/{group_name}/{field_nm}"] = (
            self.rearrange_data_according_to_axes(f_data)
        )
        self.template[f"{parent_path}/{group_name}/{field_nm}/@units"] = plot_data_info[
            "units"
        ]
        calibration = to_intended_t(plot_data_info.get("calibration", None))
        self.template[f"{parent_path}/{group_name}/{field_nm}/@calibration"] = (
            calibration
        )
        offset = to_intended_t(plot_data_info.get("offset", None))
        self.template[f"{parent_path}/{group_name}/{field_nm}/@offset"] = offset
        # x and y axis
        self.template[f"{parent_path}/{group_name}/x"] = plot_data_info["x_axis"]
        x_unit = plot_data_info["x_units"]
        self.template[f"{parent_path}/{group_name}/x/@units"] = x_unit
        self.template[f"{parent_path}/{group_name}/x/@long_name"] = f"X ({x_unit})"
        self.template[f"{parent_path}/{group_name}/y"] = plot_data_info["y_axis"]
        y_unit = plot_data_info["y_units"]
        self.template[f"{parent_path}/{group_name}/y/@units"] = y_unit
        self.template[f"{parent_path}/{group_name}/y/@long_name"] = f"Y ({y_unit})"

    def construct_scan_data_grps(
        self,
        partial_conf_dict,
        parent_path: str,
        group_name="SCAN_DATA[scan_data]",
    ):
        """Constructs the NXdata groups for all available scan data in raw file
        using single_scan_data_grp function."""

        if isinstance(partial_conf_dict, list):
            # NXdata group will be handled in the general function
            # walk_through_config_nested_dict
            return None
        # create multiple groups for scan_data for multiple scans
        data, _, _ = _get_data_unit_and_others(
            data_dict=self.raw_data,
            end_dict=partial_conf_dict,
        )
        ## Example of data des and info and each column is separated by tab
        # Channel	Name	Unit	Direction	Calibration	Offset
        # 14	Z	m	both	9.000E-9	0.000E+0
        # 0	Current	A	both	1.000E-9	-1.132E-13
        data_headers = [dt.strip().split("\t") for dt in data.split("\n")]

        expected_keys = [
            "Channel",
            "Name",
            "Unit",
            "Direction",
            "Calibration",
            "Offset",
        ]
        plot_data_list: list[dict[str, Any]] = []
        for ind, row in enumerate(data_headers):
            if ind == 0 and expected_keys != row:
                raise ValueError(
                    f"Scan data mismatch: Expected keys {expected_keys} but got {row}"
                )
            if ind > 0 and len(row) == len(expected_keys):
                if row[3] == "both":
                    data_key_f = f"/{row[1]}/forward"
                    data_key_b = f"/{row[1]}/backward"
                    plot_data_list = plot_data_list + (
                        [
                            {
                                "data_path": data_key_f,
                                "units": row[2],
                                "calibration": row[4],
                                "offset": row[5],
                                "x_axis": np.linspace(
                                    self.NXScanControl.x_start,
                                    self.NXScanControl.x_end,
                                    int(self.NXScanControl.x_points),
                                ),
                                "x_units": row[2],
                                "y_axis": np.linspace(
                                    self.NXScanControl.y_start,
                                    self.NXScanControl.y_end,
                                    int(self.NXScanControl.y_points),
                                ),
                                "y_units": row[2],
                            },
                            {
                                "data_path": data_key_b,
                                "units": row[2],
                                "calibration": row[4],
                                "offset": row[5],
                                "x_axis": np.linspace(
                                    self.NXScanControl.x_start,
                                    self.NXScanControl.x_end,
                                    int(self.NXScanControl.x_points),
                                ),
                                "x_units": row[2],
                                "y_axis": np.linspace(
                                    self.NXScanControl.y_start,
                                    self.NXScanControl.y_end,
                                    int(self.NXScanControl.y_points),
                                ),
                                "y_units": row[2],
                            },
                        ]
                    )
                else:
                    data_key = f"/{row[1]}/forward"
                    plot_data_list.append(
                        {
                            "data_path": data_key,
                            "units": row[2],
                            "calibration": row[4],
                            "offset": row[5],
                            "x_axis": np.linspace(
                                self.NXScanControl.x_start,
                                self.NXScanControl.x_end,
                                int(self.NXScanControl.x_points),
                            ),
                            "x_units": row[2],
                            "y_axis": np.linspace(
                                self.NXScanControl.y_start,
                                self.NXScanControl.y_end,
                                int(self.NXScanControl.y_points),
                            ),
                            "y_units": row[2],
                        }
                    )
        for plot_data_info in plot_data_list:
            self.construct_single_scan_data_grp(
                parent_path=parent_path,
                plot_data_info=plot_data_info,
                group_name=group_name,
            )

    def _construct_nxscan_controllers(
        self,
        partial_conf_dict,
        parent_path: str,
        group_name="scan_control",
        **kwargs,
    ):
        """Constructs Scan Control group from the scan environment group.
        Where, scan control group constains scan region and scan pattern groups."""

        # find independent_scan_axes
        # independent_axes = "/ENTRY[entry]/INSTRUMENT[instrument]/SCAN_ENVIRONMENT/SCAN_CONTROL[scan_control]/independent_scan_axes"
        independent_axes = "independent_scan_axes"
        direction, _, _ = _get_data_unit_and_others(
            data_dict=self.raw_data,
            partial_conf_dict=partial_conf_dict,
            concept_field=independent_axes,
        )
        direction = self._arange_axes(direction.strip())
        self.template[f"{parent_path}/{group_name}/independent_scan_axes"] = str(
            direction
        )
        scan_region_grp = "scan_region"
        scan_region_dict = partial_conf_dict.get(scan_region_grp, None)
        # Intended order: construct_scan_region_grp
        if scan_region_dict is not None:
            self.construct_scan_region_grp(
                partial_conf_dict=scan_region_dict,
                parent_path=f"{parent_path}/{group_name}",
                group_name=scan_region_grp,
            )
        scan_pattern_grp = "meshSCAN[mesh_scan]"
        scan_pattern_dict = partial_conf_dict.get(scan_pattern_grp, None)
        if scan_pattern_dict is not None:
            self.construct_scan_pattern_grp(
                partial_conf_dict=scan_pattern_dict,
                parent_path=f"{parent_path}/{group_name}",
                group_name=scan_pattern_grp,
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
        """Specialization of the generic funciton to create NXdata group or plots."""
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
        nxdata_group_nm = super()._nxdata_grp_from_conf_description(
            partial_conf_dict,
            parent_path,
            group_name,
            group_index,
            is_forward=is_forward,
            rearrange_2d_data=rearrange_2d_data,
        )
        if "0" not in partial_conf_dict:
            axis_x = "x"
            axis_y = "y"
            self.template[f"{parent_path}/{nxdata_group_nm}/@axes"] = [axis_y, axis_x]
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

    def _set_start_end_time(self, val_dict, parent_path, field_name):
        """Set start and end time for the scan.

        The start and end time are set in the template
        by collecting data from raw data dict.

        note:
        val_dict Is just following the same convention as other methods
                  hooked in the _grp_to_func dict.
        """
        if "#note" not in val_dict:
            return

        def set_start_time():
            rec_time = self.raw_data.get("/REC/TIME")
            rec_date = self.raw_data.get("/REC/DATE")
            if rec_time and rec_date:
                # Check if data time has "day.month.year hour:minute:second" format
                # if it is then convert it to "day-month-year hour:minute:second"
                re_pattern = re.compile(
                    r"(\d{1,2})\.(\d{1,2})\.(\d{4}) (\d{1,2}:\d{1,2}:\d{1,2})"
                )
                match = re_pattern.match(f"{rec_date.strip()} {rec_time.strip()}")
                if match:
                    date_time_format = "%d-%m-%Y %H:%M:%S"
                    date_str = datetime.datetime.strptime(
                        f"{match.group(1)}-{match.group(2)}-{match.group(3)} {match.group(4)}",
                        date_time_format,
                    ).isoformat()
                    self.template[f"{parent_path}/{field_name}"] = date_str
            elif rec_date:
                re_pattern = re.compile(r"(\d{1,2})\.(\d{1,2})\.(\d{4})")
                match = re_pattern.match(rec_date)
                if match:
                    date_str = f"{match.group(1)}-{match.group(2)}-{match.group(3)}"
                    self.template[f"{parent_path}/{field_name}"] = date_str

        def set_end_time():
            save_time = self.raw_data.get("/REC/TIME")
            save_date = self.raw_data.get("/REC/DATE")
            if not (save_time and save_date):
                return None
            if save_date.count(".") == 2:
                save_date = save_date.replace(".", "-")
            elif not save_date.count("-") == 2:
                return
            date_format = "%d-%m-%Y %H:%M:%S"
            save_datetime = datetime.datetime.strptime(
                f"{save_date.strip()} {save_time.strip()}", date_format
            )

            acq_time = self.raw_data.get("/ACQ/TIME")
            time_delta = (
                datetime.timedelta(seconds=int(float(acq_time)))
                if (save_time is not None and save_date is not None)
                else None
            )
            if not time_delta:
                return None
            end_datetime = save_datetime + time_delta
            if time_delta is None:
                return None

            self.template[f"{parent_path}/{field_name}"] = end_datetime.isoformat()

        if field_name == "start_time":
            set_start_time()
        elif field_name == "end_time":
            # No data observed yet
            set_end_time()
