from __future__ import annotations

import typing
from builtins import str as JavaInternalDimensionID

import amulet.level.abc.dimension
import amulet.level.java.chunk_handle

__all__: list[str] = ["JavaDimension", "JavaInternalDimensionID"]

class JavaDimension(amulet.level.abc.dimension.Dimension):
    def get_chunk_handle(
        self, cx: typing.SupportsInt, cz: typing.SupportsInt
    ) -> amulet.level.java.chunk_handle.JavaChunkHandle:
        """
        Get the chunk handle for the given chunk in this dimension.
        Thread safe.

        :param cx: The chunk x coordinate to load.
        :param cz: The chunk z coordinate to load.
        """
