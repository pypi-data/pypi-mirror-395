#pragma once

#include <memory>
#include <shared_mutex>
#include <variant>

#include <amulet/level/abc/chunk_handle.hpp>
#include <amulet/level/abc/dimension.hpp>
#include <amulet/level/abc/history.hpp>
#include <amulet/level/dll.hpp>

#include "chunk_handle.hpp"
#include "raw_dimension.hpp"

namespace Amulet {

class BedrockDimension : public Dimension {
private:
    std::map<std::pair<std::int64_t, std::int64_t>, std::weak_ptr<BedrockChunkHandle>> _chunk_handles;
    std::shared_mutex _chunk_handles_mutex;

    std::shared_ptr<BedrockRawDimension> _raw_dimension;

    std::shared_ptr<HistoryManagerLayer<detail::ChunkKey>> _chunk_history;
    std::shared_ptr<HistoryManagerLayer<std::string>> _chunk_data_history;

    std::shared_ptr<bool> _history_enabled;

    BedrockDimension(
        std::shared_ptr<BedrockRawDimension> raw_dimension,
        HistoryManager& history_manager,
        std::shared_ptr<bool> history_enabled);

    friend class BedrockLevel;

    void save();

public:
    // Destructor
    AMULET_LEVEL_EXPORT ~BedrockDimension() override;

    // Get the dimension id for this dimension.
    // Thread safe.
    AMULET_LEVEL_EXPORT const DimensionId& get_dimension_id() const override;

    // The editable region of the dimension.
    // Thread safe.
    AMULET_LEVEL_EXPORT std::variant<SelectionBox, SelectionBoxGroup> get_bounds() const override;

    // Get the default block for this dimension.
    // Thread safe.
    AMULET_LEVEL_EXPORT const BlockStack& get_default_block() const override;

    // Get the default biome for this dimension.
    // Thread safe.
    AMULET_LEVEL_EXPORT const Biome& get_default_biome() const override;

    // Get a chunk handle for a specific chunk.
    // Thread safe.
    AMULET_LEVEL_EXPORT std::shared_ptr<BedrockChunkHandle> get_bedrock_chunk_handle(std::int64_t cx, std::int64_t cz);

    // Get a chunk handle for a specific chunk.
    // Thread safe.
    AMULET_LEVEL_EXPORT std::shared_ptr<ChunkHandle> get_chunk_handle(std::int64_t cx, std::int64_t cz) override;
};

} // namespace Amulet
