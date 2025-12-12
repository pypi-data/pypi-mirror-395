#!/usr/bin/env python3
"""
Chosses the appropriate parser based on the file extension and the ELN data.
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

from typing import Dict, Union, Callable, Optional, Iterable, Any
from pynxtools_spm.parsers.nanonis_sxm import SxmGenericNanonis
from pynxtools_spm.parsers.nanonis_dat import DatGenericNanonis
from pynxtools_spm.parsers.omicron_sm4 import Sm4Omicron
import pynxtools_spm.parsers.helpers as phs
import logging
from pathlib import Path, PosixPath
import os

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s - %(message)s")


class SPMParser:
    """This class is intended for taking care of vendor's name,
    experiment (stm, sts, afm) and software versions.

    Raises
    ------
    ValueError
        If experiment is not in ['sts', 'stm', 'afm']
    ValueError
        if vendor's name is not in ['nanonis']
    ValueError
        if software version is not in ['Generic 5e', 'Generic 4.5']
    """

    # parser navigate type
    par_nav_t = Dict[str, Union["par_nav_t", Callable]]
    __parser_navigation: Dict[str, par_nav_t] = {
        "sxm": {
            "nanonis": {
                "generic5e": SxmGenericNanonis,
                "generic4.5": SxmGenericNanonis,
                "generic4": SxmGenericNanonis,
                "generic5": SxmGenericNanonis,
            }
        },
        "dat": {
            "nanonis": {
                "generic5e": DatGenericNanonis,
                "generic5": DatGenericNanonis,
                "generic4.5": DatGenericNanonis,
            }
        },
        "sm4": {
            "omicron": {
                "005.0041": Sm4Omicron,
                "5.41": Sm4Omicron,
                "5.4": Sm4Omicron,
            }
        },
    }

    def __get_appropriate_parser(
        self,
        file: Union[str, Path],
        eln: Optional[Dict] = {},
        file_ext: Optional[str] = None,
    ) -> Iterable[Callable]:
        """Search for appropriate prser and pass it the reader.

        Parameters
        ----------
        file : Union[str, Path]
            File path to parse.
        eln : Dict
            User provided eln file (yaml) that must contain all the info about
            experiment, vendor's name and version of the vendor's software.
        file_ext : Optional[str], optional
            File extension (e.g. 'sxm'), by default None
        Returns
        -------
            Return Callable function that has capability to run the correponding parser.
        """
        if file_ext is None:
            if file is None:
                raise ValueError("No file has been provided to parse.")
            else:
                if isinstance(file, PosixPath) and Path.exists(file):
                    file_ext = str(file.absolute()).rsplit(".", 1)[-1]
                elif isinstance(file, str) and os.path.exists(file):
                    file_ext = file.rsplit(".", 1)[-1]
        parser: Optional[Callable] = None
        # experiment_t_key: str = "/ENTRY[entry]/experiment_type"
        # experiment_t: str = eln[experiment_t_key]
        try:
            experiment_dict: SPMParser.par_nav_t = self.__parser_navigation[file_ext]
        except KeyError as exc:
            raise KeyError(
                f"Add correct experiment type in ELN file "
                f" from {list(self.__parser_navigation.keys())}."
            ) from exc

        vendor_key: str = "/ENTRY[entry]/INSTRUMENT[instrument]/software/vendor"
        vendor_n: str = eln.get(vendor_key, None)
        vendor_n = vendor_n.replace(" ", "").lower() if vendor_n else None
        try:
            vendor_dict: SPMParser.par_nav_t = experiment_dict.get(vendor_n, {})  # type: ignore[assignment]
        except (KeyError, ValueError):
            pass

        software_v_key: str = "/ENTRY[entry]/INSTRUMENT[instrument]/software/model"
        software_v: str = eln.get(software_v_key, None)
        software_v = software_v.replace(" ", "").lower() if software_v else None
        try:
            parser = vendor_dict.get(software_v, None)  # type: ignore[assignment]
        except (ValueError, KeyError):
            pass
        # collect all parsers
        if parser is not None:
            return iter([parser])
        else:
            flat_dict: dict[str, Callable] = {}
            phs.nested_path_to_slash_separated_path(experiment_dict, flat_dict)
            return flat_dict.values()

    def get_raw_data_dict(
        self,
        file: Union[str, Path],
        eln: Dict = None,
        file_ext: Optional[str] = None,
    ):
        """Get the raw data from the file."""
        parsers: Iterable[Callable] = self.__get_appropriate_parser(
            file=file, eln=eln or {}, file_ext=file_ext
        )
        raw_data_dict: Optional[Dict[str, Any]] = None
        for parser in parsers:
            try:
                raw_data_dict = parser(file).parse()
            except Exception:
                pass
            if raw_data_dict is not None:
                return raw_data_dict
        raise ValueError(f"No valid parser found to parse the file: {file}")

    def parse(self, file):
        return self.get_raw_data_dict(file)


def get_nanonis_sxm_parsed_data(file_path: str):
    """This function is intended to parse the Nanonis SXM file and return the parsed data.

    Parameters
    ----------
    file_path : str
        The path to the Nanonis SXM file.

    Returns
    -------
    Dict
        The parsed data from the Nanonis SXM file.
    """
    return SPMParser().get_raw_data_dict(file_path)


def write_spm_raw_file_data(raw_file, output_file=None):
    """Parse the raw_file into a dictionary with / as the separator for keywords."""

    base_name = os.path.basename(raw_file)
    raw_name = base_name.split(".", 1)[0]
    data_dict = SPMParser().get_raw_data_dict(raw_file)
    if (
        output_file is not None
        and os.path.exists(str(output_file).rsplit("/", 1)[0])
        and output_file.endswith(".txt")
    ):
        temp_file = output_file
    else:
        temp_file = f"{raw_name}.txt"
    with open(temp_file, mode="w", encoding="utf-8") as txt_f:
        for key, val in data_dict.items():
            txt_f.write(f"{key} : {val}\n")
    logging.info(" %s has been created to investigate raw data structure.", temp_file)


def get_nanonis_dat_parsed_data(file_path: str):
    """This function is intended to parse the Nanonis DAT file and return the parsed data.

    Parameters
    ----------
    file_path : str
        The path to the Nanonis DAT file.

    Returns
    -------
    Dict
        The parsed data from the Nanonis DAT file.
    """
    raise NotImplementedError("This function is not implemented yet.")


def get_bruker_spm_parsed_data(file_path: str):
    """This function is intended to parse the Bruker SPM file and return the parsed data.

    Parameters
    ----------
    file_path : str
        The path to the Bruker SPM file.

    Returns
    -------
    Dict
        The parsed data from the Bruker SPM file.
    """
    raise NotImplementedError("This function is not implemented yet.")


def get_spm_parsed_data(file_path: str):
    """This function is intended to parse the SPM file and return the parsed data.

    Parameters
    ----------
    file_path : str
        The path to the SPM file.

    Returns
    -------
    Dict
        The parsed data from the SPM file.
    """
    raise NotImplementedError("This function is not implemented yet.")
