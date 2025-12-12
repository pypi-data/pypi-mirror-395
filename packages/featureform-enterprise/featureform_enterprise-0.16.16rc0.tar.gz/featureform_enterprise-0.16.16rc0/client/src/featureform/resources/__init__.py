# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Resources module for Featureform.

This module contains high-level resource classes including Source, Feature, Label,
TrainingSet, Model, and related classes.

All resource classes have been migrated to focused modules for better organization.

USAGE:
------
```python
from featureform.resources import (
    Source, SourceVariant, SourceReference,
    Feature, FeatureVariant, OnDemandFeatureVariant,
    Label, LabelVariant,
    TrainingSet, TrainingSetVariant,
    Model,
    FeatureView,
)
```

MODULE STRUCTURE:
-----------------
- resources/base.py - Base classes and Resource union type
- resources/source.py - Source, SourceVariant, SourceReference, EntityReference, ProviderReference
- resources/feature.py - Feature, FeatureVariant, OnDemandFeatureVariant, AttributeFeature, AggregateFeature
- resources/label.py - Label, LabelVariant
- resources/training_set.py - TrainingSet, TrainingSetVariant, TrainingSetFeatures
- resources/model.py - Model
- resources/feature_view.py - FeatureView, FeatureViewTableOptions, MaterializationOptions
- resources/stream.py - BaseStream, StreamFeature, StreamLabel
- resources/mappings.py - EntityMapping, EntityMappings
- resources/transformations.py - DFTransformation
"""

# Import from focused modules
# Re-export from config for backwards compatibility
from ..config import *  # noqa: F401, F403

# Re-export from enums for backwards compatibility
from ..enums import AggregateFunction, ResourceStatus

# Re-export from state for backwards compatibility
from ..state import ResourceRedefinedError, ResourceState

# Re-export from resources submodules for backwards compatibility
from .base import (
    Config,
    HasNameVariant,
    Location_Duplicate,
    NameVariant,
    Resource,
    ResourceVariant,
    valid_name_variant,
)
from .entity import Entity, EntityReference
from .feature import (
    Additional_Parameters,
    AggregateFeature,
    AttributeFeature,
    Feature,
    FeatureDefinition,
    FeatureDefinitionPayload,
    FeatureVariant,
    OndemandFeatureParameters,
    OnDemandFeatureVariant,
    PrecomputedFeatureParameters,
)
from .feature_view import FeatureView, FeatureViewTableOptions, MaterializationOptions
from .label import Label, LabelVariant
from .locations import (
    FileStore,
    GlueCatalogTable,
    Location,
    SQLTable,
    StreamChannel,
    UnityCatalogTable,
)
from .mappings import (
    EntityMapping,
    EntityMappings,
    FeaturesSchema,
    ResourceColumnMapping,
)
from .model import Model
from .provider import ErrorInfo, Properties, Provider, ServerStatus
from .schedule import DailyPartition, HashPartition, PartitionType, Schedule
from .source import (
    ProviderReference,
    Source,
    SourceDefinition,
    SourceReference,
    SourceVariant,
)
from .stream import (
    BaseStream,
    FeatureStreamResource,
    LabelStreamResource,
    StreamFeature,
    StreamLabel,
)
from .training_set import TrainingSet, TrainingSetFeatures, TrainingSetVariant
from .transformations import (
    DFTransformation,
    PrimaryData,
    SQLTransformation,
    Transformation,
)
from .user import User

# Explicitly list main exports for clarity
__all__ = [
    # Base classes
    "Config",
    "HasNameVariant",
    "Location_Duplicate",
    "NameVariant",
    "Resource",
    "ResourceVariant",
    "valid_name_variant",
    # Re-exported from resources submodules
    "DailyPartition",
    "DFTransformation",
    "HashPartition",
    "Entity",
    "EntityReference",
    "ErrorInfo",
    "FileStore",
    "GlueCatalogTable",
    "Location",
    "PartitionType",
    "PrimaryData",
    "Properties",
    "Provider",
    "ResourceColumnMapping",
    "Schedule",
    "ServerStatus",
    "SQLTable",
    "SQLTransformation",
    "StreamChannel",
    "Transformation",
    "UnityCatalogTable",
    "User",
    # Re-exported from state
    "ResourceRedefinedError",
    "ResourceState",
    # Re-exported from enums
    "AggregateFunction",
    "ResourceStatus",
    # Source classes
    "Source",
    "SourceVariant",
    "SourceReference",
    "SourceDefinition",
    "EntityReference",
    "ProviderReference",
    # Feature classes
    "Feature",
    "FeatureVariant",
    "OnDemandFeatureVariant",
    "OndemandFeatureParameters",
    "PrecomputedFeatureParameters",
    "Additional_Parameters",
    "AttributeFeature",
    "AggregateFeature",
    "FeatureDefinition",
    "FeatureDefinitionPayload",
    # Label classes
    "Label",
    "LabelVariant",
    # TrainingSet classes
    "TrainingSet",
    "TrainingSetVariant",
    "TrainingSetFeatures",
    # Model
    "Model",
    # FeatureView
    "FeatureView",
    "FeatureViewTableOptions",
    "MaterializationOptions",
    # Stream classes
    "BaseStream",
    "StreamFeature",
    "StreamLabel",
    "FeatureStreamResource",
    "LabelStreamResource",
    # Mapping classes
    "EntityMapping",
    "EntityMappings",
    "FeaturesSchema",
    # Transformation
    "DFTransformation",
]
