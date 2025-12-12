# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Helper utility functions for Featureform.

This module contains small utility functions used throughout the codebase.
"""

from typing import List, Optional


def set_tags_properties(tags: Optional[List[str]], properties: Optional[dict]):
    """
    Helper function to set default values for tags and properties.

    Args:
        tags: Optional list of tags
        properties: Optional dictionary of properties

    Returns:
        Tuple of (tags, properties) with defaults applied
    """
    if tags is None:
        tags = []
    if properties is None:
        properties = {}
    return tags, properties


def get_name_variant(query, source_str):
    """
    Extract name and variant from a source string.

    Args:
        query: The SQL query (for error messages)
        source_str: String in format "name.variant" or "name"

    Returns:
        Tuple of (name, variant)

    Raises:
        InvalidSQLQuery: If source_str contains more than one period
    """
    from ..core.exceptions import InvalidSQLQuery

    # Based on the source string, split the name and variant
    name_variant = source_str.split(".")
    if len(name_variant) > 2:
        raise InvalidSQLQuery(
            query, "Source name and variant cannot contain more than one period."
        )
    elif len(name_variant) == 2:
        name = name_variant[0]
        variant = name_variant[1]
    else:
        name = name_variant[0]
        variant = ""

    return name, variant
