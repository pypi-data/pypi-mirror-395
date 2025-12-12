# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Registration module - Re-exports from registrar for backwards compatibility.

DEPRECATED: The registration module has been renamed to registrar.
Import from featureform.registrar instead.

This module exists only for backwards compatibility and will be removed in a future version.
"""

import warnings

# Issue deprecation warning
warnings.warn(
    "The 'registration' module has been renamed to 'registrar'. "
    "Please update your imports to use 'from featureform.registrar import ...' instead. "
    "This compatibility module will be removed in a future version.",
    DeprecationWarning,
    stacklevel=2,
)

# Re-export everything from registrar for backwards compatibility
from .registrar import *  # noqa: F401, F403

__all__ = [
    "EntityRegistrar",
    "UserRegistrar",
    "SourceRegistrar",
    "ColumnSourceRegistrar",
    "ResourceRegistrar",
    "ModelRegistrar",
]
