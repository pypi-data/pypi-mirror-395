# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Credential classes for various cloud providers and services.
"""

import json
import os
import re
import sys
from dataclasses import dataclass, field
from typing import Union

from typeguard import typechecked


def read_file(file_path: str) -> str:
    """Read file content as string."""
    with open(file_path, "r") as f:
        return f.read()


@typechecked
@dataclass
class AWSStaticCredentials:
    """
    Static Credentials for an AWS services.

    **Example**
    ```
    aws_credentials = ff.AWSStaticCredentials(
        access_key="<AWS_ACCESS_KEY>",
        secret_key="<AWS_SECRET_KEY>"
    )
    ```

    Args:
        access_key (str): AWS Access Key.
        secret_key (str): AWS Secret Key.
    """

    access_key: str = field(default="")
    secret_key: str = field(default="")
    _type: str = field(default="AWS_STATIC_CREDENTIALS")

    def __post_init__(
        self,
    ):
        if self.access_key == "":
            raise Exception("'AWSStaticCredentials' access_key cannot be empty")

        if self.secret_key == "":
            raise Exception("'AWSStaticCredentials' secret_key cannot be empty")

    @staticmethod
    def type() -> str:
        return "AWS_STATIC_CREDENTIALS"

    def config(self):
        return {
            "AccessKeyId": self.access_key,
            "SecretKey": self.secret_key,
            "Type": self._type,
        }


@typechecked
@dataclass
class AWSAssumeRoleCredentials:
    """
    Assume Role Credentials for an AWS services.

    If an IAM role for service account (IRSA) has been configured, the default credentials provider chain
        will be used to get the credentials stored on the pod. See the following link for more information:
        https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html

    **Example**
    ```
    aws_credentials = ff.AWSAssumeRoleCredentials()
    ```
    """

    _type: str = field(default="AWS_ASSUME_ROLE_CREDENTIALS")

    @staticmethod
    def type() -> str:
        return "AWS_ASSUME_ROLE_CREDENTIALS"

    def config(self):
        return {
            "Type": self._type,
        }


@typechecked
@dataclass
class GCPCredentials:
    def __init__(
        self, project_id: str, credentials_path: str = "", credential_json: dict = None
    ):
        """
        Credentials for an GCP.

        **Example**
        ```
        gcp_credentials = ff.GCPCredentials(
            project_id="<project_id>",
            credentials_path="<path_to_credentials>"
        )
        ```

        Args:
            project_id (str): The project id.
            credentials_path (str): The path to the credentials file.
        """
        if project_id == "":
            raise Exception("'GCPCredentials' project_id cannot be empty")

        self.project_id = project_id
        self.credentials_path = credentials_path

        if self.credentials_path == "" and credential_json is None:
            raise ValueError(
                "Either a path to credentials or json credentials must be provided"
            )
        elif self.credentials_path != "" and credential_json is not None:
            raise ValueError(
                "Only one of credentials_path or credentials_json can be provided"
            )
        elif self.credentials_path != "" and credential_json is None:
            if not os.path.isfile(credentials_path):
                raise Exception(
                    f"'GCPCredentials' credentials_path '{credentials_path}' file not found"
                )
            with open(credentials_path) as f:
                self.credentials = json.load(f)
        else:
            self.credentials = credential_json

    def type(self):
        return "GCPCredentials"

    def config(self):
        return {
            "ProjectId": self.project_id,
            "JSON": self.credentials,
        }

    def to_json(self):
        return self.credentials


@typechecked
@dataclass
class BasicCredentials:
    def __init__(
        self,
        username: str,
        password: str = "",
    ):
        """
        Credentials for an EMR cluster.

        **Example**
        ```
        creds = ff.BasicCredentials(
            username="<username>",
            password="<password>",
        )

        hdfs = ff.register_hdfs(
            name="hdfs",
            credentials=creds,
            ...
        )
        ```

        Args:
            username (str): the username of account.
            password (str): the password of account (optional).
        """
        self.username = username
        self.password = password

    def type(self):
        return "BasicCredential"

    def config(self):
        return {
            "Username": self.username,
            "Password": self.password,
        }


@typechecked
@dataclass
class KerberosCredentials:
    def __init__(
        self,
        username: str,
        password: str,
        krb5s_file: str,
    ):
        """
        Credentials for an EMR cluster.

        **Example**
        ```
        kerberos = ff.KerberosCredentials(
            username="<username>",
            password="<password>",
            krb5s_file="<path/to/krb5s_file>",
        )

        hdfs = ff.register_hdfs(
            name="hdfs",
            credentials=kerberos,
            ...
        )
        ```

        Args:
            username (str): the username of account.
            password (str): the password of account.
            krb5s_file (str): the path to krb5s file.
        """
        self.username = username
        self.password = password
        self.krb5s_conf = read_file(krb5s_file)

    def type(self):
        return "KerberosCredential"

    def config(self):
        return {
            "Username": self.username,
            "Password": self.password,
            "Krb5Conf": self.krb5s_conf,
        }


# Constants for Pyspark Versions
MAJOR_VERSION = "3"
MINOR_VERSIONS = ["9", "10", "11", "12"]


@typechecked
@dataclass
class DatabricksCredentials:
    """
    Credentials for a Databricks cluster.

    **Example**
    ```
    databricks = ff.DatabricksCredentials(
        username="<my_username>",
        password="<my_password>",
        host="<databricks_hostname>",
        token="<databricks_token>",
        cluster_id="<databricks_cluster>",
    )

    spark = ff.register_spark(
        name="spark",
        executor=databricks,
        ...
    )
    ```

    Args:
        username (str): Username for a Databricks cluster.
        password (str): Password for a Databricks cluster.
        host (str): The hostname of a Databricks cluster.
        token (str): The token for a Databricks cluster.
        cluster_id (str): ID of an existing Databricks cluster.
    """

    username: str = ""
    password: str = ""
    host: str = ""
    token: str = ""
    cluster_id: str = ""

    def __post_init__(self):
        host_token_provided = (
            self.username == ""
            and self.password == ""
            and self.host != ""
            and self.token != ""
        )
        username_password_provided = (
            self.username != ""
            and self.password != ""
            and self.host == ""
            and self.token == ""
        )

        if (
            not host_token_provided
            and not username_password_provided
            or host_token_provided
            and username_password_provided
        ):
            raise Exception(
                "The DatabricksCredentials requires only one credentials set ('username' and 'password' or 'host' and 'token' set.)"
            )

        if not self.cluster_id:
            raise Exception("Cluster_id of existing cluster must be provided")

        if not self._validate_cluster_id():
            raise ValueError(
                f"Invalid cluster_id: expected id in the format 'xxxx-xxxxxx-xxxxxxxx' but received '{self.cluster_id}'"
            )

        if self.host and not self._validate_token():
            raise ValueError(
                f"Invalid token: expected token in the format 'dapi' + 32 alphanumeric characters (optionally ending with '-' and 1 alphanumeric character) but received '{self.token}'"
            )

    def _validate_cluster_id(self):
        cluster_id_regex = r"^\w{4}-\w{6}-\w{8}$"
        return re.match(cluster_id_regex, self.cluster_id)

    def _validate_token(self):
        token_regex = r"^dapi[a-zA-Z0-9]{32}(-[a-zA-Z0-9])?$"
        return re.match(token_regex, self.token)

    def type(self):
        return "DATABRICKS"

    def config(self):
        return {
            "Username": self.username,
            "Password": self.password,
            "Host": self.host,
            "Token": self.token,
            "Cluster": self.cluster_id,
        }


@typechecked
@dataclass
class EMRCredentials:
    def __init__(
        self,
        emr_cluster_id: str,
        emr_cluster_region: str,
        credentials: Union[AWSStaticCredentials, AWSAssumeRoleCredentials],
    ):
        """
        Credentials for an EMR cluster.

        **Example**
        ```
        emr = ff.EMRCredentials(
            emr_cluster_id="<cluster_id>",
            emr_cluster_region="<cluster_region>",
            credentials="<AWS_Credentials>",
        )

        spark = ff.register_spark(
            name="spark",
            executor=emr,
            ...
        )
        ```

        Args:
            emr_cluster_id (str): ID of an existing EMR cluster.
            emr_cluster_region (str): Region of an existing EMR cluster.
            credentials (Union[AWSStaticCredentials, AWSAssumeRoleCredentials]): Credentials for an AWS account with access to the cluster
        """
        self.emr_cluster_id = emr_cluster_id
        self.emr_cluster_region = emr_cluster_region
        self.credentials = credentials

    def type(self):
        return "EMR"

    def config(self):
        return {
            "ClusterName": self.emr_cluster_id,
            "ClusterRegion": self.emr_cluster_region,
            "Credentials": self.credentials.config(),
        }


@typechecked
@dataclass
class SparkCredentials:
    def __init__(
        self,
        master: str,
        deploy_mode: str,
        python_version: str,
        core_site_path: str = "",
        yarn_site_path: str = "",
    ):
        """
        Credentials for a Generic Spark Cluster

        **Example**
        ```
        spark_credentials = ff.SparkCredentials(
            master="yarn",
            deploy_mode="cluster",
            python_version="3.7.12",
            core_site_path="core-site.xml",
            yarn_site_path="yarn-site.xml"
        )

        spark = ff.register_spark(
            name="spark",
            executor=spark_credentials,
            ...
        )
        ```

        Args:
            master (str): The hostname of the Spark cluster. (The same that would be passed to `spark-submit`).
            deploy_mode (str): The deploy mode of the Spark cluster. (The same that would be passed to `spark-submit`).
            python_version (str): The Python version running on the cluster. Supports 3.9-3.12
            core_site_path (str): The path to the core-site.xml file. (For Yarn clusters only)
            yarn_site_path (str): The path to the yarn-site.xml file. (For Yarn clusters only)
        """
        self.master = master.lower()
        self.deploy_mode = deploy_mode.lower()
        self.core_site_path = core_site_path
        self.yarn_site_path = yarn_site_path

        if self.deploy_mode != "cluster" and self.deploy_mode != "client":
            raise Exception(
                f"Spark does not support '{self.deploy_mode}' deploy mode. It only supports 'cluster' and 'client'."
            )

        self.python_version = self._verify_python_version(
            self.deploy_mode, python_version
        )

        self._verify_yarn_config()

    def _verify_python_version(self, deploy_mode, version):
        if deploy_mode == "cluster" and version == "":
            client_python_version = sys.version_info
            client_major = str(client_python_version.major)
            client_minor = str(client_python_version.minor)

            if client_major != MAJOR_VERSION:
                client_major = "3"
            if client_minor not in MINOR_VERSIONS:
                client_minor = "7"

            version = f"{client_major}.{client_minor}"

        if version.count(".") == 2:
            major, minor, _ = version.split(".")
        elif version.count(".") == 1:
            major, minor = version.split(".")
        else:
            raise Exception(
                "Please specify your Python version on the Spark cluster. Accepted formats: Major.Minor or Major.Minor.Patch; ex. '3.9' or '3.9.16"
            )

        if major != MAJOR_VERSION or minor not in MINOR_VERSIONS:
            raise Exception(
                f"The Python version {version} is not supported. Currently, supported versions are 3.9-3.12."
            )

        """
        The Python versions on the Docker image are 3.9.16, 3.10.10, and 3.11.2.
        This conditional statement sets the patch number based on the minor version.
        """
        if minor == "10":
            patch = "10"
        elif minor == "11":
            patch = "2"
        else:
            patch = "16"

        return f"{major}.{minor}.{patch}"

    def _verify_yarn_config(self):
        if self.master == "yarn" and (
            self.core_site_path == "" or self.yarn_site_path == ""
        ):
            raise Exception(
                "Yarn requires core-site.xml and yarn-site.xml files."
                "Please copy these files from your Spark instance to local, then provide the local path in "
                "core_site_path and yarn_site_path. "
            )

    def type(self):
        return "SPARK"

    def config(self):
        core_site = (
            "" if self.core_site_path == "" else open(self.core_site_path, "r").read()
        )
        yarn_site = (
            "" if self.yarn_site_path == "" else open(self.yarn_site_path, "r").read()
        )

        return {
            "Master": self.master,
            "DeployMode": self.deploy_mode,
            "PythonVersion": self.python_version,
            "CoreSite": core_site,
            "YarnSite": yarn_site,
        }


# Type alias for executor credentials
ExecutorCredentials = Union[DatabricksCredentials, EMRCredentials, SparkCredentials]
