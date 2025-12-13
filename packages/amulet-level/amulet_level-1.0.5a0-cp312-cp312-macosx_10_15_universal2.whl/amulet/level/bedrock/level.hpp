#pragma once

#include <chrono>
#include <filesystem>
#include <map>
#include <memory>
#include <variant>

#include <amulet/utils/image.hpp>

#include <amulet/level/abc/history.hpp>
#include <amulet/level/abc/level.hpp>

#include "dimension.hpp"
#include "raw_level.hpp"

namespace Amulet {

class BedrockLevelOpenData {
public:
    HistoryManager history_manager;
    std::shared_ptr<bool> history_enabled;
    std::shared_mutex dimensions_mutex;
    std::map<std::variant<DimensionId, BedrockInternalDimensionID>, std::shared_ptr<BedrockDimension>> dimensions;

    BedrockLevelOpenData();
};

class BedrockLevel : public Level, public CompactibleLevel, public DiskLevel, public ReloadableLevel {
private:
    std::unique_ptr<BedrockRawLevel> _raw_level;

    // Data that is only valid when the level is open.
    std::unique_ptr<BedrockLevelOpenData> _open_data;

    // Validate _open_data is valid and return a reference.
    // External Read:SharedReadWrite lock required.
    BedrockLevelOpenData& _get_open_data();

    BedrockLevel(std::unique_ptr<BedrockRawLevel>);

public:
    BedrockLevel() = delete;
    BedrockLevel(const BedrockLevel&) = delete;
    BedrockLevel& operator=(const BedrockLevel&) = delete;
    BedrockLevel(BedrockLevel&&) = delete;
    BedrockLevel& operator=(BedrockLevel&&) = delete;

    AMULET_LEVEL_EXPORT ~BedrockLevel() override;

    // Load an existing Bedrock level from the given directory.
    // Thread safe.
    AMULET_LEVEL_EXPORT static std::unique_ptr<BedrockLevel> load(const std::filesystem::path&);

    //    // Create a new Bedrock level at the given directory.
    //    // Thread safe.
    //    AMULET_LEVEL_EXPORT static std::unique_ptr<BedrockLevel> create(const BedrockCreateArgsV1&);

    // LevelMetadata

    // Is the level open.
    // External Read:SharedReadWrite lock required.
    AMULET_LEVEL_EXPORT bool is_open() override;

    // The platform string for the level.
    // External Read:SharedReadWrite lock required.
    AMULET_LEVEL_EXPORT const std::string get_platform() override;

    // The maximum game version the level has been opened with.
    // External Read:SharedReadWrite lock required.
    AMULET_LEVEL_EXPORT VersionNumber get_max_game_version() override;

    // Get the suggested maximum block version this level can accept.
    // Note that the real max version may be higher.
    // External Read:SharedReadWrite lock required.
    AMULET_LEVEL_EXPORT VersionNumber get_max_block_version() override;

    // Is this level a supported version.
    // This is true for all versions we support and false for snapshots and unsupported newer versions.
    // External Read:SharedReadWrite lock required.
    AMULET_LEVEL_EXPORT bool is_supported() override;

    // The thumbnail for the level.
    // External Read:SharedReadWrite lock required.
    AMULET_LEVEL_EXPORT PIL::Image::Image get_thumbnail() override;

    // The name of the level.
    // External Read:SharedReadWrite lock required.
    AMULET_LEVEL_EXPORT const std::string get_level_name() override;

    // The time when the level was last modified.
    // External Read:SharedReadWrite lock required.
    AMULET_LEVEL_EXPORT std::chrono::system_clock::time_point get_modified_time() override;

    // The size of the sub-chunk. Must be a cube.
    // External Read:SharedReadWrite lock required.
    AMULET_LEVEL_EXPORT size_t get_sub_chunk_size() override;

    // DiskLevel

    // The path to the level on disk.
    // External Read:SharedReadWrite lock required.
    AMULET_LEVEL_EXPORT const std::filesystem::path& get_path() override;

    // Level

    // Open the level.
    // If the level is already open, this does nothing.
    // External ReadWrite:Unique lock required.
    AMULET_LEVEL_EXPORT void open() override;

    // Clear all unsaved changes and restore points.
    // External ReadWrite:Unique lock required.
    AMULET_LEVEL_EXPORT void purge() override;

    // Save changes to the level.
    // External ReadWrite:Unique lock required.
    AMULET_LEVEL_EXPORT void save() override;

    // Close the level.
    // If the level is not open, this does nothing.
    // External ReadWrite:Unique lock required.
    AMULET_LEVEL_EXPORT void close() override;

    // Create a new history restore point.
    // Any changes made after this point can be reverted by calling undo.
    // External Read:SharedReadWrite lock required.
    AMULET_LEVEL_EXPORT void create_restore_point() override;

    // Get the number of times undo can be called.
    // External Read:SharedReadWrite lock required.
    // External Read:SharedReadOnly lock optional.
    AMULET_LEVEL_EXPORT size_t get_undo_count() override;

    // Revert the changes made since the previous restore point.
    // External ReadWrite:SharedReadWrite lock required.
    // External ReadWrite:Unique lock optional.
    AMULET_LEVEL_EXPORT void undo() override;

    // Get the number of times redo can be called.
    // External Read:SharedReadWrite lock required.
    // External Read:SharedReadOnly lock optional.
    AMULET_LEVEL_EXPORT size_t get_redo_count() override;

    // Redo changes that were previously reverted.
    // External ReadWrite:SharedReadWrite lock required.
    // External ReadWrite:Unique lock optional.
    AMULET_LEVEL_EXPORT void redo() override;

    // Get if the history system is enabled.
    // If this is true, the caller must call create_restore_point before making changes.
    // External Read:SharedReadWrite lock required.
    AMULET_LEVEL_EXPORT bool get_history_enabled() override;

    // Set if the history system is enabled.
    // External ReadWrite:SharedReadWrite lock required.
    AMULET_LEVEL_EXPORT void set_history_enabled(bool) override;

    // The identifiers for all dimensions in the level
    // External Read:SharedReadWrite lock required.
    // External Read:SharedReadOnly lock optional.
    AMULET_LEVEL_EXPORT std::vector<std::string> get_dimension_ids() override;

    // Get a dimension.
    // External Read:SharedReadWrite lock required.
    // External ReadWrite:SharedReadWrite lock required when calling code in Dimension (and its children) that need write permission.
    AMULET_LEVEL_EXPORT std::shared_ptr<BedrockDimension> get_bedrock_dimension(std::variant<DimensionId, BedrockInternalDimensionID>);

    // Get a dimension.
    // External Read:SharedReadWrite lock required.
    // External ReadWrite:SharedReadWrite lock required when calling code in Dimension (and its children) that need write permission.
    AMULET_LEVEL_EXPORT std::shared_ptr<Dimension> get_dimension(const DimensionId&) override;

    // CompactibleLevel

    // Compact the level data to reduce file size.
    // External ReadWrite:SharedReadWrite lock required.
    AMULET_LEVEL_EXPORT void compact() override;

    // ReloadableLevel

    // Reload the level metadata.
    // This can only be done when the level is not open.
    // External ReadWrite:Unique lock required.
    AMULET_LEVEL_EXPORT void reload_metadata() override;

    // Reload the level.
    // This is like closing and opening the level but does not release locks.
    // This can only be done when the level is open.
    // External ReadWrite:Unique lock required.
    AMULET_LEVEL_EXPORT void reload() override;

    // Access the raw level instance.
    // Before calling any mutating functions, the caller must call `purge` (optionally saving before)
    // External ReadWrite:Unique lock required.
    AMULET_LEVEL_EXPORT BedrockRawLevel& get_raw_level();
};

} // namespace Amulet
