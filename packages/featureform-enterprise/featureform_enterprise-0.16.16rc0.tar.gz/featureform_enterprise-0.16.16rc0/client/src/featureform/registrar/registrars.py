# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Registrar classes for Featureform resources.

These classes wrap registered resources and provide convenient methods for
interacting with them.
"""

from typing import TYPE_CHECKING, List, Union

if TYPE_CHECKING:
    from ..enums import ResourceType

# NameVariant type alias
NameVariant = tuple[str, str]


class EntityRegistrar:
    """Wrapper for registered entities."""

    def __init__(self, registrar, entity):
        self.__registrar = registrar
        self.__entity = entity

    def name(self) -> str:
        return self.__entity.name


class UserRegistrar:
    """Wrapper for registered users."""

    def __init__(self, registrar, user):
        self.__registrar = registrar
        self.__user = user

    def name(self) -> str:
        return self.__user.name

    def make_default_owner(self):
        self.__registrar.set_default_owner(self.name())


class SourceRegistrar:
    """Wrapper for registered sources."""

    def __init__(self, registrar, source):
        self.__registrar = registrar
        self.__source = source

    def id(self) -> NameVariant:
        return self.__source.name, self.__source.variant

    def name_variant(self) -> NameVariant:
        return self.id()

    def registrar(self):
        return self.__registrar

    def source(self):
        return self.__source

    def __eq__(self, other):
        return self.__source == other.__source and self.__registrar == other.__registrar

    def get_resource_type(self) -> "ResourceType":
        return self.__source.get_resource_type()


class ColumnSourceRegistrar(SourceRegistrar):
    """Wrapper for column-based sources that support subscript notation."""

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
        return (self.registrar(), self, columns)

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
        """
        Registers a features and/or labels that can be used in training sets or served.

        **Examples**:
        ``` py
        average_user_transaction.register_resources(
            entity=user,
            entity_column="CustomerID",
            inference_store=local,
            features=[
                {"name": "avg_transactions", "variant": "quickstart", "column": "TransactionAmount", "type": "float32"},
            ],
        )
        ```

        Args:
            entity (Union[str, EntityRegistrar]): The name to reference the entity by when serving features
            entity_column (str): The name of the column in the source to be used as the entity
            owner (Union[str, UserRegistrar]): The owner of the resource(s)
            inference_store (Union[str, OnlineProvider, FileStoreProvider]): Where to store the materialized feature for serving. (Use the local provider in Localmode)
            features (List[ColumnMapping]): A list of column mappings to define the features
            labels (List[ColumnMapping]): A list of column mappings to define the labels
            timestamp_column: (str): The name of an optional timestamp column in the dataset. Will be used to match the features and labels with point-in-time correctness

        Returns:
            registrar (ResourceRegister): Registrar
        """
        return self.registrar().register_column_resources(
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


class ResourceRegistrar:
    """Wrapper for registered resources (features and labels)."""

    def __init__(self, registrar, features, labels):
        self.__registrar = registrar
        self.__features = features
        self.__labels = labels

    def create_training_set(
        self,
        name: str,
        variant: str = "",
        label: NameVariant = None,
        schedule: str = "",
        features: List[NameVariant] = None,
        resources: List = None,
        owner: Union[str, "UserRegistrar"] = "",
        description: str = "",
    ):
        if len(self.__labels) == 0:
            raise ValueError("A label must be included in a training set")
        if len(self.__features) == 0:
            raise ValueError("A feature must be included in a training set")
        if len(self.__labels) > 1 and label is None:
            raise ValueError("Only one label may be specified in a TrainingSet.")
        if features is not None:
            featureSet = set(
                [(feature["name"], feature["variant"]) for feature in self.__features]
            )
            for feature in features:
                if feature not in featureSet:
                    raise ValueError(f"Feature {feature} not found.")
        else:
            features = [
                (feature["name"], feature["variant"]) for feature in self.__features
            ]
        if label is None:
            label = (self.__labels[0]["name"], self.__labels[0]["variant"])
        else:
            labelSet = set(
                [(label["name"], label["variant"]) for label in self.__labels]
            )
            if label not in labelSet:
                raise ValueError(f"Label {label} not found.")
        return self.__registrar.register_training_set(
            name=name,
            variant=variant,
            label=label,
            features=features,
            resources=resources,
            owner=owner,
            schedule=schedule,
            description=description,
        )

    def features(self):
        return self.__features

    def label(self):
        if isinstance(self.__labels, list):
            if len(self.__labels) > 1:
                raise ValueError(
                    "A resource used has multiple labels. A training set can only have one label"
                )
            elif len(self.__labels) == 1:
                self.__labels = (self.__labels[0]["name"], self.__labels[0]["variant"])
            else:
                self.__labels = ()
        return self.__labels


class ModelRegistrar:
    """Wrapper for registered models."""

    def __init__(self, registrar, model):
        self.__registrar = registrar
        self.__model = model

    def name(self) -> str:
        return self.__model.name
