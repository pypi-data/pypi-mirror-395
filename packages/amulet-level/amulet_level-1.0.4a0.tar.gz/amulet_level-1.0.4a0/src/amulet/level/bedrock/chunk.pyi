from __future__ import annotations

import amulet.core.chunk
import amulet.core.chunk.component.block_component
import amulet.level.bedrock.chunk_components

__all__: list[str] = ["BedrockChunk", "BedrockChunk118"]

class BedrockChunk(amulet.core.chunk.Chunk):
    pass

class BedrockChunk118(
    BedrockChunk,
    amulet.level.bedrock.chunk_components.BedrockRawChunkComponent,
    amulet.core.chunk.component.block_component.BlockComponent,
):
    pass
