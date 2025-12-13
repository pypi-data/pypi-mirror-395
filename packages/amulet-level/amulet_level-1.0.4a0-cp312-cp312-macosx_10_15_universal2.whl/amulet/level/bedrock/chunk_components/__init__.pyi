from __future__ import annotations

import typing

import amulet.level.bedrock.raw_chunk

__all__: list[str] = ["BedrockRawChunkComponent"]

class BedrockRawChunkComponent:
    ComponentID: typing.ClassVar[str] = "Amulet::BedrockRawChunkComponent"
    @property
    def raw_data(self) -> amulet.level.bedrock.raw_chunk.BedrockRawChunk:
        """
        This is subject to change as data gets moved into the chunk class.
        Do not rely on data in here existing.
        """

    @raw_data.setter
    def raw_data(
        self, arg1: amulet.level.bedrock.raw_chunk.BedrockRawChunk
    ) -> None: ...
