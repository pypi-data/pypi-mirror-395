# Copyright 2025 Subnoto
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

from dataclasses import dataclass
from typing import Optional


@dataclass
class SubnotoConfig:
    """Configuration for the Subnoto API client"""
    
    api_base_url: str
    access_key: str
    secret_key: str
    unattested: bool = False
    attester_key: Optional[bytes] = None


class SubnotoError(Exception):
    """Base exception for Subnoto API client errors"""
    
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)
    
    def __str__(self) -> str:
        if self.status_code:
            return f"SubnotoError({self.status_code}): {self.message}"
        return f"SubnotoError: {self.message}"

