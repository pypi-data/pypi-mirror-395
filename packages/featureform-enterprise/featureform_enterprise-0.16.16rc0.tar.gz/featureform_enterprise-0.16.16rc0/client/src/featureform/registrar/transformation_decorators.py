# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Transformation decorator classes for Featureform.

This module contains decorator classes for SQL and DataFrame transformations.
"""

import inspect
import re
from dataclasses import dataclass, field
from datetime import timedelta
from typing import TYPE_CHECKING, Callable, List, Optional, Union

import dill
from typeguard import typechecked

from ..config.compute import EmptySparkFlags, K8sArgs, SparkFlags
from ..config.offline_stores import ResourceSnowflakeConfig
from ..core.exceptions import InvalidSQLQuery
from ..enums import ResourceType
from ..parse import add_variant_to_name, canonicalize_function_definition
from ..resources import (
    DFTransformation,
    PartitionType,
    SourceVariant,
    SQLTransformation,
)
from ..utils.helpers import get_name_variant

if TYPE_CHECKING:
    from . import EntityRegistrar, UserRegistrar


__all__ = [
    "SubscriptableTransformation",
    "SQLTransformationDecorator",
    "DFTransformationDecorator",
]


class SubscriptableTransformation:
    """
    SubscriptableTransformation creates a wrapped decorator that's callable and subscriptable,
    which allows for the following syntax:

    ``` py
    @local.transformation(variant="quickstart")
    def average_user_transaction():
        return "SELECT CustomerID as user_id, avg(TransactionAmount) as avg_transaction_amt from {{transactions.v1}} GROUP BY user_id"

    feature = ff.Feature(average_user_transaction[["user_id", "avg_transaction_amt"]])
    ```

    Given the function type does not implement __getitem__ we need to wrap it in a class that
    enables this behavior while still maintaining the original function signature and behavior.
    """

    def __init__(
        self,
        fn,
        registrar,
        provider,
        decorator_register_resources_method,
        decorator_name_variant_method,
        transformation,
    ):
        # if not self.__has_return_statement(fn):
        #     raise Exception(
        #         "Transformation function seems to be missing a return statement"
        #     )

        self.fn = fn
        self.registrar = registrar
        self.provider = provider
        # Previously, the descriptor protocol was used to apply methods from the decorator classes
        # to instances of SubscriptableTransformation such that a user could call `fn.name_variant()`
        # and receive a tuple of (name, variant) where name was the name of the wrapped function and
        # variant was either the value passed to the decorator or the default value. This was achieved
        # via the following syntax: `self.name_variant = decorator_name_variant_method.__get__(self)`
        # For as-of-yet unknown reasons, this behavior was not working as expected in Python 3.11.2,
        # so the code has been reverted to the original syntax, which simply passes a reference to
        # the decorator methods to the SubscriptableTransformation class.
        self.register_resources = decorator_register_resources_method
        self.name_variant = decorator_name_variant_method
        self.transformation = transformation

    def name_variant(self):
        return self.transformation.name_variant()

    def get_resource_type(self):
        return self.transformation.get_resource_type()

    def to_key(self):
        n, v = self.name_variant()
        return self.get_resource_type(), n, v

    def __getitem__(self, columns: List[str]):
        col_len = len(columns)
        if col_len < 2:
            raise Exception(
                f"Expected 2 columns, but found {col_len}. Missing entity and/or source columns"
            )
        elif col_len > 3:
            raise Exception(
                f"Found unrecognized columns {', '.join(columns[3:])}. Expected 2 required columns and an optional 3rd timestamp column"
            )
        return (self.registrar, self.transformation, columns)

    def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)

    @staticmethod
    def __has_return_statement(fn):
        """
        Parses the function’s source code into an abstract syntax tree
        and then walks through the tree to check for any Return nodes.
        Not full-proof but will at least catch cases on the client.
        """
        tree = ast.parse(inspect.getsource(fn))
        for node in ast.walk(tree):
            if isinstance(node, ast.Return):
                return True
        return False


@dataclass
class SQLTransformationDecorator:
    registrar: "Registrar"
    owner: str
    provider: str
    tags: List[str]
    properties: dict
    run: str = ""
    variant: str = ""
    name: str = ""
    schedule: str = ""
    incremental: bool = False
    incremental_inputs: list = field(default_factory=list)
    is_streaming: bool = False
    streaming_inputs: list = field(default_factory=list)
    inputs: list = field(default_factory=list)
    description: str = ""
    args: Union[K8sArgs, None] = None
    query: str = field(default_factory=str, init=False)
    partition_options: Optional[PartitionType] = None
    func_params_to_inputs: dict = field(default_factory=dict, init=False)
    max_job_duration: timedelta = timedelta(hours=48)
    spark_flags: SparkFlags = field(default_factory=lambda: EmptySparkFlags)
    resource_snowflake_config: Optional[ResourceSnowflakeConfig] = None

    def __post_init__(self):
        if self.inputs is None:
            self.inputs = []
        if self.incremental_inputs is None:
            self.incremental_inputs = []
        if self.streaming_inputs is None:
            self.streaming_inputs = []

    def __call__(self, fn: Callable[[], str]):
        if self.description == "" and fn.__doc__ is not None:
            self.description = fn.__doc__
        if self.name == "":
            self.name = fn.__name__

        func_params = inspect.signature(fn).parameters

        if len(func_params) > 0:
            if len(func_params) > len(self.inputs):
                raise ValueError(
                    f"Transformation function has more parameters than inputs. \n"
                    f"Make sure each function parameter has a corresponding input in the decorator."
                )

            if len(func_params) < len(self.inputs):
                raise ValueError(
                    f"Too many inputs for transformation function. Expected {len(func_params)} inputs, but found {len(self.inputs)}.\n"
                )

            if not isinstance(self.inputs, list):
                raise ValueError("Dataframe transformation inputs must be a list")

            self.func_params_to_inputs = dict(zip(func_params, self.inputs))

            self.__set_query(fn(*self.inputs))
        else:
            self.__set_query(fn())

        self.registrar.map_client_object_to_resource(self, self.to_source())
        self.registrar.add_resource(self.to_source())
        return SubscriptableTransformation(
            fn,
            self.registrar,
            self.provider,
            self.register_resources,
            self.name_variant,
            self,
        )

    @typechecked
    def __set_query(self, query: str):
        if query == "":
            raise ValueError("Query cannot be an empty string")

        self._assert_query_contains_at_least_one_source(query)
        if len(self.inputs) > 0:
            # if inputs are specified, then the query will be resolved at the time of creation (when #kwargs is called)
            self.query = query
        else:
            self.query = add_variant_to_name(query, self.run)

    def to_source(self) -> SourceVariant:
        return SourceVariant(
            created=None,
            name=self.name,
            variant=self.variant,
            definition=SQLTransformation(
                query=self.query,
                args=self.args,
                func_params_to_inputs=self.func_params_to_inputs,
                is_incremental=self.incremental,
                incremental_inputs=self.incremental_inputs,
                is_streaming=self.is_streaming,
                streaming_inputs=self.streaming_inputs,
                partition_options=self.partition_options,
                spark_flags=self.spark_flags,
                resource_snowflake_config=self.resource_snowflake_config,
            ),
            owner=self.owner,
            schedule=self.schedule,
            provider=self.provider,
            description=self.description,
            tags=self.tags,
            properties=self.properties,
            max_job_duration=self.max_job_duration,
        )

    def name_variant(self):
        return (self.name, self.variant)

    def get_resource_type(self):
        return ResourceType.SOURCE_VARIANT

    def register_resources(
        self,
        entity: Union[str, "EntityRegistrar"],
        entity_column: str,
        owner: Union[str, "UserRegistrar"] = "",
        inference_store: Union[str, "OnlineProvider", "FileStoreProvider"] = "",
        features: List["ColumnMapping"] = None,
        labels: List["ColumnMapping"] = None,
        timestamp_column: str = "",
        description: str = "",
        schedule: str = "",
    ):
        return self.registrar.register_column_resources(
            source=self,
            entity=entity,
            entity_column=entity_column,
            owner=owner,
            inference_store=inference_store,
            features=features,
            labels=labels,
            timestamp_column=timestamp_column,
            description=description,
            schedule=schedule,
            client_object=self,
        )

    @staticmethod
    def _assert_query_contains_at_least_one_source(query):
        # Checks to verify that the query contains a FROM {{ name.variant }}

        # the pattern pulls the string within the double curly braces
        pattern = r"\{\{\s*(.*?)\s*\}\}"
        matches = re.findall(pattern, query)
        if len(matches) == 0:
            raise InvalidSQLQuery(query, "No source specified.")

        for m in matches:
            name, variant = get_name_variant(query, m)
            if name == "":
                raise InvalidSQLQuery(query, "Source name is empty.")

            # Check for invalid characters in the source name and variant
            if name.startswith(" ") or name.endswith(" "):
                raise InvalidSQLQuery(
                    query, "Source name cannot start or end with a space."
                )
            if variant.startswith(" ") or variant.endswith(" "):
                raise InvalidSQLQuery(
                    query, "Source variant cannot start or end with a space."
                )

            if name.startswith("_") or name.endswith("_"):
                raise InvalidSQLQuery(
                    query, "Source name cannot start or end with an underscore."
                )
            if variant.startswith("_") or variant.endswith("_"):
                raise InvalidSQLQuery(
                    query, "Source variant cannot start or end with an underscore."
                )

            if "__" in name or "__" in variant:
                raise InvalidSQLQuery(
                    query,
                    "Source name and variant cannot contain consecutive underscores.",
                )


# get_name_variant moved to utils/helpers.py


@dataclass
class DFTransformationDecorator:
    registrar: "Registrar"
    owner: str
    provider: str
    tags: List[str]
    properties: dict
    variant: str = ""
    name: str = ""
    description: str = ""
    incremental: bool = False
    incremental_inputs: list = field(default_factory=list)
    partition_options: Optional[PartitionType] = None
    inputs: list = field(default_factory=list)
    args: Union[K8sArgs, None] = None
    source_text: str = ""
    canonical_func_text: str = ""
    query: bytes = field(default_factory=bytes, init=False)
    max_job_duration: timedelta = timedelta(hours=48)
    spark_flags: SparkFlags = field(default_factory=lambda: EmptySparkFlags)

    def __call__(self, fn):
        if self.description == "" and fn.__doc__ is not None:
            self.description = fn.__doc__
        if self.name == "":
            self.name = fn.__name__

        func_params = inspect.signature(fn).parameters
        if len(func_params) > len(self.inputs):
            raise ValueError(
                f"Transformation function has more parameters than inputs. \n"
                f"Make sure each function parameter has a corresponding input in the decorator."
            )

        if not isinstance(self.inputs, list):
            raise ValueError("Dataframe transformation inputs must be a list")

        # Check that the function doesn't have free variables.
        # A free variable is one that is captured from the environment. This is an issue
        # because it's not serialized with the function, so later when it's deserialized
        # and attempted to run, it will complain about unbound variables.
        if fn.__code__.co_freevars:
            raise ValueError(
                f"a dataframe transformation must be top-level and self-contained; free vars: {fn.__code__.co_freevars}"
            )

        # check that input isn't self referencing
        for nv in self.inputs:
            if isinstance(
                nv, tuple
            ):  # TODO all that should be called here is name_variant()
                n, v = nv
            else:
                n, v = nv.name_variant()
            if self.name is n and self.variant is v:
                raise ValueError(
                    f"Transformation cannot be input for itself: {self.name} {self.variant}"
                )
        self.query = dill.dumps(fn.__code__)
        self.source_text = dill.source.getsource(fn)
        self.canonical_func_text = canonicalize_function_definition(fn)
        self.registrar.map_client_object_to_resource(self, self.to_source())
        self.registrar.add_resource(self.to_source())
        return SubscriptableTransformation(
            fn,
            self.registrar,
            self.provider,
            self.register_resources,
            self.name_variant,
            self,
        )

    def to_source(self) -> SourceVariant:
        return SourceVariant(
            created=None,
            name=self.name,
            variant=self.variant,
            definition=DFTransformation(
                query=self.query,
                inputs=self.inputs,
                args=self.args,
                source_text=self.source_text,
                canonical_func_text=self.canonical_func_text,
                spark_flags=self.spark_flags,
                is_incremental=self.incremental,
                incremental_inputs=self.incremental_inputs,
                partition_options=self.partition_options,
            ),
            owner=self.owner,
            provider=self.provider,
            description=self.description,
            tags=self.tags,
            properties=self.properties,
            max_job_duration=self.max_job_duration,
        )

    def name_variant(self):
        return (self.name, self.variant)

    def register_resources(
        self,
        entity: Union[str, "EntityRegistrar"],
        entity_column: str,
        owner: Union[str, "UserRegistrar"] = "",
        inference_store: Union[str, "OnlineProvider", "FileStoreProvider"] = "",
        features: List["ColumnMapping"] = None,
        labels: List["ColumnMapping"] = None,
        timestamp_column: str = "",
        description: str = "",
    ):
        return self.registrar.register_column_resources(
            source=self,
            entity=entity,
            entity_column=entity_column,
            owner=owner,
            inference_store=inference_store,
            features=features,
            labels=labels,
            timestamp_column=timestamp_column,
            description=description,
            client_object=self,
        )


# ColumnSourceRegistrar, ResourceRegistrar, and ModelRegistrar are imported from .registrar
