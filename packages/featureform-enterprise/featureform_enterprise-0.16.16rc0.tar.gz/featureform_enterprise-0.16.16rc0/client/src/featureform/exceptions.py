# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Exceptions - Re-exports from core.exceptions for backwards compatibility.

DEPRECATED: Import from featureform.core.exceptions instead.
"""

# Re-export from core.exceptions for backwards compatibility
from .core.exceptions import (
    FeatureformException,
    FeatureNotFound,
    InvalidSQLQuery,
    InvalidTrainingSetFeatureComputationMode,
    LabelNotFound,
)

__all__ = [
    "FeatureformException",
    "FeatureNotFound",
    "LabelNotFound",
    "InvalidSQLQuery",
    "InvalidTrainingSetFeatureComputationMode",
]
