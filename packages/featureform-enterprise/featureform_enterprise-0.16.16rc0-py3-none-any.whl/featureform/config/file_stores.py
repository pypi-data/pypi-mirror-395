# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Configuration classes for file store providers.
"""

import json
from dataclasses import dataclass, field
from typing import List, Optional, Union

from typeguard import typechecked

from ..utils import is_valid_url
from .credentials import (
    AWSAssumeRoleCredentials,
    AWSStaticCredentials,
    BasicCredentials,
    GCPCredentials,
    KerberosCredentials,
)


@typechecked
@dataclass
class S3StoreConfig:
    bucket_path: str
    bucket_region: str
    credentials: Union[AWSStaticCredentials, AWSAssumeRoleCredentials]
    path: str = ""

    def __post_init__(self):
        # Validate that the bucket_path does not end with a slash
        if self.bucket_path.endswith("/"):
            raise ValueError("The 'bucket_path' cannot end with '/'.")

    def software(self) -> str:
        return "S3"

    def type(self) -> str:
        return "S3"

    def serialize(self) -> bytes:
        config = self.config()
        return bytes(json.dumps(config), "utf-8")

    def config(self):
        return {
            "Credentials": self.credentials.config(),
            "BucketRegion": self.bucket_region,
            "BucketPath": self.bucket_path,
            "Path": self.path,
        }

    def store_type(self):
        return self.type()


@typechecked
@dataclass
class GCSFileStoreConfig:
    credentials: GCPCredentials
    bucket_name: str
    bucket_path: str = ""

    def software(self) -> str:
        return "gcs"

    def type(self) -> str:
        return "GCS"

    def serialize(self) -> bytes:
        config = {
            "BucketName": self.bucket_name,
            "BucketPath": self.bucket_path,
            "Credentials": self.credentials.config(),
        }
        return bytes(json.dumps(config), "utf-8")

    def config(self):
        return {
            "BucketName": self.bucket_name,
            "BucketPath": self.bucket_path,
            "Credentials": self.credentials.config(),
        }

    def store_type(self):
        return self.type()


@typechecked
@dataclass
class AzureFileStoreConfig:
    account_name: str
    account_key: str
    container_name: str
    root_path: str

    def software(self) -> str:
        return "azure"

    def type(self) -> str:
        return "AZURE"

    def serialize(self) -> bytes:
        config = {
            "AccountName": self.account_name,
            "AccountKey": self.account_key,
            "ContainerName": self.container_name,
            "Path": self.root_path,
        }
        return bytes(json.dumps(config), "utf-8")

    def config(self):
        return {
            "AccountName": self.account_name,
            "AccountKey": self.account_key,
            "ContainerName": self.container_name,
            "Path": self.root_path,
        }

    def store_type(self):
        return self.type()


@typechecked
@dataclass
class VaultConfig:
    address: str
    token: str
    mount_path: str = "secret"
    default_secret_path: str = ""

    def __post_init__(self):
        if not self.address:
            raise ValueError("The 'address' field cannot be empty.")
        if not self.token:
            raise ValueError("The 'token' field cannot be empty.")
        if not self.mount_path:
            raise ValueError("The 'mount_path' field cannot be empty.")

        if not is_valid_url(self.address):
            raise ValueError(
                "The 'address' field must be in the form of schema://host:port"
            )

    def software(self) -> str:
        return "vault"

    def type(self) -> str:
        return "VAULT"

    def config(self):
        return {
            "Address": self.address,
            "Token": self.token,
            "MountPath": self.mount_path,
            "DefaultSecretPath": self.default_secret_path,
        }

    def serialize(self) -> bytes:
        return bytes(json.dumps(self.config()), "utf-8")

    @classmethod
    def deserialize(cls, json_bytes: bytes) -> "VaultConfig":
        config = json.loads(json_bytes)
        return cls(
            address=config["Address"],
            token=config["Token"],
            mount_path=config["MountPath"],
            default_secret_path=config["DefaultSecretPath"],
        )


@typechecked
@dataclass
class KafkaConfig:
    bootstrap_servers: List[str]
    use_msk_iam_auth: bool = False
    options: Optional[dict] = field(default_factory=dict)

    def software(self) -> str:
        return "kafka"

    def type(self) -> str:
        return "KAFKA"

    def config(self):
        return {
            "BootstrapServers": self.bootstrap_servers,
            "UseMSKIAMAuth": self.use_msk_iam_auth,
            "Options": self.options,
        }

    def serialize(self) -> bytes:
        return bytes(json.dumps(self.config()), "utf-8")

    @classmethod
    def deserialize(cls, json_str: bytes) -> "KafkaConfig":
        config = json.loads(json_str)
        return cls(
            bootstrap_servers=config["BootstrapServers"],
            use_msk_iam_auth=config["UseMSKIAMAuth"],
            options=config.get("Options"),
        )


def read_file(file_path: str) -> str:
    """Read file content as string."""
    with open(file_path, "r") as f:
        return f.read()


@typechecked
@dataclass
class HDFSConfig:
    def __init__(
        self,
        host: str,
        port: str,
        path: str,
        hdfs_site_file: str = "",
        core_site_file: str = "",
        hdfs_site_contents: str = "",
        core_site_contents: str = "",
        credentials: Union[BasicCredentials, KerberosCredentials] = BasicCredentials(
            ""
        ),
    ):
        bucket_path_ends_with_slash = len(path) != 0 and path[-1] == "/"

        if bucket_path_ends_with_slash:
            raise Exception("The 'bucket_path' cannot end with '/'.")

        self.path = path
        self.host = host
        self.port = port
        self.credentials = credentials

        self.hdfs_site_conf = self.__get_hdfs_site_contents(
            hdfs_site_file, hdfs_site_contents
        )
        self.core_site_conf = self.__get_core_site_contents(
            core_site_file, core_site_contents
        )

    def __get_hdfs_site_contents(self, site_file, site_contents):
        return self.__get_site_contents(site_file, site_contents, "hdfs")

    def __get_core_site_contents(self, site_file, site_contents):
        return self.__get_site_contents(site_file, site_contents, "core")

    @staticmethod
    def __get_site_contents(site_file, site_contents, config_type):
        if site_file == "" and site_contents == "":
            raise ValueError(
                f"{config_type} site config must be provided. Either provide a path to the xml file "
                f"({config_type}_site_file) or the contents of the file ({config_type}_site_contents)."
            )

        elif site_file != "" and site_contents != "":
            raise ValueError(
                f"Only one of {config_type}_site_file or {config_type}_site_contents should be provided."
            )

        elif site_file != "" and site_contents == "":
            return read_file(site_file)

        else:
            return site_contents

    def software(self) -> str:
        return "HDFS"

    def type(self) -> str:
        return "HDFS"

    def serialize(self) -> bytes:
        config = self.config()
        return bytes(json.dumps(config), "utf-8")

    def config(self):
        return {
            "Host": self.host,
            "Port": self.port,
            "Path": self.path,
            "HDFSSiteConf": self.hdfs_site_conf,
            "CoreSiteConf": self.core_site_conf,
            "CredentialType": self.credentials.type(),
            "CredentialConfig": self.credentials.config(),
        }

    def store_type(self):
        return self.type()


@typechecked
@dataclass
class OnlineBlobConfig:
    store_type: str
    store_config: dict

    def software(self) -> str:
        return self.store_type

    def type(self) -> str:
        return "BLOB_ONLINE"

    def config(self):
        return self.store_config

    def serialize(self) -> bytes:
        config = {
            "Type": self.store_type,
            "Config": self.store_config,
        }
        return bytes(json.dumps(config), "utf-8")

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, OnlineBlobConfig):
            return False
        return (
            self.store_type == __value.store_type
            and self.store_config == __value.store_config
        )
