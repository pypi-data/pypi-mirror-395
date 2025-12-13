#include <mutex>
#include <shared_mutex>

#include "raw_dimension.hpp"

namespace Amulet {

JavaRawDimension::~JavaRawDimension()
{
    destroy();
}

OrderedMutex& JavaRawDimension::get_mutex()
{
    return _public_mutex;
}

const DimensionId& JavaRawDimension::get_dimension_id() const
{
    return _dimension_id;
}

const JavaInternalDimensionID& JavaRawDimension::get_relative_path() const
{
    return _relative_path;
}

const SelectionBox& JavaRawDimension::get_bounds() const
{
    return _bounds;
}

const BlockStack& JavaRawDimension::get_default_block() const
{
    return _default_block;
}

const Biome& JavaRawDimension::get_default_biome() const
{
    return _default_biome;
}

AnvilChunkCoordIterator JavaRawDimension::all_chunk_coords() const
{
    return _anvil_dimension.all_chunk_coords();
}

bool JavaRawDimension::has_chunk(std::int64_t cx, std::int64_t cz)
{
    OrderedLockGuard<ThreadAccessMode::Read, ThreadShareMode::SharedReadWrite> lock(_anvil_dimension.get_mutex());
    return _anvil_dimension.has_chunk(cx, cz);
}
void JavaRawDimension::delete_chunk(std::int64_t cx, std::int64_t cz)
{
    OrderedLockGuard<ThreadAccessMode::ReadWrite, ThreadShareMode::SharedReadWrite> lock(_anvil_dimension.get_mutex());
    _anvil_dimension.delete_chunk(cx, cz);
}
JavaRawChunk JavaRawDimension::get_raw_chunk(std::int64_t cx, std::int64_t cz)
{
    OrderedLockGuard<ThreadAccessMode::Read, ThreadShareMode::SharedReadWrite> lock(_anvil_dimension.get_mutex());
    try {
        return _anvil_dimension.get_chunk_data(cx, cz);
    } catch (const RegionEntryDoesNotExist& e) {
        throw ChunkDoesNotExist(e.what());
    }
}
void JavaRawDimension::set_raw_chunk(std::int64_t cx, std::int64_t cz, const JavaRawChunk& chunk)
{
    OrderedLockGuard<ThreadAccessMode::ReadWrite, ThreadShareMode::SharedReadWrite> lock(_anvil_dimension.get_mutex());
    _anvil_dimension.set_chunk_data(cx, cz, chunk);
}
void JavaRawDimension::compact()
{
    OrderedLockGuard<ThreadAccessMode::ReadWrite, ThreadShareMode::SharedReadOnly> lock(_anvil_dimension.get_mutex());
    _anvil_dimension.compact();
}

std::unique_ptr<JavaChunk> JavaRawDimension::get_chunk(std::int64_t cx, std::int64_t cz) {
    return decode_chunk(get_raw_chunk(cx, cz), cz, cz);
}

void JavaRawDimension::set_chunk(std::int64_t cx, std::int64_t cz, JavaChunk& chunk) {
    set_raw_chunk(cx, cz, encode_chunk(chunk, cx, cz));
}

void JavaRawDimension::destroy()
{
    _destroyed = true;
    std::lock_guard lock(_anvil_dimension.get_mutex());
    _anvil_dimension.destroy();
}

bool JavaRawDimension::is_destroyed()
{
    return _destroyed;
}

} // namespace Amulet
