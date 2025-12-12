# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Schedule and partition classes for Featureform resources.
"""

from dataclasses import dataclass
from typing import Tuple, Union

from typeguard import typechecked

from ..enums import OperationType, ResourceType
from ..proto import metadata_pb2 as pb


@typechecked
@dataclass
class Schedule:
    name: str
    variant: str
    resource_type: int
    schedule_string: str

    @staticmethod
    def operation_type() -> OperationType:
        return OperationType.CREATE

    @staticmethod
    def get_resource_type() -> ResourceType:
        return ResourceType.SCHEDULE

    def _create(self, req_id, stub) -> Tuple[None, None]:
        serialized = pb.SetScheduleChangeRequest(
            resource=pb.ResourceId(
                pb.NameVariant(name=self.name, variant=self.variant),
                resource_type=self.resource_type,
            ),
            schedule=self.schedule_string,
        )
        stub.RequestScheduleChange(serialized)
        return None, None


class HashPartition:
    def __init__(self, column, num_buckets):
        self.column = column
        self.num_buckets = num_buckets

    def proto_kwargs(self):
        return {
            "HashPartition": pb.HashPartition(
                column=self.column, buckets=self.num_buckets
            )
        }


class DailyPartition:
    def __init__(self, column):
        self.column = column

    def proto_kwargs(self):
        return {"DailyPartition": pb.DailyPartition(column=self.column)}


PartitionType = Union[HashPartition, DailyPartition]
