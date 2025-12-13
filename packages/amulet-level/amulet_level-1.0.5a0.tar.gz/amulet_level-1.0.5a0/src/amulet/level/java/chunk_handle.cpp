#include <stdexcept>

#include <amulet/utils/mutex.hpp>

#include <amulet/level/abc/chunk_handle_helper_impl.hpp>

#include "chunk_handle.hpp"

namespace Amulet {

template class ChunkHandleHelper<
    JavaRawDimension,
    JavaDimension,
    JavaRawChunk,
    JavaChunk,
    detail::get_java_null_chunk,
    detail::get_java_chunk_id>;

std::unique_ptr<JavaChunk> JavaChunkHandle::get_java_chunk(std::optional<std::set<std::string>> component_ids)
{
    return get_native_chunk(std::move(component_ids));
}

void JavaChunkHandle::set_java_chunk(const JavaChunk& chunk)
{
    set_native_chunk(chunk);
}

} // namespace Amulet
