from __future__ import annotations

import typing

import amulet.core.biome
import amulet.core.block
import amulet.core.selection.box
import amulet.level.bedrock.chunk
import amulet.level.bedrock.raw_chunk
import amulet.utils.lock

__all__: list[str] = ["BedrockChunkCoordIterator", "BedrockRawDimension"]

class BedrockChunkCoordIterator:
    def __iter__(self) -> typing.Any: ...
    def __next__(self) -> tuple[int, int]: ...

class BedrockRawDimension:
    def decode_chunk(
        self,
        raw_chunk: amulet.level.bedrock.raw_chunk.BedrockRawChunk,
        cx: typing.SupportsInt,
        cz: typing.SupportsInt,
    ) -> amulet.level.bedrock.chunk.BedrockChunk:
        """
        Decode a raw chunk to a chunk object.
        TODO: thread safety
        """

    def delete_chunk(self, cx: typing.SupportsInt, cz: typing.SupportsInt) -> None:
        """
        Delete the chunk from this dimension.
        External ReadWrite:SharedReadWrite lock required.
        """

    def destroy(self) -> None:
        """
        Destroy the instance.
        Calls made after this will fail.
        This may only be called by the owner of the instance.
        External ReadWrite:Unique lock required.
        """

    def encode_chunk(
        self,
        chunk: amulet.level.bedrock.chunk.BedrockChunk,
        cx: typing.SupportsInt,
        cz: typing.SupportsInt,
    ) -> amulet.level.bedrock.raw_chunk.BedrockRawChunk:
        """
        Encode a chunk object to its raw data.
        This will mutate the chunk data.
        TODO: thread safety
        """

    def get_chunk(
        self, cx: typing.SupportsInt, cz: typing.SupportsInt
    ) -> amulet.level.bedrock.chunk.BedrockChunk:
        """
        Get and decode the chunk.
        TODO: thread safety
        """

    def get_raw_chunk(
        self, cx: typing.SupportsInt, cz: typing.SupportsInt
    ) -> amulet.level.bedrock.raw_chunk.BedrockRawChunk:
        """
        Get the raw chunk from this dimension.
        External Read:SharedReadWrite lock required.
        """

    def has_chunk(self, cx: typing.SupportsInt, cz: typing.SupportsInt) -> bool:
        """
        Does the chunk exist in this dimension.
        External Read:SharedReadWrite lock required.
        External Read:SharedReadOnly lock optional.
        """

    def is_destroyed(self) -> bool:
        """
        Has the instance been destroyed.
        If this is false, other calls will fail.
        External Read:SharedReadWrite lock required.
        """

    def set_chunk(
        self,
        cx: typing.SupportsInt,
        cz: typing.SupportsInt,
        chunk: amulet.level.bedrock.chunk.BedrockChunk,
    ) -> None:
        """
        Encode and set the chunk.
        This will mutate the chunk data.
        TODO: thread safety
        """

    def set_raw_chunk(
        self,
        cx: typing.SupportsInt,
        cz: typing.SupportsInt,
        chunk: amulet.level.bedrock.raw_chunk.BedrockRawChunk,
    ) -> None:
        """
        Set the chunk in this dimension from raw data.
        External ReadWrite:SharedReadWrite lock required.
        """

    @property
    def all_chunk_coords(self) -> BedrockChunkCoordIterator:
        """
        An iterator of all chunk coordinates in the dimension.
        External Read:SharedReadWrite lock required.
        External Read:SharedReadOnly lock optional.
        """

    @property
    def bounds(self) -> amulet.core.selection.box.SelectionBox:
        """
        The selection box that fills the whole world.
        Thread safe.
        """

    @property
    def default_biome(self) -> amulet.core.biome.Biome:
        """
        The default biome for this dimension.
        Thread safe.
        """

    @property
    def default_block(self) -> amulet.core.block.BlockStack:
        """
        The default block for this dimension.
        Thread safe.
        """

    @property
    def dimension_id(self) -> str:
        """
        The identifier for this dimension. eg. "minecraft:overworld".
        Thread safe.
        """

    @property
    def internal_dimension_id(self) -> int:
        """
        The internal identifier for this dimension. eg 0, 1 or 2
        Thread safe.
        """

    @property
    def lock(self) -> amulet.utils.lock.OrderedLock:
        """
        The public lock
        Thread safe.
        """
