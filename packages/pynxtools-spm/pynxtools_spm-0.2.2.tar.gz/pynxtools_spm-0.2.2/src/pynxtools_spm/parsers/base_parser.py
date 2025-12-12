#!/usr/bin/env python
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
import os
from abc import ABC, abstractmethod


class SPMBase(ABC):
    """Base class for all the SPM readers."""

    def __init__(self, file_path) -> None:
        super().__init__()
        if os.path.exists(file_path):
            self.file_path = file_path
        else:
            raise FileNotFoundError(f"File {file_path} not found.")

    @abstractmethod
    def parse(self):
        """Parse the file and return the parsed data."""
        pass
