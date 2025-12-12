# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Client module for Featureform.

This module contains client classes for interacting with Featureform:
- Client: The main unified client for all Featureform operations (recommended)
- ResourceClient: Legacy client for querying resources (deprecated)
"""

from .resource_client import ResourceClient
from .unified_client import Client

__all__ = ["Client", "ResourceClient"]
