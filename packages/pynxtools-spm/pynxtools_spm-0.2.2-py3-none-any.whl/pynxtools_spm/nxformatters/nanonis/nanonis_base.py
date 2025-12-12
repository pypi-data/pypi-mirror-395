#!/usr/bin/env python3
"""
Base formatter for Nanonis SPM data.
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
from typing import List, Optional
import numpy as np

from pynxtools_spm.nxformatters.base_formatter import SPMformatter


class NanonisBase(SPMformatter):
    """Base class for Nanonis SPM data formatters."""

    def _arange_axes(self, direction="down"):
        """Arrange fast and slow axes according to the scan direction."""

        fast_slow: List[str]
        if direction.lower() == "down":
            fast_slow = ["-Y", "X"]
        elif direction.lower() == "up":
            fast_slow = ["Y", "X"]
        elif direction.lower() == "right":
            fast_slow = ["X", "Y"]
        elif direction.lower() == "left":
            fast_slow = ["-X", "Y"]
        else:
            fast_slow = ["X", "Y"]
        self.NXScanControl.fast_axis = fast_slow[0].lower()
        self.NXScanControl.slow_axis = fast_slow[1].lower()

        return fast_slow

    def rearrange_data_according_to_axes(self, data, is_forward: Optional[bool] = None):
        """Rearrange array data according to the fast and slow axes.

        (NOTE: This tachnique is proved for NANONIS data only, for others it may
        not work.)
        Parameters
        ----------
        data : np.ndarray
            Two dimensional array data from scan.
        is_forward : bool, optional
            Default scan direction.
        """

        # if NXcontrol is not defined (e.g. for Bias Spectroscopy)
        if not hasattr(self.NXScanControl, "fast_axis") and not hasattr(
            self.NXScanControl, "slow_axis"
        ):
            return data
        fast_axis, slow_axis = (
            self.NXScanControl.fast_axis,
            self.NXScanControl.slow_axis,
        )

        rearraged = None
        if fast_axis == "x":
            if slow_axis == "-y":
                rearraged = np.flipud(data)
            rearraged = data
        elif fast_axis == "-x":
            if slow_axis == "y":
                rearraged = np.fliplr(data)
            elif slow_axis == "-y":
                # np.flip(data)
                np.flip(data)
        elif fast_axis == "-y":
            rearraged = np.flipud(data)
            if slow_axis == "-x":
                rearraged = np.fliplr(rearraged)
        elif fast_axis == "y":
            rearraged = data
            if slow_axis == "-x":
                rearraged = np.fliplr(rearraged)
        else:
            rearraged = data
        # Consider backward scan
        if is_forward is False:
            rearraged = np.fliplr(rearraged)
        return rearraged
