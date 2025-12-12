# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Model resource classes for Featureform.

This module contains classes for defining and managing models.
"""

from dataclasses import dataclass, field
from typing import Tuple

from typeguard import typechecked

from ..enums import OperationType, ResourceType
from ..proto import metadata_pb2 as pb
from .provider import Properties


@typechecked
@dataclass
class Model:
    name: str
    description: str = ""
    tags: list = field(default_factory=list)
    properties: dict = field(default_factory=dict)

    @staticmethod
    def operation_type() -> OperationType:
        return OperationType.CREATE

    @staticmethod
    def get_resource_type() -> ResourceType:
        return ResourceType.MODEL

    def _create(self, req_id, stub) -> Tuple[None, None]:
        properties = pb.Properties(property=self.properties)
        serialized = pb.ModelRequest(
            model=pb.Model(
                name=self.name,
                tags=pb.Tags(tag=self.tags),
                properties=Properties(self.properties).serialized,
            ),
            request_id="",
        )

        stub.CreateModel(serialized)
        return None, None

    def to_dictionary(self):
        return {
            "name": self.name,
            "description": self.description,
            "tags": self.tags,
            "properties": self.properties,
        }
