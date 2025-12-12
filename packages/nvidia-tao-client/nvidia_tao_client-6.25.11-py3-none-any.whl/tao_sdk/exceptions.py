# Copyright (c) 2025, NVIDIA CORPORATION.  All rights reserved.
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

"""TAO SDK exceptions."""


class TaoError(Exception):
    """Base exception for TAO SDK."""
    pass


class TaoAuthenticationError(TaoError):
    """Exception raised for authentication errors."""
    pass


class TaoAPIError(TaoError):
    """Exception raised for API errors."""
    def __init__(self, message: str, status_code: int = None, response_text: str = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_text = response_text


class TaoNotFoundError(TaoAPIError):
    """Exception raised when a resource is not found."""
    pass


class TaoValidationError(TaoError):
    """Exception raised for validation errors."""
    pass
