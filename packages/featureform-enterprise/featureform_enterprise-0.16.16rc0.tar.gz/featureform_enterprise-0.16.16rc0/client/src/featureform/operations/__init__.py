# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Operations module for Featureform.

This module contains operation-related classes and functions including
cleanup operations and equivalence checking.
"""

from .cleanup import CleanupResult
from .equivalence import _get_and_set_equivalent_variant

__all__ = [
    "CleanupResult",
    "_get_and_set_equivalent_variant",
]
