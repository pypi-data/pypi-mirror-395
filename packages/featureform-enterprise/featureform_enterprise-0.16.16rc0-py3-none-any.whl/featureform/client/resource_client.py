# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
ResourceClient for Featureform.

DEPRECATED: This class is deprecated in favor of the unified Client class.
Use featureform.Client instead.

This module contains the legacy ResourceClient class for querying and listing
Featureform resources.
"""

import inspect
import logging
import os
import warnings
from typing import List, Optional, Union, get_args

from ..enums import ResourceType
from ..grpc_client import GrpcClient
from ..list import (
    list_name,
    list_name_status,
    list_name_variant_status,
    list_name_variant_status_desc,
)
from ..operations.cleanup import CleanupResult
from ..proto import metadata_pb2
from ..proto import metadata_pb2 as pb
from ..proto import metadata_pb2_grpc as ff_grpc
from ..resources import *
from ..status_display import display_statuses
from ..tls import insecure_channel, secure_channel

__all__ = ["ResourceClient"]


class ResourceClient:
    """
    The resource client is used to retrieve information on specific resources
    (entities, providers, features, labels, training sets, models, users).

    Args:
        host (str): The hostname of the Featureform instance.
        insecure (bool): True if connecting to an insecure Featureform endpoint. False if using a self-signed or public TLS certificate
        cert_path (str): The path to a public certificate if using a self-signed certificate.

    **Using the Resource Client:**
    ``` py title="definitions.py"
    import featureform as ff
    from featureform import ResourceClient

    rc = ResourceClient("localhost:8000")

    # example query:
    redis = client.get_provider("redis-quickstart")
    ```
    """

    def __init__(
        self,
        host=None,
        local=False,
        insecure=False,
        cert_path=None,
        dry_run=False,
        debug=False,
    ):
        if local:
            raise Exception(
                "Local mode is not supported in this version. Use featureform <= 1.12.0 for localmode"
            )

        # This line ensures that the warning is only raised if ResourceClient is instantiated directly
        # TODO: Remove this check once ServingClient is deprecated
        is_instantiated_directed = inspect.stack()[1].function != "__init__"
        if is_instantiated_directed:
            warnings.warn(
                "ResourceClient is deprecated and will be removed in future versions; use Client instead.",
                PendingDeprecationWarning,
            )
        self._dry_run = dry_run
        self._stub = None
        self.local = local

        if dry_run:
            return

        host = host or os.getenv("FEATUREFORM_HOST")
        if host is None:
            raise RuntimeError(
                "If not in local mode then `host` must be passed or the environment"
                " variable FEATUREFORM_HOST must be set."
            )
        if insecure:
            channel = insecure_channel(host)
        else:
            channel = secure_channel(host, cert_path)
        self._stub = GrpcClient(ff_grpc.ApiStub(channel), debug=debug)
        self._host = host
        self._cert_path = cert_path or os.getenv("FEATUREFORM_CERT")
        self._insecure = insecure
        self.logger = logging.getLogger(__name__)

    def apply(
        self, asynchronous=False, verbose=False, cleanup=False
    ) -> Optional["CleanupResult"]:
        """
        Apply all definitions, creating and retrieving all specified resources.

        ```python
        import featureform as ff
        client = ff.Client()

        ff.register_postgres(
            host="localhost",
            port=5432,
        )

        client.apply()
        ```

        Args:
            asynchronous (bool): If True, apply will return immediately and not wait for resources to be created. If False, apply will wait for resources to be created and print out the status of each resource.

        """
        # Import here to avoid circular dependency
        from ..register import get_run, global_registrar, set_run

        try:
            resource_state = global_registrar.state()

            if resource_state.is_empty():
                print("No resources to apply")
                return

            print(f"Applying Run: {get_run()}")

            if self._dry_run:
                print(resource_state.sorted_list())
                return

            resource_state.create_all(
                self._stub,
                asynchronous,
                self._host,
                global_registrar.get_client_objects_for_resource(),
            )

            print()

            if not asynchronous and self._stub:
                resources = resource_state.sorted_list()
                display_statuses(self._stub, resources, self._host)

            if cleanup and not self._dry_run and self._stub:
                if asynchronous:
                    print(
                        "Warning: Cleanup is not supported in asynchronous mode. Skipping cleanup."
                    )
                return self._cleanup(resource_state, "total")
        finally:
            set_run("")
            global_registrar.clear_state()

    def delete(
        self,
        source: Union["DeletableResourceObjects", str],
        variant: Optional[str] = None,
        resource_type: Optional[ResourceType] = None,
        *,
        asynchronous: bool = True,
    ):
        """
        Delete a resource by name and variant or by resource object.

        There are three ways to delete a resource:
        1. Using a resource object (Feature, Label, Source, etc.)
        2. Using a provider object (OnlineProvider, OfflineProvider)
        3. Using a string name with required parameters

        Examples:
            ```python
            import featureform as ff
            client = ff.Client()

            # Delete using string name (requires variant and resource_type)
            client.delete("transactions", "kaggle", ff.ResourceType.SOURCE)

            # Delete using resource object
            feature = client.get_feature("my_feature", "v1")
            client.delete(feature)

            # Delete provider (no variant needed)
            client.delete("redis_provider", resource_type=ff.ResourceType.PROVIDER)
            ```

        Args:
            source: Either a resource object (Feature, Label, Source, etc.) or the name of the resource as a string.
                If a string is provided, resource_type is required and variant is required for non-provider resources.
            variant: Variant of the resource to delete. Required if source is a string and resource_type is not PROVIDER.
            resource_type: Type of resource to delete. Required if source is a string.
            asynchronous: If True, return immediately after issuing the delete request (default).

        Raises:
            ValueError: If source is a string and:
                - resource_type is not provided
                - variant is not provided (for non-provider resources)
            RuntimeError: If the resource does not exist
        """
        # Prepare the request based on the input type
        request = self._create_delete_request(source, variant, resource_type)

        # Send the request to delete the resource
        response = self._stub.MarkForDeletion(request)
        task_id = getattr(response, "task_id", "")

        resource_to_task = (
            (
                pb.ResourceType.Name(request.resource_id.resource_type),
                request.resource_id.resource.name,
                request.resource_id.resource.variant,
            ),
            task_id,
        )

        if asynchronous:
            print("Deleting resource async")
            return resource_to_task

        from ..status_display import StatusDisplayer

        displayer = StatusDisplayer(self._stub, [])
        displayer.simple_poll({resource_to_task[0]: resource_to_task[1]})

        return resource_to_task

    def prune(
        self,
        source: Union["DeletableResourceObjects", str],
        variant: Optional[str] = None,
        resource_type: Optional[ResourceType] = None,
        *,
        asynchronous: bool = True,
    ):
        """Prune a resource and its unreferenced dependencies.

        Args:
            asynchronous: If True, return immediately after issuing the prune request (default).
        """
        if (
            isinstance(source, FeatureView)
            or resource_type == ResourceType.FEATURE_VIEW
        ):
            raise ValueError(
                "Pruning FeatureViews is not supported. Use `delete` instead."
            )
        # Import here to avoid circular dependency
        from ..providers import OfflineProvider, OnlineProvider

        request = self._create_prune_request(source, variant, resource_type)

        # Send the request to delete the resource
        response = self._stub.PruneResource(request)
        if (
            isinstance(source, str) and resource_type == ResourceType.PROVIDER
        ) or isinstance(source, (OfflineProvider, OnlineProvider)):
            print(
                "Run `delete` on provider after pruning to remove provider from Featureform"
            )
        resources_to_tasks = {
            (
                pb.ResourceType.Name(r.resource.resource_type),
                r.resource.resource.name,
                r.resource.resource.variant,
            ): r.task_id
            for r in response.results
        }

        if asynchronous:
            print("Pruning resource async")
            return resources_to_tasks

        if not resources_to_tasks:
            print("No resources to prune")
            return {}

        from ..status_display import StatusDisplayer

        displayer = StatusDisplayer(self._stub, [])

        displayer.simple_poll(resources_to_tasks)

        return resources_to_tasks

    def get_task_statuses(self, task_ids: List[str]):
        """Fetch the latest status for the given task IDs."""
        request = metadata_pb2.GetTaskStatusesRequest(task_ids=task_ids)
        response = self._stub.GetTaskStatuses(request)
        return response.task_statuses

    def _print_detailed_cleanup_summary(
        self, asynchronous, stats, deleted_resources, failed_resources
    ):
        """
        Print a detailed summary of the cleanup operation.

        Args:
            asynchronous: Whether the cleanup was async
            stats: Dictionary with cleanup statistics
            deleted_resources: Set of successfully deleted resources
            failed_resources: List of resources that failed to delete
        """
        print(f"\n{'=' * 50}")

        if asynchronous:
            print("CLEANUP INITIATED (ASYNC)")
            print(f"{'=' * 50}")
            print(f"Total queued for deletion: {stats['queued']}")
            print(f"Total failed: {stats['failed']}")
        else:
            print("CLEANUP COMPLETE")
            print(f"{'=' * 50}")
            print(f"Total deleted: {stats['queued']}")
            print(f"Total failed: {stats['failed']}")

        # Print successfully deleted resources
        if deleted_resources:
            print(
                f"\n{'DELETED RESOURCES:' if not asynchronous else 'RESOURCES QUEUED FOR DELETION:'}"
            )
            print("-" * 30)
            # Group by resource type
            resources_by_type = {}
            for res_type, name, variant in deleted_resources:
                if res_type not in resources_by_type:
                    resources_by_type[res_type] = []
                resources_by_type[res_type].append((name, variant))

            for res_type, resources in resources_by_type.items():
                print(f"\n{res_type}:")
                for name, variant in sorted(resources):
                    if variant:
                        print(f"  - {name} (variant: {variant})")
                    else:
                        print(f"  - {name}")

        # Print failed resources
        if failed_resources:
            print(f"\nFAILED TO DELETE:")
            print("-" * 30)
            # Group by resource type
            failed_by_type = {}
            for res_type, name, variant in failed_resources:
                if res_type not in failed_by_type:
                    failed_by_type[res_type] = []
                failed_by_type[res_type].append((name, variant))

            for res_type, resources in failed_by_type.items():
                print(f"\n{res_type}:")
                for name, variant in sorted(resources):
                    if variant:
                        print(f"  - {name} (variant: {variant})")
                    else:
                        print(f"  - {name}")

        # Show detailed errors if any
        if stats["errors"] and self.logger.level <= logging.DEBUG:
            print("\nDETAILED ERRORS:")
            print("-" * 30)
            for resource_id, error in stats["errors"][:10]:
                print(f"  {resource_id}:")
                print(f"    Error: {error}")
            if len(stats["errors"]) > 10:
                print(f"  ... and {len(stats['errors']) - 10} more errors")

        # Final status message
        if not asynchronous:
            if stats["failed"] == 0:
                print(f"\n[SUCCESS] All resources cleaned up successfully")
            else:
                print(f"\n[WARNING] Cleanup completed with {stats['failed']} failures")
        else:
            print(f"\n[INFO] Resources will be deleted in the background")
            print(f"       Monitor progress in your Featureform dashboard")

        print(f"{'=' * 50}\n")

    def _cleanup(self, resource_state, mode, asynchronous=False) -> "CleanupResult":
        """
        Execute cleanup based on mode.

        Args:
            resource_state: Current state of resources that were just applied
            mode (str): Cleanup mode - currently only "total" is supported
            asynchronous (bool): If True, cleanup runs in background

        Returns:
            set: Resources that were deleted or queued for deletion
        """
        # Validate cleanup mode
        if mode != "total":
            self.logger.error(f"Only 'total' mode is currently supported, got '{mode}'")
            return set()

        print(f"\n{'=' * 50}")
        print(f"Starting cleanup (mode: {mode}, async: {asynchronous})")
        print(f"{'=' * 50}\n")

        # Collect resources to keep from current run
        resources_to_keep = self._get_resources_to_keep(resource_state)
        print(f"Resources to keep from current run: {len(resources_to_keep)}")
        for res_type, name, variant in resources_to_keep:
            print(f"  - {res_type}: {name} (variant: {variant})")

        # Find resources to delete
        resources_to_delete = self._find_resources_to_delete(resources_to_keep)

        if not resources_to_delete:
            return CleanupResult.empty()

        print(f"\nFound {len(resources_to_delete)} resources to delete")
        print("Resources to delete:")
        for res_type, name, variant in resources_to_delete:
            print(f"  - {res_type}: {name} (variant: {variant})")

        # Execute cleanup
        return self._execute_cleanup(resources_to_delete, asynchronous)

    def _get_resources_to_keep(self, resource_state):
        """
        Build set of resources from current run that should be kept.

        Args:
            resource_state: Current state of resources

        Returns:
            set: Tuples of (type, name, variant) to keep
        """
        resources_to_keep = set()

        for res in resource_state.sorted_list():
            if isinstance(res, ResourceVariant) or isinstance(res, FeatureView):
                resources_to_keep.add(res.to_key())

        return resources_to_keep

    def _find_resources_to_delete(self, resources_to_keep):
        """
        Find all resources that are not in the current run.

        Note: Feature views must be deleted first as they may depend on other resources.

        Args:
            resources_to_keep: Set of (type, name, variant) tuples to keep

        Returns:
            list: Tuples of (type, name, variant) to delete, with feature views first
        """
        # Define resource types and their list functions
        # IMPORTANT: Feature views MUST be first in this list
        resource_config = [
            (ResourceType.FEATURE_VIEW, self._stub.ListFeatureViews),
            (ResourceType.SOURCE_VARIANT, self._stub.ListSources),
            (ResourceType.FEATURE_VARIANT, self._stub.ListFeatures),
            (ResourceType.LABEL_VARIANT, self._stub.ListLabels),
            (ResourceType.TRAININGSET_VARIANT, self._stub.ListTrainingSets),
        ]

        resources_to_delete = []

        for resource_type, list_func in resource_config:
            try:
                resources = list_func(metadata_pb2.ListRequest())
                for item in resources:
                    # Feature views don't have variants, just use name directly
                    if resource_type == ResourceType.FEATURE_VIEW:
                        resource_tuple = (resource_type, item.name, "")
                        if resource_tuple not in resources_to_keep:
                            resources_to_delete.append(resource_tuple)
                    else:
                        # All other resource types have variants
                        for variant in getattr(item, "variants", []):
                            resource_tuple = (resource_type, item.name, variant)
                            if resource_tuple not in resources_to_keep:
                                resources_to_delete.append(resource_tuple)

            except Exception as e:
                self.logger.error(f"Failed to list {resource_type.name}: {e}")
                # Continue with other resource types

        return resources_to_delete

    def _execute_cleanup(self, resources_to_delete, asynchronous) -> "CleanupResult":
        """
        Execute the cleanup of resources.

        Args:
            resources_to_delete: List of (type, name, variant) tuples to delete
            asynchronous: If True, cleanup runs in background

        Returns:
            CleanupResult: Object containing cleanup results
        """
        deleted_resources = set()
        failed_resources = []
        stats = {"queued": 0, "failed": 0, "errors": []}

        operation = "Queuing" if asynchronous else "Deleting"
        print(f"\n{operation} resources...")

        for resource_type, name, variant in resources_to_delete:
            # Feature views don't have variants
            if resource_type == ResourceType.FEATURE_VIEW:
                resource_id = f"{resource_type} {name}"
            else:
                resource_id = f"{resource_type} {name}.{variant}"

            try:
                print(f"  {operation} {resource_id} ({resource_type.name})...")
                if (resource_type, name, variant) in deleted_resources:
                    print("    [SKIPPED] Already deleted or queued for deletion")
                    continue

                resources_to_tasks = {}
                # Feature views use delete, other resources use prune
                if resource_type == ResourceType.FEATURE_VIEW:
                    resource, task = self.delete(
                        name,
                        resource_type=resource_type,
                        asynchronous=asynchronous,
                    )
                    resources_to_tasks[resource] = task
                else:
                    resources_to_tasks = self.prune(
                        name,
                        variant,
                        resource_type=resource_type,
                        asynchronous=asynchronous,
                    )
                    resources_to_tasks = resources_to_tasks or {}

                if resources_to_tasks:
                    deleted_resources.update(resources_to_tasks.keys())
                    stats["queued"] += len(resources_to_tasks)
                    print(f"    [SUCCESS] {operation} completed for {resource_id}")

            except Exception as e:
                err_msg = str(e)
                if "Could not find resource to delete" in err_msg:
                    self.logger.debug(f"Skipping {resource_id}: {err_msg}")
                    continue

                stats["failed"] += 1
                stats["errors"].append((resource_id, str(e)))
                failed_resources.append((resource_type, name, variant))
                print(f"    [FAILED] Could not delete {resource_id}: {e}")

        # Print summary
        self._print_detailed_cleanup_summary(
            asynchronous, stats, deleted_resources, failed_resources
        )

        return CleanupResult(
            deleted_resources=deleted_resources,
            failed_resources=failed_resources,
            error_count=stats["failed"],
            errors=stats["errors"],
        )

    def _create_prune_request(
        self,
        source: Union["DeletableResourceObjects", str],
        variant: Optional[str] = None,
        resource_type: Optional[ResourceType] = None,
    ) -> metadata_pb2.PruneResourceRequest:
        return metadata_pb2.PruneResourceRequest(
            resource_id=self._build_resource_id(source, variant, resource_type)
        )

    def _create_delete_request(
        self,
        source: Union["DeletableResourceObjects", str],
        variant: Optional[str] = None,
        resource_type: Optional[ResourceType] = None,
    ) -> metadata_pb2.MarkForDeletionRequest:
        return metadata_pb2.MarkForDeletionRequest(
            resource_id=self._build_resource_id(source, variant, resource_type)
        )

    def _build_resource_id(
        self,
        source: Union["DeletableResourceObjects", str],
        variant: Optional[str] = None,
        resource_type: Optional[ResourceType] = None,
    ) -> metadata_pb2.ResourceID:
        """Helper to construct a ResourceID for prune or delete requests."""
        # Import here to avoid circular dependency
        from ..providers import OfflineProvider, OnlineProvider
        from ..register import DeletableResourceObjects

        if isinstance(source, str):
            if resource_type is None:
                raise ValueError(
                    "resource_type must be specified if source is a string"
                )

            if not ResourceType.is_deletable(resource_type):
                raise ValueError("resource_type must be deletable")

            # handle resources without variants
            if resource_type == ResourceType.PROVIDER or resource_type == FeatureView:
                return metadata_pb2.ResourceID(
                    resource=metadata_pb2.NameVariant(name=source),
                    resource_type=resource_type.to_proto(),
                )

            if not variant and resource_type != ResourceType.FEATURE_VIEW:
                raise ValueError("variant must be specified for non-provider resources")

            return metadata_pb2.ResourceID(
                resource=metadata_pb2.NameVariant(name=source, variant=variant),
                resource_type=resource_type.to_proto(),
            )

        if isinstance(source, FeatureView):
            return metadata_pb2.ResourceID(
                resource=metadata_pb2.NameVariant(name=source.name),
                resource_type=ResourceType.FEATURE_VIEW.to_proto(),
            )

        if isinstance(source, (OfflineProvider, OnlineProvider)):
            return metadata_pb2.ResourceID(
                resource=metadata_pb2.NameVariant(name=source.name()),
                resource_type=ResourceType.PROVIDER.to_proto(),
            )

        if not isinstance(source, get_args(DeletableResourceObjects)):
            raise ValueError("resource is not deletable")

        name, variant = source.name_variant()
        return metadata_pb2.ResourceID(
            resource=metadata_pb2.NameVariant(name=name, variant=variant),
            resource_type=source.get_resource_type().to_proto(),
        )

    def run(self):
        """
        Run tasks for all definitions, creating and retrieving all specified resources.

        ```python
        import featureform as ff
        client = ff.Client()

        ff.register_postgres(
            host="localhost",
            port=5432,
        )

        client.run()
        ```
        """
        # Import here to avoid circular dependency
        from ..register import global_registrar

        try:
            resource_state = global_registrar.state()
            if resource_state.is_empty():
                print("No resources to run")
                return

            if self._dry_run:
                print(resource_state.sorted_list())
                return

            resource_state.run_all(
                self._stub, global_registrar.get_client_objects_for_resource()
            )

        finally:
            global_registrar.clear_state()

    def get_auth_config(self):
        if not self.local:
            return self._stub.GetAuthConfig(metadata_pb2.Empty())
        return None

    def get_user(self, name, local=False):
        """Get a user. Prints out name of user, and all resources associated with the user.

        **Examples:**

        ``` py title="Input"
        featureformer = rc.get_user("featureformer")
        ```

        ``` json title="Output"
        // get_user prints out formatted information on user
        USER NAME:                     featureformer
        -----------------------------------------------

        NAME                           VARIANT                        TYPE
        avg_transactions               quickstart                     feature
        fraudulent                     quickstart                     label
        fraud_training                 quickstart                     training set
        transactions                   kaggle                         source
        average_user_transaction       quickstart                     source
        -----------------------------------------------
        ```

        ``` py title="Input"
        print(featureformer)
        ```

        ``` json title="Output"
        // get_user returns the User object

        name: "featureformer"
        features {
        name: "avg_transactions"
        variant: "quickstart"
        }
        labels {
        name: "fraudulent"
        variant: "quickstart"
        }
        trainingsets {
        name: "fraud_training"
        variant: "quickstart"
        }
        sources {
        name: "transactions"
        variant: "kaggle"
        }
        sources {
        name: "average_user_transaction"
        variant: "quickstart"
        }
        ```

        Args:
            name (str): Name of user to be retrieved

        Returns:
            user (User): User
        """
        return get_user_info(self._stub, name)

    def get_entity(self, name, local=False):
        """Get an entity. Prints out information on entity, and all resources associated with the entity.

        **Examples:**

        ``` py title="Input"
        entity = rc.get_entity("user")
        ```

        ``` json title="Output"
        // get_entity prints out formatted information on entity

        ENTITY NAME:                   user
        STATUS:                        NO_STATUS
        -----------------------------------------------

        NAME                           VARIANT                        TYPE
        avg_transactions               quickstart                     feature
        fraudulent                     quickstart                     label
        fraud_training                 quickstart                     training set
        -----------------------------------------------
        ```

        ``` py title="Input"
        print(postgres)
        ```

        ``` json title="Output"
        // get_entity returns the Entity object

        name: "user"
        features {
            name: "avg_transactions"
            variant: "quickstart"
        }
        labels {
            name: "fraudulent"
            variant: "quickstart"
        }
        trainingsets {
            name: "fraud_training"
            variant: "quickstart"
        }
        ```
        """
        return get_entity_info(self._stub, name)

    def get_model(self, name, local=False) -> Model:
        """Get a model. Prints out information on model, and all resources associated with the model.

        Args:
            name (str): Name of model to be retrieved

        Returns:
            model (Model): Model
        """
        model = None
        model_proto = get_resource_info(self._stub, "model", name)
        if model_proto is not None:
            model = Model(model_proto.name, description="", tags=[], properties={})

        return model

    def get_provider(self, name, local=False):
        """Get a provider. Prints out information on provider, and all resources associated with the provider.

        **Examples:**

        ``` py title="Input"
        postgres = client.get_provider("postgres-quickstart")
        ```

        ``` json title="Output"
        // get_provider prints out formatted information on provider

        NAME:                          postgres-quickstart
        DESCRIPTION:                   A Postgres deployment we created for the Featureform quickstart
        TYPE:                          POSTGRES_OFFLINE
        SOFTWARE:                      postgres
        STATUS:                        NO_STATUS
        -----------------------------------------------
        SOURCES:
        NAME                           VARIANT
        transactions                   kaggle
        average_user_transaction       quickstart
        -----------------------------------------------
        FEATURES:
        NAME                           VARIANT
        -----------------------------------------------
        LABELS:
        NAME                           VARIANT
        fraudulent                     quickstart
        -----------------------------------------------
        TRAINING SETS:
        NAME                           VARIANT
        fraud_training                 quickstart
        -----------------------------------------------
        ```

        ``` py title="Input"
        print(postgres)
        ```

        ``` json title="Output"
        // get_provider returns the Provider object

        name: "postgres-quickstart"
        description: "A Postgres deployment we created for the Featureform quickstart"
        type: "POSTGRES_OFFLINE"
        software: "postgres"
        serialized_config: "{\"Host\": \"quickstart-postgres\",
                            \"Port\": \"5432\",
                            \"Username\": \"postgres\",
                            \"Password\": \"password\",
                            \"Database\": \"postgres\"}"
        sources {
        name: "transactions"
        variant: "kaggle"
        }
        sources {
        name: "average_user_transaction"
        variant: "quickstart"
        }
        trainingsets {
        name: "fraud_training"
        variant: "quickstart"
        }
        labels {
        name: "fraudulent"
        variant: "quickstart"
        }
        ```

        Args:
            name (str): Name of provider to be retrieved

        Returns:
            provider (Provider): Provider
        """
        return get_provider_info(self._stub, name)

    def get_feature(self, name, variant):
        return FeatureVariant.get_by_name_variant(self._stub, name, variant)

    def print_feature(self, name, variant=None, local=False):
        """Get a feature. Prints out information on feature, and all variants associated with the feature. If variant is included, print information on that specific variant and all resources associated with it.

        **Examples:**

        ``` py title="Input"
        avg_transactions = rc.get_feature("avg_transactions")
        ```

        ``` json title="Output"
        // get_feature prints out formatted information on feature

        NAME:                          avg_transactions
        STATUS:                        NO_STATUS
        -----------------------------------------------
        VARIANTS:
        quickstart                     default
        -----------------------------------------------
        ```

        ``` py title="Input"
        print(avg_transactions)
        ```

        ``` json title="Output"
        // get_feature returns the Feature object

        name: "avg_transactions"
        default_variant: "quickstart"
        variants: "quickstart"
        ```

        ``` py title="Input"
        avg_transactions_variant = ff.get_feature("avg_transactions", "quickstart")
        ```

        ``` json title="Output"
        // get_feature with variant provided prints out formatted information on feature variant

        NAME:                          avg_transactions
        VARIANT:                       quickstart
        TYPE:                          float32
        ENTITY:                        user
        OWNER:                         featureformer
        PROVIDER:                      redis-quickstart
        STATUS:                        NO_STATUS
        -----------------------------------------------
        SOURCE:
        NAME                           VARIANT
        average_user_transaction       quickstart
        -----------------------------------------------
        TRAINING SETS:
        NAME                           VARIANT
        fraud_training                 quickstart
        -----------------------------------------------
        ```

        ``` py title="Input"
        print(avg_transactions_variant)
        ```

        ``` json title="Output"
        // get_feature returns the FeatureVariant object

        name: "avg_transactions"
        variant: "quickstart"
        source {
        name: "average_user_transaction"
        variant: "quickstart"
        }
        type: "float32"
        entity: "user"
        created {
        seconds: 1658168552
        nanos: 142461900
        }
        owner: "featureformer"
        provider: "redis-quickstart"
        trainingsets {
        name: "fraud_training"
        variant: "quickstart"
        }
        columns {
        entity: "user_id"
        value: "avg_transaction_amt"
        }
        ```

        Args:
            name (str): Name of feature to be retrieved
            variant (str): Name of variant of feature

        Returns:
            feature (Union[Feature, FeatureVariant]): Feature or FeatureVariant
        """
        if not variant:
            return get_resource_info(self._stub, "feature", name)
        return get_feature_variant_info(self._stub, name, variant)

    def _get_all_and_latest_variants(
        self, resource_name, resource_type, get_latest_variant=False
    ):
        # Import here to avoid circular dependency
        from ..register import Variants
        from ..registrar import (
            ColumnSourceRegistrar,
            FeatureColumnResource,
            LabelColumnResource,
            SubscriptableTransformation,
        )

        if isinstance(resource_name, str):
            res_name = resource_name
            if resource_type is None:
                raise ValueError(
                    "A resource type param must be provided if the resource name param is of type string."
                )
            res_type = resource_type
        elif isinstance(
            resource_name,
            (
                FeatureColumnResource,
                LabelColumnResource,
                TrainingSetVariant,
                ColumnSourceRegistrar,
                SubscriptableTransformation,
            ),
        ):
            res_name = resource_name.name_variant()[0]
            res_type = resource_name.get_resource_type()
        elif isinstance(resource_name, Variants):
            if resource_type is None:
                raise ValueError(
                    f"{resource_name} is of type Variants. Please provide a resource type."
                )
            for _, res in resource_name.resources.items():
                res_name = res.name
                break
            res_type = resource_type
        else:
            raise ValueError(
                f"Expected input: string, Feature, Label, Source or Training Set object, actual input: {resource_name}."
            )

        search_name = metadata_pb2.NameRequest(name=metadata_pb2.Name(name=res_name))

        stub_get_functions = {
            ResourceType.FEATURE_VARIANT: self._stub.GetFeatures,
            ResourceType.ONDEMAND_FEATURE: self._stub.GetFeatures,
            ResourceType.LABEL_VARIANT: self._stub.GetLabels,
            ResourceType.SOURCE_VARIANT: self._stub.GetSources,
            ResourceType.TRAININGSET_VARIANT: self._stub.GetTrainingSets,
        }

        try:
            get_func = stub_get_functions[res_type]
        except KeyError:
            raise ValueError(
                f"Resource type {res_type.to_string()} doesnt have variants."
            )
        # Only the variants of the first resource are needed
        for x in get_func(iter([search_name])):
            return x.default_variant if get_latest_variant else x.variants

    def get_variants(self, resource_name, resource_type=None):
        """
        Get all variants of a resource.

        Args:
            resource_name (Union[str, FeatureColumnResource, LabelColumnResource, TrainingSetVariant, ColumnSourceRegistrar, Variants]): Name of resource or Resource object
            resource_type (ResourceType): Type of resource

        Returns:
            variants (List[str]): List of variants of the resource
        """
        return self._get_all_and_latest_variants(
            resource_name, resource_type, get_latest_variant=False
        )

    def latest_variant(self, resource_name, resource_type=None):
        """
        Get the most recent variant of a resource.

        Args:
            resource_name (Union[str, FeatureColumnResource, LabelColumnResource, TrainingSetVariant, ColumnSourceRegistrar, Variants]): Name of resource or Resource object
            resource_type (ResourceType): Type of resource

        Returns:
            variants (str): Latest variant of the resource
        """
        return self._get_all_and_latest_variants(
            resource_name, resource_type, get_latest_variant=True
        )

    def get_label(self, name, variant):
        return LabelVariant.get_by_name_variant(self._stub, name, variant)

    def print_label(self, name, variant=None, local=False):
        """Get a label. Prints out information on label, and all variants associated with the label. If variant is included, print information on that specific variant and all resources associated with it.

        **Examples:**

        ``` py title="Input"
        fraudulent = rc.get_label("fraudulent")
        ```

        ``` json title="Output"
        // get_label prints out formatted information on label

        NAME:                          fraudulent
        STATUS:                        NO_STATUS
        -----------------------------------------------
        VARIANTS:
        quickstart                     default
        -----------------------------------------------
        ```

        ``` py title="Input"
        print(fraudulent)
        ```

        ``` json title="Output"
        // get_label returns the Label object

        name: "fraudulent"
        default_variant: "quickstart"
        variants: "quickstart"
        ```

        ``` py title="Input"
        fraudulent_variant = ff.get_label("fraudulent", "quickstart")
        ```

        ``` json title="Output"
        // get_label with variant provided prints out formatted information on label variant

        NAME:                          fraudulent
        VARIANT:                       quickstart
        TYPE:                          bool
        ENTITY:                        user
        OWNER:                         featureformer
        PROVIDER:                      postgres-quickstart
        STATUS:                        NO_STATUS
        -----------------------------------------------
        SOURCE:
        NAME                           VARIANT
        transactions                   kaggle
        -----------------------------------------------
        TRAINING SETS:
        NAME                           VARIANT
        fraud_training                 quickstart
        -----------------------------------------------
        ```

        ``` py title="Input"
        print(fraudulent_variant)
        ```

        ``` json title="Output"
        // get_label returns the LabelVariant object

        name: "fraudulent"
        variant: "quickstart"
        type: "bool"
        source {
        name: "transactions"
        variant: "kaggle"
        }
        entity: "user"
        created {
        seconds: 1658168552
        nanos: 154924300
        }
        owner: "featureformer"
        provider: "postgres-quickstart"
        trainingsets {
        name: "fraud_training"
        variant: "quickstart"
        }
        columns {
        entity: "customerid"
        value: "isfraud"
        }
        ```

        Args:
            name (str): Name of label to be retrieved
            variant (str): Name of variant of label

        Returns:
            label (Union[label, LabelVariant]): Label or LabelVariant
        """
        if not variant:
            return get_resource_info(self._stub, "label", name)
        return get_label_variant_info(self._stub, name, variant)

    def get_training_set(self, name, variant):
        return TrainingSetVariant.get_by_name_variant(self._stub, name, variant)

    def print_training_set(self, name, variant=None, local=False):
        """Get a training set. Prints out information on training set, and all variants associated with the training set. If variant is included, print information on that specific variant and all resources associated with it.

        **Examples:**

        ``` py title="Input"
        fraud_training = rc.get_training_set("fraud_training")
        ```

        ``` json title="Output"
        // get_training_set prints out formatted information on training set

        NAME:                          fraud_training
        STATUS:                        NO_STATUS
        -----------------------------------------------
        VARIANTS:
        quickstart                     default
        -----------------------------------------------
        ```

        ``` py title="Input"
        print(fraud_training)
        ```

        ``` json title="Output"
        // get_training_set returns the TrainingSet object

        name: "fraud_training"
        default_variant: "quickstart"
        variants: "quickstart"
        ```

        ``` py title="Input"
        fraudulent_variant = ff.get_training set("fraudulent", "quickstart")
        ```

        ``` json title="Output"
        // get_training_set with variant provided prints out formatted information on training set variant

        NAME:                          fraud_training
        VARIANT:                       quickstart
        OWNER:                         featureformer
        PROVIDER:                      postgres-quickstart
        STATUS:                        NO_STATUS
        -----------------------------------------------
        LABEL:
        NAME                           VARIANT
        fraudulent                     quickstart
        -----------------------------------------------
        FEATURES:
        NAME                           VARIANT
        avg_transactions               quickstart
        -----------------------------------------------
        ```

        ``` py title="Input"
        print(fraudulent_variant)
        ```

        ``` json title="Output"
        // get_training_set returns the TrainingSetVariant object

        name: "fraud_training"
        variant: "quickstart"
        owner: "featureformer"
        created {
        seconds: 1658168552
        nanos: 157934800
        }
        provider: "postgres-quickstart"
        features {
        name: "avg_transactions"
        variant: "quickstart"
        }
        label {
        name: "fraudulent"
        variant: "quickstart"
        }
        ```

        Args:
            name (str): Name of training set to be retrieved
            variant (str): Name of variant of training set

        Returns:
            training_set (Union[TrainingSet, TrainingSetVariant]): TrainingSet or TrainingSetVariant
        """
        if not variant:
            return get_resource_info(self._stub, "training-set", name)
        return get_training_set_variant_info(self._stub, name, variant)

    def get_source(self, name, variant):
        # Import here to avoid circular dependency
        from ..register import global_registrar
        from ..registrar import ColumnSourceRegistrar

        source_variant = SourceVariant.get_by_name_variant(self._stub, name, variant)
        return ColumnSourceRegistrar(global_registrar, source_variant)

    def print_source(self, name, variant=None, local=False):
        """Get a source. Prints out information on source, and all variants associated with the source. If variant is included, print information on that specific variant and all resources associated with it.

        **Examples:**

        ``` py title="Input"
        transactions = rc.get_transactions("transactions")
        ```

        ``` json title="Output"
        // get_source prints out formatted information on source

        NAME:                          transactions
        STATUS:                        NO_STATUS
        -----------------------------------------------
        VARIANTS:
        kaggle                         default
        -----------------------------------------------
        ```

        ``` py title="Input"
        print(transactions)
        ```

        ``` json title="Output"
        // get_source returns the Source object

        name: "transactions"
        default_variant: "kaggle"
        variants: "kaggle"
        ```

        ``` py title="Input"
        transactions_variant = rc.get_source("transactions", "kaggle")
        ```

        ``` json title="Output"
        // get_source with variant provided prints out formatted information on source variant

        NAME:                          transactions
        VARIANT:                       kaggle
        OWNER:                         featureformer
        DESCRIPTION:                   Fraud Dataset From Kaggle
        PROVIDER:                      postgres-quickstart
        STATUS:                        NO_STATUS
        -----------------------------------------------
        DEFINITION:
        TRANSFORMATION

        -----------------------------------------------
        SOURCES
        NAME                           VARIANT
        -----------------------------------------------
        PRIMARY DATA
        Transactions
        FEATURES:
        NAME                           VARIANT
        -----------------------------------------------
        LABELS:
        NAME                           VARIANT
        fraudulent                     quickstart
        -----------------------------------------------
        TRAINING SETS:
        NAME                           VARIANT
        fraud_training                 quickstart
        -----------------------------------------------
        ```

        ``` py title="Input"
        print(transactions_variant)
        ```

        ``` json title="Output"
        // get_source returns the SourceVariant object

        name: "transactions"
        variant: "kaggle"
        owner: "featureformer"
        description: "Fraud Dataset From Kaggle"
        provider: "postgres-quickstart"
        created {
        seconds: 1658168552
        nanos: 128768000
        }
        trainingsets {
        name: "fraud_training"
        variant: "quickstart"
        }
        labels {
        name: "fraudulent"
        variant: "quickstart"
        }
        primaryData {
        table {
            name: "Transactions"
        }
        }
        ```

        Args:
            name (str): Name of source to be retrieved
            variant (str): Name of variant of source

        Returns:
            source (Union[Source, SourceVariant]): Source or SourceVariant
        """
        if not variant:
            return get_resource_info(self._stub, "source", name)
        return get_source_variant_info(self._stub, name, variant)

    def list_features(self, local=False):
        """List all features.

        **Examples:**
        ``` py title="Input"
        features_list = rc.list_features()
        ```

        ``` json title="Output"
        // list_features prints out formatted information on all features

        NAME                           VARIANT                        STATUS
        user_age                       quickstart (default)           READY
        avg_transactions               quickstart (default)           READY
        avg_transactions               production                     CREATED
        ```

        ``` py title="Input"
        print(features_list)
        ```

        ``` json title="Output"
        // list_features returns a list of Feature objects

        [name: "user_age"
        default_variant: "quickstart"
        variants: "quickstart"
        , name: "avg_transactions"
        default_variant: "quickstart"
        variants: "quickstart"
        variants: "production"
        ]
        ```

        Returns:
            features (List[Feature]): List of Feature Objects
        """
        return list_name_variant_status(self._stub, "feature")

    def list_labels(self, local=False):
        """List all labels.

        **Examples:**
        ``` py title="Input"
        features_list = rc.list_labels()
        ```

        ``` json title="Output"
        // list_labels prints out formatted information on all labels

        NAME                           VARIANT                        STATUS
        user_age                       quickstart (default)           READY
        avg_transactions               quickstart (default)           READY
        avg_transactions               production                     CREATED
        ```

        ``` py title="Input"
        print(label_list)
        ```

        ``` json title="Output"
        // list_features returns a list of Feature objects

        [name: "user_age"
        default_variant: "quickstart"
        variants: "quickstart"
        , name: "avg_transactions"
        default_variant: "quickstart"
        variants: "quickstart"
        variants: "production"
        ]
        ```

        Returns:
            labels (List[Label]): List of Label Objects
        """
        return list_name_variant_status(self._stub, "label")

    def list_users(self, local=False):
        """List all users. Prints a list of all users.

        **Examples:**
        ``` py title="Input"
        users_list = rc.list_users()
        ```

        ``` json title="Output"
        // list_users prints out formatted information on all users

        NAME                           STATUS
        featureformer                  NO_STATUS
        featureformers_friend          CREATED
        ```

        ``` py title="Input"
        print(features_list)
        ```

        ``` json title="Output"
        // list_features returns a list of Feature objects

        [name: "featureformer"
        features {
        name: "avg_transactions"
        variant: "quickstart"
        }
        labels {
        name: "fraudulent"
        variant: "quickstart"
        }
        trainingsets {
        name: "fraud_training"
        variant: "quickstart"
        }
        sources {
        name: "transactions"
        variant: "kaggle"
        }
        sources {
        name: "average_user_transaction"
        variant: "quickstart"
        },
        name: "featureformers_friend"
        features {
        name: "user_age"
        variant: "production"
        }
        sources {
        name: "user_profiles"
        variant: "production"
        }
        ]
        ```

        Returns:
            users (List[User]): List of User Objects
        """
        return list_name_status(self._stub, "user")

    def list_entities(self, local=False):
        """List all entities. Prints a list of all entities.

        **Examples:**
        ``` py title="Input"
        entities = rc.list_entities()
        ```

        ``` json title="Output"
        // list_entities prints out formatted information on all entities

        NAME                           STATUS
        user                           CREATED
        transaction                    CREATED
        ```

        ``` py title="Input"
        print(features_list)
        ```

        ``` json title="Output"
        // list_entities returns a list of Entity objects

        [name: "user"
        features {
        name: "avg_transactions"
        variant: "quickstart"
        }
        features {
        name: "avg_transactions"
        variant: "production"
        }
        features {
        name: "user_age"
        variant: "quickstart"
        }
        labels {
        name: "fraudulent"
        variant: "quickstart"
        }
        trainingsets {
        name: "fraud_training"
        variant: "quickstart"
        }
        ,
        name: "transaction"
        features {
        name: "amount_spent"
        variant: "production"
        }
        ]
        ```

        Returns:
            entities (List[Entity]): List of Entity Objects
        """
        return list_name_status(self._stub, "entity")

    def list_sources(self, local=False):
        """List all sources. Prints a list of all sources.

        **Examples:**
        ``` py title="Input"
        sources_list = rc.list_sources()
        ```

        ``` json title="Output"
        // list_sources prints out formatted information on all sources

        NAME                           VARIANT                        STATUS                         DESCRIPTION
        average_user_transaction       quickstart (default)           NO_STATUS                      the average transaction amount for a user
        transactions                   kaggle (default)               NO_STATUS                      Fraud Dataset From Kaggle
        ```

        ``` py title="Input"
        print(sources_list)
        ```

        ``` json title="Output"
        // list_sources returns a list of Source objects

        [name: "average_user_transaction"
        default_variant: "quickstart"
        variants: "quickstart"
        , name: "transactions"
        default_variant: "kaggle"
        variants: "kaggle"
        ]
        ```

        Returns:
            sources (List[Source]): List of Source Objects
        """
        return list_name_variant_status_desc(self._stub, "source")

    def list_training_sets(self, local=False):
        """List all training sets. Prints a list of all training sets.

        **Examples:**
        ``` py title="Input"
        training_sets_list = rc.list_training_sets()
        ```

        ``` json title="Output"
        // list_training_sets prints out formatted information on all training sets

        NAME                           VARIANT                        STATUS                         DESCRIPTION
        fraud_training                 quickstart (default)           READY                          Training set for fraud detection.
        fraud_training                 v2                             CREATED                        Improved training set for fraud detection.
        recommender                    v1 (default)                   CREATED                        Training set for recommender system.
        ```

        ``` py title="Input"
        print(training_sets_list)
        ```

        ``` json title="Output"
        // list_training_sets returns a list of TrainingSet objects

        [name: "fraud_training"
        default_variant: "quickstart"
        variants: "quickstart", "v2",
        name: "recommender"
        default_variant: "v1"
        variants: "v1"
        ]
        ```

        Returns:
            training_sets (List[TrainingSet]): List of TrainingSet Objects
        """
        return list_name_variant_status_desc(self._stub, "training-set")

    def list_models(self, local=False) -> List[Model]:
        """List all models. Prints a list of all models.

        Returns:
            models (List[Model]): List of Model Objects
        """
        model_protos = list_name(self._stub, "model")
        # TODO: apply values from proto
        models = [Model(proto.name, tags=[], properties={}) for proto in model_protos]

        return models

    def list_providers(self, local=False):
        """List all providers. Prints a list of all providers.

        **Examples:**
        ``` py title="Input"
        providers_list = rc.list_providers()
        ```

        ``` json title="Output"
        // list_providers prints out formatted information on all providers

        NAME                           STATUS                         DESCRIPTION
        redis-quickstart               CREATED                      A Redis deployment we created for the Featureform quickstart
        postgres-quickstart            CREATED                      A Postgres deployment we created for the Featureform quickst
        ```

        ``` py title="Input"
        print(providers_list)
        ```

        ``` json title="Output"
        // list_providers returns a list of Providers objects

        [name: "redis-quickstart"
        description: "A Redis deployment we created for the Featureform quickstart"
        type: "REDIS_ONLINE"
        software: "redis"
        serialized_config: "{\"Addr\": \"quickstart-redis:6379\", \"Password\": \"\", \"DB\": 0}"
        features {
        name: "avg_transactions"
        variant: "quickstart"
        }
        features {
        name: "avg_transactions"
        variant: "production"
        }
        features {
        name: "user_age"
        variant: "quickstart"
        }
        , name: "postgres-quickstart"
        description: "A Postgres deployment we created for the Featureform quickstart"
        type: "POSTGRES_OFFLINE"
        software: "postgres"
        serialized_config: "{\"Host\": \"quickstart-postgres\", \"Port\": \"5432\", \"Username\": \"postgres\", \"Password\": \"password\", \"Database\": \"postgres\"}"
        sources {
        name: "transactions"
        variant: "kaggle"
        }
        sources {
        name: "average_user_transaction"
        variant: "quickstart"
        }
        trainingsets {
        name: "fraud_training"
        variant: "quickstart"
        }
        labels {
        name: "fraudulent"
        variant: "quickstart"
        }
        ]
        ```

        Returns:
            providers (List[Provider]): List of Provider Objects
        """
        return list_name_status_desc(self._stub, "provider")

    def search(self, raw_query, local=False):
        """Search for registered resources. Prints a list of results.

        **Examples:**
        ``` py title="Input"
        providers_list = rc.search("transact")
        ```

        ``` json title="Output"
        // search prints out formatted information on all matches

        NAME                           VARIANT            TYPE
        avg_transactions               default            Source
        ```
        """
        if type(raw_query) != str or len(raw_query) == 0:
            raise Exception("query must be string and cannot be empty")
        processed_query = raw_query.translate({ord(i): None for i in ".,-@!*#"})
        return search(processed_query, self._host)

    def list_feature_views(self, local=False):
        """List all feature views. Prints a list of all feature views."""
        return list_name_status(self._stub, "feature_view")

    def get_feature_view(self, name, local=False):
        """Get a feature view. Prints out information on feature view, and all resources associated with the feature view."""
        return get_feature_view_info(self._stub, name)
