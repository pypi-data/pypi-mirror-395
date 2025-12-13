#pragma once

#include <cstdint>
#include <filesystem>
#include <map>
#include <string>

#include <amulet/nbt/tag/named_tag.hpp>

#include <amulet/core/biome/biome.hpp>
#include <amulet/core/block/block.hpp>
#include <amulet/core/selection/box_group.hpp>

#include <amulet/utils/mutex.hpp>

#include <amulet/anvil/dimension.hpp>

#include <amulet/level/dll.hpp>
#include <amulet/level/abc/dimension.hpp>

#include "chunk.hpp"

namespace Amulet {

using JavaInternalDimensionID = std::string;

class JavaRawLevel;

class JavaRawDimension {
private:
    OrderedMutex _public_mutex;
    AnvilDimension _anvil_dimension;
    JavaInternalDimensionID _relative_path;
    DimensionId _dimension_id;
    SelectionBox _bounds;
    BlockStack _default_block;
    Biome _default_biome;
    bool _destroyed = false;

    template <typename layersT>
    JavaRawDimension(
        const std::filesystem::path& path,
        bool mcc,
        const layersT& layers,
        const JavaInternalDimensionID& relative_path,
        const DimensionId& dimension_id,
        const SelectionBox& bounds,
        const BlockStack& default_block,
        const Biome& default_biome)
        : _anvil_dimension(
              [&path] {
                  if (!std::filesystem::exists(path)) {
                      std::filesystem::create_directories(path);
                  } else if (!std::filesystem::is_directory(path)) {
                      throw std::invalid_argument("JavaRawDimension path is not a directory: " + path.string());
                  }
                  return path;
              }(),
              layers, mcc)
        , _relative_path(relative_path)
        , _dimension_id(dimension_id)
        , _bounds(bounds)
        , _default_block(default_block)
        , _default_biome(default_biome)
    {
    }

    friend JavaRawLevel;

public:
    // Destructor.
    AMULET_LEVEL_EXPORT ~JavaRawDimension();

    // The public mutex
    // Thread safe.
    AMULET_LEVEL_EXPORT OrderedMutex& get_mutex();

    // The identifier for this dimension. eg. "minecraft:overworld".
    // Thread safe.
    AMULET_LEVEL_EXPORT const DimensionId& get_dimension_id() const;

    // The relative path to the dimension. eg. "DIM1".
    // Thread safe.
    AMULET_LEVEL_EXPORT const JavaInternalDimensionID& get_relative_path() const;

    // The selection box that fills the whole world.
    // Thread safe.
    AMULET_LEVEL_EXPORT const SelectionBox& get_bounds() const;

    // The default block for this dimension.
    // Thread safe.
    AMULET_LEVEL_EXPORT const BlockStack& get_default_block() const;

    // The default biome for this dimension.
    // Thread safe.
    AMULET_LEVEL_EXPORT const Biome& get_default_biome() const;

    // An iterator of all chunk coordinates in the dimension.
    // External Read:SharedReadWrite lock required.
    // External Read:SharedReadOnly lock optional.
    AMULET_LEVEL_EXPORT AnvilChunkCoordIterator all_chunk_coords() const;

    // Does the chunk exist in this dimension.
    // External Read:SharedReadWrite lock required.
    // External Read:SharedReadOnly lock optional.
    AMULET_LEVEL_EXPORT bool has_chunk(std::int64_t cx, std::int64_t cz);

    // Delete the chunk from this dimension.
    // External ReadWrite:SharedReadWrite lock required.
    AMULET_LEVEL_EXPORT void delete_chunk(std::int64_t cx, std::int64_t cz);

    // Get the raw chunk from this dimension.
    // External Read:SharedReadWrite lock required.
    AMULET_LEVEL_EXPORT JavaRawChunk get_raw_chunk(std::int64_t cx, std::int64_t cz);

    // Set the chunk in this dimension from raw data.
    // External ReadWrite:SharedReadWrite lock required.
    AMULET_LEVEL_EXPORT void set_raw_chunk(std::int64_t cx, std::int64_t cz, const JavaRawChunk& chunk);

    // Decode a raw chunk to a chunk object.
    // This will mutate the chunk data.
    // TODO: thread safety
    AMULET_LEVEL_EXPORT std::unique_ptr<JavaChunk> decode_chunk(JavaRawChunk raw_chunk, std::int64_t cx, std::int64_t cz);

    // Encode a chunk object to its raw data.
    // This will mutate the chunk data.
    // TODO: thread safety
    AMULET_LEVEL_EXPORT JavaRawChunk encode_chunk(JavaChunk& chunk, std::int64_t cx, std::int64_t cz);
    
    // Get and decode the chunk.
    // TODO: thread safety
    AMULET_LEVEL_EXPORT std::unique_ptr<JavaChunk> get_chunk(std::int64_t cx, std::int64_t cz);

    // Encode and set the chunk.
    // This will mutate the chunk data.
    // TODO: thread safety
    AMULET_LEVEL_EXPORT void set_chunk(std::int64_t cx, std::int64_t cz, JavaChunk& chunk);

    // Compact the level.
    // External Read:SharedReadWrite lock required.
    AMULET_LEVEL_EXPORT void compact();

    // Destroy the instance.
    // Calls made after this will fail.
    // This may only be called by the owner of the instance.
    // External ReadWrite:Unique lock required.
    AMULET_LEVEL_EXPORT void destroy();

    // Has the instance been destroyed.
    // If this is false, other calls will fail.
    // External Read:SharedReadWrite lock required.
    AMULET_LEVEL_EXPORT bool is_destroyed();
};

} // namespace Amulet
