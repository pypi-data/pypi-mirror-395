from __future__ import annotations

from builtins import str as JavaInternalDimensionID

from amulet.level.java.chunk_handle import JavaChunkHandle
from amulet.level.java.dimension import JavaDimension
from amulet.level.java.level import JavaLevel
from amulet.level.java.raw_dimension import JavaRawDimension
from amulet.level.java.raw_level import JavaCreateArgsV1, JavaRawLevel

from . import (
    chunk,
    chunk_components,
    chunk_handle,
    dimension,
    level,
    long_array,
    raw_dimension,
    raw_level,
)

__all__: list[str] = [
    "JavaChunkHandle",
    "JavaCreateArgsV1",
    "JavaDimension",
    "JavaInternalDimensionID",
    "JavaLevel",
    "JavaRawDimension",
    "JavaRawLevel",
    "chunk",
    "chunk_components",
    "chunk_handle",
    "dimension",
    "level",
    "long_array",
    "raw_dimension",
    "raw_level",
]
