# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Entity decorator for Featureform.

This module contains the @entity decorator for registering entities and their
associated features and labels.
"""

from .column_resources import (
    EmbeddingColumnResource,
    FeatureColumnResource,
    LabelColumnResource,
    MultiFeatureColumnResource,
)
from .variants import Variants

__all__ = ["entity"]


# Import register_entity from the module that will contain Registrar
def register_entity(name: str):
    """Register an entity. This will be replaced with actual implementation."""
    from . import global_registrar

    return global_registrar.register_entity(name)


def entity(cls):
    """
    Class decorator for registering entities and their associated features and labels.

    **Examples**
    ```python
    @ff.entity
    class User:
        avg_transactions = ff.Feature()
        fraudulent = ff.Label()
    ```

    Returns:
        entity (EntityRegistrar): Decorated entity registrar with features/labels as attributes
    """
    # 1. Use the lowercase name of the class as the entity name
    entity = register_entity(cls.__name__.lower())
    # 2. Given the Feature/Label/Variant class constructors are evaluated
    #    before the entity decorator, apply the entity name to their
    #    respective name dictionaries prior to registration
    for attr_name in cls.__dict__:
        if isinstance(
            cls.__dict__[attr_name],
            (FeatureColumnResource, LabelColumnResource, EmbeddingColumnResource),
        ):
            resource = cls.__dict__[attr_name]
            resource.name = attr_name if resource.name == "" else resource.name
            resource.entity = entity
            resource.register()
            # Set the resource as an attribute on the entity object
            setattr(entity, attr_name, resource)
        elif isinstance(cls.__dict__[attr_name], Variants):
            variants = cls.__dict__[attr_name]
            for variant_key, resource in variants.resources.items():
                resource.name = attr_name if resource.name == "" else resource.name
                resource.entity = entity
                resource.register()
            # Set the variants object as an attribute on the entity object
            setattr(entity, attr_name, variants)
        elif isinstance(cls.__dict__[attr_name], MultiFeatureColumnResource):
            multi_feature = cls.__dict__[attr_name]
            multi_feature_resources = multi_feature.features
            for resource in multi_feature_resources:
                setattr(entity, resource.name, resource)
                resource.entity = entity
                resource.register()
            # Set the MultiFeature object itself as an attribute on the entity object
            setattr(entity, attr_name, multi_feature)

    # Return the entity object so it can be used in the code
    return entity
