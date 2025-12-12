# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Cleanup operations for Featureform resources.

This module contains classes and functions for cleaning up resources.
"""

from dataclasses import dataclass
from typing import List, Set, Tuple

from ..enums import ResourceType


@dataclass
class CleanupResult:
    """
    Result of a cleanup operation.

    Attributes:
        deleted_resources: Set of successfully deleted/queued resources as tuples (resource_type, name, variant)
        failed_resources: List of resources that failed to delete as tuples (resource_type, name, variant)
        error_count: Total number of errors encountered
        errors: List of tuples containing (resource_id, error_message)
    """

    deleted_resources: Set[Tuple[ResourceType, str, str]]
    failed_resources: List[Tuple[ResourceType, str, str]]
    error_count: int
    errors: List[Tuple[str, str]]

    @staticmethod
    def empty():
        return CleanupResult(set(), [], 0, [])

    @property
    def success_count(self) -> int:
        """Number of successfully deleted resources."""
        return len(self.deleted_resources)

    @property
    def total_attempted(self) -> int:
        """Total number of resources attempted to delete."""
        return self.success_count + len(self.failed_resources)

    @property
    def has_failures(self) -> bool:
        """Whether any resources failed to delete."""
        return len(self.failed_resources) > 0

    @property
    def is_complete_success(self) -> bool:
        """Whether all resources were successfully deleted."""
        return not self.has_failures

    def get_failed_by_type(self) -> dict:
        """Group failed resources by type."""
        failed_by_type = {}
        for res_type, name, variant in self.failed_resources:
            if res_type not in failed_by_type:
                failed_by_type[res_type] = []
            failed_by_type[res_type].append((name, variant))
        return failed_by_type

    def get_deleted_by_type(self) -> dict:
        """Group deleted resources by type."""
        deleted_by_type = {}
        for res_type, name, variant in self.deleted_resources:
            if res_type not in deleted_by_type:
                deleted_by_type[res_type] = []
            deleted_by_type[res_type].append((name, variant))
        return deleted_by_type
