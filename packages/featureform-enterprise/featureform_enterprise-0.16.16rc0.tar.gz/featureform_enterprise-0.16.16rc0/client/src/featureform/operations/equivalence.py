# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Equivalence operations for Featureform resources.

This module contains functions for finding and setting equivalent resource variants.
"""

import logging
from typing import Optional

from ..proto import metadata_pb2 as pb

logger = logging.getLogger(__name__)


def _get_and_set_equivalent_variant(
    req_id, resource_variant_proto, variant_field, stub
) -> Optional[str]:
    """
    Get an equivalent variant for a resource and set it if found.

    Args:
        req_id: Request ID for the operation
        resource_variant_proto: The resource variant protobuf
        variant_field: The field name for the variant type
        stub: The gRPC stub for making requests

    Returns:
        The equivalent variant name if found, None otherwise
    """
    res_pb = pb.ResourceVariant(
        **{variant_field: getattr(resource_variant_proto, variant_field)}
    )
    logger.info("Starting to get equivalent")
    # Get equivalent from stub
    equivalent = stub.GetEquivalent(
        pb.GetEquivalentRequest(
            request_id=resource_variant_proto.request_id,
            variant=res_pb,
        )
    )
    rv_proto = getattr(resource_variant_proto, variant_field)
    logger.info("Finished get equivalent")

    # grpc call returns the default ResourceVariant proto when equivalent doesn't exist which explains the below check
    if equivalent != pb.ResourceVariant():
        variant_value = getattr(getattr(equivalent, variant_field), "variant")
        print(
            f"Looks like an equivalent {variant_field.replace('_', ' ')} already exists, going to use its variant: ",
            variant_value,
        )
        # TODO add confirmation from user before using equivalent variant
        rv_proto.variant = variant_value
        return variant_value
    return None
