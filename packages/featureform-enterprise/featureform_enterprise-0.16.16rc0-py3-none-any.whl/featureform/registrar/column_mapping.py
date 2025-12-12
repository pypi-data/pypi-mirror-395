# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Column mapping for registrar.

This module contains the ColumnMapping class used for defining feature and label columns.
"""

from typing import List, Optional

from ..config.offline_stores import ResourceSnowflakeConfig
from ..enums import ResourceType


class ColumnMapping(dict):
    """
    Dictionary-based class for mapping columns to features or labels.

    Attributes:
        name: Name of the feature or label
        column: Column name in the source
        resource_type: Type of resource (FEATURE or LABEL)
        tags: List of tags
        properties: Dictionary of properties
        variant: Variant name (optional)
        resource_snowflake_config: Snowflake-specific configuration (optional)
    """

    name: str
    column: str
    resource_type: ResourceType
    tags: List[str]
    properties: dict
    variant: str = ""
    resource_snowflake_config: Optional[ResourceSnowflakeConfig] = None
