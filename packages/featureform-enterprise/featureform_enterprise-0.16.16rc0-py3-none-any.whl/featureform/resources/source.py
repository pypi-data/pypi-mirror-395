# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Source resource classes for Featureform.

This module contains classes for defining and managing data sources.
"""

from dataclasses import dataclass
from datetime import timedelta
from typing import List, Optional, Tuple, Union

import grpc
from google.protobuf.duration_pb2 import Duration
from typeguard import typechecked

from ..enums import OperationType, ResourceStatus, ResourceType, SourceType
from ..operations.equivalence import _get_and_set_equivalent_variant
from ..proto import metadata_pb2 as pb
from .base import NameVariant, ResourceVariant
from .entity import Entity
from .provider import Properties, Provider, ServerStatus
from .schedule import Schedule
from .transformations import PrimaryData, Transformation

# Type alias for source definitions
SourceDefinition = Union[PrimaryData, Transformation, str]


@typechecked
@dataclass
class Source:
    """High-level source resource containing multiple variants."""

    name: str
    default_variant: str
    variants: List[str]

    def to_dictionary(self):
        return {
            "name": self.name,
            "default_variant": self.default_variant,
            "variants": self.variants,
        }


@typechecked
@dataclass
class SourceVariant(ResourceVariant):
    """A specific variant of a source with its definition and metadata."""

    name: str
    definition: SourceDefinition
    owner: str
    provider: str
    description: str
    tags: list
    properties: dict
    variant: str
    created: str = None
    status: str = (
        "ready"  # there is no associated status by default but it always stores ready
    )
    schedule: str = ""
    schedule_obj: Schedule = None
    is_transformation = (
        SourceType.PRIMARY_SOURCE.value
    )  # TODO this is the same as source_type below; pick one
    source_text: str = ""
    source_type: str = ""
    transformation: str = ""
    inputs: list = ([],)
    error: Optional[str] = None
    server_status: Optional[ServerStatus] = None
    max_job_duration: timedelta = timedelta(hours=48)

    def update_schedule(self, schedule) -> None:
        self.schedule_obj = Schedule(
            name=self.name,
            variant=self.variant,
            resource_type=7,
            schedule_string=schedule,
        )
        self.schedule = schedule

    @staticmethod
    def operation_type() -> OperationType:
        return OperationType.CREATE

    @staticmethod
    def get_resource_type() -> ResourceType:
        return ResourceType.SOURCE_VARIANT

    def name_variant(self) -> NameVariant:
        return (self.name, self.variant)

    def get(self, stub):
        return SourceVariant.get_by_name_variant(stub, self.name, self.variant)

    @staticmethod
    def get_by_name_variant(stub, name, variant):
        name_variant = pb.NameVariantRequest(
            name_variant=pb.NameVariant(name=name, variant=variant)
        )
        source = next(stub.GetSourceVariants(iter([name_variant])))
        definition = SourceVariant._get_source_definition(source)

        return SourceVariant(
            created=None,
            name=source.name,
            definition=definition,
            owner=source.owner,
            provider=source.provider,
            description=source.description,
            variant=source.variant,
            tags=list(source.tags.tag),
            properties=dict(source.properties.property.items()),
            status=source.status.Status._enum_type.values[source.status.status].name,
            error=source.status.error_message,
            server_status=ServerStatus.from_proto(source.status),
            max_job_duration=source.max_job_duration.ToTimedelta(),
        )

    @staticmethod
    def _get_source_definition(source):
        definition_type = source.WhichOneof("definition")
        if definition_type == "primaryData":
            return PrimaryData.from_proto(source.primaryData)
        elif definition_type == "transformation":
            return Transformation.from_proto(source.transformation)
        else:
            raise Exception(f"Invalid source definition type {definition_type}")

    def _get_and_set_equivalent_variant(self, req_id, stub):
        defArgs = self.definition.kwargs()
        duration = Duration()
        duration.FromTimedelta(self.max_job_duration)

        serialized = pb.SourceVariantRequest(
            source_variant=pb.SourceVariant(
                created=None,
                name=self.name,
                variant=self.variant,
                owner=self.owner,
                description=self.description,
                schedule=self.schedule,
                provider=self.provider,
                tags=pb.Tags(tag=self.tags),
                properties=Properties(self.properties).serialized,
                status=pb.ResourceStatus(status=pb.ResourceStatus.NO_STATUS),
                max_job_duration=duration,
                **defArgs,
            ),
            request_id="",
        )

        existing_variant = _get_and_set_equivalent_variant(
            req_id, serialized, "source_variant", stub
        )
        return serialized, existing_variant, "source_variant"

    def _create(self, req_id, stub) -> Tuple[Optional[str], Optional[str]]:
        serialized, existing_variant, _ = self._get_and_set_equivalent_variant(
            req_id, stub
        )
        if existing_variant is None:
            stub.CreateSourceVariant(serialized)
        return serialized.source_variant.variant, existing_variant

    def get_status(self):
        return ResourceStatus(self.status)

    def is_transformation_type(self):
        return isinstance(self.definition, Transformation)

    def is_ready(self):
        return self.status == ResourceStatus.READY.value


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


@typechecked
@dataclass
class ProviderReference:
    """Reference to a provider resource."""

    name: str
    provider_type: str
    obj: Union[Provider, None]

    @staticmethod
    def operation_type() -> OperationType:
        return OperationType.GET

    @staticmethod
    def get_resource_type() -> ResourceType:
        return ResourceType.PROVIDER

    def _get(self, stub):
        providerList = stub.GetProviders(
            iter([pb.NameRequest(name=pb.Name(name=self.name))])
        )
        try:
            for provider in providerList:
                self.obj = provider
        except grpc._channel._MultiThreadedRendezvous:
            raise ValueError(
                f"Provider {self.name} of type {self.provider_type} not found."
            )


@typechecked
@dataclass
class SourceReference:
    """Reference to a source variant resource."""

    name: str
    variant: str
    obj: Union["SourceVariant", None]

    @staticmethod
    def operation_type() -> OperationType:
        return OperationType.GET

    @staticmethod
    def get_resource_type() -> ResourceType:
        return ResourceType.SOURCE_VARIANT

    def name_variant(self) -> NameVariant:
        return (self.name, self.variant)

    def _get(self, stub):
        sourceList = stub.GetSourceVariants(
            iter(
                [
                    pb.NameVariantRequest(
                        name_variant=pb.NameVariant(
                            name=self.name, variant=self.variant
                        )
                    )
                ]
            )
        )
        try:
            for source in sourceList:
                self.obj = source
        except grpc._channel._MultiThreadedRendezvous:
            raise ValueError(f"Source {self.name}, variant {self.variant} not found.")
