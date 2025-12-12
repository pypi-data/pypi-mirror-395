# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Configuration classes for online store providers.
"""

import json
import re
from dataclasses import dataclass, field
from typing import Optional, Union

from typeguard import typechecked

from .credentials import AWSAssumeRoleCredentials, AWSStaticCredentials, GCPCredentials


@typechecked
@dataclass
class RedisConfig:
    host: str
    port: int
    password: str
    db: int
    ssl_mode: bool = False

    def software(self) -> str:
        return "redis"

    def type(self) -> str:
        return "REDIS_ONLINE"

    def serialize(self) -> bytes:
        config = {
            "Addr": f"{self.host}:{self.port}",
            "Password": self.password,
            "DB": self.db,
            "SSLMode": self.ssl_mode,
        }
        return bytes(json.dumps(config), "utf-8")

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, RedisConfig):
            return False
        return (
            self.host == __value.host
            and self.port == __value.port
            and self.password == __value.password
            and self.db == __value.db
            and self.ssl_mode == __value.ssl_mode
        )


@typechecked
@dataclass
class PineconeConfig:
    project_id: str = ""
    environment: str = ""
    api_key: str = ""

    def software(self) -> str:
        return "pinecone"

    def type(self) -> str:
        return "PINECONE_ONLINE"

    def serialize(self) -> bytes:
        config = {
            "ProjectID": self.project_id,
            "Environment": self.environment,
            "ApiKey": self.api_key,
        }
        return bytes(json.dumps(config), "utf-8")

    def deserialize(self, config):
        config = json.loads(config)
        self.project_id = config["ProjectID"]
        self.environment = config["Environment"]
        self.api_key = config["ApiKey"]
        return self

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, PineconeConfig):
            return False
        return (
            self.project_id == __value.project_id
            and self.environment == __value.environment
            and self.api_key == __value.api_key
        )


@typechecked
@dataclass
class WeaviateConfig:
    url: str = ""
    api_key: str = ""

    def software(self) -> str:
        return "weaviate"

    def type(self) -> str:
        return "WEAVIATE_ONLINE"

    def serialize(self) -> bytes:
        if self.url == "":
            raise Exception("URL cannot be empty")
        config = {
            "URL": self.url,
            "ApiKey": self.api_key,
        }
        return bytes(json.dumps(config), "utf-8")

    def deserialize(self, config):
        config = json.loads(config)
        self.url = config["URL"]
        self.api_key = config["ApiKey"]
        return self


@typechecked
@dataclass
class FirestoreConfig:
    collection: str
    project_id: str
    credentials: GCPCredentials

    def software(self) -> str:
        return "firestore"

    def type(self) -> str:
        return "FIRESTORE_ONLINE"

    def serialize(self) -> bytes:
        config = {
            "Collection": self.collection,
            "ProjectID": self.project_id,
            "Credentials": self.credentials.to_json(),
        }
        return bytes(json.dumps(config), "utf-8")

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, FirestoreConfig):
            return False
        return (
            self.collection == __value.collection
            and self.project_id == __value.project_id
        )


@typechecked
@dataclass
class CassandraConfig:
    keyspace: str
    host: str
    port: int
    username: str
    password: str
    consistency: str
    replication: int

    def software(self) -> str:
        return "cassandra"

    def type(self) -> str:
        return "CASSANDRA_ONLINE"

    def serialize(self) -> bytes:
        config = {
            "Keyspace": self.keyspace,
            "Addr": f"{self.host}:{self.port}",
            "Username": self.username,
            "Password": self.password,
            "Consistency": self.consistency,
            "Replication": self.replication,
        }
        return bytes(json.dumps(config), "utf-8")

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, CassandraConfig):
            return False
        return (
            self.keyspace == __value.keyspace
            and self.host == __value.host
            and self.port == __value.port
            and self.username == __value.username
            and self.password == __value.password
            and self.consistency == __value.consistency
            and self.replication == __value.replication
        )


@typechecked
@dataclass
class DynamodbConfig:
    region: str
    credentials: Union[AWSStaticCredentials, AWSAssumeRoleCredentials]
    table_tags: Optional[dict] = field(default_factory=dict)

    def __post_init__(self):
        errors = self.validate_table_tags(self.table_tags)
        if len(errors) > 0:
            raise ValueError(
                "Table tags validation errors found:\n" + "\n".join(errors)
            )

    def software(self) -> str:
        return "dynamodb"

    def type(self) -> str:
        return "DYNAMODB_ONLINE"

    def serialize(self) -> bytes:
        config = {
            "Region": self.region,
            "Credentials": self.credentials.config(),
            "Tags": self.table_tags,
        }
        return bytes(json.dumps(config), "utf-8")

    @classmethod
    def deserialize(cls, json_bytes: bytes) -> "DynamodbConfig":
        deserialized_config = json.loads(json_bytes.decode("utf-8"))

        try:
            if (
                deserialized_config["Credentials"]["Type"]
                == AWSStaticCredentials.type()
            ):
                credentials = AWSStaticCredentials(
                    deserialized_config["Credentials"]["AccessKeyId"],
                    deserialized_config["Credentials"]["SecretKey"],
                )
            elif (
                deserialized_config["Credentials"]["Type"]
                == AWSAssumeRoleCredentials.type()
            ):
                credentials = AWSAssumeRoleCredentials()
            else:
                raise ValueError("Invalid Credentials Type")

            return DynamodbConfig(
                region=deserialized_config["Region"],
                credentials=credentials,
                table_tags=deserialized_config.get("Tags"),
            )
        except KeyError as e:
            raise ValueError(f"Missing key in deserialized config: {e}")

    def validate_table_tags(self, table_tags: Optional[dict]) -> list:
        """
        Validates that:
        - Keys are at most 128 Unicode characters.
        - Values are at most 256 Unicode characters.
        - Keys and values contain only allowed characters.
        - Keys do not start with "aws".

        Returns a list of validation errors. If the list is empty, the dictionary is valid.
        """
        if table_tags is None:
            return []
        allowed_pattern = re.compile(r"^[a-zA-Z0-9\s+\-=._:/]+$")
        errors = []

        for key, value in table_tags.items():
            if not isinstance(key, str) or not isinstance(value, str):
                errors.append(
                    f"Both keys and values must be strings. Invalid pair: ({key}, {value})"
                )
                continue  # Skip further validation for this key-value pair

            if len(key) > 128:
                errors.append(
                    f"Key '{key}' exceeds the maximum length of 128 characters."
                )

            if len(value) > 256:
                errors.append(
                    f"Value for key '{key}' exceeds the maximum length of 256 characters."
                )

            if not allowed_pattern.match(key):
                errors.append(f"Key '{key}' contains invalid characters.")

            if not allowed_pattern.match(value):
                errors.append(f"Value '{value}' contains invalid characters.")

            if key.startswith("aws"):
                errors.append(f"Key '{key}' cannot start with 'aws'.")

        return errors


@typechecked
@dataclass
class MongoDBConfig:
    username: str
    password: str
    host: str
    port: str
    database: str
    throughput: int

    def software(self) -> str:
        return "mongodb"

    def type(self) -> str:
        return "MONGODB_ONLINE"

    def serialize(self) -> bytes:
        config = {
            "Username": self.username,
            "Password": self.password,
            "Host": self.host,
            "Port": self.port,
            "Database": self.database,
            "Throughput": self.throughput,
        }
        return bytes(json.dumps(config), "utf-8")

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, MongoDBConfig):
            return False
        return (
            self.username == __value.username
            and self.password == __value.password
            and self.host == __value.host
            and self.port == __value.port
            and self.database == __value.database
            and self.throughput == __value.throughput
        )
