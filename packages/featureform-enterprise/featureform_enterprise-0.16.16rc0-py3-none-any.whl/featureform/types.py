# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Type definitions - Re-exports from core.types for backwards compatibility.

DEPRECATED: Import from featureform.core.types instead.
"""

# Re-export from core.types for backwards compatibility
from .core.types import VectorType, pd_to_ff_datatype, type_from_proto

__all__ = ["VectorType", "pd_to_ff_datatype", "type_from_proto"]
