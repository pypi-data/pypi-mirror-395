#pragma once

#include <memory>

#include <amulet/level/dll.hpp>

#include <amulet/level/abc/chunk_handle_helper.hpp>
#include <amulet/level/abc/history.hpp>

#include "chunk.hpp"
#include "raw_dimension.hpp"

namespace Amulet {

class JavaDimension;

class JavaChunkHandle : public ChunkHandleHelper<
    JavaRawDimension, 
    JavaDimension,
    JavaRawChunk,
    JavaChunk,
    detail::get_java_null_chunk,
    detail::get_java_chunk_id
> {
private:
    using ChunkHandleHelper::ChunkHandleHelper;

public:
    // Get a unique copy of the chunk data.
    AMULET_LEVEL_EXPORT std::unique_ptr<JavaChunk> get_java_chunk(std::optional<std::set<std::string>> component_ids = std::nullopt);

    // Overwrite the chunk data.
    AMULET_LEVEL_EXPORT void set_java_chunk(const JavaChunk&);
};

} // namespace Amulet
