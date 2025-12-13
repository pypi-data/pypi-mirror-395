#include <chrono>
#include <filesystem>
#include <memory>
#include <mutex>
#include <shared_mutex>
#include <stdexcept>
#include <string>

#include <amulet/game/game.hpp>

#include "level.hpp"

namespace Amulet {

BedrockLevelOpenData::BedrockLevelOpenData()
    : history_enabled(std::make_shared<bool>(true))
{
}

BedrockLevelOpenData& BedrockLevel::_get_open_data()
{
    if (!_open_data) {
        throw std::runtime_error("The level is not open.");
    }
    return *_open_data;
}

BedrockLevel::BedrockLevel(std::unique_ptr<BedrockRawLevel> raw_level)
    : _raw_level(std::move(raw_level))
{
}

BedrockLevel::~BedrockLevel()
{
    close();
}

std::unique_ptr<BedrockLevel> BedrockLevel::load(const std::filesystem::path& path)
{
    return std::unique_ptr<BedrockLevel>(new BedrockLevel(BedrockRawLevel::load(path)));
}

// std::unique_ptr<BedrockLevel> BedrockLevel::create(const BedrockCreateArgsV1& args)
//{
//     return std::unique_ptr<BedrockLevel>(new BedrockLevel(BedrockRawLevel::create(args)));
// }

bool BedrockLevel::is_open()
{
    return bool(_open_data);
}

const std::string BedrockLevel::get_platform()
{
    return _raw_level->get_platform();
}

VersionNumber BedrockLevel::get_max_game_version()
{
    OrderedLockGuard<Amulet::ThreadAccessMode::Read, Amulet::ThreadShareMode::SharedReadWrite> lock(_raw_level->get_mutex());
    return _raw_level->get_last_opened_version();
}

VersionNumber BedrockLevel::get_max_block_version()
{
    return game::get_game_version("bedrock", get_max_game_version())->get_max_known_block_version();
}

bool BedrockLevel::is_supported()
{
    return _raw_level->is_supported();
}

PIL::Image::Image BedrockLevel::get_thumbnail()
{
    return _raw_level->get_thumbnail();
};

const std::string BedrockLevel::get_level_name()
{
    OrderedLockGuard<Amulet::ThreadAccessMode::Read, Amulet::ThreadShareMode::SharedReadWrite> lock(_raw_level->get_mutex());
    return _raw_level->get_level_name();
}

std::chrono::system_clock::time_point BedrockLevel::get_modified_time()
{
    OrderedLockGuard<Amulet::ThreadAccessMode::Read, Amulet::ThreadShareMode::SharedReadWrite> lock(_raw_level->get_mutex());
    return _raw_level->get_modified_time();
}

size_t BedrockLevel::get_sub_chunk_size()
{
    return 16;
}

const std::filesystem::path& BedrockLevel::get_path()
{
    return _raw_level->get_path();
}

void BedrockLevel::open()
{
    if (_open_data) {
        return;
    }
    {
        OrderedLockGuard<Amulet::ThreadAccessMode::ReadWrite, Amulet::ThreadShareMode::Unique> lock(_raw_level->get_mutex());
        _raw_level->open();
    }
    _open_data = std::make_unique<BedrockLevelOpenData>();
    opened.dispatch();
}

void BedrockLevel::purge()
{
    {
        auto& open_data = _get_open_data();
        std::lock_guard lock(open_data.history_manager.get_mutex());
        open_data.history_manager.reset();
    }
    purged.dispatch();
    history_changed.dispatch();
}

void BedrockLevel::save()
{
    for (const auto& dimension_id : get_dimension_ids()) {
        auto dimension = get_bedrock_dimension(dimension_id);
        dimension->save();
    }
}

void BedrockLevel::close()
{
    if (!_open_data) {
        return;
    }
    _open_data = nullptr;
    {
        OrderedLockGuard<Amulet::ThreadAccessMode::ReadWrite, Amulet::ThreadShareMode::Unique> lock(_raw_level->get_mutex());
        _raw_level->close();
    }
    closed.dispatch();
}

void BedrockLevel::create_restore_point()
{
    {
        auto& open_data = _get_open_data();
        std::lock_guard lock(open_data.history_manager.get_mutex());
        open_data.history_manager.create_undo_bin();
    }
    history_changed.dispatch();
}

size_t BedrockLevel::get_undo_count()
{
    auto& open_data = _get_open_data();
    std::shared_lock lock(open_data.history_manager.get_mutex());
    return open_data.history_manager.get_undo_count();
}

void BedrockLevel::undo()
{
    {
        auto& open_data = _get_open_data();
        std::lock_guard lock(open_data.history_manager.get_mutex());
        open_data.history_manager.undo();
    }
    history_changed.dispatch();
}

size_t BedrockLevel::get_redo_count()
{
    auto& open_data = _get_open_data();
    std::shared_lock lock(open_data.history_manager.get_mutex());
    return open_data.history_manager.get_redo_count();
}

void BedrockLevel::redo()
{
    {
        auto& open_data = _get_open_data();
        std::lock_guard lock(open_data.history_manager.get_mutex());
        open_data.history_manager.redo();
    }
    history_changed.dispatch();
}

bool BedrockLevel::get_history_enabled()
{
    return *_get_open_data().history_enabled;
}

void BedrockLevel::set_history_enabled(bool history_enabled)
{
    *_get_open_data().history_enabled = history_enabled;
    history_enabled_changed.dispatch();
}

std::vector<std::string> BedrockLevel::get_dimension_ids()
{
    OrderedLockGuard<Amulet::ThreadAccessMode::Read, Amulet::ThreadShareMode::SharedReadWrite> lock(_raw_level->get_mutex());
    return _raw_level->get_dimension_ids();
}

std::shared_ptr<BedrockDimension> BedrockLevel::get_bedrock_dimension(std::variant<DimensionId, BedrockInternalDimensionID> dimension_id)
{
    auto& open_data = _get_open_data();
    {
        // Find the dimension with a shared lock.
        std::shared_lock dimensions_lock(open_data.dimensions_mutex);
        auto it = open_data.dimensions.find(dimension_id);
        if (it != open_data.dimensions.end()) {
            return it->second;
        }
    }
    {
        // If it doesn't exist try again with a unique lock.
        std::lock_guard dimensions_lock(open_data.dimensions_mutex);
        auto it = open_data.dimensions.find(dimension_id);
        if (it != open_data.dimensions.end()) {
            return it->second;
        }
        OrderedLockGuard<
            ThreadAccessMode::Read,
            ThreadShareMode::SharedReadWrite>
            raw_level_lock(_raw_level->get_mutex());
        auto raw_dimension = std::visit(
            [&](auto&& arg) {
                return _raw_level->get_dimension(arg);
            },
            dimension_id);
        auto dimension = std::shared_ptr<BedrockDimension>(new BedrockDimension(
            raw_dimension,
            open_data.history_manager,
            open_data.history_enabled));
        open_data.dimensions.emplace(raw_dimension->get_dimension_id(), dimension);
        open_data.dimensions.emplace(raw_dimension->get_internal_dimension_id(), dimension);
        return dimension;
    }
}

std::shared_ptr<Dimension> BedrockLevel::get_dimension(const DimensionId& dimension_id)
{
    return get_bedrock_dimension(dimension_id);
}

void BedrockLevel::compact()
{
    OrderedLockGuard<Amulet::ThreadAccessMode::Read, Amulet::ThreadShareMode::SharedReadWrite> lock(_raw_level->get_mutex());
    _raw_level->compact();
}

void BedrockLevel::reload_metadata()
{
    std::lock_guard lock(_raw_level->get_mutex());
    _raw_level->reload_metadata();
}

void BedrockLevel::reload()
{
    {
        // purge loaded data.
        auto& open_data = _get_open_data();
        std::lock_guard lock(open_data.history_manager.get_mutex());
        open_data.history_manager.reset();
    }
    {
        // reload the raw level.
        std::lock_guard lock(_raw_level->get_mutex());
        _raw_level->reload();
    }
    reloaded.dispatch();
    history_changed.dispatch();
}

BedrockRawLevel& BedrockLevel::get_raw_level()
{
    return *_raw_level;
}

} // namespace Amulet
