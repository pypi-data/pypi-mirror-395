# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
File store provider wrapper classes for Featureform.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


__all__ = ["FileStoreProvider"]


class FileStoreProvider:
    def __init__(self, registrar, provider, config, store_type):
        self.__registrar = registrar
        self.__provider = provider
        self.__config = config.config()
        self.__store_type = store_type

    def name(self) -> str:
        return self.__provider.name

    def store_type(self) -> str:
        return self.__store_type

    def config(self):
        return self.__config

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, FileStoreProvider):
            return False
        return (
            self.__provider == __value.__provider
            and self.__registrar == __value.__registrar
            and self.__config == __value.__config
            and self.__store_type == __value.__store_type
        )


# SourceRegistrar and ColumnMapping are imported from .registrar
