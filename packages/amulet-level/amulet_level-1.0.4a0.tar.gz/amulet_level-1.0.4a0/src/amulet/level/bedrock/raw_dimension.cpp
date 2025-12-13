#include <bit>
#include <memory>
#include <string>
#include <string_view>
#include <variant>

#include <amulet/io/binary_reader.hpp>

#include <amulet/leveldb.hpp>
#include <leveldb/write_batch.h>

#include <amulet/nbt/nbt_encoding/binary.hpp>

#include "raw_dimension.hpp"

namespace Amulet {

BedrockChunkCoordIterator::BedrockChunkCoordIterator(
    std::unique_ptr<LevelDBIterator> it,
    BedrockInternalDimensionID dimension_id)
    : _it_ptr(std::move(it))
    , _it(_it_ptr->get_iterator())
{
    if (dimension_id != 0) {
        TemplateBaseBinaryWriter<StaticLittleEndian, false> dimension_id_writer(_dimension_id);
        dimension_id_writer.write_numeric<std::int32_t>(dimension_id);
    }
}

BedrockChunkCoordIterator::BedrockChunkCoordIterator(BedrockChunkCoordIterator&&) = default;

BedrockChunkCoordIterator::~BedrockChunkCoordIterator() = default;

bool BedrockChunkCoordIterator::is_vaild() const
{
    return bool(*_it_ptr);
}

// Seek to the next valid chunk. Note this may be the current key.
bool BedrockChunkCoordIterator::_find_next_chunk()
{
    const size_t key_size = 9 + _dimension_id.size();
    const size_t tag_index = key_size - 1;
    while (_it.Valid()) {
        auto key = _it.key();

        if (key.size() == key_size && (key[tag_index] == ',' || key[tag_index] == 'v')) {
            return true;
        } else {
            _it.Next();
        }
    }
    return false;
}

bool BedrockChunkCoordIterator::seek_to_first()
{
    _it.SeekToFirst();
    return _find_next_chunk();
}

bool BedrockChunkCoordIterator::seek_to_next()
{
    if (!_it.Valid()) {
        return false;
    }
    // Validate the key
    const auto& key = _it.key();
    if (key.size() < 8) {
        // This shouldn't happen.
        // The iterator should be invalid or at a version key.
        throw std::runtime_error("seek_to_next: invalid key");
    }
    _it.Next();

    // Find the next version key
    return _find_next_chunk();
}

const std::pair<std::int32_t, std::int32_t> BedrockChunkCoordIterator::get_coord() const
{
    auto key = _it.key();
    if (key.size() != 9 + _dimension_id.size()) {
        throw std::runtime_error("Chunk version key is not valid");
    }
    TemplateBinaryReader<StaticLittleEndian, false> key_reader({ key.data(), key.size() }, 0);
    auto cx = key_reader.read_numeric<std::int32_t, false>();
    auto cz = key_reader.read_numeric<std::int32_t, false>();
    return std::make_pair(cx, cz);
}

BedrockRawDimension::BedrockRawDimension(
    std::shared_ptr<LevelDB> db,
    BedrockInternalDimensionID internal_dimension_id,
    const DimensionId& dimension_id,
    const SelectionBox& bounds,
    std::int16_t legacy_floor,
    const BlockStack& default_block,
    const Biome& default_biome,
    std::uint32_t actor_group,
    VersionNumber max_version)
    : _db(std::move(db))
    , _internal_dimension_id(internal_dimension_id)
    , _dimension_id(dimension_id)
    , _bounds(bounds)
    , _legacy_floor(legacy_floor)
    , _default_block(default_block)
    , _default_biome(default_biome)
    , _actor_group(actor_group)
    , _actor_index(0)
    , _max_version(std::move(max_version))
{
}

BedrockRawDimension::~BedrockRawDimension()
{
    destroy();
}

OrderedMutex& BedrockRawDimension::get_mutex()
{
    return _public_mutex;
}

const DimensionId& BedrockRawDimension::get_dimension_id() const
{
    return _dimension_id;
}

BedrockInternalDimensionID BedrockRawDimension::get_internal_dimension_id() const
{
    return _internal_dimension_id;
}

const SelectionBox& BedrockRawDimension::get_bounds() const
{
    return _bounds;
}

const BlockStack& BedrockRawDimension::get_default_block() const
{
    return _default_block;
}

const Biome& BedrockRawDimension::get_default_biome() const
{
    return _default_biome;
}

BedrockChunkCoordIterator BedrockRawDimension::all_chunk_coords() const
{
    return BedrockChunkCoordIterator(_db->create_iterator(), _internal_dimension_id);
}

static std::string get_key_prefix(std::int32_t dimension, std::int32_t cx, std::int32_t cz)
{
    std::string key;
    TemplateBaseBinaryWriter<StaticLittleEndian, false> writer(key);
    writer.write_numeric<std::int32_t>(cx);
    writer.write_numeric<std::int32_t>(cz);
    if (dimension != 0) {
        writer.write_numeric<std::int32_t>(dimension);
    }
    return key;
}

bool BedrockRawDimension::has_chunk(std::int32_t cx, std::int32_t cz)
{
    auto& db = _db->get_database();
    std::string value;
    auto key_prefix = get_key_prefix(_internal_dimension_id, cx, cz);
    return db.Get(_db->get_read_options(), key_prefix + ',', &value).ok() || db.Get(_db->get_read_options(), key_prefix + 'v', &value).ok();
}

// Arbitrary tag type start.
// This allows us to skip over other dimensions without losing keys.
// Reduce this number if tags are added before this.
static const char MinTag = 0x10;

static void for_keys_in_chunk(LevelDB& _db, std::string key_prefix, std::function<void(const leveldb::Slice&)> callback)
{
    {
        auto it_ptr = _db.create_iterator();
        auto& it = it_ptr->get_iterator();

        auto key_start = key_prefix + MinTag;
        auto key_end = key_prefix + "\xFF\xFF";

        it.Seek(key_start);
        while (it.Valid()) {
            const auto& key = it.key();
            if (0 <= it.key().compare(key_end)) {
                break;
            }
            if (key_start.size() == key.size() || key_end.size() == key.size()) {
                callback(key);
            }
            it.Next();
        }
    }

    auto& db = _db.get_database();

    {
        auto& read_options = _db.get_read_options();
        std::string digp_key = "digp" + key_prefix;
        callback(digp_key);
        std::string digp;
        if (db.Get(read_options, digp_key, &digp).ok()) {
            size_t actor_count = (digp.size() / 8) * 8;
            for (size_t i = 0; i < actor_count; i += 8) {
                std::string actor_key;
                actor_key.reserve(19);
                actor_key = "actorprefix";
                actor_key += std::string_view(digp.data() + i, 8);

                callback(actor_key);
            }
        }
    }
}

void BedrockRawDimension::delete_chunk(std::int32_t cx, std::int32_t cz)
{
    auto key_prefix = get_key_prefix(_internal_dimension_id, cx, cz);

    leveldb::WriteBatch batch;
    for_keys_in_chunk(
        *_db,
        key_prefix,
        [&batch](const leveldb::Slice& key) {
            batch.Delete(key);
        });

    _db->get_database().Write(_db->get_write_options(), &batch);
}

BedrockRawChunk BedrockRawDimension::get_raw_chunk(std::int32_t cx, std::int32_t cz)
{
    auto key_prefix = get_key_prefix(_internal_dimension_id, cx, cz);
    std::map<Bytes, Bytes> data;

    {
        auto it_ptr = _db->create_iterator();
        auto& it = it_ptr->get_iterator();

        auto key_start = key_prefix + MinTag;
        auto key_end = key_prefix + "\xFF\xFF";

        it.Seek(key_start);
        while (it.Valid()) {
            const auto& key = it.key();
            if (0 <= it.key().compare(key_end)) {
                break;
            }
            if (key_start.size() == key.size() || key_end.size() == key.size()) {
                auto value = it.value();
                data.emplace(
                    Bytes(key.begin() + key_prefix.size(), key.size() - key_prefix.size()),
                    Bytes(value.data(), value.size()));
            }
            it.Next();
        }
    }

    std::vector<std::shared_ptr<NBT::NamedTag>> actors;

    {
        auto& db = _db->get_database();
        auto& read_options = _db->get_read_options();
        std::string digp_key = "digp" + key_prefix;
        std::string digp;
        if (db.Get(read_options, digp_key, &digp).ok()) {
            size_t actor_count = (digp.size() / 8) * 8;
            for (size_t i = 0; i < actor_count; i += 8) {
                std::string actor_key;
                actor_key.reserve(19);
                actor_key = "actorprefix";
                actor_key += std::string_view(digp.data() + i, 8);

                std::string actor_bytes;
                if (!db.Get(read_options, actor_key, &actor_bytes).ok()) {
                    error("Could not find actor " + actor_key + ". Skipping.");
                    continue;
                }

                std::shared_ptr<NBT::NamedTag> actor;
                try {
                    actor = std::make_shared<NBT::NamedTag>(
                        NBT::decode_nbt(actor_bytes, std::endian::little, NBT::utf8_to_utf8_escape));
                } catch (...) {
                    error("Failed to parse actor " + actor_key + ". Skipping.");
                    continue;
                }

                auto* actor_tag_ptr = std::get_if<NBT::CompoundTagPtr>(&actor->tag_node);
                if (!actor_tag_ptr) {
                    error("Actor " + actor_key + " is not a CompoundTag. Skipping.");
                    continue;
                }
                auto& actor_tag = **actor_tag_ptr;

                // Remove internal tags if they exist.
                actor_tag.erase("UniqueID");
                actor_tag.erase("internalComponents");

                actors.emplace_back(std::move(actor));
            }
        }
    }

    if (data.empty() && actors.empty()) {
        throw ChunkDoesNotExist();
    }

    return BedrockRawChunk(std::move(data), std::move(actors));
}

void BedrockRawDimension::set_raw_chunk(std::int32_t cx, std::int32_t cz, BedrockRawChunk& chunk)
{
    auto key_prefix = get_key_prefix(_internal_dimension_id, cx, cz);

    // Find keys that were in the chunk
    std::set<std::string> keys_to_delete;
    for_keys_in_chunk(
        *_db,
        key_prefix,
        [&keys_to_delete](const leveldb::Slice& key) {
            keys_to_delete.emplace(key.data(), key.size());
        });

    leveldb::WriteBatch batch;
    auto batch_put = [&batch, &keys_to_delete](const std::string& key, const std::string& value) {
        batch.Put(key, value);
        keys_to_delete.erase(key);
    };

    // Write all normal keys to the batch
    for (const auto& [tag, value] : chunk.get_data()) {
        if (2 < tag.size()) {
            // Chunk tags are only 1 or 2 bytes
            continue;
        }
        std::string key = key_prefix + tag;
        batch_put(key, value);
    }

    // Encode and write actors to the batch
    auto& actors = chunk.get_actors();
    if (!actors.empty()) {
        std::string digp;

        // Get the actor index and increment by the number of actors we are going to write.
        std::uint32_t actor_index = _actor_index.fetch_add(actors.size());

        for (std::uint32_t i = 0; i < actors.size(); i++, actor_index++) {
            std::string actor_key;
            {
                actor_key.reserve(8);
                TemplateBaseBinaryWriter<StaticBigEndian, false> actor_key_writer(actor_key);
                actor_key_writer.write_numeric<std::uint32_t>(_actor_group);
                actor_key_writer.write_numeric<std::uint32_t>(actor_index);
            }

            auto& actor = actors[i];

            auto* actor_tag_ptr = std::get_if<NBT::CompoundTagPtr>(&actor->tag_node);
            if (!actor_tag_ptr) {
                error("Actor " + std::to_string(i) + " in " + _dimension_id + " " + std::to_string(cx) + " " + std::to_string(cz) + " is not a CompoundTag. Skipping.");
                continue;
            }
            auto& actor_tag = **actor_tag_ptr;

            // Set UniqueID
            actor_tag.insert_or_assign("UniqueID", NBT::LongTag(i - (static_cast<std::int64_t>(_actor_group) << 32)));

            // Set internalComponents
            auto entity_component = std::make_shared<NBT::CompoundTag>();
            entity_component->emplace("StorageKey", NBT::StringTag(actor_key));
            auto internal_components = std::make_shared<NBT::CompoundTag>();
            internal_components->emplace("EntityStorageKeyComponent", std::move(entity_component));
            actor_tag.insert_or_assign(
                "internalComponents",
                std::move(internal_components));

            std::string actor_bytes;
            try {
                actor_bytes = NBT::encode_nbt(*actor, std::endian::little, NBT::utf8_escape_to_utf8);
            } catch (...) {
                error("Failed encoding actor " + std::to_string(i) + " in " + _dimension_id + " " + std::to_string(cx) + " " + std::to_string(cz) + ". Skipping.");
                continue;
            }

            batch_put("actorprefix" + actor_key, actor_bytes);

            digp += actor_key;
        }

        batch_put("digp" + key_prefix, digp);
    }

    // Mark all keys for deletion that were not overwritten.
    for (const auto& key : keys_to_delete) {
        batch.Delete(key);
    }

    // Write the batch.
    _db->get_database().Write(_db->get_write_options(), &batch);
}

std::unique_ptr<BedrockChunk> BedrockRawDimension::get_chunk(std::int32_t cx, std::int32_t cz)
{
    return decode_chunk(get_raw_chunk(cx, cz), cz, cz);
}

void BedrockRawDimension::set_chunk(std::int32_t cx, std::int32_t cz, BedrockChunk& chunk)
{
    auto encoded_chunk = encode_chunk(chunk, cx, cz);
    set_raw_chunk(cx, cz, encoded_chunk);
}

void BedrockRawDimension::destroy()
{
    _destroyed = true;
}

bool BedrockRawDimension::is_destroyed()
{
    return _destroyed;
}

} // namespace Amulet
