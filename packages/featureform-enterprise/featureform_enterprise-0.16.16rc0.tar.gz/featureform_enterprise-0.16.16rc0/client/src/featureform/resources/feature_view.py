# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Feature view resource classes for Featureform.

This module contains classes for defining and managing feature views.
"""

import difflib
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Union

from typeguard import typechecked

from ..core.exceptions import FeatureformException, FeatureNotFound
from ..core.protocols import HasNameVariant
from ..enums import JoinStrategy, OperationType, ResourceStatus, ResourceType
from ..proto import metadata_pb2 as pb
from .locations import OnlineLocation
from .provider import ServerStatus


class FeatureViewTableOptions:
    pass


@typechecked
@dataclass
class MaterializationOptions:
    """Client-side representation of feature view materialization configuration.

    Parameters
    ----------
    join_strategy:
        Join strategy to use when combining feature sources during materialization.
        Defaults to INNER. Use :class:`featureform.JoinStrategy` members for type safety.

    Notes
    -----
    The class provides a :meth:`from_input` helper that allows end users to supply
    dictionaries or enums when registering resources. This keeps the registration
    API ergonomic, while ensuring validation happens consistently before requests
    are serialized and sent to the metadata service.
    """

    join_strategy: JoinStrategy = JoinStrategy.INNER
    _expected_keys = {"join_strategy"}

    def to_proto(self) -> pb.FeatureViewMaterializationOptions:
        opts = pb.FeatureViewMaterializationOptions()
        opts.join_strategy = self.join_strategy.to_proto()
        return opts

    @classmethod
    def from_input(
        cls, value: Optional[Union["MaterializationOptions", Dict[str, Any]]]
    ) -> Optional["MaterializationOptions"]:
        if value is None:
            return None
        if isinstance(value, MaterializationOptions):
            return value
        if isinstance(value, dict):
            cls._check_expected_keys(value)
            join_value = value.get("join_strategy")
            join_strategy = JoinStrategy.normalize(join_value)
            return cls(join_strategy=join_strategy)

        raise TypeError(
            "materialization_opts must be a MaterializationOptions instance, dict, or None"
        )

    @classmethod
    def _check_expected_keys(cls, data: Dict[str, Any]) -> None:
        """Fail fast if any unexpected or missing keys are present."""
        keys = set(data.keys())
        unexpected = keys - cls._expected_keys
        if unexpected:
            # Offer helpful suggestions (e.g., joinStrategy -> join_strategy)
            suggestions = {
                k: difflib.get_close_matches(k, cls._expected_keys, n=1, cutoff=0.6)
                for k in unexpected
            }
            hint_lines = []
            for k, sugg in suggestions.items():
                hint_lines.append(
                    f"- {k}" + (f" (did you mean {sugg[0]}?)" if sugg else "")
                )
            hint = "\n".join(hint_lines)
            raise ValueError(
                "Unexpected keys in MaterializationOptions:\n"
                f"{hint}\n\n"
                f"Allowed keys: {sorted(cls._expected_keys)}"
            )

        missing = cls._expected_keys - keys
        if missing:
            raise ValueError(f"Missing required keys: {sorted(missing)}")


@typechecked
@dataclass
class FeatureView:
    name: str
    provider: str
    features: List[Union[Tuple[str, str], HasNameVariant]] = field(default_factory=list)
    materialization_engine: Optional[str] = None
    materialization_options: Optional[MaterializationOptions] = None
    entity: str = None
    description: str = None
    table_options: Optional[FeatureViewTableOptions] = None
    owner: str = None
    created: str = None
    last_updated: str = None
    status: str = "NO_STATUS"
    server_status: Optional["ServerStatus"] = None
    error: Optional[str] = None
    online_location: Optional[OnlineLocation] = None
    use_super_admin_delete_override: bool = False

    def _extract_name_variant(
        self, feature: Union[Tuple[str, str], HasNameVariant]
    ) -> Tuple[str, str]:
        """Helper method to extract name and variant from either tuple or FeatureColumnResource"""
        if isinstance(feature, HasNameVariant):
            return feature.name, feature.variant
        else:
            return feature[0], feature[1]

    @staticmethod
    def operation_type() -> OperationType:
        return OperationType.CREATE

    @staticmethod
    def get_resource_type() -> ResourceType:
        return ResourceType.FEATURE_VIEW

    @staticmethod
    def get_by_name(stub, name: str) -> "FeatureView":
        name_req = pb.NameRequest(name=pb.Name(name=name))
        feature_view = next(stub.GetFeatureViews(iter([name_req])))
        if not feature_view:
            raise ValueError(f"FeatureView {name} not found.")

        return FeatureView(
            name=feature_view.name,
            provider=feature_view.provider,
            features=(
                [(f.name, f.variant) for f in feature_view.features]
                if feature_view.features
                else []
            ),
            entity=feature_view.entity,
            description=feature_view.description,
            owner=feature_view.owner,
            created=(
                feature_view.created.ToDatetime().isoformat()
                if feature_view.created and feature_view.created.seconds != 0
                else None
            ),
            last_updated=(
                feature_view.last_updated.ToDatetime().isoformat()
                if feature_view.last_updated and feature_view.last_updated.seconds != 0
                else None
            ),
            status=feature_view.status.Status._enum_type.values[
                feature_view.status.status
            ].name,
            server_status=ServerStatus.from_proto(feature_view.status),
            error=feature_view.status.error_message,
            online_location=(
                OnlineLocation.from_proto(feature_view.online_location)
                if feature_view.online_location
                else None
            ),
        )

    def _to_proto(self) -> pb.FeatureView:
        """Convert to protobuf FeatureView"""
        return pb.FeatureView(
            name=self.name,
            provider=self.provider,
            features=[
                pb.NameVariant(name=name, variant=variant)
                for name, variant in [
                    self._extract_name_variant(f) for f in self.features
                ]
            ],
            description=self.description,
            owner=self.owner,
        )

    def _create_request(
        self, use_super_admin_delete_override: bool
    ) -> pb.FeatureViewRequest:
        """Create the protobuf request"""
        return pb.FeatureViewRequest(
            feature_view=self._to_proto(),
            materialization_engine=self.materialization_engine,
            use_super_admin_delete_override=use_super_admin_delete_override,
            materialization_options=self.materialization_options.to_proto()
            if self.materialization_options
            else None,
        )

    def get(self, stub) -> "FeatureView":
        return FeatureView.get_by_name(stub, self.name)

    def _materialize(
        self, stub, use_super_admin_delete_override: bool
    ) -> "FeatureView":
        """Create feature view via direct API call (used by materialize_feature_view)"""
        """TODO we may want to get rid of this and keep create"""
        req = self._create_request(use_super_admin_delete_override)
        stub.MaterializeFeatureView(req)
        return self

    def _create(self, req_id, stub) -> Tuple[None, None]:
        """Create feature view via generic registration flow (used by create_all)"""
        self._wait_for_features(stub)
        req = self._create_request(self.use_super_admin_delete_override)
        stub.MaterializeFeatureView(req)
        return None, None

    def to_key(self) -> Tuple[ResourceType, str, str]:
        """Returns a tuple key of (resource_type, name, variant)"""
        return self.get_resource_type(), self.name, ""

    def _wait_for_features(self, stub, timeout_seconds=300):
        """Wait for all features in the feature view to be ready"""
        all_ready = False
        start_time = time.time()
        while not all_ready:
            all_ready = True
            for feature in self.features:
                try:
                    name, variant = self._extract_name_variant(feature)
                    print(f"Checking status of feature {name}, variant {variant}")
                    feature_variant = next(
                        stub.GetFeatureVariants(
                            iter(
                                [
                                    pb.NameVariantRequest(
                                        name_variant=pb.NameVariant(
                                            name=name, variant=variant
                                        )
                                    )
                                ]
                            )
                        )
                    )
                except FeatureformException as e:
                    # Check if this is a "not found" error using gRPC status code.
                    # This is more reliable than checking reason strings since the server
                    # uses codes.NotFound for all "not found" errors regardless of the
                    # specific reason string (e.g., "Key Not Found", "Resource Not Found").
                    if e.is_not_found():
                        print(
                            f"Feature ({name}, {variant}) does not exist - failing immediately"
                        )
                        raise FeatureNotFound(name, variant) from e
                    print(
                        f"FeatureformException getting feature variants for {feature}: {e}"
                    )
                    all_ready = False
                    continue
                except Exception as e:
                    print(
                        f"Unexpected error getting feature variants for {feature}: {e}"
                    )
                    all_ready = False
                    continue
                server_status = ServerStatus.from_proto(feature_variant.status)
                if server_status.status != ResourceStatus.READY:
                    print(
                        f"Feature ({name}, {variant}) not ready yet. Status: {server_status.status}"
                    )
                    all_ready = False
                    continue
            if not all_ready:
                if time.time() - start_time > timeout_seconds:
                    raise TimeoutError(
                        f"Timeout waiting for features to be ready in feature view {self.name}"
                    )
                time.sleep(5)


## Executor Providers


# Looks to see if there is an existing resource variant that matches on a resources key fields
# and sets the serialized to it.
#
# i.e. for a source variant, looks for a source variant with the same name and definition
# _get_and_set_equivalent_variant moved to operations/equivalence.py
from ..operations import _get_and_set_equivalent_variant  # noqa: F401
