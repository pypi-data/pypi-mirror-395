# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Entity resource classes.
"""

from dataclasses import dataclass, field
from typing import Tuple, Union

import grpc
from typeguard import typechecked

from ..enums import OperationType, ResourceType
from ..proto import metadata_pb2 as pb
from .provider import Properties


@typechecked
@dataclass
class Entity:
    """Entity resource representing a business object."""

    name: str
    description: str
    status: str = "NO_STATUS"
    tags: list = field(default_factory=list)
    properties: dict = field(default_factory=dict)

    @staticmethod
    def operation_type() -> OperationType:
        return OperationType.CREATE

    @staticmethod
    def get_resource_type() -> ResourceType:
        return ResourceType.ENTITY

    def _create(self, req_id, stub) -> Tuple[None, None]:
        serialized = pb.EntityRequest(
            entity=pb.Entity(
                name=self.name,
                description=self.description,
                tags=pb.Tags(tag=self.tags),
                properties=Properties(self.properties).serialized,
            ),
            request_id="",
        )

        stub.CreateEntity(serialized)
        return None, None

    def to_dictionary(self):
        return {
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "tags": self.tags,
            "properties": self.properties,
        }


class EntityReference:
    """Reference to an entity resource."""

    name: str
    obj: Union[Entity, None]

    @staticmethod
    def operation_type() -> OperationType:
        return OperationType.GET

    @staticmethod
    def get_resource_type() -> ResourceType:
        return ResourceType.ENTITY

    def _get(self, stub):
        entityList = stub.GetEntities(
            iter([pb.NameRequest(name=pb.Name(name=self.name))])
        )
        try:
            for entity in entityList:
                self.obj = entity
        except grpc._channel._MultiThreadedRendezvous:
            raise ValueError(f"Entity {self.name} not found.")
