# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Transformation classes for Featureform resources.

This module contains all transformation-related classes including Transformation base class,
SQLTransformation, DFTransformation, and PrimaryData.
"""

import re
from abc import ABC
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from typeguard import typechecked

from ..config.compute import EmptySparkFlags, K8sArgs, SparkFlags
from ..config.offline_stores import ResourceSnowflakeConfig
from ..enums import LocationType, SourceType
from ..proto import metadata_pb2 as pb
from .schedule import PartitionType

if TYPE_CHECKING:
    pass


class Transformation(ABC):
    """Base class for all transformations."""

    @classmethod
    def from_proto(cls, source_transformation: pb.Transformation):
        # Import here to avoid circular dependency
        transformation_type = source_transformation.WhichOneof("type")
        if transformation_type == "DFTransformation":
            return DFTransformation.from_proto(source_transformation.DFTransformation)
        elif transformation_type == "SQLTransformation":
            return SQLTransformation.from_proto(source_transformation.SQLTransformation)
        else:
            raise Exception(f"Invalid transformation type {source_transformation}")


@typechecked
@dataclass
class SQLTransformation(Transformation):
    """SQL-based transformation with query and optional parameters."""

    query: str
    args: Optional[K8sArgs] = None
    func_params_to_inputs: Dict[str, Any] = field(default_factory=dict)
    is_incremental: bool = False
    incremental_inputs: list = field(default_factory=list)
    is_streaming: bool = False
    streaming_inputs: list = field(default_factory=list)
    partition_options: Optional[PartitionType] = None
    spark_flags: SparkFlags = field(default_factory=lambda: EmptySparkFlags)
    resource_snowflake_config: Optional[ResourceSnowflakeConfig] = None

    _sql_placeholder_regex: str = field(
        default=r"\{\{\s*\w+\s*\}\}", init=False, repr=False
    )

    def __post_init__(self):
        self._validate_inputs_to_func_params(self.func_params_to_inputs)

    def type(self) -> str:
        """Return the type of the SQL transformation."""
        return SourceType.SQL_TRANSFORMATION.value

    def kwargs(self) -> Dict[str, pb.Transformation]:
        return {"transformation": self.to_proto()}

    @classmethod
    def from_proto(cls, sql_transformation: pb.SQLTransformation):
        return SQLTransformation(sql_transformation.query)

    def _validate_inputs_to_func_params(self, inputs: Dict[str, Any]) -> None:
        # Find and replace placeholders in the query with source name variants
        for placeholder in self._get_placeholders():
            clean_placeholder = placeholder.strip(" {}")
            if clean_placeholder not in self.func_params_to_inputs.keys():
                raise ValueError(
                    f"SQL placeholder '{placeholder}' not found in input arguments. "
                    f"Available input arguments: {', '.join(inputs.keys())}.\n"
                    f"Expected inputs based on function parameters: {', '.join(self.func_params_to_inputs.keys())}."
                )

    def _resolve_input_variants(self) -> Dict[str, Any]:
        """Resolve inputs to their name variants."""
        return {
            func_param: inp.name_variant() if hasattr(inp, "name_variant") else inp
            for func_param, inp in self.func_params_to_inputs.items()
        }

    def _get_placeholders(self) -> List[str]:
        """Get placeholders from the query."""
        return re.findall(self._sql_placeholder_regex, self.query)

    def to_proto(self) -> pb.Transformation:
        input_to_name_variant = self._resolve_input_variants()

        for i, inp in enumerate(self.incremental_inputs):
            if hasattr(inp, "name_variant"):
                self.incremental_inputs[i] = inp.name_variant()

        for i, inp in enumerate(self.streaming_inputs):
            if hasattr(inp, "name_variant"):
                self.streaming_inputs[i] = inp.name_variant()

        incremental_nvs = []
        for inp in self.incremental_inputs:
            incremental_nvs.append(pb.NameVariant(name=inp[0], variant=inp[1]))

        streaming_nvs = []
        for inp in self.streaming_inputs:
            streaming_nvs.append(pb.NameVariant(name=inp[0], variant=inp[1]))

        # Find and replace placeholders in the query with source name variants
        final_query = self.query
        for placeholder in self._get_placeholders():
            clean_placeholder = placeholder.strip(" {}")
            name_variant = input_to_name_variant[clean_placeholder]
            replacement = "{{ " + f"{name_variant[0]}.{name_variant[1]}" + " }}"
            final_query = final_query.replace(placeholder, replacement)

        partition_kwargs = {}
        if self.partition_options is not None:
            partition_kwargs = self.partition_options.proto_kwargs()

        # Construct the SQLTransformation protobuf message
        transformation = pb.Transformation(
            SQLTransformation=pb.SQLTransformation(
                query=final_query,
                is_incremental=self.is_incremental,
                incremental_source=incremental_nvs,
                is_streaming=self.is_streaming,
                streaming_sources=streaming_nvs,
                resource_snowflake_config=(
                    self.resource_snowflake_config.to_proto()
                    if self.resource_snowflake_config
                    else None
                ),
            ),
            spark_flags=self.spark_flags.to_proto() if self.spark_flags else None,
            **partition_kwargs,
        )

        # Apply args transformations if any
        if self.args is not None:
            transformation = self.args.apply(transformation)

        return transformation


@typechecked
@dataclass
class DFTransformation(Transformation):
    """DataFrame transformation for processing data using Python/Spark."""

    query: bytes
    inputs: list
    args: K8sArgs = None
    source_text: str = ""
    canonical_func_text: str = ""
    is_incremental: bool = False
    incremental_inputs: list = field(default_factory=list)
    partition_options: Optional[PartitionType] = None
    spark_flags: SparkFlags = field(default_factory=lambda: EmptySparkFlags)

    def type(self):
        return SourceType.DF_TRANSFORMATION.value

    def to_proto(self) -> pb.Transformation:
        # Create a new list of name variants without modifying self.inputs
        name_variants = []
        for inp in self.inputs:
            if hasattr(inp, "name_variant"):
                name_variants.append(inp.name_variant())
            else:
                name_variants.append(inp)

        name_variant_protos = [
            pb.NameVariant(name=inp[0], variant=inp[1]) for inp in name_variants
        ]

        partition_kwargs = {}
        if self.partition_options is not None:
            partition_kwargs = self.partition_options.proto_kwargs()

        transformation = pb.Transformation(
            DFTransformation=pb.DFTransformation(
                query=self.query,
                inputs=name_variant_protos,
                source_text=self.source_text,
                is_incremental=self.is_incremental,
                incremental_sources=name_variant_protos,
                canonical_func_text=self.canonical_func_text,
            ),
            spark_flags=self.spark_flags.to_proto() if self.spark_flags else None,
            **partition_kwargs,
        )

        if self.args is not None:
            transformation = self.args.apply(transformation)

        return transformation

    def kwargs(self):
        return {"transformation": self.to_proto()}

    @classmethod
    def from_proto(cls, df_transformation: pb.DFTransformation):
        return DFTransformation(
            query=df_transformation.query,
            inputs=[(input.name, input.variant) for input in df_transformation.inputs],
            source_text=df_transformation.source_text,
        )


@dataclass
class PrimaryData:
    """Primary data source with location and optional timestamp column."""

    location: Any  # Location type - using Any to avoid circular import with typeguard
    timestamp_column: str = ""

    def kwargs(self) -> dict:
        # Import here to avoid circular dependency
        from .locations import (
            FileStore,
            GlueCatalogTable,
            SQLTable,
            StreamChannel,
            UnityCatalogTable,
        )

        primary_data_kwargs: Dict[str, Any] = {
            "timestamp_column": self.timestamp_column,
        }

        if isinstance(self.location, SQLTable):
            primary_data_kwargs["table"] = pb.SQLTable(
                schema=self.location.schema,
                database=self.location.database,
                name=self.location.name,
            )
        elif isinstance(self.location, FileStore):
            primary_data_kwargs["filestore"] = pb.FileStoreTable(
                path=self.location.resource_identifier(),
            )
        elif isinstance(self.location, GlueCatalogTable):
            primary_data_kwargs["catalog"] = pb.CatalogTable(
                catalog_type=pb.GLUE,
                database=self.location.database,
                table=self.location.table,
                table_format=self.location.table_format,
            )
        elif isinstance(self.location, UnityCatalogTable):
            primary_data_kwargs["catalog"] = pb.CatalogTable(
                catalog_type=pb.UNITY,
                database=self.location.database,
                schema=self.location.schema,
                table=self.location.table,
                table_format=self.location.table_format,
            )
        elif isinstance(self.location, StreamChannel):
            primary_data_kwargs["stream_channel"] = pb.StreamChannel(
                name=self.location.name,
                channel_name=self.location.channel_name,
                provider=self.location.provider,
            )
        else:
            raise ValueError(f"Unsupported location type: {type(self.location)}")

        return {"primaryData": pb.PrimaryData(**primary_data_kwargs)}

    def path(self) -> str:
        return self.location.resource_identifier()

    @staticmethod
    def from_proto(source_primary_data):
        # Import here to avoid circular dependency
        from .locations import FileStore, GlueCatalogTable, SQLTable, UnityCatalogTable

        primary_type = source_primary_data.WhichOneof("location")
        if primary_type == LocationType.TABLE:
            location = SQLTable.from_proto(source_primary_data.table)
        elif primary_type == LocationType.FILESTORE:
            location = FileStore.from_proto(source_primary_data.filestore)
        elif primary_type == LocationType.CATALOG:
            if source_primary_data.catalog.catalog_type == pb.GLUE:
                location = GlueCatalogTable.from_proto(source_primary_data.catalog)
            elif source_primary_data.catalog.catalog_type == pb.UNITY:
                location = UnityCatalogTable.from_proto(source_primary_data.catalog)
            else:
                raise Exception(
                    f"Unknown catalog type '{source_primary_data.catalog.catalog_type}'"
                )
        else:
            raise Exception(f"Invalid primary data type {source_primary_data}")

        return PrimaryData(location, source_primary_data.timestamp_column)
