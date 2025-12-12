# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Registrar module for Featureform.

This module contains registrar classes that wrap registered resources and
provide registration functionality.
"""

from .column_mapping import ColumnMapping
from .column_resources import (
    ColumnResource,
    EmbeddingColumnResource,
    FeatureColumnResource,
    LabelColumnResource,
    MultiFeatureColumnResource,
)
from .entity_decorator import entity
from .registrar import Incremental, Registrar, Stream
from .registrars import (
    ColumnSourceRegistrar,
    EntityRegistrar,
    ModelRegistrar,
    ResourceRegistrar,
    SourceRegistrar,
    UserRegistrar,
)
from .transformation_decorators import (
    DFTransformationDecorator,
    SQLTransformationDecorator,
    SubscriptableTransformation,
)
from .variants import Variants

__all__ = [
    "Registrar",
    "Incremental",
    "Stream",
    "EntityRegistrar",
    "UserRegistrar",
    "SourceRegistrar",
    "ColumnSourceRegistrar",
    "ResourceRegistrar",
    "ModelRegistrar",
    "ColumnMapping",
    "Variants",
    "SubscriptableTransformation",
    "SQLTransformationDecorator",
    "DFTransformationDecorator",
    "ColumnResource",
    "FeatureColumnResource",
    "LabelColumnResource",
    "EmbeddingColumnResource",
    "MultiFeatureColumnResource",
    "entity",
]

# Create global registrar instance
global_registrar = Registrar()
