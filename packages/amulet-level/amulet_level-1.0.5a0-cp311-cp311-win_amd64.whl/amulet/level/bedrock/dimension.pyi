from __future__ import annotations

import typing
from builtins import str as BedrockInternalDimensionID

import amulet.level.abc.dimension
import amulet.level.bedrock.chunk_handle

__all__: list[str] = ["BedrockDimension", "BedrockInternalDimensionID"]

class BedrockDimension(amulet.level.abc.dimension.Dimension):
    def get_chunk_handle(
        self, cx: typing.SupportsInt, cz: typing.SupportsInt
    ) -> amulet.level.bedrock.chunk_handle.BedrockChunkHandle:
        """
        Get the chunk handle for the given chunk in this dimension.
        Thread safe.

        :param cx: The chunk x coordinate to load.
        :param cz: The chunk z coordinate to load.
        """
