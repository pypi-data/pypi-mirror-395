#include <bit>
#include <memory>
#include <stdexcept>

#include <amulet/io/binary_reader.hpp>

#include <amulet/nbt/nbt_encoding/binary.hpp>
#include <amulet/nbt/string_encoding/string_encoding.hpp>

#include "chunk.hpp"
#include "raw_chunk.hpp"
#include "raw_dimension.hpp"

using namespace Amulet::NBT;

namespace Amulet {

// Parse a packed array as documented here
// https://gist.github.com/Tomcc/a96af509e275b1af483b25c543cfbf37
static std::vector<std::uint16_t> decode_packed_array(BinaryReader& reader)
{
    // Ignore LSB of data (its a flag)
    std::uint8_t bits_per_value = reader.read_numeric<std::uint8_t>() >> 1;

    std::vector<std::uint16_t> arr;

    if (0 < bits_per_value) {
        if (6 < bits_per_value && bits_per_value != 8 && bits_per_value != 16) {
            throw std::runtime_error("Invalid bits per value: " + std::to_string(bits_per_value));
        }

        // Word = 4 bytes, basis of compacting.
        const std::uint8_t values_per_word = 32 / bits_per_value;

        // Find the number of words required to fit 4096 values.
        const std::uint16_t word_count = (4096 + values_per_word - 1) / values_per_word;

        // Read the packed array
        std::vector<std::uint32_t> packed_array;
        reader.read_numeric_array<std::uint32_t>(packed_array, word_count);

        // Unpack the array
        const std::uint32_t bit_mask = (1 << bits_per_value) - 1;
        arr.reserve(4096 + values_per_word);
        for (auto word : packed_array) {
            for (std::uint8_t i = 0; i < values_per_word; i++) {
                arr.emplace_back(word & bit_mask);
                word >>= bits_per_value;
            }
        }
        arr.resize(4096);
    }

    return arr;
}

static void add_paletted_section(
    BinaryReader& reader,
    BlockStorage& block_storage,
    std::uint8_t count,
    std::int64_t cy)
{
    if (2 < count) {
        warning("Chunk section has more than two layers. Extra layers will be discarded");
        count = 2;
    }
    std::vector<
        std::pair<
            std::vector<std::uint16_t>,
            std::vector<Block>>>
        layers;
    layers.reserve(count);
    for (std::uint8_t layer_i = 0; layer_i < count; layer_i++) {
        auto layer_array = decode_packed_array(reader);

        // Get the palette length
        std::uint32_t palette_len;
        if (layer_array.empty()) {
            palette_len = 1;
            layer_array.resize(4096);
        } else {
            reader.read_numeric_into<std::uint32_t>(palette_len);
        }

        if (palette_len) {
            // Decode the NBT
            std::vector<Block> layer_palette;
            for (std::uint32_t i = 0; i < palette_len; i++) {
                // Decode the block
                auto named_tag = NBT::decode_nbt(reader);

                // Get the compound tag
                auto* tag_ptr = std::get_if<NBT::CompoundTagPtr>(&named_tag.tag_node);
                if (!tag_ptr) {
                    throw std::runtime_error("Block is not a CompoundTag");
                }
                auto& tag = **tag_ptr;

                // Get the name tag
                auto name_it = tag.find("name");
                if (name_it == tag.end()) {
                    throw std::runtime_error("Block[\"name\"] does not exist");
                }
                auto* name_ptr = std::get_if<NBT::StringTag>(&name_it->second);
                if (!name_ptr) {
                    throw std::runtime_error("Block[\"name\"] is not a StringTag");
                }
                auto& name_tag = *name_ptr;

                // Get the namespace and base name
                std::string namespace_;
                std::string base_name;
                auto colon_index = name_tag.find_first_of(':');
                if (colon_index == std::string::npos) {
                    namespace_ = "minecraft";
                    base_name = name_tag;
                } else {
                    namespace_ = name_tag.substr(0, colon_index);
                    base_name = name_tag.substr(colon_index + 1);
                }

                // Get version
                std::int64_t version = -1;
                auto version_it = tag.find("version");
                if (version_it != tag.end()) {
                    auto* version_ptr = std::get_if<NBT::IntTag>(&version_it->second);
                    if (version_ptr) {
                        version = *version_ptr;
                    } else {
                        throw std::runtime_error("Unsupported block version tag: " + std::to_string(version_it->second.index()));
                    }
                }

                // Get properties
                Block::PropertyMap properties;
                if (auto states_it = tag.find("states"); states_it != tag.end()) {
                    auto* states_ptr = std::get_if<NBT::CompoundTagPtr>(&states_it->second);
                    if (!states_ptr) {
                        throw std::runtime_error("Block states is not a CompoundTag");
                    }
                    for (const auto& [k, v] : **states_ptr) {
                        std::visit(
                            [&properties, &k](auto&& arg) {
                                using T = std::decay_t<decltype(arg)>;
                                if constexpr (
                                    std::is_same_v<T, Amulet::NBT::ByteTag>
                                    || std::is_same_v<T, Amulet::NBT::ShortTag>
                                    || std::is_same_v<T, Amulet::NBT::IntTag>
                                    || std::is_same_v<T, Amulet::NBT::LongTag>
                                    || std::is_same_v<T, Amulet::NBT::StringTag>) {
                                    properties.emplace(k, arg);
                                }
                            },
                            v);
                    }
                    if (version == -1) {
                        version = 17694720; // 1, 14, 0, 0
                    }
                } else if (auto val_it = tag.find("val"); val_it == tag.end()) {
                    if (version == -1) {
                        version = 17694720; // 1, 14, 0, 0
                    }
                } else {
                    auto* val_ptr = std::get_if<NBT::ShortTag>(&val_it->second);
                    if (!val_ptr) {
                        throw std::runtime_error("Block val is not a ShortTag");
                    }
                    properties.emplace("block_data", IntTag(*val_ptr));
                }

                // Add the block to the layer palette
                layer_palette.emplace_back(
                    Block {
                        "bedrock",
                        VersionNumber({ version }),
                        std::move(namespace_),
                        std::move(base_name),
                        std::move(properties) });
            }

            layers.emplace_back(
                std::make_pair(
                    std::move(layer_array),
                    std::move(layer_palette)));
        }
    }

    if (!layers.empty()) {
        auto& palette = block_storage.get_palette();
        auto& sections = block_storage.get_sections();
        sections.populate_section(cy);
        auto* section_buffer = sections.get_section(cy).get_buffer();

        auto& layer_0_palette = layers[0].second;
        auto& layer_0_array = layers[0].first;

        if (layers.size() == 1) {
            std::map<std::uint16_t, size_t> stack_to_index;

            // For each block in the sub-chunk
            for (std::uint16_t x = 0; x < 16; x++) {
                for (std::uint16_t y = 0; y < 16; y++) {
                    for (std::uint16_t z = 0; z < 16; z++) {

                        // Find the indexes for this block
                        std::uint32_t block_index = layer_0_array[(x << 8) + (z << 4) + y];

                        // Find which palette index this maps to.
                        size_t palette_index;
                        if (auto it = stack_to_index.find(block_index); it != stack_to_index.end()) {
                            // If we have already created the block then use the cached value
                            palette_index = it->second;
                        } else {
                            // Create the block stack and cache the value
                            if (layer_0_palette.size() <= block_index) {
                                throw std::runtime_error("Block index is larger than the block palette");
                            }
                            // Add to the palette and update the cache.
                            palette_index = palette.block_stack_to_index(
                                BlockStack { layer_0_palette[block_index] });
                            stack_to_index.emplace(block_index, palette_index);
                        }

                        // Write the index to the section
                        *(section_buffer + ((x << 8) + (y << 4) + z)) = palette_index;
                    }
                }
            }
        } else if (layers.size() == 2) {
            auto& layer_1_palette = layers[1].second;
            auto& layer_1_array = layers[1].first;
            std::map<std::uint32_t, size_t> stack_to_index;

            // For each block in the sub-chunk
            for (std::uint16_t x = 0; x < 16; x++) {
                for (std::uint16_t y = 0; y < 16; y++) {
                    for (std::uint16_t z = 0; z < 16; z++) {

                        // Find the indexes for this block
                        const std::uint16_t src_index = (x << 8) + (z << 4) + y;
                        std::uint16_t block_index_0 = layer_0_array[src_index];
                        std::uint16_t block_index_1 = layer_1_array[src_index];
                        std::uint32_t block_indexes = block_index_0 | (block_index_1 << 16);

                        // Find which palette index this maps to.
                        size_t palette_index;
                        if (auto it = stack_to_index.find(block_indexes); it != stack_to_index.end()) {
                            // If we have already created the block then use the cached value
                            palette_index = it->second;
                        } else {
                            // Create the block stack and cache the value
                            if (layer_0_palette.size() <= block_index_0 || layer_1_palette.size() <= block_index_1) {
                                throw std::runtime_error("Block index is larger than the block palette");
                            }
                            // Add to the palette and update the cache.
                            palette_index = palette.block_stack_to_index(
                                BlockStack { layer_0_palette[block_index_0], layer_1_palette[block_index_1] });
                            stack_to_index.emplace(block_indexes, palette_index);
                        }

                        // Write the index to the section
                        *(section_buffer + ((x << 8) + (y << 4) + z)) = palette_index;
                    }
                }
            }
        }
    }
}

static void _decode_bedrock_chunk_terrain(
    std::int16_t legacy_floor,
    std::int32_t cx,
    std::int32_t cz,
    std::map<Bytes, Bytes>& data,
    BlockComponent& chunk)
{
    // decode block data
    // https://gist.github.com/Tomcc/a96af509e275b1af483b25c543cfbf37
    auto it2f = data.lower_bound("\x2F\x00");
    while (it2f != data.end() && !it2f->first.empty() && it2f->first[0] == '\x2F') {
        if (it2f->first.size() != 2) {
            it2f++;
            continue;
        }

        // Increment the iterator and extract the node.
        auto node = data.extract(it2f++);
        auto cy = static_cast<std::int64_t>(node.key()[1]) + legacy_floor;
        auto& value = node.mapped();

        BinaryReader reader(value, 0, std::endian::little, NBT::utf8_to_utf8_escape);
        auto block_format = reader.read_numeric<std::uint8_t>();
        if (block_format == 9) {
            auto layer_count = reader.read_numeric<std::uint8_t>();
            cy = reader.read_numeric<std::int8_t>();
            add_paletted_section(
                reader,
                chunk.get_block_storage(),
                layer_count,
                cy);
        } else if (block_format == 8) {
            auto layer_count = reader.read_numeric<std::uint8_t>();
            add_paletted_section(
                reader,
                chunk.get_block_storage(),
                layer_count,
                cy);
        } else if (block_format == 1) {
            add_paletted_section(
                reader,
                chunk.get_block_storage(),
                1,
                cy);
        } else if (block_format <= 7) {
            throw std::runtime_error("NotImplementedError: Legacy block format.");
        } else {
            error("Unknown SubChunkPrefix version. v=" + std::to_string(block_format) + ",cx=" + std::to_string(cx) + ",cy=" + std::to_string(cy) + ",cz=" + std::to_string(cz));
            continue;
        }
    }
}

template <typename ChunkT>
void _decode_bedrock_chunk_common(ChunkT& chunk, BedrockRawChunk& raw_chunk)
{
    // Move the remaining raw data into the chunk.
    chunk.set_raw_data(std::make_shared<BedrockRawChunk>(std::move(raw_chunk)));
}

static std::unique_ptr<BedrockChunk> _decode_bedrock_chunk_0(
    BedrockRawChunk& raw_chunk,
    std::int32_t cx,
    std::int32_t cz,
    std::map<Bytes, Bytes>::const_iterator& it30)
{
    throw std::runtime_error("LegacyTerrain NotImplementedError");
}

static std::unique_ptr<BedrockChunk> _decode_bedrock_chunk_0b(
    BedrockRawChunk& raw_chunk,
    std::int32_t cx,
    std::int32_t cz,
    std::map<Bytes, Bytes>::const_iterator& it30)
{
    // 2D biomes with RGB
    // TODO: extract biome and height data
    throw std::runtime_error("LegacyTerrain NotImplementedError");
}

static std::unique_ptr<BedrockChunk> _decode_bedrock_chunk_1(
    const BlockStack& default_block,
    const Biome& default_biome,
    std::int16_t legacy_floor,
    std::int32_t cx,
    std::int32_t cz,
    BedrockRawChunk& raw_chunk,
    std::map<Bytes, Bytes>::const_iterator& it2d)
{
    // 2D biomes
    auto chunk = std::make_unique<BedrockChunk1>(default_block, default_biome);
    _decode_bedrock_chunk_terrain(legacy_floor, cx, cz, raw_chunk.get_data(), *chunk);
    // TODO: extract biome and height data
    _decode_bedrock_chunk_common(*chunk, raw_chunk);
    return chunk;
}

static std::unique_ptr<BedrockChunk> _decode_bedrock_chunk_118(
    const BlockStack& default_block,
    const Biome& default_biome,
    std::int16_t legacy_floor,
    std::int32_t cx,
    std::int32_t cz,
    BedrockRawChunk& raw_chunk)
{
    // 3D biomes
    auto chunk = std::make_unique<BedrockChunk118>(default_block, default_biome);
    _decode_bedrock_chunk_terrain(legacy_floor, cx, cz, raw_chunk.get_data(), *chunk);
    // TODO: extract biome and height data
    _decode_bedrock_chunk_common(*chunk, raw_chunk);
    return chunk;
}

std::unique_ptr<BedrockChunk> BedrockRawDimension::decode_chunk(
    BedrockRawChunk raw_chunk,
    std::int32_t cx,
    std::int32_t cz)
{
    const auto& data = raw_chunk.get_data();

    if (auto it30 = data.find("\x30"); it30 != data.end()) {
        // LegacyTerrain
        return _decode_bedrock_chunk_0(raw_chunk, cx, cz, it30);
    } else if (auto it2e = data.find("\x2E"); it2e != data.end()) {
        // ? TODO
        return _decode_bedrock_chunk_0b(raw_chunk, cx, cz, it2e);
    } else if (auto it2d = data.find("\x2D"); it2d != data.end()) {
        // Data2D and SubChunkPrefix
        return _decode_bedrock_chunk_1(get_default_block(), get_default_biome(), _legacy_floor, cx, cz, raw_chunk, it2d);
    } else {
        // Data3D and SubChunkPrefix
        return _decode_bedrock_chunk_118(get_default_block(), get_default_biome(), _legacy_floor, cx, cz, raw_chunk);
    }
}

} // namespace Amulet
