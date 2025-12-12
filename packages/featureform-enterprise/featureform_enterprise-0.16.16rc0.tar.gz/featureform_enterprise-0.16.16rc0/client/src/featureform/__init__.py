# To properly display pending deprecation warnings for the ResourceClient
# and ServingClient classes, we need to set the formatwarning function
# to a custom function to avoid the default behavior of printing the
# the absolute path to the file where the warning was raised. Additionally,
# we need to set the default filter to 'default' to avoid the default
# behavior of ignoring all warnings.
# TODO: Remove this code once the ResourceClient and ServingClient classes
# are deprecated.
import warnings


def custom_warning_formatter(message, category, filename, lineno, file=None, line=None):
    return f"{category.__name__}: {message}\n"


warnings.formatwarning = custom_warning_formatter
warnings.simplefilter("default")

from .client import Client
from .client import ResourceClient as _ResourceClient
from .config.catalogs import SnowflakeCatalog, SnowflakeDynamicTableConfig, UnityCatalog
from .enums import (
    ComputationMode,
    DataResourceType,
    FilePrefix,
    Initialize,
    JoinStrategy,
    RefreshMode,
    ResourceType,
    TableFormat,
    TrainingSetType,
)
from .register import *
from .resources import (
    AWSAssumeRoleCredentials,
    AWSStaticCredentials,
    BasicCredentials,
    DailyPartition,
    DatabricksCredentials,
    EMRCredentials,
    EntityMapping,
    EntityMappings,
    FeaturesSchema,
    GCPCredentials,
    GlueCatalog,
    HashPartition,
    KerberosCredentials,
    MaterializationOptions,
    PostgresConfig,
    SparkCredentials,
)
from .serving import ServingClient

ServingClient = ServingClient
ResourceClient = _ResourceClient
Client = Client

# Executor Credentials
DatabricksCredentials = DatabricksCredentials
EMRCredentials = EMRCredentials
SparkCredentials = SparkCredentials

# Cloud Provider Credentials
AWSStaticCredentials = AWSStaticCredentials
AWSAssumeRoleCredentials = AWSAssumeRoleCredentials
GCPCredentials = GCPCredentials
GlueCatalog = GlueCatalog
UnityCatalog = UnityCatalog
SnowflakeCatalog = SnowflakeCatalog
SnowflakeDynamicTableConfig = SnowflakeDynamicTableConfig

# HDFS Credentials
BasicCredentials = BasicCredentials
KerberosCredentials = KerberosCredentials

# Feature Views
MaterializationOptions = MaterializationOptions
JoinStrategy = JoinStrategy
FeaturesSchema = FeaturesSchema
EntityMappings = EntityMappings
EntityMapping = EntityMapping

# Partitioning
DailyPartition = DailyPartition
HashPartition = HashPartition

# Provider Configs
PostgresConfig = PostgresConfig

# Class API
Feature = FeatureColumnResource
Label = LabelColumnResource
Variants = Variants
Embedding = EmbeddingColumnResource
FeatureStream = FeatureStreamResource
LabelStream = LabelStreamResource
MultiFeature = MultiFeatureColumnResource

set_run = set_run
get_run = get_run

# Enums
DataResourceType = DataResourceType
ResourceType = ResourceType
TableFormat = TableFormat
FilePrefix = FilePrefix
TrainingSetType = TrainingSetType
ComputationMode = ComputationMode
JoinStrategy = JoinStrategy
RefreshMode = RefreshMode
Initialize = Initialize
