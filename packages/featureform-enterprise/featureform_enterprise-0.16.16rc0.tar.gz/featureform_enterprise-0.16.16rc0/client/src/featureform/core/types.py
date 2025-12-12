# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Core type definitions and conversions.

This module contains type-related utilities including VectorType and
pandas-to-featureform datatype mappings.
"""

from typing import Union

import numpy

from ..enums import ScalarType
from ..proto import metadata_pb2 as pb

# Mapping from pandas/numpy dtypes to Featureform scalar types
pd_to_ff_datatype = {
    numpy.dtype("float64"): ScalarType.FLOAT64,
    numpy.dtype("float32"): ScalarType.FLOAT32,
    numpy.dtype("int64"): ScalarType.INT64,
    numpy.dtype("int"): ScalarType.INT,
    numpy.dtype("int32"): ScalarType.INT32,
    numpy.dtype("O"): ScalarType.STRING,
    numpy.dtype("str"): ScalarType.STRING,
    numpy.dtype("bool"): ScalarType.BOOL,
}


class VectorType:
    """Represents a vector type with scalar element type and dimensions."""

    def __init__(
        self, scalarType: Union[ScalarType, str], dims: int, is_embedding: bool = False
    ):
        self.scalarType = (
            scalarType if isinstance(scalarType, ScalarType) else ScalarType(scalarType)
        )
        self.dims = dims
        self.is_embedding = is_embedding

    def to_proto(self):
        proto_vec = pb.VectorType(
            scalar=self.scalarType.to_proto_enum(),
            dimension=self.dims,
            is_embedding=self.is_embedding,
        )
        return pb.ValueType(vector=proto_vec)

    @classmethod
    def from_proto(cls, proto_val):
        proto_vec = proto_val.vector
        scalar = ScalarType.from_proto(proto_vec.scalar)
        dims = proto_vec.dimension
        is_embedding = proto_vec.is_embedding
        return VectorType(scalar, dims, is_embedding)


def type_from_proto(proto_val):
    """Convert a protobuf ValueType to a Python type."""
    value_type = proto_val.WhichOneof("Type")
    if value_type == "scalar":
        return ScalarType.from_proto(proto_val.scalar)
    elif value_type == "vector":
        return VectorType.from_proto(proto_val)
    else:
        return ScalarType.NIL
