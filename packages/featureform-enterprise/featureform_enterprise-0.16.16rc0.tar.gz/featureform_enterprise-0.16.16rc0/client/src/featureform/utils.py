# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Utilities - Re-exports from utils package for backwards compatibility.

DEPRECATED: Import from featureform.utils instead.
"""

# Re-export from utils package for backwards compatibility
from .utils import is_valid_url  # noqa: F401

__all__ = ["is_valid_url"]
