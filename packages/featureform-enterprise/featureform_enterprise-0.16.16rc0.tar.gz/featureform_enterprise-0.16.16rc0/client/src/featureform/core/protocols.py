# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Protocol definitions for Featureform resources.

This module defines protocols (structural typing) for resources to enable
duck typing and reduce coupling.
"""

from typing import Protocol, runtime_checkable

from ..enums import OperationType, ResourceType


@runtime_checkable
class HasNameVariant(Protocol):
    """Protocol for resources that have name and variant attributes."""

    name: str
    variant: str


@runtime_checkable
class ResourceProtocol(Protocol):
    """Protocol for all Featureform resources."""

    name: str

    def get_resource_type(self) -> ResourceType:
        """Return the resource type."""
        ...

    def operation_type(self) -> OperationType:
        """Return the operation type (CREATE or GET)."""
        ...


@runtime_checkable
class ResourceVariantProtocol(ResourceProtocol, Protocol):
    """Protocol for resources that have variants."""

    variant: str

    def to_key(self) -> tuple:
        """Return a unique key for this resource variant."""
        ...
