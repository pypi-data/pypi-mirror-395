#include <bit>
#include <memory>
#include <stdexcept>

#include <amulet/io/binary_writer.hpp>

#include <amulet/nbt/nbt_encoding/binary.hpp>
#include <amulet/nbt/string_encoding/string_encoding.hpp>

#include <amulet/core/version/version.hpp>

#include "chunk.hpp"
#include "raw_chunk.hpp"
#include "raw_dimension.hpp"

using namespace Amulet::NBT;

namespace Amulet {

static void _encode_legacy_terrain()
{
    throw std::runtime_error("LegacyTerrain NotImplementedError");
}

class BedrockEncodedLayer {
public:
    // Index array
    std::array<std::uint16_t, 4096> arr;
    // Convert from block to index
    std::map<Block, std::uint16_t> block_to_index;
    // Convert from index to block
    std::vector<const Block*> palette;

    BedrockEncodedLayer(const Block& default_block)
        : arr {}
    {
        get_index(default_block);
    }

    // Delete copy
    BedrockEncodedLayer(const BedrockEncodedLayer& other) = delete;
    BedrockEncodedLayer& operator=(const BedrockEncodedLayer& other) = delete;

    // Default move
    BedrockEncodedLayer(BedrockEncodedLayer&& other) noexcept = default;
    BedrockEncodedLayer& operator=(BedrockEncodedLayer&& other) noexcept = default;

    std::uint16_t get_index(const Block& block)
    {
        auto it = block_to_index.find(block);
        if (it == block_to_index.end()) {
            it = block_to_index.emplace(block, static_cast<std::uint16_t>(palette.size())).first;
            palette.emplace_back(&it->first);
        }
        return it->second;
    }
};

static void encode_packed_array(
    BaseBinaryWriter& writer,
    const std::array<std::uint16_t, 4096>& array,
    std::uint16_t max_value,
    std::uint8_t min_bit_size = 1)
{
    // Get the number of bits required to fit the maximum value
    std::uint8_t bits_per_value = std::max(
        min_bit_size,
        static_cast<std::uint8_t>(16 - std::countl_zero(max_value)));

    // Fix invalid states
    if (bits_per_value == 7) {
        bits_per_value = 8;
    } else if (9 <= bits_per_value) {
        bits_per_value = 16;
    }

    // Write the header.
    // LSB is always 0 for the persistant format.
    writer.write_numeric<std::uint8_t>(bits_per_value << 1);

    // Find how many values can fit in a word (32 bits)
    std::uint8_t values_per_word = 32 / bits_per_value;

    // Find the number of words required to fit 4096 values.
    const std::uint16_t word_count = (4096 + values_per_word - 1) / values_per_word;

    const std::uint32_t bit_mask = (1 << bits_per_value) - 1;

    for (std::uint16_t array_index = 0; array_index < 4096;) {
        std::uint32_t word = 0;
        for (
            std::uint8_t i = 0;
            i < values_per_word && array_index < 4096;
            i++, array_index++) {
            word |= (array[array_index] & bit_mask) << (i * bits_per_value);
        }
        writer.write_numeric<std::uint32_t>(word);
    }
}

template <std::uint8_t SubChunkVersion>
std::int8_t _encode_bedrock_palette_section_terrain(
    BaseBinaryWriter& writer,
    const Block& default_block,
    const IndexArray3D& section,
    const BlockPalette& palette)
{
    const auto* section_buffer = section.get_buffer();

    auto palette_size = palette.size();

    // Convert from the chunk palette index to local palette indexes
    std::vector<std::vector<std::uint16_t>> palette_to_layer_indexes(palette_size);

    // Data for each layer
    std::vector<BedrockEncodedLayer> layers;

    // Convert the sub-chunk array and block stack palette into layer arrays and block palettes
    for (std::uint16_t x = 0; x < 16; x++) {
        for (std::uint16_t y = 0; y < 16; y++) {
            for (std::uint16_t z = 0; z < 16; z++) {
                // Get the chunk palette index
                auto palette_index = *(section_buffer + ((x << 8) + (y << 4) + z));

                // Check the index is valid
                if (palette_size <= palette_index) {
                    throw std::runtime_error("Index is larger than the palette.");
                }

                // Get the layer array index
                // Note the layers are stored in encoded order. (XZY)
                std::uint16_t layer_array_index = (x << 8) + (z << 4) + y;

                auto& layer_block_indexes = palette_to_layer_indexes[palette_index];
                if (layer_block_indexes.empty()) {
                    // If we have not already computed the indexes then compute them
                    const auto& block_stack = palette.index_to_block_stack(palette_index);
                    size_t stack_size;
                    if constexpr (8 <= SubChunkVersion) {
                        stack_size = std::min(block_stack.size(), static_cast<size_t>(127));
                    } else {
                        stack_size = 1;
                    }
                    for (size_t layer_index = 0; layer_index < stack_size; layer_index++) {
                        const auto& block = block_stack.at(layer_index);
                        if (layers.size() <= layer_index) {
                            // Add a new layer if required.
                            layers.emplace_back(default_block);
                        }
                        auto& layer = layers[layer_index];
                        auto block_index = layer.get_index(block);
                        layer_block_indexes.emplace_back(block_index);
                        layer.arr[layer_array_index] = block_index;
                    }
                } else {
                    // Use the pre-computed indexes
                    for (size_t layer_index = 0; layer_index < layer_block_indexes.size(); layer_index++) {
                        layers[layer_index].arr[layer_array_index] = layer_block_indexes[layer_index];
                    }
                }
            }
        }
    }

    // Encode each layer.
    for (const auto& layer : layers) {
        // Encode the array
        encode_packed_array(writer, layer.arr, layer.palette.size() - 1);

        // Encode the palette
        writer.write_numeric<std::uint32_t>(layer.palette.size());
        for (const auto* block_ptr : layer.palette) {
            const auto& block = *block_ptr;
            NBT::CompoundTag block_tag;

            // Create the block name
            NBT::StringTag block_name;
            block_name.reserve(block.get_namespace().size() + 1 + block.get_base_name().size());
            block_name += block.get_namespace();
            block_name += ':';
            block_name += block.get_base_name();
            block_tag.emplace("name", std::move(block_name));

            // Add the version tag
            auto version = block.get_version()[0];
            const auto& properties = block.get_properties();
            if (0 <= version) {
                block_tag.emplace("version", NBT::IntTag(version));
                auto states_ptr = std::make_shared<NBT::CompoundTag>();
                auto& states = *states_ptr;
                for (const auto& [k, v] : properties) {
                    std::visit(
                        [&states, &k](auto&& arg) {
                            states.emplace(k, arg);
                        },
                        v);
                }
                block_tag.emplace("states", std::move(states_ptr));
            } else {
                NBT::ShortTag block_data = 0;
                auto block_data_it = properties.find("block_data");
                if (block_data_it != properties.end()) {
                    const auto* block_data_ptr = std::get_if<NBT::IntTag>(&block_data_it->second);
                    if (block_data_ptr) {
                        block_data = *block_data_ptr;
                    }
                }
                block_tag.emplace("val", NBT::ShortTag());
            }

            NBT::encode_nbt(writer, "", block_tag);
        }
    }

    return layers.size();
}

template <std::uint8_t SubChunkVersion>
void _encode_bedrock_palette_chunk_terrain(
    std::int16_t legacy_floor,
    const Block& default_block,
    BlockComponent& chunk,
    std::map<Bytes, Bytes>& data)
{
    auto& block_storage = chunk.get_block_storage();
    auto& palette = block_storage.get_palette();
    auto& sections = block_storage.get_sections();

    for (const auto& [cy, section] : sections) {
        if (cy < -128 || 127 < cy) {
            continue;
        }

        std::string buffer;
        BaseBinaryWriter writer(buffer, std::endian::little, NBT::utf8_escape_to_utf8);
        writer.reserve(4096);

        // Sub-Chunk version 0, 1, 8 or 9
        writer.write_numeric<std::uint8_t>(SubChunkVersion);

        if constexpr (8 <= SubChunkVersion) {
            // The number of layers. Reserved now and written after layers are written.
            writer.write_numeric<std::int8_t>(0);
        }

        if constexpr (9 <= SubChunkVersion) {
            // The cy coordinate
            writer.write_numeric<std::int8_t>(cy);
        }

        // Write the sections
        std::int8_t layer_count = _encode_bedrock_palette_section_terrain<SubChunkVersion>(
            writer,
            default_block,
            *section,
            palette);

        if constexpr (8 <= SubChunkVersion) {
            // Set the number of layers
            buffer[1] = layer_count;
        }

        // Create the key
        std::string key("\x2F\x00", 2);
        key[1] = static_cast<std::int8_t>(cy - legacy_floor);

        // Add to the chunk data
        data.insert_or_assign(std::move(key), std::move(buffer));
    }
}

// Version not verified
static const VersionNumber Biome3DVersion { 1, 18, 0 };

// This version may have been added in the 1.17.20 betas but I can't access them.
static const VersionNumber SubChunkVersion9 { 1, 17, 30 };

// 1.2.10.2 < real version <= 1.4.2.0
static const VersionNumber SubChunkVersion8 { 1, 4, 2 };

// Version not verified
static const VersionNumber SubChunkVersion0 { 1, 0, 0 };

template <typename ChunkT>
BedrockRawChunk _encode_bedrock_chunk(
    const VersionNumber& max_version,
    std::int16_t legacy_floor,
    const Block& default_block,
    ChunkT& chunk)
{
    // Extract the raw chunk data
    auto raw_chunk_ptr = chunk.get_raw_data();
    if (!raw_chunk_ptr) {
        throw std::runtime_error("raw_data pointer is empty");
    }
    auto& raw_chunk = *raw_chunk_ptr;
    auto& data = raw_chunk.get_data();

    if constexpr (std::is_same_v<ChunkT, BedrockChunk0>) {
        // LegacyTerrain
        _encode_legacy_terrain();
    } else {
        if constexpr (std::is_same_v<ChunkT, BedrockChunk1>) {
            // Data2D
            // TODO: Encode biome and height data
        } else {
            static_assert(std::is_same_v<ChunkT, BedrockChunk118>);
            // Data3D
            // TODO: Encode biome and height data
        }

        {
            // Encode block data
            if (SubChunkVersion9 <= max_version) {
                // sub-chunk version 9
                _encode_bedrock_palette_chunk_terrain<9>(legacy_floor, default_block, chunk, data);
            } else if (SubChunkVersion8 <= max_version) {
                // sub-chunk version 8
                _encode_bedrock_palette_chunk_terrain<8>(legacy_floor, default_block, chunk, data);
            }
            // else if (VersionNumber {} < max_version) {
            //     // sub-chunk version 1
            // }
            else {
                // sub-chunk version 0
                throw std::runtime_error("NotImplementedError: Legacy block format.");
            }
        }
    }

    // Return the raw chunk data.
    // Move is needed here because raw_chunk is a refernce.
    return std::move(raw_chunk);
}

BedrockRawChunk BedrockRawDimension::encode_chunk(
    BedrockChunk& chunk,
    std::int32_t cx,
    std::int32_t cz)
{
    if (auto* chunk_ = dynamic_cast<BedrockChunk118*>(&chunk)) {
        return _encode_bedrock_chunk(_max_version, _legacy_floor, _default_block.at(0), *chunk_);
    } else if (auto* chunk_ = dynamic_cast<BedrockChunk1*>(&chunk)) {
        return _encode_bedrock_chunk(_max_version, _legacy_floor, _default_block.at(0), *chunk_);
    } else if (auto* chunk_ = dynamic_cast<BedrockChunk0*>(&chunk)) {
        return _encode_bedrock_chunk(_max_version, _legacy_floor, _default_block.at(0), *chunk_);
    } else {
        throw std::invalid_argument("Unsupported Bedrock chunk class: " + chunk.get_chunk_id());
    }
}

} // namespace Amulet
