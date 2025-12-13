#pragma once

#include <stdexcept>

#include <amulet/utils/mutex.hpp>

#include "chunk_handle_helper.hpp"

namespace Amulet {

template <
    typename RawDimensionT,
    typename DimensionT,
    typename RawChunkT,
    typename ChunkT,
    std::unique_ptr<ChunkT> (&get_null_chunk)(const std::string&),
    std::string (&get_chunk_id)(const ChunkT&)>
ChunkHandleHelper<RawDimensionT, DimensionT, RawChunkT, ChunkT, get_null_chunk, get_chunk_id>::ChunkHandleHelper(
    const DimensionId& dimension_id,
    std::int64_t cx,
    std::int64_t cz,
    std::shared_ptr<RawDimensionT> raw_dimension,
    std::shared_ptr<HistoryManagerLayer<detail::ChunkKey>> chunk_history,
    std::shared_ptr<HistoryManagerLayer<std::string>> chunk_data_history,
    std::shared_ptr<bool> history_enabled)
    : ChunkHandle(dimension_id, cx, cz)
    , _raw_dimension(std::move(raw_dimension))
    , _chunk_history(std::move(chunk_history))
    , _chunk_data_history(std::move(chunk_data_history))
    , _history_enabled(std::move(history_enabled))
{
}

template <
    typename RawDimensionT,
    typename DimensionT,
    typename RawChunkT,
    typename ChunkT,
    std::unique_ptr<ChunkT> (&get_null_chunk)(const std::string&),
    std::string (&get_chunk_id)(const ChunkT&)>
bool ChunkHandleHelper<RawDimensionT, DimensionT, RawChunkT, ChunkT, get_null_chunk, get_chunk_id>::exists()
{
    {
        std::shared_lock history_lock(_chunk_history->get_mutex());
        if (_chunk_history->has_resource(_key)) {
            return !_chunk_history->get_value(_key).empty();
        }
        OrderedLockGuard<ThreadAccessMode::Read, ThreadShareMode::SharedReadWrite> raw_lock(_raw_dimension->get_mutex());
        return _raw_dimension->has_chunk(_cx, _cz);
    }
}

template <
    typename RawDimensionT,
    typename DimensionT,
    typename RawChunkT,
    typename ChunkT,
    std::unique_ptr<ChunkT> (&get_null_chunk)(const std::string&),
    std::string (&get_chunk_id)(const ChunkT&)>
std::unique_ptr<ChunkT> ChunkHandleHelper<RawDimensionT, DimensionT, RawChunkT, ChunkT, get_null_chunk, get_chunk_id>::_get_null_chunk()
{
    std::string data = _chunk_history->get_value(_key);
    if (data.empty()) {
        // Empty if chunk does not exist.
        throw ChunkDoesNotExist();
    } else if (data[0] == 'c') {
        // c followed by the chunk id if a valid chunk.
        return get_null_chunk(data.substr(1));
    } else if (data[0] == 'e') {
        // e followed by the string if other error.
        throw ChunkLoadError(data.substr(1));
    } else {
        throw std::runtime_error("Invalid chunk id prefix.");
    }
}

template <
    typename RawDimensionT,
    typename DimensionT,
    typename RawChunkT,
    typename ChunkT,
    std::unique_ptr<ChunkT> (&get_null_chunk)(const std::string&),
    std::string (&get_chunk_id)(const ChunkT&)>
void ChunkHandleHelper<RawDimensionT, DimensionT, RawChunkT, ChunkT, get_null_chunk, get_chunk_id>::_preload()
{
    // Get the chunk data.
    RawChunkT raw_chunk;
    try {
        raw_chunk = _raw_dimension->get_raw_chunk(_cx, _cz);
    } catch (const ChunkDoesNotExist&) {
        _chunk_history->set_initial_value(_key, "");
        return;
    }

    // Decode the chunk.
    std::unique_ptr<ChunkT> chunk;
    try {
        chunk = _raw_dimension->decode_chunk(std::move(raw_chunk), _cx, _cz);
    } catch (const std::exception& e) {
        _chunk_history->set_initial_value(_key, 'e' + std::string(e.what()));
        return;
    } catch (...) {
        _chunk_history->set_initial_value(_key, "e");
        return;
    }

    // Save the chunk.
    _chunk_history->set_initial_value(_key, 'c' + get_chunk_id(*chunk));
    for (const auto& [component_id, component_data] : chunk->serialise_chunk()) {
        if (!component_data) {
            throw std::runtime_error("Component " + component_id + " cannot be undefined when initialising chunk");
        }
        _chunk_data_history->set_initial_value(std::string(_key) + '/' + component_id, *component_data);
    }
}

template <
    typename RawDimensionT,
    typename DimensionT,
    typename RawChunkT,
    typename ChunkT,
    std::unique_ptr<ChunkT> (&get_null_chunk)(const std::string&),
    std::string (&get_chunk_id)(const ChunkT&)>
std::unique_ptr<ChunkT> ChunkHandleHelper<RawDimensionT, DimensionT, RawChunkT, ChunkT, get_null_chunk, get_chunk_id>::get_native_chunk(std::optional<std::set<std::string>> component_ids)
{
    auto get_chunk = [&]() -> std::unique_ptr<ChunkT> {
        // Load the chunk from the cache.
        auto chunk = _get_null_chunk();
        auto chunk_component_ids = chunk->get_component_ids();
        std::set<std::string> valid_components;
        if (component_ids) {
            // Filter the requested component ids to those in the chunk.
            std::set_intersection(
                chunk_component_ids.begin(), chunk_component_ids.end(),
                component_ids->begin(), component_ids->end(),
                std::inserter(valid_components, valid_components.begin()));
        } else {
            // Get all component ids in the chunk.
            valid_components = std::move(chunk_component_ids);
        }

        // Load all the requested component ids.
        SerialisedChunkComponents component_data;
        for (const auto& component_id : valid_components) {
            component_data.emplace(
                component_id,
                _chunk_data_history->get_value(std::string(_key) + '/' + component_id));
        }

        chunk->reconstruct_chunk(component_data);
        return chunk;
    };

    {
        std::shared_lock lock(_chunk_history->get_mutex());
        if (_chunk_history->has_resource(_key)) {
            // Get the chunk if it has previously been populated.
            return get_chunk();
        }
    }
    {
        std::lock_guard lock(_chunk_history->get_mutex());
        // Load the chunk if it wasn't previously populated.
        if (!_chunk_history->has_resource(_key)) {
            _preload();
        }
    }
    {
        std::shared_lock lock(_chunk_history->get_mutex());
        // Get the chunk.
        return get_chunk();
    }
}

template <
    typename RawDimensionT,
    typename DimensionT,
    typename RawChunkT,
    typename ChunkT,
    std::unique_ptr<ChunkT> (&get_null_chunk)(const std::string&),
    std::string (&get_chunk_id)(const ChunkT&)>
std::unique_ptr<Chunk> ChunkHandleHelper<RawDimensionT, DimensionT, RawChunkT, ChunkT, get_null_chunk, get_chunk_id>::get_chunk(std::optional<std::set<std::string>> component_ids)
{
    return get_native_chunk(component_ids);
}

template <
    typename RawDimensionT,
    typename DimensionT,
    typename RawChunkT,
    typename ChunkT,
    std::unique_ptr<ChunkT> (&get_null_chunk)(const std::string&),
    std::string (&get_chunk_id)(const ChunkT&)>
void ChunkHandleHelper<RawDimensionT, DimensionT, RawChunkT, ChunkT, get_null_chunk, get_chunk_id>::set_native_chunk(const ChunkT& chunk)
{
    // This can be done in parallel
    auto new_chunk_id = 'c' + get_chunk_id(chunk);
    auto component_data = chunk.serialise_chunk();

    std::list<std::pair<std::string, std::string>> defined_component_data;

    auto get_defined_components = [&]<bool error_undefined>() {
        for (const auto& [component_id, data] : component_data) {
            if (data) {
                defined_component_data.emplace_back(std::string(_key) + '/' + component_id, *data);
            } else if constexpr (error_undefined) {
                throw std::runtime_error("When changing chunk class all the data must be present.");
            }
        }
    };

    auto set_new_chunk = [&] {
        // Get the previous chunk id.
        auto old_chunk_id = _chunk_history->get_value(_key);

        // Copy defined component data.
        if (old_chunk_id != new_chunk_id) {
            // Error if any component is undefined
            get_defined_components.template operator()<true>();
        } else {
            // Remove undefined components.
            get_defined_components.template operator()<false>();
        }

        // Set new state.
        _chunk_history->set_value(_key, new_chunk_id);
        if (!defined_component_data.empty()) {
            _chunk_data_history->set_values<HistoryInitialisationMode::Empty>(defined_component_data);
        }
    };

    // Lock the history state
    std::lock_guard lock(_chunk_history->get_mutex());

    if (_chunk_history->has_resource(_key)) {
        set_new_chunk();
    } else if (*_history_enabled) {
        _preload();
        set_new_chunk();
    } else {
        // Resource does not exist and history is disabled

        // Copy components. Error if any component is undefined.
        get_defined_components.template operator()<true>();

        // Set new state. If the resource isn't initialised use this value.
        _chunk_history->set_value<HistoryInitialisationMode::Value>(_key, new_chunk_id);
        if (!defined_component_data.empty()) {
            _chunk_data_history->set_values<HistoryInitialisationMode::Value>(defined_component_data);
        }
    }

    // Notify listeners that it has changed.
    changed.dispatch();
}

template <
    typename RawDimensionT,
    typename DimensionT,
    typename RawChunkT,
    typename ChunkT,
    std::unique_ptr<ChunkT> (&get_null_chunk)(const std::string&),
    std::string (&get_chunk_id)(const ChunkT&)>
void ChunkHandleHelper<RawDimensionT, DimensionT, RawChunkT, ChunkT, get_null_chunk, get_chunk_id>::set_chunk(const Chunk& chunk)
{
    auto* native_chunk = dynamic_cast<const ChunkT*>(&chunk);
    if (!native_chunk) {
        throw std::invalid_argument("chunk is not an instance of the native chunk");
    }
    set_native_chunk(*native_chunk);
}

template <
    typename RawDimensionT,
    typename DimensionT,
    typename RawChunkT,
    typename ChunkT,
    std::unique_ptr<ChunkT> (&get_null_chunk)(const std::string&),
    std::string (&get_chunk_id)(const ChunkT&)>
void ChunkHandleHelper<RawDimensionT, DimensionT, RawChunkT, ChunkT, get_null_chunk, get_chunk_id>::delete_chunk()
{
    std::lock_guard lock(_chunk_history->get_mutex());

    // Set initial state.
    if (*_history_enabled) {
        if (!_chunk_history->has_resource(_key)) {
            _preload();
        }
    } else if (!_chunk_history->has_resource(_key)) {
        _chunk_history->set_initial_value(_key, "");
    }

    // Delete
    _chunk_history->set_value(_key, "");

    // Notify listeners that it has changed.
    changed.dispatch();
}

} // namespace Amulet
