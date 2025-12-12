# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Mapping classes for Featureform resources.

This module contains classes for mapping entities and columns in features and labels,
including ResourceColumnMapping, EntityMapping, EntityMappings, and schema classes.
"""

from dataclasses import dataclass
from typing import List, Optional

from typeguard import typechecked

from ..enums import ScalarType
from ..proto import metadata_pb2 as pb


@typechecked
@dataclass
class ResourceColumnMapping:
    """Maps entity, value, and timestamp columns for a resource."""

    entity: str
    value: str
    timestamp: str = ""

    def proto(self) -> pb.Columns:
        return pb.Columns(
            entity=self.entity,
            value=self.value,
            ts=self.timestamp,
        )

    def to_entity_mappings_proto(self, entity_name: str) -> pb.EntityMappings:
        mapping = pb.EntityMapping(name=entity_name, entity_column=self.entity)
        return pb.EntityMappings(
            mappings=[mapping],
            value_column=self.value,
            timestamp_column=self.timestamp,
        )


@typechecked
@dataclass
class ColumnSchema:
    """Schema definition for a column."""

    name: str
    value_type: ScalarType

    def to_proto(self) -> pb.ColumnSchema:
        return pb.ColumnSchema(name=self.name, type=self.value_type.to_proto())

    @staticmethod
    def from_proto(proto: pb.ColumnSchema) -> "ColumnSchema":
        if proto is None:
            raise ValueError("Feature definitions require column schemas")
        if proto.type is None or proto.type.WhichOneof("Type") != "scalar":
            raise ValueError("Feature definitions require scalar column schemas")
        return ColumnSchema(
            name=proto.name,
            value_type=ScalarType.from_proto(proto.type.scalar),
        )


@typechecked
@dataclass
class FeatureColumn:
    """Schema for a feature column with optional timestamp."""

    feature_col: ColumnSchema
    timestamp_col: Optional[ColumnSchema] = None

    @staticmethod
    def from_proto(proto: pb.FeatureColumn) -> "FeatureColumn":
        return FeatureColumn(
            feature_col=ColumnSchema(
                name=proto.feature_col.name,
                value_type=ScalarType.from_proto(proto.feature_col.type.scalar),
            ),
            timestamp_col=(
                ColumnSchema(
                    name=proto.timestamp_col.name,
                    value_type=ScalarType.from_proto(proto.timestamp_col.type.scalar),
                )
                if proto.HasField("timestamp_col")
                else None
            ),
        )


@typechecked
@dataclass
class FeaturesSchema:
    """Schema for features including entity and feature columns."""

    entity_col: ColumnSchema
    feature_cols: list[FeatureColumn]

    @staticmethod
    def from_proto(proto: pb.FeaturesSchema) -> "FeaturesSchema":
        entity_col = ColumnSchema(
            name=proto.entity_col.name,
            value_type=ScalarType.from_proto(proto.entity_col.type.scalar),
        )
        feature_cols = [
            FeatureColumn.from_proto(feature_col) for feature_col in proto.feature_cols
        ]
        return FeaturesSchema(entity_col, feature_cols)


@typechecked
@dataclass
class EntityMapping:
    """Mapping between entity names and columns."""

    name: str
    entity_column: str

    def to_proto(self):
        return pb.EntityMapping(
            name=self.name,
            entity_column=self.entity_column,
        )


@typechecked
@dataclass
class EntityMappings:
    """Collection of entity mappings with value and timestamp columns."""

    mappings: List[EntityMapping]
    value_column: str
    timestamp_column: Optional[str] = None

    def to_proto(self):
        return pb.EntityMappings(
            mappings=[m.to_proto() for m in self.mappings],
            value_column=self.value_column,
            timestamp_column=self.timestamp_column,
        )
