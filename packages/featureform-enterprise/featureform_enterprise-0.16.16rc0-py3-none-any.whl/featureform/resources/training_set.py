# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Training set resource classes for Featureform.

This module contains classes for defining and managing training sets.
"""

from dataclasses import dataclass, field
from typing import Any, List, Optional, Tuple

from typeguard import typechecked

from ..config import ResourceSnowflakeConfig
from ..enums import OperationType, ResourceStatus, ResourceType, TrainingSetType
from ..operations.equivalence import _get_and_set_equivalent_variant
from ..proto import metadata_pb2 as pb
from .base import NameVariant, ResourceVariant, valid_name_variant
from .provider import Properties, ServerStatus
from .schedule import Schedule


@typechecked
@dataclass
class TrainingSet:
    name: str
    default_variant: str
    variants: List[str]

    def to_dictionary(self):
        return {
            "name": self.name,
            "default_variant": self.default_variant,
            "variants": self.variants,
        }


@typechecked
@dataclass
class TrainingSetVariant(ResourceVariant):
    name: str
    owner: str
    label: Any
    features: List[Any]
    description: str
    variant: str
    feature_lags: list = field(default_factory=list)
    tags: list = field(default_factory=list)
    properties: dict = field(default_factory=dict)
    created: str = None
    schedule: str = ""
    schedule_obj: Schedule = None
    provider: str = ""
    status: str = "NO_STATUS"
    error: Optional[str] = None
    server_status: Optional[ServerStatus] = None
    resource_snowflake_config: Optional[ResourceSnowflakeConfig] = None
    type: TrainingSetType = field(default=TrainingSetType.DYNAMIC)

    def update_schedule(self, schedule) -> None:
        self.schedule_obj = Schedule(
            name=self.name,
            variant=self.variant,
            resource_type=6,
            schedule_string=schedule,
        )
        self.schedule = schedule

    def __post_init__(self):
        from featureform import FeatureColumnResource, LabelColumnResource

        if not isinstance(self.label, LabelColumnResource) and not valid_name_variant(
            self.label
        ):
            raise ValueError("Label must be set")
        if len(self.features) == 0:
            raise ValueError("A training-set must have at least one feature")
        for feature in self.features:
            if not isinstance(
                feature, FeatureColumnResource
            ) and not valid_name_variant(feature):
                raise ValueError("Invalid Feature")

    @staticmethod
    def operation_type() -> OperationType:
        return OperationType.CREATE

    @staticmethod
    def get_resource_type() -> ResourceType:
        return ResourceType.TRAININGSET_VARIANT

    def name_variant(self) -> NameVariant:
        return (self.name, self.variant)

    def get(self, stub):
        return TrainingSetVariant.get_by_name_variant(stub, self.name, self.variant)

    @staticmethod
    def get_by_name_variant(stub, name, variant):
        name_variant = pb.NameVariantRequest(
            name_variant=pb.NameVariant(name=name, variant=variant)
        )
        ts = next(stub.GetTrainingSetVariants(iter([name_variant])))

        return TrainingSetVariant(
            created=None,
            name=ts.name,
            variant=ts.variant,
            owner=ts.owner,
            description=ts.description,
            status=ts.status.Status._enum_type.values[ts.status.status].name,
            label=(ts.label.name, ts.label.variant),
            features=[(f.name, f.variant) for f in ts.features],
            feature_lags=[],
            provider=ts.provider,
            tags=list(ts.tags.tag),
            properties=dict(ts.properties.property.items()),
            error=ts.status.error_message,
            server_status=ServerStatus.from_proto(ts.status),
            resource_snowflake_config=ResourceSnowflakeConfig.from_proto(
                ts.resource_snowflake_config
            ),
            type=TrainingSetType.from_proto(ts.type),
        )

    def _get_and_set_equivalent_variant(self, req_id, stub):
        feature_lags = []
        for lag in self.feature_lags:
            lag_duration = Duration()
            _ = lag_duration.FromTimedelta(lag["lag"])
            feature_lag = pb.FeatureLag(
                feature=lag["feature"],
                variant=lag["variant"],
                name=lag["name"],
                lag=lag_duration,
            )
            feature_lags.append(feature_lag)

        for i, f in enumerate(self.features):
            if hasattr(f, "name_variant"):
                self.features[i] = f.name_variant()

        if hasattr(self.label, "name_variant"):
            self.label = self.label.name_variant()

        serialized = pb.TrainingSetVariantRequest(
            training_set_variant=pb.TrainingSetVariant(
                created=None,
                name=self.name,
                variant=self.variant,
                description=self.description,
                schedule=self.schedule,
                owner=self.owner,
                features=[
                    pb.NameVariant(name=v[0], variant=v[1]) for v in self.features
                ],
                label=pb.NameVariant(name=self.label[0], variant=self.label[1]),
                feature_lags=feature_lags,
                tags=pb.Tags(tag=self.tags),
                properties=Properties(self.properties).serialized,
                status=pb.ResourceStatus(status=pb.ResourceStatus.NO_STATUS),
                provider=self.provider,
                resource_snowflake_config=(
                    self.resource_snowflake_config.to_proto()
                    if self.resource_snowflake_config
                    else None
                ),
                type=self.type.to_proto(),
            ),
            request_id="",
        )
        return (
            serialized,
            _get_and_set_equivalent_variant(
                req_id, serialized, "training_set_variant", stub
            ),
            "training_set_variant",
        )

    def _create(self, req_id, stub) -> Tuple[Optional[str], Optional[str]]:
        serialized, existing_variant, _ = self._get_and_set_equivalent_variant(
            req_id, stub
        )
        if existing_variant is None:
            stub.CreateTrainingSetVariant(serialized)
        return serialized.training_set_variant.variant, existing_variant

    def get_status(self):
        return ResourceStatus(self.status)

    def is_ready(self):
        return self.status == ResourceStatus.READY.value


@typechecked
@dataclass
class TrainingSetFeatures:
    training_set_name: str
    training_set_variant: str
    feature_name: str
    feature_variant: str

    def to_dictionary(self):
        return {
            "training_set_name": self.training_set_name,
            "training_set_variant": self.training_set_variant,
            "feature_name": self.feature_name,
            "feature_variant": self.feature_variant,
        }
