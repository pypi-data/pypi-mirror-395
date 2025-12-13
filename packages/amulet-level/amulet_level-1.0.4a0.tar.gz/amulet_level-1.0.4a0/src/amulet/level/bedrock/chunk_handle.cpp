#include <stdexcept>

#include <amulet/utils/mutex.hpp>

#include <amulet/level/abc/chunk_handle_helper_impl.hpp>

#include "chunk_handle.hpp"

namespace Amulet {

template class ChunkHandleHelper<
    BedrockRawDimension,
    BedrockDimension,
    BedrockRawChunk,
    BedrockChunk,
    detail::get_bedrock_null_chunk,
    detail::get_bedrock_chunk_id>;

std::unique_ptr<BedrockChunk> BedrockChunkHandle::get_bedrock_chunk(std::optional<std::set<std::string>> component_ids)
{
    return get_native_chunk(std::move(component_ids));
}

void BedrockChunkHandle::set_bedrock_chunk(const BedrockChunk& chunk)
{
    set_native_chunk(chunk);
}

} // namespace Amulet
