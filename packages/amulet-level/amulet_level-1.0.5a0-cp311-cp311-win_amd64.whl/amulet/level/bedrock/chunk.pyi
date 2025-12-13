from __future__ import annotations

import amulet.core.chunk
import amulet.core.chunk.component.block_component
import amulet.core.chunk.component.block_entity_component
import amulet.level.bedrock.chunk_components

__all__: list[str] = [
    "BedrockChunk",
    "BedrockChunk0",
    "BedrockChunk1",
    "BedrockChunk118",
]

class BedrockChunk(amulet.core.chunk.Chunk):
    pass

class BedrockChunk0(
    BedrockChunk,
    amulet.level.bedrock.chunk_components.BedrockRawChunkComponent,
    amulet.core.chunk.component.block_component.BlockComponent,
    amulet.core.chunk.component.block_entity_component.BlockEntityComponent,
):
    pass

class BedrockChunk1(
    BedrockChunk,
    amulet.level.bedrock.chunk_components.BedrockRawChunkComponent,
    amulet.core.chunk.component.block_component.BlockComponent,
    amulet.core.chunk.component.block_entity_component.BlockEntityComponent,
):
    pass

class BedrockChunk118(
    BedrockChunk,
    amulet.level.bedrock.chunk_components.BedrockRawChunkComponent,
    amulet.core.chunk.component.block_component.BlockComponent,
    amulet.core.chunk.component.block_entity_component.BlockEntityComponent,
):
    pass
