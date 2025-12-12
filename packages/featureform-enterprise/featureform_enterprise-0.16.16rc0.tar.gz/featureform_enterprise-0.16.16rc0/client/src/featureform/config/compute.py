# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Configuration classes for compute providers (Spark, K8s).
"""

import json
from dataclasses import dataclass, field
from typing import Dict, Optional, Union

from typeguard import typechecked

from ..proto import metadata_pb2 as pb


@dataclass
class SparkFlags:
    spark_params: Dict[str, str] = field(default_factory=dict)
    write_options: Dict[str, str] = field(default_factory=dict)
    table_properties: Dict[str, str] = field(default_factory=dict)

    def serialize(self) -> dict:
        return {
            "SparkParams": self.spark_params,
            "WriteOptions": self.write_options,
            "TableProperties": self.table_properties,
        }

    @classmethod
    def deserialize(cls, config: dict) -> Optional["SparkFlags"]:
        """
        Deserialize a dictionary into a SparkFlags object.

        Args:
            config (dict): The dictionary containing SparkFlags configuration.

        Returns:
            Optional[SparkFlags]: The deserialized SparkFlags object, or None if the config is missing.
        """
        if not config:
            return None
        return cls(
            spark_params=config.get("SparkParams", {}),
            write_options=config.get("WriteOptions", {}),
            table_properties=config.get("TableProperties", {}),
        )

    def to_proto(self) -> pb.SparkFlags:
        return pb.SparkFlags(
            spark_params=[
                pb.SparkParam(key=k, value=v) for k, v in self.spark_params.items()
            ],
            write_options=[
                pb.WriteOption(key=k, value=v) for k, v in self.write_options.items()
            ],
            table_properties=[
                pb.TableProperty(key=k, value=v)
                for k, v in self.table_properties.items()
            ],
        )


EmptySparkFlags = SparkFlags()


@typechecked
@dataclass
class SparkConfig:
    executor_type: str
    executor_config: dict
    store_type: str
    store_config: dict
    kafka_config: Optional[dict] = None
    catalog_type: Optional[str] = None
    catalog_config: Optional[dict] = None
    spark_flags: Optional[SparkFlags] = field(default_factory=lambda: EmptySparkFlags)

    def __post_init__(self):
        if self.spark_flags is None:
            self.spark_flags = EmptySparkFlags

    def software(self) -> str:
        return "spark"

    def type(self) -> str:
        return "SPARK_OFFLINE"

    def serialize(self) -> bytes:
        config = {
            "ExecutorType": self.executor_type,
            "StoreType": self.store_type,
            "ExecutorConfig": self.executor_config,
            "StoreConfig": self.store_config,
            "SparkFlags": self.spark_flags.serialize(),
        }

        if self.catalog_type is not None and self.catalog_config is not None:
            config["CatalogType"] = self.catalog_type
            config["CatalogConfig"] = self.catalog_config

        if self.kafka_config is not None:
            config["KafkaConfig"] = self.kafka_config

        return bytes(json.dumps(config), "utf-8")

    @classmethod
    def deserialize(cls, json_bytes: bytes) -> "SparkConfig":
        deserialized_config = json.loads(json_bytes.decode("utf-8"))

        spark_flags = (
            SparkFlags.deserialize(deserialized_config.get("SparkFlags"))
            if deserialized_config.get("SparkFlags")
            else EmptySparkFlags
        )

        try:
            return cls(
                executor_type=deserialized_config["ExecutorType"],
                executor_config=deserialized_config["ExecutorConfig"],
                store_type=deserialized_config["StoreType"],
                store_config=deserialized_config["StoreConfig"],
                catalog_type=deserialized_config.get("CatalogType"),
                catalog_config=deserialized_config.get("CatalogConfig"),
                spark_flags=spark_flags,
            )
        except KeyError as e:
            raise ValueError(f"Missing expected config key: {e}")


@typechecked
@dataclass
class K8sResourceSpecs:
    cpu_request: str = ""
    cpu_limit: str = ""
    memory_request: str = ""
    memory_limit: str = ""


@typechecked
@dataclass
class K8sArgs:
    # TODO Delete and Deprecate
    docker_image: str
    specs: Union[K8sResourceSpecs, None] = None

    def apply(self, transformation: pb.Transformation):
        transformation.kubernetes_args.docker_image = self.docker_image
        if self.specs is not None:
            transformation.kubernetes_args.specs.cpu_request = self.specs.cpu_request
            transformation.kubernetes_args.specs.cpu_limit = self.specs.cpu_limit
            transformation.kubernetes_args.specs.memory_request = (
                self.specs.memory_request
            )
            transformation.kubernetes_args.specs.memory_limit = self.specs.memory_limit
        return transformation


@typechecked
@dataclass
class K8sConfig:
    store_type: str
    store_config: dict
    docker_image: str = ""

    def software(self) -> str:
        return "k8s"

    def type(self) -> str:
        return "K8S_OFFLINE"

    def serialize(self) -> bytes:
        config = {
            "ExecutorType": "K8S",
            "ExecutorConfig": {"docker_image": self.docker_image},
            "StoreType": self.store_type,
            "StoreConfig": self.store_config,
        }
        return bytes(json.dumps(config), "utf-8")


@typechecked
@dataclass
class EmptyConfig:
    def software(self) -> str:
        return ""

    def type(self) -> str:
        return ""

    def serialize(self) -> bytes:
        return bytes("", "utf-8")

    def deserialize(self, config):
        return self
