# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Exception classes for Featureform.
"""

from typing import Dict, Optional

from ..enums import ComputationMode
from . import status_codes


class FeatureformException(Exception):
    """
    Base exception class for Featureform errors that preserves error details
    from gRPC responses.

    Attributes:
        reason: The error reason/type (e.g., "Key Not Found", "Internal Error")
        message: The detailed error message
        metadata: Additional key-value metadata from the error
        code: The gRPC status code (see status_codes module)
    """

    def __init__(
        self,
        reason: str,
        message: str,
        metadata: Optional[Dict[str, str]] = None,
        code: Optional[int] = None,
    ):
        self.reason = reason
        self.message = message
        self.metadata = metadata or {}
        self.code = code

        # Format the full error message
        full_message = f"{reason}: {message}"
        if self.metadata:
            metadata_str = "\n".join([f"{k}: {v}" for k, v in self.metadata.items()])
            full_message = f"{full_message}\n{metadata_str}"

        super().__init__(full_message)

    def is_not_found(self) -> bool:
        """Check if this is a NOT_FOUND error based on gRPC status code."""
        return self.code == status_codes.NOT_FOUND


class InvalidTrainingSetFeatureComputationMode(Exception):
    def __init__(
        self,
        feature_name,
        feature_variant,
        mode=ComputationMode.CLIENT_COMPUTED.value,
        message=None,
    ):
        if message is None:
            message = (
                f"Feature '{feature_name}:{feature_variant}' is on demand. "
                f"Cannot use {mode} features for training sets. "
            )

        Exception.__init__(self, message)


class FeatureNotFound(Exception):
    def __init__(self, feature_name, feature_variant, message=None):
        error_message = f"Feature '{feature_name}:{feature_variant}' not found. Verify that the feature is registered."

        if message is not None:
            error_message = f"{error_message} {message}"

        Exception.__init__(self, error_message)


class LabelNotFound(Exception):
    def __init__(self, label_name, label_variant, message=None):
        error_message = f"Label '{label_name}:{label_variant}' not found. Verify that the label is registered."
        if message is not None:
            error_message = f"{error_message} {message}"

        Exception.__init__(self, error_message)


class InvalidSQLQuery(Exception):
    def __init__(self, query, message=None):
        error_message = f"Invalid SQL query. Query: ' {query} '"
        if message is not None:
            error_message = f"{error_message} {message}"

        Exception.__init__(self, error_message)
