# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Resource state management for tracking registered resources.
"""

from __future__ import annotations

import uuid

# Import resource types - these will be imported from their new locations
# For now, we'll use TYPE_CHECKING to avoid circular imports
from typing import TYPE_CHECKING, List
from urllib.parse import urlencode, urlunparse

import grpc

from .. import feature_flag
from ..enums import OperationType, ResourceType
from ..proto import metadata_pb2 as pb
from ..version import check_up_to_date

if TYPE_CHECKING:
    from ..resources import Resource


class ResourceRedefinedError(Exception):
    def __init__(self, resource: Resource):
        variant_str = (
            f" variant {resource.variant}" if hasattr(resource, "variant") else ""
        )
        resource_id = f"{resource.name}{variant_str}"
        super().__init__(
            f"{resource.get_resource_type()} resource {resource_id} defined in multiple places"
        )


class ResourceState:
    def __init__(self):
        self.__state = {}

    def reset(self):
        self.__state = {}

    def add(self, resource: Resource) -> None:
        if hasattr(resource, "variant"):
            key = (
                resource.operation_type().name,
                resource.get_resource_type(),
                resource.name,
                resource.variant,
            )
        else:
            key = (
                resource.operation_type().name,
                resource.get_resource_type().to_string(),
                resource.name,
            )
        if key in self.__state:
            if resource == self.__state[key]:
                print(
                    f"Resource {resource.get_resource_type().to_string()} already registered."
                )
                return
            raise ResourceRedefinedError(resource)
        self.__state[key] = resource
        if hasattr(resource, "schedule_obj") and resource.schedule_obj is not None:
            my_schedule = resource.schedule_obj
            key = (my_schedule.get_resource_type(), my_schedule.name)
            self.__state[key] = my_schedule

    def is_empty(self) -> bool:
        return len(self.__state) == 0

    def sorted_list(self) -> List[Resource]:
        resource_order = {
            ResourceType.USER: 0,
            ResourceType.PROVIDER: 1,
            ResourceType.SOURCE_VARIANT: 2,
            ResourceType.ENTITY: 3,
            ResourceType.FEATURE_VARIANT: 4,
            ResourceType.ONDEMAND_FEATURE: 5,
            ResourceType.LABEL_VARIANT: 6,
            ResourceType.TRAININGSET_VARIANT: 7,
            ResourceType.SCHEDULE: 8,
            ResourceType.MODEL: 9,
            ResourceType.STREAM_CHANNEL: 10,
            ResourceType.FEATURE_VIEW: 11,
        }

        def to_sort_key(res):
            resource_num = resource_order[res.get_resource_type()]
            return resource_num

        return sorted(self.__state.values(), key=to_sort_key)

    def create_all_dryrun(self) -> None:
        for resource in self.sorted_list():
            if resource.operation_type() is OperationType.GET:
                print(
                    "Getting", resource.get_resource_type().to_string(), resource.name
                )
            if resource.operation_type() is OperationType.CREATE:
                print(
                    "Creating", resource.get_resource_type().to_string(), resource.name
                )

    def run_all(self, stub, client_objs_for_resource: dict = None) -> None:
        if not feature_flag.is_enabled("FF_GET_EQUIVALENT_VARIANTS", True):
            print("Runs are not supported when env:FF_GET_EQUIVALENT_VARIANTS is false")
            return
        req_id = uuid.uuid4()
        resources = []
        for resource in self.sorted_list():
            if (
                resource.get_resource_type() == ResourceType.PROVIDER
                and resource.name == "local-mode"
            ):
                continue
            try:
                resource_variant = getattr(resource, "variant", "")
                rv_for_print = f" {resource_variant}" if resource_variant else ""
                if resource.operation_type() is OperationType.CREATE:
                    from ..resources import ResourceVariant

                    if isinstance(resource, ResourceVariant):
                        (
                            serialized,
                            equiv_variant,
                            var_type,
                        ) = resource._get_and_set_equivalent_variant(req_id, stub)
                        if equiv_variant is None:
                            print(
                                f"{resource.name}{rv_for_print} has not been applied. Aborting the run."
                            )
                            return
                        client_obj = client_objs_for_resource.get(
                            resource.to_key(), None
                        )
                        resource.variant = equiv_variant
                        if client_obj is not None:
                            client_obj.variant = equiv_variant
                        resources.append((resource, serialized, var_type))

            except grpc.RpcError as e:
                raise e
        proto_resources = []
        for resource, serialized, var_type in resources:
            resource_variant = getattr(resource, "variant", "")
            rv_for_print = f" {resource_variant}" if resource_variant else ""
            print(
                f"Running {resource.get_resource_type().to_string()} {resource.name}{rv_for_print}"
            )
            res_pb = pb.ResourceVariant(**{var_type: getattr(serialized, var_type)})
            proto_resources.append(res_pb)
        req = pb.RunRequest(
            request_id=str(req_id),
            variants=proto_resources,
        )
        stub.Run(req)

    def build_dashboard_url(self, host, resource_type, name, variant=""):
        scheme = "https"
        if "localhost" in host:
            scheme = "http"
            host = "localhost"

        resource_type_to_resource_url = {
            ResourceType.FEATURE_VARIANT: "features",
            ResourceType.SOURCE_VARIANT: "sources",
            ResourceType.LABEL_VARIANT: "labels",
            ResourceType.TRAININGSET_VARIANT: "training-sets",
            ResourceType.PROVIDER: "providers",
            ResourceType.ONDEMAND_FEATURE: "features",
            ResourceType.TRANSFORMATION: "sources",
            ResourceType.ENTITY: "entities",
            ResourceType.MODEL: "models",
            ResourceType.USER: "users",
            ResourceType.FEATURE_VIEW: "feature-views",
        }
        resource_url = resource_type_to_resource_url[resource_type]
        path = f"{resource_url}/{name}"
        if variant:
            query = urlencode({"variant": variant})
            dashboard_url = urlunparse((scheme, host, path, "", query, ""))
        else:
            dashboard_url = urlunparse((scheme, host, path, "", "", ""))

        return dashboard_url

    def create_all(
        self, stub, asynchronous, host, client_objs_for_resource: dict = None
    ) -> None:
        check_up_to_date(False, "register")
        req_id = uuid.uuid4()
        for resource in self.sorted_list():
            try:
                resource_variant = getattr(resource, "variant", "")
                rv_for_print = f"{resource_variant}" if resource_variant else ""
                if resource.operation_type() is OperationType.GET:
                    print(
                        f"Getting {resource.get_resource_type().to_string()} {resource.name} {rv_for_print}"
                    )
                    resource._get(stub)
                if resource.operation_type() is OperationType.CREATE:
                    if resource.name != "default_user":
                        print(
                            f"Creating {resource.get_resource_type().to_string()} {resource.name} {rv_for_print}"
                        )
                    created_variant, existing_variant = resource._create(req_id, stub)
                    if asynchronous:
                        variant_used = (
                            existing_variant if existing_variant else created_variant
                        )
                        url = self.build_dashboard_url(
                            host,
                            resource.get_resource_type(),
                            resource.name,
                            variant_used,
                        )
                        print(url)
                        print("")

                    from ..resources import ResourceVariant

                    if isinstance(resource, ResourceVariant):
                        # look up the client object with the original resource
                        client_obj = client_objs_for_resource.get(
                            resource.to_key(), None
                        )
                        resource.variant = created_variant
                        if client_obj is not None:
                            client_obj.variant = created_variant

            except grpc.RpcError as e:
                if e.code() == grpc.StatusCode.ALREADY_EXISTS:
                    print(f"{resource.name} {rv_for_print} already exists.")
                    continue

                raise e
