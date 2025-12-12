# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Providers module for Featureform.

This module contains provider wrapper classes for offline stores, online stores,
file stores, and streaming providers.

USAGE:
------
```python
from featureform.providers import (
    OfflineProvider,
    OfflineSQLProvider,
    OfflineSparkProvider,
    OfflineK8sProvider,
    OnlineProvider,
    FileStoreProvider,
    KafkaProvider,
)
```

MODULE STRUCTURE:
-----------------
- providers/offline.py - OfflineProvider, OfflineSQLProvider, OfflineSparkProvider, OfflineK8sProvider
- providers/online.py - OnlineProvider
- providers/filestore.py - FileStoreProvider
- providers/streaming.py - KafkaProvider
"""

# Import from focused modules
from .filestore import FileStoreProvider
from .offline import (
    OfflineK8sProvider,
    OfflineProvider,
    OfflineSparkProvider,
    OfflineSQLProvider,
)
from .online import OnlineProvider
from .streaming import KafkaProvider

__all__ = [
    "OfflineProvider",
    "OfflineSQLProvider",
    "OfflineSparkProvider",
    "OfflineK8sProvider",
    "KafkaProvider",
    "OnlineProvider",
    "FileStoreProvider",
]
