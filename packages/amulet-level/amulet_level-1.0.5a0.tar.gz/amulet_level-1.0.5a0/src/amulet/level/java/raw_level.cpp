#include <bit>
#include <chrono>
#include <filesystem>
#include <fstream>
#include <memory>
#include <regex>
#include <stdexcept>
#include <variant>

#include <amulet/nbt/nbt_encoding/binary.hpp>
#include <amulet/nbt/string_encoding/string_encoding.hpp>
#include <amulet/nbt/tag/compound.hpp>
#include <amulet/nbt/tag/copy.hpp>

#include <amulet/utils/lock_file.hpp>
#include <amulet/utils/logging.hpp>

#include <amulet/zlib/zlib.hpp>

#include "raw_level.hpp"

namespace Amulet {

static const std::string OVERWORLD = "minecraft:overworld";
static const std::string THE_NETHER = "minecraft:the_nether";
static const std::string THE_END = "minecraft:the_end";
static const std::regex dim_regex(R"(^(DIM\-?\d+)$)");

JavaRawLevel::JavaRawLevel(const std::filesystem::path path)
    : _path(path)
    , _level_dat("", std::make_shared<Amulet::NBT::CompoundTag>())
    , _data_version({})
{
}

JavaRawLevelOpenData& JavaRawLevel::_get_raw_open()
{
    if (!_raw_open_data) {
        throw std::runtime_error("The level is not open.");
    }
    return *_raw_open_data;
}

JavaRawLevel::~JavaRawLevel()
{
    close();
}

std::unique_ptr<JavaRawLevel> JavaRawLevel::load(const std::filesystem::path& path)
{
    if (!std::filesystem::is_directory(path)) {
        throw std::invalid_argument("path must be a directory.");
    }
    std::unique_ptr<JavaRawLevel> self(new JavaRawLevel(path));
    self->reload_metadata();
    return self;
}

static void _write_level_dat(const std::filesystem::path& level_dat_path, const Amulet::NBT::NamedTag& level_dat)
{
    auto level_dat_temp_path = level_dat_path;
    level_dat_temp_path += ".tmp";
    // Encode
    std::string encoded_level_dat = Amulet::NBT::encode_nbt(level_dat, std::endian::big, Amulet::NBT::utf8_to_mutf8);
    // Compress
    std::string compressed_level_dat;
    zlib::compress_gzip(encoded_level_dat, compressed_level_dat);
    // Write to file
    std::ofstream level_dat_f(level_dat_temp_path, std::ios::out | std::ios::binary);
    if (!level_dat_f) {
        throw std::runtime_error("Could not open file for writing. " + level_dat_temp_path.string());
    }
    level_dat_f << compressed_level_dat;
    level_dat_f.close();
    level_dat_f.flush();
    std::filesystem::rename(level_dat_temp_path, level_dat_path);
}

std::unique_ptr<JavaRawLevel> JavaRawLevel::create(const JavaCreateArgsV1& args)
{
    // Create the directory
    if (std::filesystem::exists(args.path)) {
        if (args.overwrite) {
            std::filesystem::remove_all(args.path);
        } else {
            throw std::runtime_error("Path already exists and overwrite is false. " + args.path.string());
        }
    }
    std::filesystem::create_directories(args.path);

    // Get the data version
    Amulet::NBT::IntTagNative data_version;
    if (args.version.size() == 1) {
        data_version = static_cast<Amulet::NBT::IntTagNative>(args.version[0]);
    } else {
        throw std::runtime_error("NotImplementedError");
        // data_version = get_game_version("java", version).max_version
    }

    // Get the current unix time in milliseconds
    auto time_now = static_cast<Amulet::NBT::LongTagNative>(
        std::chrono::duration_cast<std::chrono::milliseconds>(
            std::chrono::system_clock::now().time_since_epoch())
            .count());

    // Create the level.dat file
    auto root = std::make_shared<Amulet::NBT::CompoundTag>();
    auto data = std::make_shared<Amulet::NBT::CompoundTag>();
    root->emplace("Data", data);
    data->emplace("version", Amulet::NBT::IntTag(19133));
    data->emplace("DataVersion", Amulet::NBT::IntTag(data_version));
    data->emplace("LastPlayed", Amulet::NBT::LongTag(time_now));
    data->emplace("LevelName", Amulet::NBT::StringTag(args.level_name));
    _write_level_dat(args.path / "level.dat", { "", root });

    return load(args.path);
}

OrderedMutex& JavaRawLevel::get_mutex()
{
    return _public_mutex;
}

bool JavaRawLevel::is_open() const
{
    return bool(_raw_open_data);
}

VersionNumber JavaRawLevel::_get_data_version()
{
    try {
        auto& root = std::get<Amulet::NBT::CompoundTagPtr>(_level_dat.tag_node);
        auto& data = std::get<Amulet::NBT::CompoundTagPtr>(root->at("Data"));
        auto& data_version = std::get<Amulet::NBT::IntTag>(data->at("DataVersion"));
        return { data_version.value };
    } catch (...) {
        return { -1 };
    }
}

void JavaRawLevel::reload_metadata()
{
    if (is_open()) {
        throw std::runtime_error("Cannot reload metadata while the level is open.");
    }

    // Load the level.dat
    auto level_dat_path = _path / "level.dat";
    // Open the file
    std::ifstream level_dat_f(level_dat_path, std::ios::in | std::ios::binary);
    if (!level_dat_f) {
        throw std::runtime_error("Could not open file for reading " + level_dat_path.string());
    }
    // Find the file length
    level_dat_f.seekg(0, std::ios::end);
    size_t level_dat_size = level_dat_f.tellg();
    level_dat_f.seekg(0);
    // Read the file
    std::string level_dat(level_dat_size, 0);
    level_dat_f.read(&level_dat[0], level_dat_size);
    // Decompress the file
    std::string decompressed_level_dat;
    zlib::decompress_zlib_gzip(level_dat, decompressed_level_dat);
    // Decode the binary NBT.
    _level_dat = Amulet::NBT::decode_nbt(decompressed_level_dat, std::endian::big, Amulet::NBT::mutf8_to_utf8);

    // Load the data version.
    _data_version = _get_data_version();
}

void JavaRawLevel::_open(std::unique_ptr<LockFile> session_lock)
{
    // Reload the metadata to ensure it is up to date.
    reload_metadata();

    // TODO: data pack

    _raw_open_data = std::make_unique<JavaRawLevelOpenData>(
        std::move(session_lock));
}

void JavaRawLevel::open()
{
    if (is_open()) {
        return;
    }

    // Acquire session.lock
    auto session_lock = std::make_unique<LockFile>(_path / "session.lock");
    session_lock->write_to_file("\xE2\x98\x83");

    // Do the actual open
    _open(std::move(session_lock));

    // Notify listeners that the world is now open.
    opened.dispatch();
}

std::unique_ptr<LockFile> JavaRawLevel::_close()
{
    auto raw_open_data = std::move(_raw_open_data);
    auto lock_file = std::move(raw_open_data->session_lock);

    // destroy open data
    std::lock_guard dimensions_lock(raw_open_data->dimensions_mutex);
    for (auto& [_, dimension_ptr] : raw_open_data->dimensions) {
        dimension_ptr->destroy();
    }

    return lock_file;
}

void JavaRawLevel::close()
{
    if (!is_open()) {
        return;
    }
    _close()->unlock_file();
    closed.dispatch();
}

void JavaRawLevel::reload()
{
    if (!is_open()) {
        throw std::runtime_error("Level can only be reloaded when it is open.");
    }
    _open(_close());
    reloaded.dispatch();
}

const std::filesystem::path& JavaRawLevel::get_path() const
{
    return _path;
}

Amulet::NBT::NamedTag JavaRawLevel::get_level_dat() const
{
    return Amulet::NBT::deep_copy(_level_dat);
}

void JavaRawLevel::set_level_dat(const Amulet::NBT::NamedTag& level_dat)
{
    if (!is_open()) {
        throw std::runtime_error("Level is not open.");
    }
    // Copy the level.dat to internal storage
    _level_dat = Amulet::NBT::deep_copy(level_dat);

    // Save to level.dat
    _write_level_dat(_path / "level.dat", _level_dat);

    // Reload the level if the data version changed.
    if (_data_version != _get_data_version()) {
        reload();
    }
}

std::string JavaRawLevel::get_platform() const
{
    return "java";
}

// Get the "Data" CompoundTag from a level.dat NamedTag.
static Amulet::NBT::CompoundTag& get_level_dat_data(Amulet::NBT::NamedTag& level_dat)
{
    if (!std::holds_alternative<Amulet::NBT::CompoundTagPtr>(level_dat.tag_node)) {
        throw std::runtime_error("Level.dat root is not a CompoundTag.");
    }
    auto& root = std::get<Amulet::NBT::CompoundTagPtr>(level_dat.tag_node);
    auto it = root->find("Data");
    if (it == root->end()) {
        throw std::runtime_error("Level.dat does not contain \"Data\" entry.");
    }
    if (!std::holds_alternative<Amulet::NBT::CompoundTagPtr>(it->second)) {
        throw std::runtime_error("Level.dat[\"Data\"] is not a CompoundTag.");
    }
    return *std::get<Amulet::NBT::CompoundTagPtr>(it->second);
}

VersionNumber JavaRawLevel::get_data_version() const
{
    return _data_version;
}

void JavaRawLevel::set_data_version(const VersionNumber& data_version)
{
    if (data_version.size() != 1) {
        throw std::invalid_argument("Data version must have exactly one value.");
    }
    if (_data_version == data_version) {
        // Data version did not change.
        return;
    }
    auto level_dat = get_level_dat();
    auto& data = get_level_dat_data(level_dat);
    if (data_version[0] == -1) {
        data.erase("DataVersion");
    } else {
        data.insert_or_assign("DataVersion", Amulet::NBT::IntTag(static_cast<Amulet::NBT::IntTagNative>(data_version[0])));
    }
    set_level_dat(level_dat);
}

bool JavaRawLevel::is_supported() const
{
    // TODO
    return true;
}

PIL::Image::Image JavaRawLevel::get_thumbnail() const
{
    try {
        return PIL::Image::open(_path / "icon.png");
    } catch (...) {
        return get_missing_no_icon();
    }
}

std::chrono::system_clock::time_point JavaRawLevel::get_modified_time() const
{

    try {
        auto& root = std::get<Amulet::NBT::CompoundTagPtr>(_level_dat.tag_node);
        auto& data = std::get<Amulet::NBT::CompoundTagPtr>(root->at("Data"));
        return std::chrono::system_clock::time_point(std::chrono::milliseconds(
            std::get<Amulet::NBT::LongTag>(data->at("LastPlayed")).value));
    } catch (...) {
        return std::chrono::system_clock::time_point(std::chrono::milliseconds(0));
    }
}

std::string JavaRawLevel::get_level_name() const
{
    try {
        auto& root = std::get<Amulet::NBT::CompoundTagPtr>(_level_dat.tag_node);
        auto& data = std::get<Amulet::NBT::CompoundTagPtr>(root->at("Data"));
        return std::get<Amulet::NBT::StringTag>(data->at("LevelName"));
    } catch (...) {
        return "Undefined";
    }
}

void JavaRawLevel::set_level_name(const std::string& level_name)
{
    auto level_dat = get_level_dat();
    auto& data = get_level_dat_data(level_dat);
    data.insert_or_assign("LevelName", Amulet::NBT::StringTag(level_name));
    set_level_dat(level_dat);
}

static const SelectionBox DefaultSelection { -30'000'000, 0, -30'000'000, 60'000'000, 256, 60'000'000 };

SelectionBox JavaRawLevel::_get_dimension_bounds(const DimensionId& dimension_id)
{
    if (_data_version < VersionNumber { 2709 }) {
        // Old versions were hard coded.
        // This number might be smaller
        return DefaultSelection;
    }

    // Look for a dimension configuration
    Amulet::NBT::CompoundTagPtr dimension_settings;
    try {
        auto& root = std::get<Amulet::NBT::CompoundTagPtr>(_level_dat.tag_node);
        auto& data = std::get<Amulet::NBT::CompoundTagPtr>(root->at("Data"));
        auto& world_gen_settings = std::get<Amulet::NBT::CompoundTagPtr>(data->at("WorldGenSettings"));
        auto& dimensions = std::get<Amulet::NBT::CompoundTagPtr>(world_gen_settings->at("dimensions"));
        dimension_settings = std::get<Amulet::NBT::CompoundTagPtr>(dimensions->at(dimension_id));
    } catch (...) {
        return DefaultSelection;
    }
    // "type" can be a reference (string) or inline (compound) dimension-type data.
    auto& dimension_type_node = dimension_settings->at("type");
    return std::visit(
        [&](auto&& dimension_type) {
            using T = std::decay_t<decltype(dimension_type)>;
            if constexpr (std::is_same_v<Amulet::NBT::StringTag, T>) {
                // Reference type. Load the dimension data
                auto colon_index = dimension_type.find(':');
                std::string namespace_;
                std::string base_name;
                if (colon_index == std::string::npos) {
                    namespace_ = "minecraft";
                    base_name = dimension_type;
                } else {
                    namespace_ = dimension_type.substr(0, colon_index);
                    base_name = dimension_type.substr(colon_index + 1);
                }
                // TODO: implement the data pack
                //     # First try and load the reference from the data pack and then from defaults
                //     dimension_path = f"data/{namespace}/dimension_type/{base_name}.json"
                //     if self._o.data_pack.has_file(dimension_path):
                //         with self._o.data_pack.open(dimension_path) as d:
                //             try:
                //                 dimension_settings_json = json.load(d)
                //             except json.JSONDecodeError:
                //                 pass
                //             else:
                //                 if "min_y" in dimension_settings_json and isinstance(
                //                     dimension_settings_json["min_y"], int
                //                 ):
                //                     min_y = dimension_settings_json["min_y"]
                //                     if min_y % 16:
                //                         min_y = 16 * (min_y // 16)
                //                 else:
                //                     min_y = 0
                //                 if "height" in dimension_settings_json and isinstance(
                //                     dimension_settings_json["height"], int
                //                 ):
                //                     height = dimension_settings_json["height"]
                //                     if height % 16:
                //                         height = -16 * (-height // 16)
                //                 else:
                //                     height = 256
                //
                //                 return SelectionBoxGroup(
                //                     SelectionBox(
                //                         (-30_000_000, min_y, -30_000_000),
                //                         (30_000_000, min_y + height, 30_000_000),
                //                     )
                //                 )
                //
                /*else*/ if (namespace_ == "minecraft") {
                    if (base_name == "overworld" || base_name == "overworld_caves") {
                        if (VersionNumber { 2825 } <= _data_version) {
                            // If newer than the height change version
                            return SelectionBox { -30'000'000, -64, -30'000'000, 60'000'000, 384, 60'000'000 };
                        } else {
                            return DefaultSelection;
                        }
                    } else if (base_name == "the_nether" || base_name == "the_end") {
                        return DefaultSelection;
                    } else {
                        error("Could not find dimension_type minecraft:" + base_name);
                    }
                } else {
                    error("Could not find dimension_type " + namespace_ + ":" + base_name);
                }
            } else if constexpr (std::is_same_v<Amulet::NBT::CompoundTagPtr, T>) {
                // Inline type
                Amulet::NBT::IntTagNative min_y = [&dimension_type] {
                    auto it = dimension_type->find("min_y");
                    if (it != dimension_type->end()) {
                        auto* ptr = std::get_if<Amulet::NBT::IntTag>(&it->second);
                        if (ptr) {
                            return ptr->value & ~15;
                        }
                    }
                    return 0;
                }();

                Amulet::NBT::IntTagNative height = [&dimension_type] {
                    auto it = dimension_type->find("height");
                    if (it != dimension_type->end()) {
                        auto* ptr = std::get_if<Amulet::NBT::IntTag>(&it->second);
                        if (ptr) {
                            return ptr->value & ~15;
                        }
                    }
                    return 256;
                }();

                return SelectionBox { -30'000'000, min_y, -30'000'000, 60'000'000, static_cast<std::uint64_t>(std::max(0, height)), 60'000'000 };
            } else {
                error("level_dat[\"Data\"][\"WorldGenSettings\"][\"dimensions\"][\"" + dimension_id + "\"][\"type\"] was not a StringTag or CompoundTag.");
            }
            return DefaultSelection;
        },
        dimension_type_node);
}

void JavaRawLevel::_register_dimension(
    JavaRawLevelOpenData& raw_open,
    const JavaInternalDimensionID& relative_dimension_path,
    const DimensionId& dimension_id)
{
    if (!raw_open.dimension_ids.contains(dimension_id) && !raw_open.dimensions.contains(relative_dimension_path)) {
        // Get the dimension path
        auto path = _path;
        if (!relative_dimension_path.empty()) {
            path = path / relative_dimension_path;
        }

        // Build the list of layer names
        std::list<std::string> layers;
        if (VersionNumber { 2681 } <= _data_version) {
            layers = { "region", "entities" };
        } else {
            layers = { "region" };
        }

        // Create the raw dimension instance
        auto raw_dimension = std::shared_ptr<JavaRawDimension>(
            new JavaRawDimension(
                path,
                get_data_version() > VersionNumber { 2203 },
                layers,
                relative_dimension_path,
                dimension_id,
                _get_dimension_bounds(dimension_id),
                // TODO: Is this data stored somewhere?
                BlockStack { Block("java", VersionNumber { 3700 }, "minecraft", "air") },
                [&] {
                    if (dimension_id == THE_NETHER) {
                        return Biome("java", VersionNumber { 3700 }, "minecraft", "nether_wastes");
                    } else if (dimension_id == THE_END) {
                        return Biome("java", VersionNumber { 3700 }, "minecraft", "the_end");
                    } else {
                        return Biome("java", VersionNumber { 3700 }, "minecraft", "plains");
                    }
                }()));

        raw_open.dimension_ids.emplace(dimension_id, relative_dimension_path);
        raw_open.dimensions.emplace(relative_dimension_path, raw_dimension);
    }
}

JavaRawLevelOpenData& JavaRawLevel::_find_dimensions()
{
    auto& raw_open = _get_raw_open();
    std::unique_lock lock(raw_open.dimensions_mutex);

    if (!raw_open.dimensions.empty()) {
        return raw_open;
    }

    // Add hard coded dimensions
    _register_dimension(raw_open, "", OVERWORLD);
    _register_dimension(raw_open, "DIM-1", THE_NETHER);
    _register_dimension(raw_open, "DIM1", THE_END);

    // Find DIM style dimensions
    for (const auto& dir_entry : std::filesystem::directory_iterator { _path }) {
        if (!dir_entry.is_directory()) {
            continue;
        }
        auto dir_name = dir_entry.path().filename().string();
        std::smatch match;
        if (!std::regex_search(dir_name, match, dim_regex)) {
            continue;
        }
        _register_dimension(raw_open, dir_name, dir_name);
    }

    // Find dimensions in "dimensions" directory
    auto dimensions_path = _path / "dimensions";
    if (std::filesystem::is_directory(dimensions_path)) {
        for (const auto& dir_entry : std::filesystem::recursive_directory_iterator { dimensions_path }) {
            if (!dir_entry.is_directory()) {
                // Skip if it isn't a directory
                continue;
            }
            auto& path = dir_entry.path();
            if (path.filename().string() != "region") {
                // Skip if it doesn't end with region
                continue;
            }
            // Get the dimension path relative to the world
            auto rel_dimension_path = std::filesystem::relative(path.parent_path(), dimensions_path);

            std::string dimension_name;
            auto it = rel_dimension_path.begin();

            // Get the namespace
            if (it == rel_dimension_path.end()) {
                continue;
            }
            dimension_name += it->string();
            dimension_name += ":";
            it++;

            // Get the base name
            if (it == rel_dimension_path.end()) {
                continue;
            }
            dimension_name += it->string();

            // Get base name extension
            for (; it == rel_dimension_path.end(); it++) {
                dimension_name += "/";
                dimension_name += it->string();
            }

            _register_dimension(raw_open, rel_dimension_path.string(), dimension_name);
        }
    }

    return raw_open;
}

std::vector<std::string> JavaRawLevel::get_dimension_ids()
{
    auto& raw_open = _find_dimensions();
    std::shared_lock lock(raw_open.dimensions_mutex);
    std::vector<DimensionId> dimension_ids;
    dimension_ids.reserve(raw_open.dimension_ids.size());
    for (auto& [dimension_id, _] : raw_open.dimension_ids) {
        dimension_ids.push_back(dimension_id);
    }
    return dimension_ids;
}

std::shared_ptr<JavaRawDimension> JavaRawLevel::get_dimension(const DimensionId& dimension_id)
{
    auto& raw_open = _find_dimensions();
    std::shared_lock lock(raw_open.dimensions_mutex);
    auto it = raw_open.dimension_ids.find(dimension_id);
    JavaInternalDimensionID internal_dimension_id = (it == raw_open.dimension_ids.end()) ? dimension_id : it->second;
    auto it2 = raw_open.dimensions.find(internal_dimension_id);
    if (it2 == raw_open.dimensions.end()) {
        throw std::invalid_argument("Dimension " + dimension_id + " does not exist.");
    }
    return it2->second;
}

void JavaRawLevel::compact()
{
    auto& raw_open = _find_dimensions();
    std::shared_lock dimensions_lock(raw_open.dimensions_mutex);
    for (const auto& [dimension_id, dimension] : raw_open.dimensions) {
        OrderedLockGuard<ThreadAccessMode::Read, ThreadShareMode::SharedReadWrite> lock(dimension->get_mutex());
        dimension->compact();
    }
}

std::shared_ptr<IdRegistry> JavaRawLevel::get_block_id_override()
{
    return _get_raw_open().block_id_override;
}

std::shared_ptr<IdRegistry> JavaRawLevel::get_biome_id_override()
{
    return _get_raw_open().biome_id_override;
}

} // namespace Amulet
