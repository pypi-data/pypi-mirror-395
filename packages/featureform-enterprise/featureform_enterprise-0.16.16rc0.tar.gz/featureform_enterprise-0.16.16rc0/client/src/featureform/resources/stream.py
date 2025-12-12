# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Stream resource classes for Featureform.

This module contains classes for defining and managing streaming resources.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Dict, List, Optional, Tuple, Union

from typeguard import typechecked

from ..enums import OperationType, ResourceType, ScalarType
from ..proto import metadata_pb2 as pb
from .provider import Properties

if TYPE_CHECKING:
    from ..providers import OfflineProvider, OnlineProvider


class BaseStream(ABC):
    def __init__(
        self,
        name: str,
        value_type: str,
        entity: str,
        owner: str,
        offline_provider: str,
        description: str,
        variant: str,
        tags: Union[list, None] = None,
        properties: Union[dict, None] = None,
        status: str = "NO_STATUS",
        error: Optional[str] = None,
    ):
        self.name = name
        self.value_type = value_type
        self.entity = entity
        self.owner = owner
        self.offline_provider = offline_provider
        self.description = description
        self.variant = variant
        self.tags = [] if tags is None else tags
        self.properties = {} if properties is None else properties
        self.status = status
        self.error = error

    def __post_init__(self):
        col_types = [member.value for member in ScalarType]
        if self.value_type not in col_types:
            raise ValueError(
                f"Invalid feature type ({self.value_type}) must be one of: {col_types}"
            )

    @staticmethod
    @abstractmethod
    def get_resource_type() -> ResourceType:
        raise NotImplementedError

    @abstractmethod
    def get(self, stub) -> "Stream":
        raise NotImplementedError

    @abstractmethod
    def _create(self, req_id, stub) -> Tuple[None, None]:
        raise NotImplementedError

    @staticmethod
    def operation_type() -> OperationType:
        return OperationType.CREATE

    def _create_local(self, db) -> None:
        pass

    def get_status(self):
        return ResourceStatus(self.status)

    def is_ready(self):
        return self.status == ResourceStatus.READY.value

    def __eq__(self, other):
        for attribute in vars(self):
            if getattr(self, attribute) != getattr(other, attribute):
                return False
        return True


@typechecked
class StreamFeature(BaseStream):
    inference_store: str = ""

    def __init__(self, inference_store: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inference_store = inference_store

    @staticmethod
    def get_resource_type() -> ResourceType:
        return ResourceType.FEATURE_VARIANT

    def get(self, stub) -> "StreamFeature":
        name_variant = pb.NameVariant(name=self.name, variant=self.variant)
        stream_feature = next(stub.GetFeatureVariants(iter([name_variant])))

        return StreamFeature(
            name=stream_feature.name,
            variant=stream_feature.variant,
            value_type=stream_feature.type,
            entity=stream_feature.entity,
            owner=stream_feature.owner,
            inference_store=stream_feature.provider,
            offline_provider=stream_feature.stream.offline_provider,
            description=stream_feature.description,
            tags=list(stream_feature.tags.tag),
            properties=dict(stream_feature.properties.property.items()),
            status=stream_feature.status.Status._enum_type.values[
                stream_feature.status.status
            ].name,
            error=stream_feature.status.error_message,
        )

    def _create(self, req_id, stub) -> Tuple[None, None]:
        serialized = pb.FeatureVariant(
            name=self.name,
            variant=self.variant,
            type=self.value_type,
            entity=self.entity,
            owner=self.owner,
            description=self.description,
            provider=self.inference_store,
            stream=pb.Stream(
                offline_provider=self.offline_provider,
            ),
            mode=ComputationMode.STREAMING.proto(),
            tags=pb.Tags(tag=self.tags),
            properties=Properties(self.properties).serialized,
        )
        stub.CreateFeatureVariant(serialized)
        return None, None


@typechecked
class StreamLabel(BaseStream):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def get_resource_type() -> ResourceType:
        return ResourceType.LABEL_VARIANT

    def get(self, stub) -> "StreamLabel":
        name_variant = pb.NameVariant(name=self.name, variant=self.variant)
        stream_label = next(stub.GetLabelVariants(iter([name_variant])))

        return StreamLabel(
            name=stream_label.name,
            variant=stream_label.variant,
            value_type=stream_label.type,
            entity=stream_label.entity,
            owner=stream_label.owner,
            offline_provider=stream_label.stream.offline_provider,
            description=stream_label.description,
            tags=list(stream_label.tags.tag),
            properties=dict(stream_label.properties.property.items()),
            status=stream_label.status.Status._enum_type.values[
                stream_label.status.status
            ].name,
            error=stream_label.status.error_message,
        )

    def _create(self, req_id, stub) -> Tuple[None, None]:
        serialized = pb.LabelVariant(
            name=self.name,
            variant=self.variant,
            type=self.value_type,
            entity=self.entity,
            owner=self.owner,
            description=self.description,
            provider=self.offline_provider,
            stream=pb.Stream(
                offline_provider=self.offline_provider,
            ),
            tags=pb.Tags(tag=self.tags),
            properties=Properties(self.properties).serialized,
        )
        stub.CreateLabelVariant(serialized)
        return None, None


class FeatureStreamResource:
    def __init__(
        self,
        type: Union[ScalarType, str],
        offline_store: Union[str, "OfflineProvider"],
        inference_store: Union[str, "OnlineProvider"],
        variant: str = "",
        owner: str = "",
        description: str = "",
        tags: Optional[List[str]] = None,
        properties: Optional[Dict[str, str]] = None,
    ) -> None:
        self.name = ""
        self.entity = ""
        self.type = type if isinstance(type, str) else type.value
        self.offline_provider = offline_store
        self.inference_store = inference_store
        self.variant = variant
        self.owner = owner
        self.description = description
        self.tags = tags or []
        self.properties = properties or {}

    def register(self) -> None:
        register_feature_stream(
            name=self.name,
            entity=self.entity,
            type=self.type,
            offline_provider=self.offline_provider,
            inference_store=self.inference_store,
            variant=self.variant,
            owner=self.owner,
            description=self.description,
            tags=self.tags,
            properties=self.properties,
        )


class LabelStreamResource:
    def __init__(
        self,
        type: Union[ScalarType, str],
        offline_store: Union[str, "OfflineProvider"],
        variant: str = "",
        owner: str = "",
        description: str = "",
        tags: Optional[List[str]] = None,
        properties: Optional[Dict[str, str]] = None,
    ) -> None:
        self.name = ""
        self.entity = ""
        self.type = type if isinstance(type, str) else type.value
        self.offline_provider = offline_store
        self.variant = variant
        self.owner = owner
        self.description = description
        self.tags = tags or []
        self.properties = properties or {}

    def register(self) -> None:
        register_label_stream(
            name=self.name,
            entity=self.entity,
            type=self.type,
            offline_provider=self.offline_provider,
            variant=self.variant,
            owner=self.owner,
            description=self.description,
            tags=self.tags,
            properties=self.properties,
        )
