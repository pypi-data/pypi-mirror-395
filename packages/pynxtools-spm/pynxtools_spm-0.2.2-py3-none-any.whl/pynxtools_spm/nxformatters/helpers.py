"""Helpers for nxformatters."""

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
import json
import logging
import re
import zoneinfo
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Tuple, Union, Type

import numpy as np
import tzlocal
from findiff import Diff
from pynxtools.units import ureg

#  try to create a common logger for all the modules
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s - %(message)s")

_SCIENTIFIC_NUM_PATTERN = r"[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?"


def add_local_timezone(ts: str, tz: Optional[str] = None) -> str:
    """
    Add a timezone to a timestamp if it has none.

    Parameters
    ----------
    ts : str
        Input timestamp string.
    tz : str | None
        Optional timezone name (e.g. "Europe/Berlin").
        If None, the system local timezone will be used.

    Returns
    -------
    str
        ISO8601 timestamp string. If input is invalid, returns `ts` unchanged.
    """
    # Already has timezone? -> return unchanged
    if re.search(r"(Z|[+-]\d{2}:\d{2})$", ts):
        return ts

    # Try parsing the timestamp safely
    try:
        dt = datetime.fromisoformat(ts)
    except ValueError:
        # Invalid input -> return as-is
        return ts

    # Use provided timezone or system local
    if tz:
        try:
            tzinfo = zoneinfo.ZoneInfo(tz)
        except Exception:
            # Invalid tz string -> fallback to local
            tzinfo = tzlocal.get_localzone()
    else:
        tzinfo = tzlocal.get_localzone()

    # Attach timezone
    dt = dt.replace(tzinfo=tzinfo)
    return dt.isoformat()


def read_config_file(config_file: Union[str, Path]) -> Dict:
    """Read the config file and return the dictionary.

    Parameters
    ----------
    config_file : str
        The path to the config file.

    Returns
    -------
    Dict
        The dictionary from the config file.
    """
    if isinstance(config_file, Path):
        config_file = str(config_file.absolute())

    if config_file.endswith("json"):
        with open(config_file, mode="r", encoding="utf-8") as f_obj:
            config_dict = json.load(f_obj)
        return config_dict
    else:
        raise ValueError("The config file should be in JSON format.")


def _verify_unit(
    base_key=None, conf_dict=None, data_dict=None, unit=None, concept=None
):
    unit_derived = None
    if unit is not None:
        unit_derived = unit
    elif base_key:
        unit_or_path = conf_dict[f"{base_key}/@units"]
        if unit_or_path.starswith("@default:"):
            unit_derived = unit_or_path.split("@default:")[-1]
        else:
            unit_derived = (
                data_dict.get(unit_or_path, None)
                if isinstance(data_dict, dict)
                else None
            )
    try:
        unit_derived = str(ureg(unit_derived).units)
        return unit_derived
    except Exception as e:
        # TODO: add nomad logger here
        logger.debug("Check the unit for nx concept %s.\nError : %s", concept, e)
        return None


def _get_data_unit_and_others(
    data_dict: dict,
    partial_conf_dict: dict = None,
    concept_field: str = None,
    end_dict: dict = None,
    func_on_raw_key: Callable = lambda x: x,
) -> Tuple[Any, str, Optional[dict]]:
    """Destructure the raw data, units, and other attrs.

    TODO: write doc test for this function

    Parameters:
    -----------
        data_dict : Dict[str, Any]
            The data dict that comes from the raw file. A partial example of data dict

            example:
            data_dict = {
              /SCAN/TIME" :              1.792E-1             1.792E-1
              /SCAN/RANGE :            4.000000E-9           4.000000E-9
              /SCAN/OFFSET :              -2.583985E-7         1.223062E-7
              /SCAN/ANGLE :             0.000E+0
              /SCAN/DIR : down
            }

        partial_conf_dict : Dict[str, Any]
            The dict is a map from nx concept field (or group especially for NXdata)
            to dict which explains raw data path, units, and other attributes (
            if exists).

            example for grp "scan_region"
            partial_conf_dict ={
                "scan_angle_N[scan_angle_n]": {
                    "raw_path": "/SCAN/ANGLE",
                    "@units": "@default:deg"
                },
                "scan_offset_N[scan_offset_n]": {
                    "raw_path": "/SCAN/OFFSET",
                },
                "scan_range_N[scan_range_n]": {
                    "raw_path": "/SCAN/RANGE",
                    "@units": "/path/to/unit/in/raw/file",
                    "@example_attr": "test_attr",
                }
            },
        concept_field : str
            The name of the concept field which is a key in partial_conf_dict

            example: scan_angle_N[scan_angle_n]
        end_dict : Dict[str, Any]
            Tail dictionary of the config file. With this parameter the function does
            not need any concept_field.
            {
                "raw_path": "/SCAN/ANGLE",
                "@units": "@default:deg"
            },
        func_on_raw_key : callable
            Function to apply on raw keywith one input parameter.
            If there any modification is need on the raw key, this function can be used.

            For example:
                In omicron stm file the scans current and topography, scan region could be differ.
                A raw key example is `/Topography_forward/...` is slightly different
                for current scan as `/current_forward/...`. A single function (probably
                lambda function) is sufficient to modify this.

    Returns:
    --------
        tuple :
            The tuple contains components like raw data string, unit string, and dict that
            contains other attributes (if any attributes comes as a part of value dict).
    """

    def get_data_modified_key(key):
        if not key:
            return None
        if isinstance(func_on_raw_key, Callable):
            data = data_dict.get(func_on_raw_key(key), None)
        else:
            data = data_dict.get(key, None)
        return to_intended_t(data)

    if end_dict in [None, ""] and isinstance(partial_conf_dict, dict):
        end_dict = partial_conf_dict.get(concept_field, "")

    if not end_dict:
        return "", "", None

    raw_path = end_dict.get("raw_path", "")

    # if raw_path have multiple possibel path to the raw data
    if isinstance(raw_path, list):
        for path in raw_path:
            raw_data = get_data_modified_key(path)
            if isinstance(raw_data, np.ndarray) or raw_data not in ["", None]:
                break
    elif raw_path.startswith("@default:"):
        raw_data = raw_path.split("@default:")[-1]
    else:
        raw_data = get_data_modified_key(raw_path)
    unit_path = end_dict.get("@units", None)

    try:
        val_copy = deepcopy(end_dict)
        del val_copy["raw_path"]
        del val_copy["@units"]
    except KeyError:
        pass

    if unit_path and isinstance(unit_path, list):
        for unit_item in unit_path:
            unit = get_data_modified_key(unit_item)
            if unit is not None:
                break
    elif unit_path and unit_path.startswith("@default:"):
        unit = unit_path.split("@default:")[-1]
    else:
        unit = get_data_modified_key(unit_path)
    if unit is None or unit == "":
        return to_intended_t(raw_data), "", val_copy
    return to_intended_t(raw_data), _verify_unit(unit=unit), val_copy


def get_actual_from_variadic_name(name: str) -> str:
    """Get the actual name from the variadic name.

    Parameters
    ----------
    name : str
        The variadic name e.g. scan_angle_N_X[scan_angle_n_x]

    Returns
    -------
    str
        The actual name.
    """
    return name.split("[")[-1].split("]")[0]


def flatten_nested_list(list_dt: Union[list, tuple, Any]):
    """Flatten a nested list or tuple."""
    for elem in list_dt:
        if isinstance(elem, (list, tuple)):
            yield from flatten_nested_list(elem)
        else:
            yield elem


# pylint: disable=too-many-return-statements
def to_intended_t(
    data: Any,
    data_type: Optional[Union[str, Callable[[Any], Any]]] = None,
):
    """
        Transform string to the intended data type, if not then return data.
    e.g '2.5E-2' will be transfor into 2.5E-2
    tested with: '2.4E-23', '28', '45.98', 'test', ['59', '3.00005', '498E-34'], None
    with result: 2.4e-23, 28, 45.98, test, [5.90000e+01 3.00005e+00 4.98000e-32], None

    Parameters
    ----------
    data : Any
        The data to be converted.
    data_type : Optional[Union[str, Callable]]
        The intended data type. It can be 'list', 'ndarray', 'int', 'float', 'str'
        or the callable function like int, float, str, np.ndarray
        If None, the function will try to convert to int or float if possible.

    Returns
    -------
    Union[str, int, float, np.ndarray]
        Converted data type
    """
    data_struct_map = {
        "list": list,
        "ndarray": np.ndarray,
        "int": int,
        "float": float,
        "str": str,
    }

    cnv_dtype: Optional[Union[Type, Callable[[Any], Any]]] = None
    if isinstance(data_type, str):
        cnv_dtype = data_struct_map.get(data_type)
    else:
        cnv_dtype = data_type

    def _array_from(data, dtype=None):
        try:
            transformed = np.array(
                data,
                dtype=np.dtype(dtype)
                if isinstance(dtype, str) and dtype in np.sctypeDict
                else np.float64,
            )
            return transformed
        except ValueError as e:
            if np.all(
                map(lambda x: isinstance(x, str), flatten_nested_list(data))
            ) and np.any(map(lambda x: x.isalpha(), flatten_nested_list(data))):
                pass
            else:
                print(
                    f"Warning: Data '{data}' can not be converted to an array"
                    f"and encounterd error {e}"
                )
        return data

    def _array_from_str(data):
        if data.startswith("[") and data.endswith("]"):
            transformed = json.loads(data)
            return transformed
        return data

    symbol_list_for_data_seperation = [";"]
    transformed: Optional[Any]
    if data is None:
        return data

    if isinstance(data, list):
        return _array_from(data, dtype=cnv_dtype)

    if isinstance(data, np.ndarray):
        return data

    if isinstance(data, str):
        off_on = {
            "off": "false",
            "on": "true",
            "OFF": "false",
            "ON": "true",
            "Off": "false",
            "On": "true",
        }
        inf_nan = (
            "infinitiy",
            "-infinity",
            "Infinity",
            "-Infinity",
            "INFINITY",
            "-INFINITY",
            "inf",
            "-inf",
            "Inf",
            "-Inf",
            "INF",
            "-INF",
            "NaN",
            "nan",
        )
        if data in inf_nan:
            return None
        elif data in off_on:
            return off_on[data]

        try:
            transformed = int(data) if cnv_dtype is None else cnv_dtype(data)
            return transformed
        except ValueError:
            try:
                transformed = float(data) if cnv_dtype is None else cnv_dtype(data)
                return transformed
            except ValueError:
                if "[" in data and "]" in data:
                    return _array_from_str(data)

        for sym in symbol_list_for_data_seperation:
            if sym in data:
                parts = data.split(sym)
                modified_parts = []
                for part in parts:
                    modified_parts.append(to_intended_t(part))
                if any(isinstance(part, str) for part in modified_parts):
                    return data
                return modified_parts

    return data


def get_link_compatible_key(key):
    """A unction to convert the key to compatible hdf5 link."""
    # TODO use regrex pattern to match the key
    # # DO not know why this pattern does not work
    # pattern = r"\[([^\]]+)\]"
    # Convert the key to compatible key for template
    compatible_key = key.replace("NX", "")
    key_parts = compatible_key.split("/")
    new_parts = []
    for part in key_parts[1:]:
        key = part
        ind_f = part.find("[")
        ind_e = part.find("]")
        if ind_f > 0 and ind_e > 0:
            key = part[ind_f + 1 : ind_e]
        new_parts.append(key)

    compatible_key = "/" + "/".join(new_parts)
    return compatible_key


def replace_variadic_name_part(name: str, part_to_embed: Optional[str] = None) -> str:
    """Replace the variadic part of the name with the part_to_embed.
    e.g. name = "scan_angle_N_X[scan_angle_n_x]", part_to_embed = "xy"
    then the output will be "scan_angle_xy"
    """
    if not part_to_embed:
        return name
    if not part_to_embed.startswith("_"):
        part_to_embed = "_" + part_to_embed
    f_part, _ = name.split("[") if "[" in name else (name, "")
    ind_start = None
    ind_end = None
    for ind, chr_ in enumerate(f_part):
        if chr_.isupper():
            if ind_start is None:
                ind_start = ind
        if ind_start is not None and chr_.islower():
            ind_end = ind
            break
    if ind_start == 0 and ind_end is not None:
        part_to_embed = part_to_embed[1:]  # remove the first underscore
        end_part = f_part[ind_end:]
        if end_part.startswith("_"):
            if part_to_embed.endswith("_"):
                part_to_embed = part_to_embed[0:-1]
        else:
            if not part_to_embed.endswith("_"):
                part_to_embed = part_to_embed + "_"
        f_part_mod = f_part.replace(f_part[ind_start:ind_end], part_to_embed)
        return "[".join([f_part, f_part_mod]) + "]"
    elif ind_end is None and ind_start is not None:
        start_part = f_part[0:ind_start]
        if start_part and start_part.endswith("_") and part_to_embed.startswith("_"):
            part_to_embed = part_to_embed[1:]
        elif not start_part and part_to_embed.startswith("_"):
            part_to_embed = part_to_embed[1:]
        f_part_mod = f_part.replace(f_part[ind_start:], part_to_embed)
        return "[".join([f_part, f_part_mod]) + "]"
    elif ind_end is not None and ind_start is not None:
        replacement_p = f_part[ind_start:ind_end]
        remainpart = f_part[0:ind_start]
        if remainpart.endswith("_") and part_to_embed.startswith("_"):
            part_to_embed = part_to_embed[1:]
        # if replacement_p end with '_'
        if replacement_p.endswith("_"):
            replacement_p = replacement_p[:-1]
        f_part_mod = f_part.replace(replacement_p, part_to_embed)
        return "[".join([f_part, f_part_mod]) + "]"
    else:
        return name


def cal_dy_by_dx(y_val: np.ndarray, x_val: np.ndarray) -> np.ndarray:
    """Calc conductance (dI/dV) or gradiant dx/dy for x-variable and y-variable also return the result."""
    d_dx = Diff(axis=0, grid=x_val, acc=2)
    return d_dx(y_val)


def transfer_plain_template_to_nested_dict(template, nested_dict):
    """TODO: Write a doc compatibel with doc test write test in pytest."""

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
