# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Configuration classes for offline store providers.
"""

from __future__ import annotations

import json
import warnings
from dataclasses import dataclass
from typing import Dict, Optional, Union

from typeguard import typechecked

from ..enums import Initialize, RefreshMode, SnowflakeSessionParamKey
from ..proto import metadata_pb2 as pb
from ..secret_provider import Secret, StaticSecret
from .catalogs import SnowflakeCatalog, SnowflakeDynamicTableConfig
from .credentials import GCPCredentials


@typechecked
@dataclass
class PostgresConfig:
    host: str
    port: str
    database: str
    user: str
    password: Union[Secret, str]
    sslmode: str

    def __post_init__(self):
        if isinstance(self.password, str):
            self.password = StaticSecret(self.password)

    def software(self) -> str:
        return "postgres"

    def type(self) -> str:
        return "POSTGRES_OFFLINE"

    def serialize(self) -> bytes:
        config = {
            "Host": self.host,
            "Port": self.port,
            "Username": self.user,
            "Password": self.password.serialize(),
            "Database": self.database,
            "SSLMode": self.sslmode,
        }
        return bytes(json.dumps(config), "utf-8")

    @classmethod
    def deserialize(cls, config: bytes) -> "PostgresConfig":
        config = json.loads(config.decode("utf-8"))
        return cls(
            host=config["Host"],
            port=config["Port"],
            database=config["Database"],
            user=config["Username"],
            password=Secret.deserialize(config["Password"]),
            sslmode=config["SSLMode"],
        )


@typechecked
@dataclass
class ClickHouseConfig:
    host: str
    port: int
    database: str
    user: str
    password: str
    ssl: bool

    def software(self) -> str:
        return "clickhouse"

    def type(self) -> str:
        return "CLICKHOUSE_OFFLINE"

    def serialize(self) -> bytes:
        config = {
            "Host": self.host,
            "Port": self.port,
            "Username": self.user,
            "Password": self.password,
            "Database": self.database,
            "SSL": self.ssl,
        }
        return bytes(json.dumps(config), "utf-8")

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, ClickHouseConfig):
            return False
        return (
            self.host == __value.host
            and self.port == __value.port
            and self.database == __value.database
            and self.user == __value.user
            and self.password == __value.password
            and self.ssl == __value.ssl
        )


@typechecked
@dataclass
class RedshiftConfig:
    host: str
    port: str
    database: str
    user: str
    password: str
    sslmode: str

    def software(self) -> str:
        return "redshift"

    def type(self) -> str:
        return "REDSHIFT_OFFLINE"

    def serialize(self) -> bytes:
        config = {
            "Host": self.host,
            "Port": self.port,
            "Username": self.user,
            "Password": self.password,
            "Database": self.database,
            "SSLMode": self.sslmode,
        }
        return bytes(json.dumps(config), "utf-8")

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, RedshiftConfig):
            return False
        return (
            self.host == __value.host
            and self.port == __value.port
            and self.database == __value.database
            and self.user == __value.user
            and self.password == __value.password
            and self.sslmode == __value.sslmode
        )


@typechecked
@dataclass
class BigQueryConfig:
    project_id: str
    dataset_id: str
    credentials: GCPCredentials

    def software(self) -> str:
        return "bigquery"

    def type(self) -> str:
        return "BIGQUERY_OFFLINE"

    def serialize(self) -> bytes:
        config = {
            "ProjectID": self.project_id,
            "DatasetID": self.dataset_id,
            "Credentials": self.credentials.to_json(),
        }
        return bytes(json.dumps(config), "utf-8")

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, BigQueryConfig):
            return False
        return (
            self.project_id == __value.project_id
            and self.dataset_id == __value.dataset_id
        )


@dataclass
class ResourceSnowflakeConfig:
    dynamic_table_config: Optional[SnowflakeDynamicTableConfig] = None
    warehouse: Optional[str] = None

    def config(self) -> dict:
        return {
            "DynamicTableConfig": (
                self.dynamic_table_config.config()
                if self.dynamic_table_config
                else None
            ),
            "Warehouse": self.warehouse,
        }

    def to_proto(self):
        return pb.ResourceSnowflakeConfig(
            dynamic_table_config=(
                self.dynamic_table_config.to_proto()
                if self.dynamic_table_config
                else None
            ),
            warehouse=self.warehouse,
        )

    @classmethod
    def from_proto(
        cls, config: pb.ResourceSnowflakeConfig
    ) -> "ResourceSnowflakeConfig":
        return cls(
            dynamic_table_config=(
                SnowflakeDynamicTableConfig(
                    target_lag=config.dynamic_table_config.target_lag,
                    refresh_mode=(
                        RefreshMode.from_proto(config.dynamic_table_config.refresh_mode)
                        if config.dynamic_table_config.refresh_mode
                        else None
                    ),
                    initialize=(
                        Initialize.from_proto(config.dynamic_table_config.initialize)
                        if config.dynamic_table_config.initialize
                        else None
                    ),
                )
                if config.dynamic_table_config
                else None
            ),
            warehouse=config.warehouse,
        )


@typechecked
@dataclass
class SnowflakeConfig:
    username: str
    password: str
    schema: str
    account: str = ""
    organization: str = ""
    database: str = ""
    account_locator: str = ""
    warehouse: str = ""
    role: str = ""
    catalog: Optional[SnowflakeCatalog] = None
    session_params: Optional[Dict[str, str]] = None

    def __post_init__(self):
        if self.session_params:
            for key, _ in self.session_params.items():
                if not SnowflakeSessionParamKey.validate_key(key):
                    warnings.warn(
                        f"Invalid key '{key}' in session_params. This key will be ignored in the Snowflake session."
                    )

        if self.__has_legacy_credentials() and self.__has_current_credentials():
            raise ValueError(
                "Cannot create configure Snowflake with both current and legacy credentials"
            )

        if not self.__has_legacy_credentials() and not self.__has_current_credentials():
            raise ValueError("Cannot create configure Snowflake without credentials")

    def __has_legacy_credentials(self) -> bool:
        return self.account_locator != ""

    def __has_current_credentials(self) -> bool:
        if (self.account != "" and self.organization == "") or (
            self.account == "" and self.organization != ""
        ):
            raise ValueError("Both Snowflake organization and account must be included")
        elif self.account != "" and self.organization != "":
            return True
        else:
            return False

    def software(self) -> str:
        return "Snowflake"

    def type(self) -> str:
        return "SNOWFLAKE_OFFLINE"

    def serialize(self) -> bytes:
        config = {
            "Username": self.username,
            "Password": self.password,
            "Organization": self.organization,
            "AccountLocator": self.account_locator,
            "Account": self.account,
            "Schema": self.schema,
            "Database": self.database,
            "Warehouse": self.warehouse,
            "Role": self.role,
            "Catalog": self.catalog.config() if self.catalog is not None else None,
            "SessionParams": self.session_params,
        }
        return bytes(json.dumps(config), "utf-8")

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, SnowflakeConfig):
            return False
        is_catalog_equal = (self.catalog is None and __value.catalog is None) or (
            self.catalog is not None
            and __value.catalog is not None
            and self.catalog.external_volume == __value.catalog.external_volume
            and self.catalog.base_location == __value.catalog.base_location
            and self.catalog.table_config.target_lag
            == __value.catalog.table_config.target_lag
            and self.catalog.table_config.refresh_mode
            == __value.catalog.table_config.refresh_mode
            and self.catalog.table_config.initialize
            == __value.catalog.table_config.initialize
        )
        return (
            self.username == __value.username
            and self.password == __value.password
            and self.schema == __value.schema
            and self.account == __value.account
            and self.organization == __value.organization
            and self.database == __value.database
            and self.account_locator == __value.account_locator
            and self.warehouse == __value.warehouse
            and self.role == __value.role
            and is_catalog_equal
            and self.session_params == __value.session_params
        )
