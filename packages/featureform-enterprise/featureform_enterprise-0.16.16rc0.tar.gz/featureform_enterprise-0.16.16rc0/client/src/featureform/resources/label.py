# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Label resource classes for Featureform.

This module contains classes for defining and managing labels.
"""

from dataclasses import dataclass
from typing import Any, List, Optional, Tuple, Union

from typeguard import typechecked

from ..config import ResourceSnowflakeConfig
from ..enums import OperationType, ResourceStatus, ResourceType, ScalarType
from ..operations.equivalence import _get_and_set_equivalent_variant
from ..proto import metadata_pb2 as pb
from ..types import VectorType, type_from_proto
from .base import NameVariant, ResourceVariant
from .mappings import EntityMapping, EntityMappings, ResourceColumnMapping
from .provider import Properties, ServerStatus

# Type alias for resource location
ResourceLocation = ResourceColumnMapping


@typechecked
@dataclass
class Label:
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
class LabelVariant(ResourceVariant):
    name: str
    source: Any
    value_type: Union[VectorType, ScalarType, str]
    entity: str
    owner: str
    description: str
    location: Union[ResourceLocation, EntityMappings]
    variant: str
    tags: Optional[list] = None
    properties: Optional[dict] = None
    provider: Optional[str] = None
    created: str = None
    status: str = "NO_STATUS"
    error: Optional[str] = None
    server_status: Optional[ServerStatus] = None
    resource_snowflake_config: Optional[ResourceSnowflakeConfig] = None

    def __post_init__(self):
        if isinstance(self.value_type, str):
            self.value_type = ScalarType(self.value_type)

    @staticmethod
    def operation_type() -> OperationType:
        return OperationType.CREATE

    @staticmethod
    def get_resource_type() -> ResourceType:
        return ResourceType.LABEL_VARIANT

    def name_variant(self) -> NameVariant:
        return (self.name, self.variant)

    def get(self, stub) -> "LabelVariant":
        return LabelVariant.get_by_name_variant(stub, self.name, self.variant)

    @staticmethod
    def get_by_name_variant(stub, name, variant):
        name_variant = pb.NameVariantRequest(
            name_variant=pb.NameVariant(name=name, variant=variant)
        )
        label = next(stub.GetLabelVariants(iter([name_variant])))

        loc_type = label.WhichOneof("location")
        location = None
        if loc_type == "columns":
            location = ResourceColumnMapping(
                entity=label.columns.entity,
                value=label.columns.value,
                timestamp=label.columns.ts,
            )
        elif loc_type == "entity_mappings":
            location = EntityMappings(
                mappings=[
                    EntityMapping(m.name, m.entity_column)
                    for m in label.entity_mappings.mappings
                ],
                value_column=label.entity_mappings.value_column,
                timestamp_column=(
                    label.entity_mappings.timestamp_column
                    if label.entity_mappings.timestamp_column
                    else None
                ),
            )

        return LabelVariant(
            name=label.name,
            variant=label.variant,
            source=(label.source.name, label.source.variant),
            value_type=type_from_proto(label.type),
            entity=label.entity,
            owner=label.owner,
            provider=label.provider,
            location=location,
            description=label.description,
            tags=list(label.tags.tag),
            properties=dict(label.properties.property.items()),
            status=label.status.Status._enum_type.values[label.status.status].name,
            server_status=ServerStatus.from_proto(label.status),
            error=label.status.error_message,
        )

    def _get_and_set_equivalent_variant(self, req_id, stub):
        if hasattr(self.source, "name_variant"):
            self.source = self.source.name_variant()
        label_variant = pb.LabelVariant(
            name=self.name,
            variant=self.variant,
            source=pb.NameVariant(
                name=self.source[0],
                variant=self.source[1],
            ),
            provider=self.provider,
            type=self.value_type.to_proto(),
            entity=self.entity,
            owner=self.owner,
            description=self.description,
            tags=pb.Tags(tag=self.tags),
            properties=Properties(self.properties).serialized,
            status=pb.ResourceStatus(status=pb.ResourceStatus.NO_STATUS),
            resource_snowflake_config=(
                self.resource_snowflake_config.to_proto()
                if self.resource_snowflake_config
                else None
            ),
        )
        if isinstance(self.location, ResourceLocation):
            label_variant.entity_mappings.CopyFrom(
                self.location.to_entity_mappings_proto(self.entity)
            )
        elif isinstance(self.location, EntityMappings):
            label_variant.entity_mappings.CopyFrom(self.location.to_proto())
        else:
            raise ValueError(
                f"Invalid location type {type(self.location)} for LabelVariant {self.name}"
            )
        serialized = pb.LabelVariantRequest(
            label_variant=label_variant,
            request_id="",
        )

        return (
            serialized,
            _get_and_set_equivalent_variant(req_id, serialized, "label_variant", stub),
            "label_variant",
        )

    def _create(self, req_id, stub) -> Tuple[Optional[str], Optional[str]]:
        serialized, existing_variant, _ = self._get_and_set_equivalent_variant(
            req_id, stub
        )
        if existing_variant is None:
            stub.CreateLabelVariant(serialized)
        return serialized.label_variant.variant, existing_variant

    def get_status(self):
        return ResourceStatus(self.status)

    def is_ready(self):
        return self.status == ResourceStatus.READY.value
