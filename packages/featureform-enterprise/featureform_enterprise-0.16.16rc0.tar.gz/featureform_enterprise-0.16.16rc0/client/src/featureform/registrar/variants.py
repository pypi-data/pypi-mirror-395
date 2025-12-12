# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Variants class for managing multiple resource variants.

This module contains the Variants class which allows registering multiple
variants of a resource at once.
"""

from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from ..register import ColumnResource


class Variants:
    """
    Container for managing multiple variants of a resource.

    This class allows you to register multiple variants of a feature or label
    at once by providing a dictionary mapping variant names to ColumnResource objects.

    Example:
        ```python
        variants = Variants({
            "v1": feature_v1,
            "v2": feature_v2,
        })
        variants.register()
        ```
    """

    def __init__(self, resources: Dict[str, "ColumnResource"]):
        """
        Initialize Variants with a dictionary of resources.

        Args:
            resources: Dictionary mapping variant names to ColumnResource objects
        """
        self.resources = resources
        self.validate_variant_names()

    def validate_variant_names(self):
        """
        Validate that variant names match the resource variant names.

        Raises:
            ValueError: If a variant key doesn't match the resource's variant name
        """
        for variant_key, resource in self.resources.items():
            if resource.variant == "":
                resource.variant = variant_key
            if resource.variant != variant_key:
                raise ValueError(
                    f"Variant name {variant_key} does not match resource variant name {resource.variant}"
                )

    def register(self):
        """Register all variants."""
        for resource in self.resources.values():
            resource.register()
