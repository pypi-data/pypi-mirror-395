#pragma once

#include <amulet/core/biome/biome.hpp>
#include <amulet/core/block/block.hpp>
#include <amulet/core/chunk/chunk.hpp>
#include <amulet/core/chunk/component/block_component.hpp>

#include <amulet/level/dll.hpp>

#include "chunk_components/bedrock_raw_chunk_component.hpp"

namespace Amulet {

class BedrockChunk : public Chunk { };

namespace detail {
    // Get a null chunk instance for the given chunk id.
    std::unique_ptr<BedrockChunk> get_bedrock_null_chunk(const std::string& chunk_id);

    // Get the chunk's identifier.
    std::string get_bedrock_chunk_id(const BedrockChunk& chunk);
} // namespace detail

// LegacyTerrain
class BedrockChunk0 : public ChunkComponentHelper<
                          BedrockChunk,
                          BedrockRawChunkComponent,
                          BlockComponent> {
public:
    AMULET_LEVEL_EXPORT static const std::string ChunkID;

    std::string get_chunk_id() const override;

    using ChunkComponentHelper::ChunkComponentHelper;
    AMULET_LEVEL_EXPORT BedrockChunk0(
        const BlockStack& default_block,
        const Biome& default_biome);
};

// V1.0, SubChunkPrefix and Data2D
class BedrockChunk1 : public ChunkComponentHelper<
                          BedrockChunk,
                          BedrockRawChunkComponent,
                          BlockComponent> {
public:
    AMULET_LEVEL_EXPORT static const std::string ChunkID;

    std::string get_chunk_id() const override;

    using ChunkComponentHelper::ChunkComponentHelper;
    AMULET_LEVEL_EXPORT BedrockChunk1(
        const BlockStack& default_block,
        const Biome& default_biome);
};

// V1.18, SubChunkPrefix and Data3D
class BedrockChunk118 : public ChunkComponentHelper<
                            BedrockChunk,
                            BedrockRawChunkComponent,
                            BlockComponent> {
public:
    AMULET_LEVEL_EXPORT static const std::string ChunkID;

    std::string get_chunk_id() const override;

    using ChunkComponentHelper::ChunkComponentHelper;
    AMULET_LEVEL_EXPORT BedrockChunk118(
        const BlockStack& default_block,
        const Biome& default_biome);
};

} // namespace Amulet
