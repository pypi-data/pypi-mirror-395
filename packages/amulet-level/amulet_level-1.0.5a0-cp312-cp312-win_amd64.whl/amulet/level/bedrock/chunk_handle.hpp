#pragma once

#include <memory>

#include <amulet/level/dll.hpp>

#include <amulet/level/abc/chunk_handle_helper.hpp>
#include <amulet/level/abc/history.hpp>

#include "chunk.hpp"
#include "raw_chunk.hpp"
#include "raw_dimension.hpp"

namespace Amulet {

class BedrockDimension;

class BedrockChunkHandle : public ChunkHandleHelper<
                            BedrockRawDimension,
                            BedrockDimension,
                            BedrockRawChunk,
                            BedrockChunk,
                            detail::get_bedrock_null_chunk,
                            detail::get_bedrock_chunk_id> {
private:
    using ChunkHandleHelper::ChunkHandleHelper;

public:
    // Get a unique copy of the chunk data.
    AMULET_LEVEL_EXPORT std::unique_ptr<BedrockChunk> get_bedrock_chunk(std::optional<std::set<std::string>> component_ids = std::nullopt);

    // Overwrite the chunk data.
    AMULET_LEVEL_EXPORT void set_bedrock_chunk(const BedrockChunk&);
};

} // namespace Amulet
