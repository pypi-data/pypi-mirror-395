# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Validation utilities for Featureform.

This module contains validation functions for URLs, names, and other inputs.
"""

from urllib.parse import urlparse


def is_valid_url(url: str, requires_port: bool = True) -> bool:
    """
    Validate if a string is a valid URL.

    Args:
        url: The URL string to validate
        requires_port: Whether the URL must include a port number

    Returns:
        True if the URL is valid, False otherwise
    """
    try:
        parsed = urlparse(url)

        return all(
            [
                parsed.scheme,
                parsed.hostname,
                parsed.port is not None if requires_port else True,
            ]
        )
    except ValueError:
        # Raised if the URL is invalid
        return False
