# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Online provider wrapper classes for Featureform.
"""

__all__ = ["OnlineProvider"]


class OnlineProvider:
    def __init__(self, registrar, provider):
        self.__registrar = registrar
        self.__provider = provider

    def name(self) -> str:
        return self.__provider.name

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, OnlineProvider):
            return False
        return (
            self.__provider == __value.__provider
            and self.__registrar == __value.__registrar
        )
