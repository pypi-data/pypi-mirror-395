# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
State management - Re-exports from core.state for backwards compatibility.

DEPRECATED: Import from featureform.core.state instead.
"""

# Re-export from core.state for backwards compatibility
from ..core.state import ResourceRedefinedError, ResourceState

__all__ = [
    "ResourceState",
    "ResourceRedefinedError",
]
