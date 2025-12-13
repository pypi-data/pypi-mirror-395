#include "dimension.hpp"
#include "chunk_handle.hpp"

namespace Amulet {

BedrockDimension::BedrockDimension(
    std::shared_ptr<BedrockRawDimension> raw_dimension,
    HistoryManager& history_manager,
    std::shared_ptr<bool> history_enabled)
    : _raw_dimension(std::move(raw_dimension))
    , _chunk_history(history_manager.new_layer<detail::ChunkKey>())
    , _chunk_data_history(history_manager.new_layer<std::string>())
    , _history_enabled(std::move(history_enabled))
{
}

BedrockDimension::~BedrockDimension()
{
}

void BedrockDimension::save() {
    for (const auto& [chunk_key, resource] : _chunk_history->get_resources()) {
        if (!resource->has_changed()) {
            continue;
        }
        auto cx = chunk_key.get_cx();
        auto cz = chunk_key.get_cz();
        auto chunk_handle = get_bedrock_chunk_handle(cx, cz);
        auto chunk = chunk_handle->get_bedrock_chunk();
        _raw_dimension->set_chunk(cx, cz, *chunk);
    }
}

const DimensionId& BedrockDimension::get_dimension_id() const
{
    return _raw_dimension->get_dimension_id();
}

std::variant<SelectionBox, SelectionBoxGroup> BedrockDimension::get_bounds() const
{
    return _raw_dimension->get_bounds();
}

const BlockStack& BedrockDimension::get_default_block() const
{
    return _raw_dimension->get_default_block();
}

const Biome& BedrockDimension::get_default_biome() const
{
    return _raw_dimension->get_default_biome();
}

std::shared_ptr<BedrockChunkHandle> BedrockDimension::get_bedrock_chunk_handle(std::int64_t cx, std::int64_t cz)
{
    auto key = std::make_pair(cx, cz);
    {
        std::shared_lock handle_lock(_chunk_handles_mutex);
        auto it = _chunk_handles.find(key);
        if (it != _chunk_handles.end()) {
            auto chunk_handle = it->second.lock();
            if (chunk_handle) {
                return chunk_handle;
            }
        }
    }
    {
        std::lock_guard handle_lock(_chunk_handles_mutex);
        auto it = _chunk_handles.find(key);
        if (it == _chunk_handles.end()) {
            auto chunk_handle = std::shared_ptr<BedrockChunkHandle>(
                new BedrockChunkHandle(
                    get_dimension_id(),
                    cx,
                    cz,
                    _raw_dimension,
                    _chunk_history,
                    _chunk_data_history,
                    _history_enabled));
            _chunk_handles.emplace(key, chunk_handle);
            return chunk_handle;
        } else {
            auto chunk_handle = it->second.lock();
            if (!chunk_handle) {
                chunk_handle = std::shared_ptr<BedrockChunkHandle>(
                    new BedrockChunkHandle(
                        get_dimension_id(),
                        cx,
                        cz,
                        _raw_dimension,
                        _chunk_history,
                        _chunk_data_history,
                        _history_enabled));
                it->second = chunk_handle;
            }
            return chunk_handle;
        }
    }
}

std::shared_ptr<ChunkHandle> BedrockDimension::get_chunk_handle(std::int64_t cx, std::int64_t cz)
{
    return get_bedrock_chunk_handle(cx, cz);
}

} // namespace Amulet
