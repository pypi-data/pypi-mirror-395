from __future__ import annotations

import typing

import amulet.core.biome
import amulet.core.block
import amulet.core.chunk
import amulet.core.chunk.component.block_component
import amulet.level.java.chunk_components

__all__: list[str] = [
    "JavaChunk",
    "JavaChunk0",
    "JavaChunk1444",
    "JavaChunk1466",
    "JavaChunk2203",
    "JavaChunkNA",
]

class JavaChunk(amulet.core.chunk.Chunk):
    pass

class JavaChunk0(
    JavaChunk,
    amulet.level.java.chunk_components.JavaRawChunkComponent,
    amulet.level.java.chunk_components.DataVersionComponent,
    amulet.core.chunk.component.block_component.BlockComponent,
):
    def __init__(
        self,
        data_version: typing.SupportsInt,
        default_block: amulet.core.block.BlockStack,
        default_biome: amulet.core.biome.Biome,
    ) -> None: ...

class JavaChunk1444(
    JavaChunk,
    amulet.level.java.chunk_components.JavaRawChunkComponent,
    amulet.level.java.chunk_components.DataVersionComponent,
    amulet.core.chunk.component.block_component.BlockComponent,
):
    def __init__(
        self,
        data_version: typing.SupportsInt,
        default_block: amulet.core.block.BlockStack,
        default_biome: amulet.core.biome.Biome,
    ) -> None: ...

class JavaChunk1466(
    JavaChunk,
    amulet.level.java.chunk_components.JavaRawChunkComponent,
    amulet.level.java.chunk_components.DataVersionComponent,
    amulet.core.chunk.component.block_component.BlockComponent,
):
    def __init__(
        self,
        data_version: typing.SupportsInt,
        default_block: amulet.core.block.BlockStack,
        default_biome: amulet.core.biome.Biome,
    ) -> None: ...

class JavaChunk2203(
    JavaChunk,
    amulet.level.java.chunk_components.JavaRawChunkComponent,
    amulet.level.java.chunk_components.DataVersionComponent,
    amulet.core.chunk.component.block_component.BlockComponent,
):
    def __init__(
        self,
        data_version: typing.SupportsInt,
        default_block: amulet.core.block.BlockStack,
        default_biome: amulet.core.biome.Biome,
    ) -> None: ...

class JavaChunkNA(
    JavaChunk,
    amulet.level.java.chunk_components.JavaRawChunkComponent,
    amulet.level.java.chunk_components.DataVersionComponent,
    amulet.core.chunk.component.block_component.BlockComponent,
):
    def __init__(
        self,
        default_block: amulet.core.block.BlockStack,
        default_biome: amulet.core.biome.Biome,
    ) -> None: ...
