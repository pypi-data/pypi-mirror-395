// #include <bit>
// #include <chrono>
// #include <filesystem>
// #include <fstream>
// #include <memory>
// #include <regex>
// #include <stdexcept>
#include <variant>

#include <leveldb/cache.h>
#include <leveldb/decompress_allocator.h>
#include <leveldb/env.h>
#include <leveldb/filter_policy.h>

// #include <amulet/nbt/nbt_encoding/binary.hpp>
// #include <amulet/nbt/string_encoding/string_encoding.hpp>
// #include <amulet/nbt/tag/compound.hpp>
// #include <amulet/nbt/tag/copy.hpp>
//
// #include <amulet/utils/lock_file.hpp>
// #include <amulet/utils/logging.hpp>

#include "raw_level.hpp"

namespace {

class NullLogger : public leveldb::Logger {
public:
    void Logv(const char*, va_list) override { }
};

class LevelDBOptions : public Amulet::LevelDBOptions {
public:
    NullLogger logger;
    leveldb::DecompressAllocator decompress_allocator;
};

static std::unique_ptr<Amulet::LevelDB> open_leveldb(std::filesystem::path path, bool create = false)
{
    // Expand dots and symbolic links
    path = std::filesystem::absolute(path);
    // If there is not a directory at the path
    if (!std::filesystem::is_directory(path)) {
        if (create) {
            std::filesystem::create_directories(path);
        } else {
            throw std::runtime_error("leveldb directory does not exist.");
        }
    }

    auto options = std::make_unique<LevelDBOptions>();
    options->options.create_if_missing = create;
    options->options.filter_policy = leveldb::NewBloomFilterPolicy(10);
    options->options.block_cache = leveldb::NewLRUCache(40 * 1024 * 1024);
    options->options.write_buffer_size = 4 * 1024 * 1024;
    options->options.info_log = &options->logger;
    options->options.compression = leveldb::CompressionType::kZlibRawCompression;
    options->options.block_size = 163840;

    options->read_options.decompress_allocator = &options->decompress_allocator;

    leveldb::DB* _db = NULL;
    auto status = leveldb::DB::Open(options->options, path.string(), &_db);
    if (status.ok()) {
        return std::make_unique<Amulet::LevelDB>(
            std::unique_ptr<leveldb::DB>(_db),
            std::move(options));
    }
    throw std::runtime_error("Could not create leveldb database at \"" + path.string() + "\" " + status.ToString());
}

}

namespace Amulet {

static const std::string OVERWORLD = "minecraft:overworld";
static const std::string THE_NETHER = "minecraft:the_nether";
static const std::string THE_END = "minecraft:the_end";
// static const std::regex number_regex(R"(^(\-?\d+)$)");

BedrockRawLevelOpenData::BedrockRawLevelOpenData(
    std::unique_ptr<LockFile> session_lock,
    std::shared_ptr<LevelDB> db)
    : session_lock(std::move(session_lock))
    , db(std::move(db))
    , block_id_override(std::make_shared<IdRegistry>())
    , biome_id_override(std::make_shared<IdRegistry>())
{
}

BedrockRawLevel::BedrockRawLevel(const std::filesystem::path path)
    : _path(path)
    , _level_dat()
    , _last_opened_version({})
{
}

BedrockRawLevel::~BedrockRawLevel()
{
    close();
}

BedrockRawLevelOpenData& BedrockRawLevel::_get_raw_open()
{
    if (!_raw_open_data) {
        throw std::runtime_error("The level is not open.");
    }
    return *_raw_open_data;
}

std::unique_ptr<BedrockRawLevel> BedrockRawLevel::load(const std::filesystem::path& path)
{
    if (!std::filesystem::is_directory(path)) {
        throw std::invalid_argument("path must be a directory.");
    }
    std::unique_ptr<BedrockRawLevel> self(new BedrockRawLevel(path));
    self->reload_metadata();
    return self;
}

// std::unique_ptr<BedrockRawLevel> BedrockRawLevel::create(const BedrockCreateArgsV1& args)
//{
//     // Create the directory
//     if (std::filesystem::exists(args.path)) {
//         if (args.overwrite) {
//             std::filesystem::remove_all(args.path);
//         } else {
//             throw std::runtime_error("Path already exists and overwrite is false. " + args.path.string());
//         }
//     }
//     std::filesystem::create_directories(args.path);
//
//     // Get the data version
//     NBT::IntTagNative data_version;
//     if (args.version.size() == 1) {
//         data_version = static_cast<NBT::IntTagNative>(args.version[0]);
//     } else {
//         throw std::runtime_error("NotImplementedError");
//         // data_version = get_game_version("bedrock", version).max_version
//     }
//
//     // Get the current unix time in milliseconds
//     auto time_now = static_cast<NBT::LongTagNative>(
//         std::chrono::duration_cast<std::chrono::milliseconds>(
//             std::chrono::system_clock::now().time_since_epoch())
//             .count());
//
//     // Create the level.dat file
//     auto root = std::make_shared<NBT::CompoundTag>();
//     auto data = std::make_shared<NBT::CompoundTag>();
//     root->emplace("Data", data);
//     data->emplace("version", NBT::IntTag(19133));
//     data->emplace("DataVersion", NBT::IntTag(data_version));
//     data->emplace("LastPlayed", NBT::LongTag(time_now));
//     data->emplace("LevelName", NBT::StringTag(args.level_name));
//     _write_level_dat(args.path / "level.dat", { "", root });
//
//     return load(args.path);
// }

OrderedMutex& BedrockRawLevel::get_mutex()
{
    return _public_mutex;
}

bool BedrockRawLevel::is_open() const
{
    return bool(_raw_open_data);
}

VersionNumber BedrockRawLevel::_get_last_opened_version()
{
    try {
        auto& root = std::get<NBT::CompoundTagPtr>(_level_dat.get_named_tag().tag_node);
        auto& last_opened_version_tag = std::get<NBT::ListTagPtr>(root->at("lastOpenedWithVersion"));
        auto& last_opened_version_vector = std::get<NBT::IntListTag>(*last_opened_version_tag);
        return std::vector<std::int64_t>(last_opened_version_vector.begin(), last_opened_version_vector.end());
    } catch (...) {
        return { -1 };
    }
}

void BedrockRawLevel::reload_metadata()
{
    if (is_open()) {
        throw std::runtime_error("Cannot reload metadata while the level is open.");
    }

    // Load the level.dat
    auto level_dat_path = _path / "level.dat";
    // Open the file
    _level_dat = BedrockLevelDat::from_file(level_dat_path);
    // Load the data version.
    _last_opened_version = _get_last_opened_version();
}

void BedrockRawLevel::_open(std::unique_ptr<LockFile> session_lock)
{
    // Reload the metadata to ensure it is up to date.
    reload_metadata();

    std::shared_ptr<Amulet::LevelDB> db = open_leveldb(_path / "db");

    _raw_open_data = std::make_unique<BedrockRawLevelOpenData>(
        std::move(session_lock),
        std::move(db));
}

void BedrockRawLevel::open()
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

std::unique_ptr<LockFile> BedrockRawLevel::_close()
{
    auto raw_open_data = std::move(_raw_open_data);
    auto lock_file = std::move(raw_open_data->session_lock);

    // destroy open data
    std::lock_guard dimensions_lock(raw_open_data->dimensions_mutex);
    for (auto& [_, dimension_ptr] : raw_open_data->dimensions) {
        dimension_ptr->destroy();
    }

    auto db = std::move(raw_open_data->db);
    db->close();

    return lock_file;
}

void BedrockRawLevel::close()
{
    if (!is_open()) {
        return;
    }
    _close()->unlock_file();
    std::filesystem::remove(_path / "session.lock");
    closed.dispatch();
}

void BedrockRawLevel::reload()
{
    if (!is_open()) {
        throw std::runtime_error("Level can only be reloaded when it is open.");
    }
    _open(_close());
    reloaded.dispatch();
}

const std::filesystem::path& BedrockRawLevel::get_path() const
{
    return _path;
}

BedrockLevelDat BedrockRawLevel::get_level_dat() const
{
    return _level_dat.deep_copy();
}

void BedrockRawLevel::set_level_dat(const BedrockLevelDat& level_dat)
{
    if (!is_open()) {
        throw std::runtime_error("Level is not open.");
    }

    // Copy the level.dat to internal storage
    _level_dat = level_dat.deep_copy();

    // Save to level.dat
    _level_dat.save_to(_path / "level.dat");

    // Reload the level if the data version changed.
    if (_last_opened_version != _get_last_opened_version()) {
        reload();
    }
}

std::string BedrockRawLevel::get_platform() const
{
    return "bedrock";
}

// Get the CompoundTag from a level.dat NamedTag.
static NBT::CompoundTag& get_level_dat_data(NBT::NamedTag& level_dat)
{
    if (!std::holds_alternative<NBT::CompoundTagPtr>(level_dat.tag_node)) {
        throw std::runtime_error("Level.dat root is not a CompoundTag.");
    }
    return *std::get<NBT::CompoundTagPtr>(level_dat.tag_node);
}

VersionNumber BedrockRawLevel::get_last_opened_version() const
{
    return _last_opened_version;
}

void BedrockRawLevel::set_last_opened_version(const VersionNumber& last_opened_version)
{
    if (_last_opened_version == last_opened_version) {
        // Data version did not change.
        return;
    }
    auto level_dat = get_level_dat();
    auto& data = get_level_dat_data(level_dat.get_named_tag());
    NBT::IntListTag tag;
    tag.reserve(last_opened_version.size());
    for (const auto& v : last_opened_version) {
        tag.emplace_back(static_cast<NBT::IntTag>(v));
    }
    data.insert_or_assign(
        "lastOpenedWithVersion",
        std::make_shared<NBT::ListTag>(std::move(tag)));
    set_level_dat(level_dat);
}

bool BedrockRawLevel::is_supported() const
{
    // TODO
    return true;
}

PIL::Image::Image BedrockRawLevel::get_thumbnail() const
{
    try {
        return PIL::Image::open(_path / "world_icon.jpeg");
    } catch (...) {
        return get_missing_no_icon();
    }
}

std::chrono::system_clock::time_point BedrockRawLevel::get_modified_time() const
{

    try {
        auto& root = std::get<NBT::CompoundTagPtr>(_level_dat.get_named_tag().tag_node);
        return std::chrono::system_clock::time_point(std::chrono::seconds(
            std::get<NBT::LongTag>(root->at("LastPlayed")).value));
    } catch (...) {
        return std::chrono::system_clock::time_point(std::chrono::seconds(0));
    }
}

std::string BedrockRawLevel::get_level_name() const
{
    try {
        auto& root = std::get<NBT::CompoundTagPtr>(_level_dat.get_named_tag().tag_node);
        return std::get<NBT::StringTag>(root->at("LevelName"));
    } catch (...) {
        return "Undefined";
    }
}

void BedrockRawLevel::set_level_name(const std::string& level_name)
{
    auto level_dat = get_level_dat();
    auto& data = get_level_dat_data(level_dat.get_named_tag());
    data.insert_or_assign("LevelName", NBT::StringTag(level_name));
    set_level_dat(level_dat);
}

// static const SelectionBox DefaultSelection { -30'000'000, 0, -30'000'000, 60'000'000, 256, 60'000'000 };

// SelectionBox BedrockRawLevel::_get_dimension_bounds(const DimensionId& dimension_id)
//{
//     if (_data_version < VersionNumber { 2709 }) {
//         // Old versions were hard coded.
//         // This number might be smaller
//         return DefaultSelection;
//     }
//
//     // Look for a dimension configuration
//     NBT::CompoundTagPtr dimension_settings;
//     try {
//         auto& root = std::get<NBT::CompoundTagPtr>(_level_dat.tag_node);
//         auto& data = std::get<NBT::CompoundTagPtr>(root->at("Data"));
//         auto& world_gen_settings = std::get<NBT::CompoundTagPtr>(data->at("WorldGenSettings"));
//         auto& dimensions = std::get<NBT::CompoundTagPtr>(world_gen_settings->at("dimensions"));
//         dimension_settings = std::get<NBT::CompoundTagPtr>(dimensions->at(dimension_id));
//     } catch (...) {
//         return DefaultSelection;
//     }
//     // "type" can be a reference (string) or inline (compound) dimension-type data.
//     auto& dimension_type_node = dimension_settings->at("type");
//     return std::visit(
//         [&](auto&& dimension_type) {
//             using T = std::decay_t<decltype(dimension_type)>;
//             if constexpr (std::is_same_v<NBT::StringTag, T>) {
//                 // Reference type. Load the dimension data
//                 auto colon_index = dimension_type.find(':');
//                 std::string namespace_;
//                 std::string base_name;
//                 if (colon_index == std::string::npos) {
//                     namespace_ = "minecraft";
//                     base_name = dimension_type;
//                 } else {
//                     namespace_ = dimension_type.substr(0, colon_index);
//                     base_name = dimension_type.substr(colon_index + 1);
//                 }
//                 // TODO: implement the data pack
//                 //     # First try and load the reference from the data pack and then from defaults
//                 //     dimension_path = f"data/{namespace}/dimension_type/{base_name}.json"
//                 //     if self._o.data_pack.has_file(dimension_path):
//                 //         with self._o.data_pack.open(dimension_path) as d:
//                 //             try:
//                 //                 dimension_settings_json = json.load(d)
//                 //             except json.JSONDecodeError:
//                 //                 pass
//                 //             else:
//                 //                 if "min_y" in dimension_settings_json and isinstance(
//                 //                     dimension_settings_json["min_y"], int
//                 //                 ):
//                 //                     min_y = dimension_settings_json["min_y"]
//                 //                     if min_y % 16:
//                 //                         min_y = 16 * (min_y // 16)
//                 //                 else:
//                 //                     min_y = 0
//                 //                 if "height" in dimension_settings_json and isinstance(
//                 //                     dimension_settings_json["height"], int
//                 //                 ):
//                 //                     height = dimension_settings_json["height"]
//                 //                     if height % 16:
//                 //                         height = -16 * (-height // 16)
//                 //                 else:
//                 //                     height = 256
//                 //
//                 //                 return SelectionBoxGroup(
//                 //                     SelectionBox(
//                 //                         (-30_000_000, min_y, -30_000_000),
//                 //                         (30_000_000, min_y + height, 30_000_000),
//                 //                     )
//                 //                 )
//                 //
//                 /*else*/ if (namespace_ == "minecraft") {
//                     if (base_name == "overworld" || base_name == "overworld_caves") {
//                         if (VersionNumber { 2825 } <= _data_version) {
//                             // If newer than the height change version
//                             return SelectionBox { -30'000'000, -64, -30'000'000, 60'000'000, 384, 60'000'000 };
//                         } else {
//                             return DefaultSelection;
//                         }
//                     } else if (base_name == "the_nether" || base_name == "the_end") {
//                         return DefaultSelection;
//                     } else {
//                         error("Could not find dimension_type minecraft:" + base_name);
//                     }
//                 } else {
//                     error("Could not find dimension_type " + namespace_ + ":" + base_name);
//                 }
//             } else if constexpr (std::is_same_v<NBT::CompoundTagPtr, T>) {
//                 // Inline type
//                 NBT::IntTagNative min_y = [&dimension_type] {
//                     auto it = dimension_type->find("min_y");
//                     if (it != dimension_type->end()) {
//                         auto* ptr = std::get_if<NBT::IntTag>(&it->second);
//                         if (ptr) {
//                             return ptr->value & ~15;
//                         }
//                     }
//                     return 0;
//                 }();
//
//                 NBT::IntTagNative height = [&dimension_type] {
//                     auto it = dimension_type->find("height");
//                     if (it != dimension_type->end()) {
//                         auto* ptr = std::get_if<NBT::IntTag>(&it->second);
//                         if (ptr) {
//                             return ptr->value & ~15;
//                         }
//                     }
//                     return 256;
//                 }();
//
//                 return SelectionBox { -30'000'000, min_y, -30'000'000, 60'000'000, static_cast<std::uint64_t>(std::max(0, height)), 60'000'000 };
//             } else {
//                 error("level_dat[\"Data\"][\"WorldGenSettings\"][\"dimensions\"][\"" + dimension_id + "\"][\"type\"] was not a StringTag or CompoundTag.");
//             }
//             return DefaultSelection;
//         },
//         dimension_type_node);
// }

static void _register_dimension(
    BedrockRawLevelOpenData& raw_open,
    const BedrockInternalDimensionID& internal_dimension_id,
    const DimensionId& dimension_id,
    const SelectionBox& bounds,
    std::int16_t legacy_min_cy,
    const BlockStack& default_block,
    const Biome& default_biome,
    std::uint32_t actor_group,
    VersionNumber max_version)
{
    if (!raw_open.dimension_ids.contains(dimension_id) && !raw_open.dimensions.contains(internal_dimension_id)) {
        // Create the raw dimension instance
        auto raw_dimension = std::shared_ptr<BedrockRawDimension>(
            new BedrockRawDimension(
                raw_open.db,
                internal_dimension_id,
                dimension_id,
                bounds,
                legacy_min_cy,
                default_block,
                default_biome,
                actor_group,
                max_version));

        raw_open.dimension_ids.emplace(dimension_id, internal_dimension_id);
        raw_open.dimensions.emplace(internal_dimension_id, std::move(raw_dimension));
    }
}

static bool is_caves_and_cliffs(const NBT::CompoundTag& root_tag)
{
    // Is the caves and cliffs experimental toggle enabled?
    const auto& experiments_it = root_tag.find("experiments");
    if (experiments_it != root_tag.end()) {
        auto* experiments_ptr = std::get_if<NBT::CompoundTagPtr>(&experiments_it->second);
        if (experiments_ptr) {
            auto& experiments = **experiments_ptr;
            // caves_and_cliffs tag
            const auto& caves_and_cliffs_it = experiments.find("caves_and_cliffs");
            if (caves_and_cliffs_it != experiments.end()) {
                auto* caves_and_cliffs_ptr = std::get_if<NBT::ByteTag>(&caves_and_cliffs_it->second);
                if (caves_and_cliffs_ptr && *caves_and_cliffs_ptr) {
                    return true;
                }
            }
            // caves_and_cliffs_internal tag
            const auto& caves_and_cliffs_internal_it = experiments.find("caves_and_cliffs_internal");
            if (caves_and_cliffs_internal_it != experiments.end()) {
                auto* caves_and_cliffs_internal_ptr = std::get_if<NBT::ByteTag>(&caves_and_cliffs_internal_it->second);
                if (caves_and_cliffs_internal_ptr && *caves_and_cliffs_internal_ptr) {
                    return true;
                }
            }
        }
    }
    return false;
}

BedrockRawLevelOpenData& BedrockRawLevel::_find_dimensions()
{
    auto& raw_open = _get_raw_open();
    std::unique_lock lock(raw_open.dimensions_mutex);

    if (!raw_open.dimensions.empty()) {
        return raw_open;
    }

    // Get the actor group stored in the level.dat file.

    std::uint32_t actor_group = 0;

    auto dat = get_level_dat();
    auto* root_tag_ptr = std::get_if<NBT::CompoundTagPtr>(&dat.get_named_tag().tag_node);
    if (!root_tag_ptr) {
        throw std::runtime_error("level.dat root tag is not a CompoundTag.");
    }
    auto& root_tag = **root_tag_ptr;
    const auto& world_start_count_it = root_tag.find("worldStartCount");
    if (world_start_count_it != root_tag.end()) {
        auto* world_start_count_ptr = std::get_if<NBT::LongTag>(&world_start_count_it->second);
        if (world_start_count_ptr) {
            actor_group = -static_cast<std::int32_t>(*world_start_count_ptr);
        }
    }

    // Add hard coded dimensions
    // TODO: What format should biome version use?

    std::int64_t overworld_min_y = -64;
    std::int64_t overworld_height = 384;
    std::int16_t overworld_legacy_min_y = 0;

    if (is_caves_and_cliffs(root_tag)) {
        overworld_legacy_min_y = -4;
    } else if (_last_opened_version < VersionNumber { 1, 18 }) {
        overworld_min_y = 0;
        overworld_height = 256;
    }

    _register_dimension(
        raw_open,
        0,
        OVERWORLD,
        SelectionBox(-30'000'000, overworld_min_y, -30'000'000, 60'000'000, overworld_height, 60'000'000),
        overworld_legacy_min_y,
        BlockStack { Block("bedrock", VersionNumber { 17432626 }, "minecraft", "air", Block::PropertyMap { { "block_data", NBT::IntTag(0) } }) },
        Biome("bedrock", VersionNumber { 0 }, "minecraft", "plains"),
        ++actor_group,
        get_last_opened_version());

    _register_dimension(
        raw_open,
        1,
        THE_NETHER,
        SelectionBox(-30'000'000, 0, -30'000'000, 60'000'000, 128, 60'000'000),
        0,
        BlockStack { Block("bedrock", VersionNumber { 17432626 }, "minecraft", "air", Block::PropertyMap { { "block_data", NBT::IntTag(0) } }) },
        Biome("bedrock", VersionNumber { 0 }, "minecraft", "hell"),
        ++actor_group,
        get_last_opened_version());

    _register_dimension(
        raw_open,
        2,
        THE_END,
        SelectionBox(-30'000'000, 0, -30'000'000, 60'000'000, 256, 60'000'000),
        0,
        BlockStack { Block("bedrock", VersionNumber { 17432626 }, "minecraft", "air", Block::PropertyMap { { "block_data", NBT::IntTag(0) } }) },
        Biome("bedrock", VersionNumber { 0 }, "minecraft", "the_end"),
        ++actor_group,
        get_last_opened_version());

    // if b"LevelChunkMetaDataDictionary" in self.level_db:
    //     data = self.level_db[b"LevelChunkMetaDataDictionary"]
    //     count, data = struct.unpack("<I", data[:4])[0], data[4:]
    //     for _ in range(count):
    //         key, data = data[:8], data[8:]
    //         context = ReadContext()
    //         value = load_nbt(
    //             data,
    //             little_endian=True,
    //             compressed=False,
    //             string_decoder=utf8_escape_decoder,
    //             read_context=context,
    //         ).compound
    //         data = data[context.offset :]

    //        try:
    //            dimension_name = value.get_string("DimensionName").py_str
    //            # The dimension names are stored differently TODO: split local and global names
    //            dimension_name = {
    //                "Overworld": OVERWORLD,
    //                "Nether": THE_NETHER,
    //                "TheEnd": THE_END,
    //            }.get(dimension_name, dimension_name)

    //        except KeyError:
    //            # Some entries seem to not have a dimension assigned to them. Is there a default? We will skip over these for now.
    //            # {'LastSavedBaseGameVersion': StringTag("1.19.81"), 'LastSavedDimensionHeightRange': CompoundTag({'max': ShortTag(320), 'min': ShortTag(-64)})}
    //            pass
    //        else:
    //            previous_bounds = self._bounds.get(
    //                dimension_name, DefaultSelection
    //            )
    //            min_y = min(
    //                value.get_compound(
    //                    "LastSavedDimensionHeightRange", CompoundTag()
    //                )
    //                .get_short("min", ShortTag())
    //                .py_int,
    //                value.get_compound(
    //                    "OriginalDimensionHeightRange", CompoundTag()
    //                )
    //                .get_short("min", ShortTag())
    //                .py_int,
    //                previous_bounds.min_y,
    //            )
    //            max_y = max(
    //                value.get_compound(
    //                    "LastSavedDimensionHeightRange", CompoundTag()
    //                )
    //                .get_short("max", ShortTag())
    //                .py_int,
    //                value.get_compound(
    //                    "OriginalDimensionHeightRange", CompoundTag()
    //                )
    //                .get_short("max", ShortTag())
    //                .py_int,
    //                previous_bounds.max_y,
    //            )
    //            self._bounds[dimension_name] = SelectionGroup(
    //                SelectionBox(
    //                    (previous_bounds.min_x, min_y, previous_bounds.min_z),
    //                    (previous_bounds.max_x, max_y, previous_bounds.max_z),
    //                )
    //            )

    // # Give all other dimensions found an entry
    // known_dimensions = set(self._dimension_to_internal.values())
    // for internal_dimension in self._dimension_manager.dimensions:
    //     if internal_dimension not in known_dimensions:
    //         dimension_name = f"DIM{internal_dimension}"
    //         self._dimension_to_internal[dimension_name] = internal_dimension
    //         self._bounds[dimension_name] = DefaultSelection

    root_tag.insert_or_assign(
        "worldStartCount",
        NBT::LongTag(
            static_cast<std::uint32_t>(
                -static_cast<int32_t>(actor_group))));
    set_level_dat(dat);

    return raw_open;
}

std::vector<std::string> BedrockRawLevel::get_dimension_ids()
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

std::shared_ptr<BedrockRawDimension> BedrockRawLevel::get_dimension(const DimensionId& dimension_id)
{
    auto& raw_open = _find_dimensions();
    std::shared_lock lock(raw_open.dimensions_mutex);
    auto it = raw_open.dimension_ids.find(dimension_id);
    if (it == raw_open.dimension_ids.end()) {
        throw std::invalid_argument("Dimension " + dimension_id + " does not exist.");
    }
    BedrockInternalDimensionID internal_dimension_id = it->second;
    auto it2 = raw_open.dimensions.find(internal_dimension_id);
    if (it2 == raw_open.dimensions.end()) {
        throw std::invalid_argument("dimension " + dimension_id + " does not exist.");
    }
    return it2->second;
}

std::shared_ptr<BedrockRawDimension> BedrockRawLevel::get_dimension(BedrockInternalDimensionID internal_dimension_id)
{
    auto& raw_open = _find_dimensions();
    std::shared_lock lock(raw_open.dimensions_mutex);
    auto it = raw_open.dimensions.find(internal_dimension_id);
    if (it == raw_open.dimensions.end()) {
        throw std::invalid_argument("dimension " + std::to_string(internal_dimension_id) + " does not exist.");
    }
    return it->second;
}

void BedrockRawLevel::compact()
{
    auto& db = *_get_raw_open().db;
    db->CompactRange(nullptr, nullptr);
}

std::shared_ptr<IdRegistry> BedrockRawLevel::get_block_id_override()
{
    return _get_raw_open().block_id_override;
}

std::shared_ptr<IdRegistry> BedrockRawLevel::get_biome_id_override()
{
    return _get_raw_open().biome_id_override;
}

std::shared_ptr<LevelDB> BedrockRawLevel::get_leveldb()
{
    return _get_raw_open().db;
}

} // namespace Amulet
