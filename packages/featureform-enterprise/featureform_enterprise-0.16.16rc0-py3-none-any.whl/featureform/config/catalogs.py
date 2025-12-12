# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Catalog configuration classes for data catalogs (Glue, Unity, Snowflake).
"""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional

from typeguard import typechecked

from ..enums import Initialize, RefreshMode, TableFormat
from ..proto import metadata_pb2 as pb


@dataclass
class SnowflakeDynamicTableConfig:
    """
    Configuration for Snowflake dynamic tables.

    Dynamic tables are a Snowflake feature that automatically refreshes data
    based on a target lag and refresh mode.
    """

    target_lag: Optional[str] = None
    refresh_mode: Optional[RefreshMode] = None
    initialize: Optional[Initialize] = None

    def config(self) -> dict:
        return {
            "TargetLag": self.target_lag,
            "RefreshMode": self.refresh_mode.to_string() if self.refresh_mode else None,
            "Initialize": self.initialize.to_string() if self.initialize else None,
        }

    def to_proto(self):
        return pb.SnowflakeDynamicTableConfig(
            target_lag=self.target_lag,
            refresh_mode=self.refresh_mode.to_proto() if self.refresh_mode else None,
            initialize=self.initialize.to_proto() if self.initialize else None,
        )


class Catalog(ABC):
    @abstractmethod
    def type(self):
        pass

    @abstractmethod
    def config(self):
        pass


@typechecked
@dataclass
class GlueCatalog(Catalog):
    region: str
    database: str
    warehouse: str = ""
    assume_role_arn: str = ""
    table_format: TableFormat = field(default_factory=lambda: TableFormat.ICEBERG)

    def __post_init__(self):
        self._validate_database_name()
        self._validate_iceberg_configuration()

    def type(self) -> str:
        return "glue"

    def config(self):
        return {
            "Database": self.database,
            "Warehouse": self.warehouse,
            "Region": self.region,
            "AssumeRoleArn": self.assume_role_arn,
            "TableFormat": self.table_format,
        }

    def _validate_database_name(self):
        if self.database == "":
            raise ValueError("Database name cannot be empty")
        if not all(c.isalnum() or c == "_" for c in self.database):
            raise ValueError("Database name must be alphanumeric and/or underscores")

    def _validate_iceberg_configuration(self):
        if self.table_format is TableFormat.ICEBERG:
            errors = []
            if self.warehouse == "":
                errors.append("warehouse is required for Iceberg tables")
            if self.region == "":
                errors.append("region is required for Iceberg tables")

            if len(errors) > 0:
                raise ValueError(";".join(errors))


@typechecked
@dataclass
class UnityCatalog(Catalog):
    catalog: str
    schema: str
    table_format: TableFormat = field(default_factory=lambda: TableFormat.DELTA)

    def __post_init__(self):
        self._validate_catalog_name()
        self._validate_iceberg_configuration()

    def type(self) -> str:
        return "unity"

    def config(self):
        return {
            "Catalog": self.catalog,
            "Schema": self.schema,
            "TableFormat": self.table_format,
        }

    def _validate_catalog_name(self):
        if self.catalog == "":
            raise ValueError("Database name cannot be empty")
        if self.schema == "":
            raise ValueError("Schema name cannot be empty")

    def _validate_iceberg_configuration(self):
        errors = []
        if self.table_format != TableFormat.DELTA:
            errors.append("table format must be 'DELTA'")

        if len(errors) > 0:
            raise ValueError(";".join(errors))


@typechecked
@dataclass
class SnowflakeCatalog(Catalog):
    external_volume: str
    base_location: str
    table_config: Optional[SnowflakeDynamicTableConfig] = None

    def __post_init__(self):
        if self.table_config is None:
            self.table_config = SnowflakeDynamicTableConfig(
                target_lag="DOWNSTREAM",
                refresh_mode=RefreshMode.AUTO,
                initialize=Initialize.ON_CREATE,
            )
        if not self._validate_target_lag():
            raise ValueError(
                "target_lag must be in the format of '<num> { seconds | minutes | hours | days }' or 'DOWNSTREAM'; the minimum value is 1 minute"
            )

    def type(self) -> str:
        return "snowflake"

    def config(self) -> dict:
        return {
            "ExternalVolume": self.external_volume,
            "BaseLocation": self.base_location,
            "TableFormat": TableFormat.ICEBERG,
            "TableConfig": self.table_config.config(),
        }

    def _validate_target_lag(self) -> bool:
        if self.table_config is None or self.table_config.target_lag is None:
            return True
        # See https://docs.snowflake.com/en/sql-reference/sql/create-dynamic-table#create-dynamic-iceberg-table
        # for more information on the target_lag parameter
        pattern = r"^(\d+)\s+(seconds|minutes|hours|days)$|^(?i:DOWNSTREAM)$"
        match = re.match(pattern, self.table_config.target_lag)

        if not match:
            return False

        if self.table_config.target_lag.lower() == "downstream":
            return True

        value, unit = int(match.group(1)), match.group(2)

        if unit == "seconds" and value < 60:
            return False

        if unit == "minutes" and value < 1:
            return False

        return True
