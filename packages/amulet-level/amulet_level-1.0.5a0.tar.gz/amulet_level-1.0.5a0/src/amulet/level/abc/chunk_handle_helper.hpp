#pragma once

#include <memory>

#include <amulet/level/dll.hpp>

#include "chunk_handle.hpp"
#include "history.hpp"

namespace Amulet {

// template <typename RawDimensionT, typename DimensionT, typename ChunkT>
template <
    typename RawDimensionT,
    typename DimensionT,
    typename RawChunkT,
    typename ChunkT,
    std::unique_ptr<ChunkT> (&get_null_chunk)(const std::string&),
    std::string (&get_chunk_id)(const ChunkT&)>
class ChunkHandleHelper : public ChunkHandle {
private:
    std::shared_ptr<RawDimensionT> _raw_dimension;

    std::shared_ptr<HistoryManagerLayer<detail::ChunkKey>> _chunk_history;
    std::shared_ptr<HistoryManagerLayer<std::string>> _chunk_data_history;

    std::shared_ptr<bool> _history_enabled;

    ChunkHandleHelper(
        const DimensionId& dimension_id,
        std::int64_t cx,
        std::int64_t cz,
        std::shared_ptr<RawDimensionT> raw_dimension,
        std::shared_ptr<HistoryManagerLayer<detail::ChunkKey>> chunk_history,
        std::shared_ptr<HistoryManagerLayer<std::string>> chunk_data_history,
        std::shared_ptr<bool> history_enabled);

    friend DimensionT;

    // Get the chunk instance will all components in their null state.
    // Requires _chunk_history shared lock.
    std::unique_ptr<ChunkT> _get_null_chunk();

    // Load the chunk from the raw level.
    // Requires _chunk_history unique lock.
    void _preload();

public:
    // Does the chunk exist. This is a quick way to check if the chunk exists without loading it.
    AMULET_LEVEL_EXPORT bool exists() override;

    // Get a unique copy of the chunk data.
    AMULET_LEVEL_EXPORT std::unique_ptr<ChunkT> get_native_chunk(std::optional<std::set<std::string>> component_ids = std::nullopt);

    // Get a unique copy of the chunk data.
    AMULET_LEVEL_EXPORT std::unique_ptr<Chunk> get_chunk(std::optional<std::set<std::string>> component_ids = std::nullopt) override;

    // Overwrite the chunk data.
    AMULET_LEVEL_EXPORT void set_native_chunk(const ChunkT&);

    // Overwrite the chunk data.
    AMULET_LEVEL_EXPORT void set_chunk(const Chunk&) override;

    // Delete the chunk from the level.
    AMULET_LEVEL_EXPORT void delete_chunk() override;
};

} // namespace Amulet
