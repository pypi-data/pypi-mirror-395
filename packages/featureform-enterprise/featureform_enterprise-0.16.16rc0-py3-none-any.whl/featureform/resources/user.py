# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
User resource class.
"""

from dataclasses import dataclass, field
from typing import Tuple

from typeguard import typechecked

from ..enums import OperationType, ResourceType
from ..proto import metadata_pb2 as pb
from .provider import Properties


@typechecked
@dataclass
class User:
    """User resource for ownership and access control."""

    name: str
    status: str = ""
    tags: list = field(default_factory=list)
    properties: dict = field(default_factory=dict)

    @staticmethod
    def operation_type() -> OperationType:
        return OperationType.CREATE

    @staticmethod
    def get_resource_type() -> ResourceType:
        return ResourceType.USER

    def _create(self, req_id, stub) -> Tuple[None, None]:
        serialized = pb.UserRequest(
            user=pb.User(
                name=self.name,
                tags=pb.Tags(tag=self.tags),
                properties=Properties(self.properties).serialized,
            ),
            request_id="",
        )

        stub.CreateUser(serialized)
        return None, None

    def to_dictionary(self):
        return {
            "name": self.name,
            "status": self.status,
            "tags": self.tags,
            "properties": self.properties,
        }
