# Copyright 2025 David CH.F (destroyer)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions
# and limitations under the License.

"""
PyDSK - Python DSK Image Manager for Amstrad CPC
================================================

A Python implementation of DSK image file management for Amstrad CPC.
Compatible with CPCEMU DSK format (standard and extended).

Author: CPCReady
License: GPL
"""

from .dsk import DSK
from .exceptions import (
    DSKError, 
    DSKFormatError, 
    DSKFileNotFoundError,
    DSKFileExistsError,
    DSKNoSpaceError
)

__version__ = "0.1.0"
__all__ = [
    "DSK", 
    "DSKError", 
    "DSKFormatError", 
    "DSKFileNotFoundError",
    "DSKFileExistsError",
    "DSKNoSpaceError"
]
