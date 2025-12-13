#include <algorithm>
#include <cstdint>
#include <functional>
#include <map>
#include <memory>
#include <optional>
#include <stdexcept>
#include <string>
#include <tuple>
#include <type_traits>
#include <variant>

#include <amulet/nbt/tag/compound.hpp>
#include <amulet/nbt/tag/named_tag.hpp>

#include <amulet/core/block/block.hpp>
#include <amulet/core/chunk/chunk.hpp>
#include <amulet/core/version/version.hpp>

#include <amulet/game/game.hpp>
#include <amulet/game/java/version.hpp>

#include "chunk.hpp"
#include "long_array.hpp"
#include "raw_dimension.hpp"

using namespace Amulet::NBT;
using namespace Amulet::game;

namespace Amulet {
template <typename tagT>
tagT get_tag(const CompoundTag& compound, std::string name, std::function<tagT()> get_default)
{
    const auto& it = compound.find(name);
    if (
        it != compound.end() && std::holds_alternative<tagT>(it->second)) {
        return std::get<tagT>(it->second);
    }
    return get_default();
}

template <typename tagT>
tagT pop_tag(CompoundTag& compound, std::string name, std::function<tagT()> get_default)
{
    auto node = compound.extract(name);
    if (
        node && std::holds_alternative<tagT>(node.mapped())) {
        return std::get<tagT>(node.mapped());
    }
    return get_default();
}

template <int DataVersion, typename ChunkT>
void decode_java_chunk(
    ChunkT& chunk,
    JavaRawChunk raw_chunk,
    CompoundTag& region,
    std::int64_t cx,
    std::int64_t cz,
    const VersionNumber& version,
    std::int64_t data_version,
    const BlockStack& default_block,
    const Biome& default_biome)
{
    std::shared_ptr<JavaGameVersion> game_version = get_java_game_version(version);

    std::optional<Block> _water_block;
    auto get_water = [&version, &_water_block]() -> const Block& {
        if (!_water_block) {
            auto block_translator = get_java_game_version(VersionNumber({ 3837 }))->get_block_data();
            auto converted = block_translator->translate(
                "java",
                version,
                Block(
                    "java",
                    VersionNumber({ 3837 }),
                    "minecraft",
                    "water",
                    std::initializer_list<Block::PropertyMap::value_type> { { "level", StringTag("0") } }));

            std::visit(
                [&version, &_water_block](auto&& arg) {
                    using T = std::decay_t<decltype(arg)>;
                    if constexpr (std::is_same_v<T, std::tuple<Block, std::optional<BlockEntity>, bool>>) {
                        _water_block = std::get<0>(arg);
                    } else {
                        throw std::runtime_error("Water block did not convert to a block in version Java " + version.toString());
                    }
                },
                converted);
        }
        return *_water_block;
    };

    // Get the data root
    CompoundTagPtr level_keep_alive_ptr;
    CompoundTag& level_tag = [&level_keep_alive_ptr, &region]() -> CompoundTag& {
        // In 2844 the Level tag was removed and its contents moved into the root.
        if constexpr (DataVersion >= 2844) {
            return region;
        } else {
            level_keep_alive_ptr = get_tag<CompoundTagPtr>(
                region,
                "Level",
                []() { return std::make_shared<CompoundTag>(); });
            return *level_keep_alive_ptr;
        }
    }();

    // Validate coordinates and get chunk floor
    {
        auto inline_cx = pop_tag<IntTag>(level_tag, "xPos", []() { return IntTag(); }).value;
        auto inline_cz = pop_tag<IntTag>(level_tag, "zPos", []() { return IntTag(); }).value;
        if (cx != inline_cx || cz != inline_cz) {
            throw std::runtime_error("Inline chunk coord data is incorrect.");
        }
    }
    auto floor_cy = pop_tag<IntTag>(level_tag, "yPos", []() { return IntTag(); }).value;

    // Remove old version tag
    if constexpr (DataVersion < 0) {
        // LegacyVersionComponent TODO
        // pop_tag<ByteTag>(*level_tag, "V", []() { return ByteTag(1); });
    }

    // Get sections
    ListTagPtr sections_ptr = get_tag<ListTagPtr>(
        level_tag,
        []() {
            if constexpr (DataVersion >= 2844) {
                return "sections";
            } else {
                return "Sections";
            }
        }(),
        []() { return std::make_shared<ListTag>(); });
    auto sections_map = [&sections_ptr]() {
        if (!std::holds_alternative<CompoundListTag>(*sections_ptr)) {
            throw std::invalid_argument("Chunk sections is not a list of compound tags.");
        }
        auto& sections = std::get<CompoundListTag>(*sections_ptr);
        std::map<std::int64_t, CompoundTagPtr> sections_map;
        for (auto& tag : sections) {
            sections_map.emplace(
                get_tag<ByteTag>(*tag, "Y", []() { return ByteTag(); }).value,
                tag);
        }
        return sections_map;
    }();

    // blocks
    {
        std::shared_ptr<BlockStorage> block_storage = chunk.get_block_storage_ptr();
        auto& block_palette = block_storage->get_palette();
        auto& block_sections = block_storage->get_sections();
        auto version_block_data = game_version->get_block_data();
        if constexpr (1444 <= DataVersion) {
            // Palette format
            // if 2844 <= data_version:
            //     region.sections[].block_states.data
            //     region.sections[].block_states.palette
            // elif 2836 <= data_version:
            //     region.Level.Sections[].block_states.data
            //     region.Level.Sections[].block_states.palette
            // else:
            //     region.Level.Sections[].BlockStates
            //     region.Level.Sections[].Palette

            for (auto& [cy, section] : sections_map) {
                ListTagPtr block_palette_tag;
                LongArrayTagPtr block_data_tag;
                if constexpr (DataVersion >= 2836) {
                    auto block_states_tag = pop_tag<CompoundTagPtr>(*section, "block_states", []() { return nullptr; });
                    if (!block_states_tag) {
                        continue;
                    }
                    block_palette_tag = pop_tag<ListTagPtr>(*block_states_tag, "palette", []() { return nullptr; });
                    block_data_tag = pop_tag<LongArrayTagPtr>(*block_states_tag, "data", []() { return nullptr; });
                } else {
                    block_palette_tag = pop_tag<ListTagPtr>(*section, "Palette", []() { return nullptr; });
                    block_data_tag = pop_tag<LongArrayTagPtr>(*section, "BlockStates", []() { return nullptr; });
                }
                if (!block_palette_tag || !std::holds_alternative<CompoundListTag>(*block_palette_tag)) {
                    continue;
                }
                const auto& palette = std::get<CompoundListTag>(*block_palette_tag);
                size_t palette_size = palette.size();
                std::vector<std::uint32_t> lut;
                lut.reserve(palette_size);
                for (auto& block_tag : palette) {
                    auto block_name = get_tag<StringTag>(*block_tag, "Name",
                        []() -> StringTag { throw std::invalid_argument("Block has no Name attribute."); });
                    auto [block_namespace, block_base_name] = [&block_name]() -> std::pair<std::string, std::string> {
                        auto colon_index = block_name.find(':');
                        if (colon_index == std::string::npos) {
                            return std::make_pair("", block_name);
                        } else {
                            return std::make_pair(
                                block_name.substr(0, colon_index),
                                block_name.substr(colon_index + 1));
                        }
                    }();
                    auto properties_tag = get_tag<CompoundTagPtr>(*block_tag, "Properties",
                        []() { return std::make_shared<CompoundTag>(); });
                    std::map<std::string, Block::PropertyValue> block_properties;
                    for (const auto& [k, v] : *properties_tag) {
                        std::visit(
                            [&block_properties, &k](auto&& arg) {
                                using T = std::decay_t<decltype(arg)>;
                                if constexpr (
                                    std::is_same_v<T, ByteTag>
                                    || std::is_same_v<T, ShortTag>
                                    || std::is_same_v<T, IntTag>
                                    || std::is_same_v<T, LongTag>
                                    || std::is_same_v<T, StringTag>) {
                                    block_properties.emplace(k, arg);
                                }
                            },
                            v);
                    }
                    std::vector<Block> blocks;

                    auto waterloggable = version_block_data->is_waterloggable(block_namespace, block_base_name);
                    switch (waterloggable) {
                    case Waterloggable::Yes: {
                        auto waterlogged_it = block_properties.find("waterlogged");
                        if (
                            waterlogged_it != block_properties.end() and std::holds_alternative<StringTag>(waterlogged_it->second)) {
                            if (std::get<StringTag>(waterlogged_it->second) == "true") {
                                blocks.push_back(get_water());
                            }
                            block_properties.erase(waterlogged_it);
                        }
                        break;
                    }
                    case Waterloggable::Always:
                        blocks.push_back(get_water());
                        break;
                    default:
                        break;
                    }
                    blocks.insert(
                        blocks.begin(),
                        Block(
                            "java",
                            version,
                            block_namespace,
                            block_base_name,
                            block_properties));

                    lut.push_back(static_cast<std::uint32_t>(block_palette.block_stack_to_index(blocks)));
                }

                std::shared_ptr<IndexArray3D> index_array;

                if (block_data_tag) {
                    std::vector<std::uint32_t> decoded_vector(4096);
                    std::span<std::uint32_t> decoded_span(decoded_vector);
                    decode_long_array(
                        std::span<std::uint64_t>(reinterpret_cast<std::uint64_t*>(block_data_tag->data()), block_data_tag->size()),
                        decoded_span,
                        std::max<std::uint8_t>(4, std::bit_width(palette_size - 1)),
                        DataVersion <= 2529);
                    index_array = std::make_shared<IndexArray3D>(
                        std::make_tuple<std::uint16_t>(16, 16, 16));
                    std::span<std::uint32_t> index_array_span(index_array->get_buffer(), index_array->get_size());
                    // Convert YZX to XYZ and look up in lut.
                    for (size_t y = 0; y < 16; y++) {
                        for (size_t x = 0; x < 16; x++) {
                            for (size_t z = 0; z < 16; z++) {
                                auto& block_index = decoded_span[y * 256 + z * 16 + x];
                                if (palette_size <= block_index) {
                                    throw std::runtime_error(
                                        "Block index at cx=" + std::to_string(cx)
                                        + ",cy=" + std::to_string(cy)
                                        + ",cz=" + std::to_string(cz)
                                        + ",dx=" + std::to_string(x)
                                        + ",dy=" + std::to_string(y)
                                        + ",dz=" + std::to_string(z)
                                        + " is larger than the block palette size.");
                                }
                                index_array_span[x * 256 + y * 16 + z] = lut[block_index];
                            }
                        }
                    }
                } else if (lut.size() == 1) {
                    index_array = std::make_shared<IndexArray3D>(
                        std::make_tuple<std::uint16_t>(16, 16, 16),
                        lut[0]);
                } else {
                    throw std::runtime_error("Block palette size != 1 and block array does not exist.");
                }
                block_sections.set_section(cy, index_array);
            }
        } else {
            // Numerical format
            throw std::runtime_error("NotImplemented");
            // blocks: dict[int, SubChunkNDArray] = {}
            // palette = []
            // palette_len = 0
            // for cy, section in _iter_sections():
            //     block_tag = section.pop("Blocks", None)
            //     data_tag = section.pop("Data", None)
            //     if not isinstance(block_tag, AbstractBaseArrayTag) or not isinstance(
            //             data_tag, AbstractBaseArrayTag
            //     ):
            //         continue
            //     section_blocks = numpy.asarray(block_tag, dtype=numpy.uint8)
            //     section_data = numpy.asarray(data_tag, dtype=numpy.uint8)
            //     section_blocks = section_blocks.reshape((16, 16, 16))
            //     section_blocks = section_blocks.astype(numpy.uint16)

            //    section_data = world_utils.from_nibble_array(section_data)
            //    section_data = section_data.reshape((16, 16, 16))

            //    add_tag = section.pop("Add", None)
            //    if isinstance(add_tag, AbstractBaseArrayTag):
            //        add_blocks = numpy.asarray(add_tag, dtype=numpy.uint8)
            //        add_blocks = world_utils.from_nibble_array(add_blocks)
            //        add_blocks = add_blocks.reshape((16, 16, 16))

            //        section_blocks |= add_blocks.astype(numpy.uint16) << 8
            //        # TODO: fix this

            //    (section_palette, blocks[cy]) = world_utils.fast_unique(
            //        numpy.transpose(
            //            (section_blocks << 4) + section_data, (2, 0, 1)
            //        )  # YZX -> XYZ
            //    )
            //    blocks[cy] += palette_len
            //    palette_len += len(section_palette)
            //    palette.append(section_palette)

            // if palette:
            //     final_palette, lut = numpy.unique(
            //         numpy.concatenate(palette), return_inverse=True
            //     )
            //     final_palette: numpy.ndarray = numpy.array(
            //         [final_palette >> 4, final_palette & 15]
            //     ).T
            //     for cy in blocks:
            //         blocks[cy] = lut[blocks[cy]]
            // else:
            //     final_palette = numpy.array([], dtype=object)
            // chunk.blocks = blocks
            // chunk.misc["block_palette"] = final_palette
        }
    }

    // Block entities TODO
    // if 2844 <= DataVersion:
    //     BlockEntities = ("region", [("block_entities", ListTag)], ListTag)
    // else:
    //     BlockEntities = (
    //         "region",
    //         [("Level", CompoundTag), ("TileEntities", ListTag)],
    //         ListTag,
    //     )
    // def _decode_block_entity_list(block_entities: ListTag) -> List["BlockEntity"]:
    //     entities_out = []
    //     if block_entities.list_data_type == CompoundTag.tag_id:
    //         for nbt in block_entities:
    //             if not isinstance(nbt, CompoundTag):
    //                 continue
    //             entity = self._decode_block_entity(
    //                 NamedTag(nbt),
    //                 EntityIDType.namespace_str_id,
    //                 EntityCoordType.xyz_int,
    //             )
    //             if entity is not None:
    //                 entities_out.append(entity)
    //     return entities_out
    // chunk.block_entities = _decode_block_entity_list(
    //     get_layer_obj(data, BlockEntities, pop_last=True)
    //)

    // Entities TODO
    // def _decode_entity_list(entities: ListTag) -> list["Entity"]:
    //     entities_out = []
    //     if entities.list_data_type == CompoundTag.tag_id:
    //         for nbt in entities:
    //             entity = _decode_entity(
    //                 NamedTag(nbt),
    //                 EntityIDType.namespace_str_id,
    //                 EntityCoordType.Pos_list_double,
    //             )
    //             if entity is not None:
    //                 entities_out.append(entity)
    //    return entities_out
    //
    // if 2844 <= DataVersion:
    //     Entities = ("region", [("entities", ListTag)], ListTag)
    // else:
    //     Entities = (
    //         "region",
    //         [("Level", CompoundTag), ("Entities", ListTag)],
    //         ListTag,
    //     )
    // ents = _decode_entity_list(
    //     get_layer_obj(data, Entities, pop_last=True)
    //)
    // if 2681 <= DataVersion:
    //     # TODO: it is possible the entity layer data version does not match the chunk data version
    //     EntityLayer = (
    //         "entities",
    //         [("Entities", ListTag)],
    //         ListTag,
    //     )
    //
    //    // TODO: Remove the entity data version
    //    if data_version != get_layer_obj(data, (
    //        "entities",
    //        [("DataVersion", IntTag)],
    //        IntTag,
    //    )):
    //        raise RuntimeError("region data version does not equal entities data version.")
    //
    //    ents += _decode_entity_list(
    //        get_layer_obj(data, EntityLayer, pop_last=True)
    //    )
    //
    // if amulet.entity_support:
    //     chunk.entities = ents
    // else:
    //     chunk._native_entities.extend(ents)
    //     chunk._native_version = ("java", data_version)

    // Block and fluid ticks
    // if 2844 <= DataVersion:
    //     BlockTicks = ("region", [("block_ticks", ListTag)], ListTag)
    // else:
    //     BlockTicks = (
    //         "region",
    //         [("Level", CompoundTag), ("TileTicks", ListTag)],
    //         ListTag,
    //     )
    // chunk.misc.setdefault("block_ticks", {}).update(
    //     decode_ticks(get_layer_obj(data, BlockTicks, pop_last=True))
    //)
    //
    // if 1444 <= DataVersion < 2844:
    //     ToBeTicked = (
    //         "region",
    //         [("Level", CompoundTag), ("ToBeTicked", ListTag)],
    //         ListTag,
    //     )
    //     chunk.misc["to_be_ticked"] = decode_to_be_ticked(
    //         get_layer_obj(data, ToBeTicked, pop_last=True), floor_cy
    //     )
    //
    // if 1444 <= DataVersion:
    //     if 2844 <= DataVersion:
    //         LiquidTicks = ("region", [("fluid_ticks", ListTag)], ListTag)
    //     else:
    //         LiquidTicks = (
    //             "region",
    //             [("Level", CompoundTag), ("LiquidTicks", ListTag)],
    //             ListTag,
    //         )
    //     chunk.misc.setdefault("fluid_ticks", {}).update(
    //         decode_ticks(
    //             get_layer_obj(data, LiquidTicks, pop_last=True)
    //         )
    //     )
    //
    // if 1444 <= DataVersion < 2844:
    //     LiquidsToBeTicked = (
    //         "region",
    //         [("Level", CompoundTag), ("LiquidsToBeTicked", ListTag)],
    //         ListTag,
    //     )
    //     chunk.misc["liquids_to_be_ticked"] = decode_to_be_ticked(
    //         get_layer_obj(data, LiquidsToBeTicked, pop_last=True), floor_cy
    //     )

    // PostProcessing TODO
    // if 1444 <= DataVersion:
    //     if 2844 <= DataVersion:
    //         PostProcessing = ("region", [("PostProcessing", ListTag)], ListTag)
    //     else:
    //         PostProcessing = (
    //             "region",
    //             [("Level", CompoundTag), ("PostProcessing", ListTag)],
    //             ListTag,
    //         )
    //     chunk.misc["post_processing"] = decode_to_be_ticked(
    //         get_layer_obj(data, PostProcessing, pop_last=True), floor_cy
    //     )

    // Biomes TODO
    // if 2836 <= DataVersion:
    //     biomes: dict[int, numpy.ndarray] = {}
    //     palette = BiomeManager()
    //
    //    for cy, section in _iter_sections():
    //        biomes = get_obj(section, "biomes", CompoundTag)
    //        if not (isinstance(biomes, CompoundTag) and "palette" in biomes):
    //            continue
    //        section_palette = [entry.py_data for entry in biomes.pop("palette")]
    //        assert section_palette, "Biome palette cannot be empty"
    //        data = biomes.pop("data", None)
    //        if data is None:
    //            # case 1: palette contains one value and data does not exist (undefined zero array)
    //            # TODO: in the new biome system just leave this as the number
    //            arr = numpy.zeros((4, 4, 4), numpy.uint32)
    //        else:
    //            # case 2: palette contains values and data is an index array
    //            arr = numpy.transpose(
    //                decode_long_array(
    //                    data.np_array,
    //                    4 ** 3,
    //                    max(1, (len(section_palette) - 1).bit_length()),
    //                    dense=LongArrayDense,
    //                )
    //                .astype(numpy.uint32)
    //                .reshape((4, 4, 4)),
    //                (2, 0, 1),
    //            )
    //        lut = numpy.array(
    //            [palette.get_add_biome(biome) for biome in section_palette]
    //        )
    //        biomes[cy] = lut[arr].astype(numpy.uint32)
    //
    //    chunk.biomes = biomes
    //    chunk.biome_palette = palette
    //
    // elif 2203 <= DataVersion:
    //     Biomes = (
    //         "region",
    //         [("Level", CompoundTag), ("Biomes", IntArrayTag)],
    //         None,
    //     )
    //     biomes = get_layer_obj(data, Biomes, pop_last=True)
    //     if isinstance(biomes, IntArrayTag):
    //         if (len(biomes) / 16) % 4:
    //             log.error(
    //                 f"The biome array size must be 4x4x4xN but got an array of size {biomes.np_array.size}"
    //             )
    //         else:
    //             arr = numpy.transpose(
    //                 biomes.np_array.astype(numpy.uint32).reshape((-1, 4, 4)),
    //                 (2, 0, 1),
    //             )  # YZX -> XYZ
    //             chunk.biomes = {
    //                 sy + floor_cy: arr
    //                 for sy, arr in enumerate(
    //                     numpy.split(
    //                         arr,
    //                         arr.shape[1] // 4,
    //                         1,
    //                     )
    //                 )
    //             }
    // else:
    //     if 1467 <= DataVersion:
    //         Biomes = (
    //             "region",
    //             [("Level", CompoundTag), ("Biomes", IntArrayTag)],
    //             None,
    //         )
    //     else:
    //         Biomes = (
    //             "region",
    //             [("Level", CompoundTag), ("Biomes", ByteArrayTag)],
    //             None,
    //         )
    //     biomes = get_layer_obj(data, Biomes, pop_last=True)
    //     if isinstance(biomes, AbstractBaseArrayTag) and biomes.np_array.size == 256:
    //         chunk.biomes = biomes.np_array.astype(numpy.uint32).reshape((16, 16))

    // isLightOn TODO
    // if 1934 <= DataVersion:
    //     if 2844 <= DataVersion:
    //         isLightOn = ("region", [("isLightOn", ByteTag)], ByteTag)
    //     else:
    //         isLightOn = ("region", [("Level", CompoundTag), ("isLightOn", ByteTag)], ByteTag)
    //     chunk.misc["isLightOn"] = get_layer_obj(data, isLightOn, pop_last=True)

    // lighting data TODO
    // def _unpack_light(
    //     section_key: str
    //) -> dict[int, numpy.ndarray]:
    //     light_container = {}
    //     for cy, section in _iter_sections():
    //         if self.check_type(section, section_key, ByteArrayTag):
    //             light: numpy.ndarray = section.pop(section_key).np_array
    //             if light.size == 2048:
    //                 # TODO: check if this needs transposing or if the values are the other way around
    //                 light_container[cy] = (
    //                     (
    //                         light.reshape(-1, 1)
    //                         & numpy.array([0xF, 0xF0], dtype=numpy.uint8)
    //                     )
    //                     >> numpy.array([0, 4], dtype=numpy.uint8)
    //                 ).reshape((16, 16, 16))
    //     return light_container
    //
    // chunk.misc["block_light"] = _unpack_light("BlockLight")
    // chunk.misc["sky_light"] = _unpack_light("SkyLight")

    // Heightmaps TODO
    // if 1466 <= DataVersion:
    //     if 2844 <= DataVersion:
    //         Heightmaps = ("region", [("Heightmaps", CompoundTag)], CompoundTag)
    //     else:
    //         Heightmaps = (
    //             "region",
    //             [("Level", CompoundTag), ("Heightmaps", CompoundTag)],
    //             CompoundTag,
    //         )
    //
    //    heights = get_layer_obj(data, Heightmaps, pop_last=True)
    //    chunk.misc["height_mapC"] = h = {}
    //    for key, value in heights.items():
    //        if isinstance(value, LongArrayTag):
    //            try:
    //                h[key] = decode_long_array(
    //                    value.np_array,
    //                    256,
    //                    (height_cy << 4).bit_length(),
    //                    dense=LongArrayDense,
    //                ).reshape((16, 16)) + (floor_cy << 4)
    //            except Exception as e:
    //                log.warning(e)
    // else:
    //    HeightMap = (
    //        "region",
    //        [("Level", CompoundTag), ("HeightMap", IntArrayTag)],
    //        IntArrayTag,
    //    )
    //    height = get_layer_obj(data, HeightMap, pop_last=True).np_array
    //    if isinstance(height, numpy.ndarray) and height.size == 256:
    //        chunk.misc["height_map256IA"] = height.reshape((16, 16))

    // Last Update TODO
    // pop_tag<LongTag>(level_tag, "LastUpdate", []() { return LongTag(); }).value;

    // Status TODO
    // if constexpr (1444 <= DataVersion) {
    //      std::string status = pop_tag<StringTag>(level_tag, "Status", []() { return StringTag(); });
    //      if (!status.empty()) {
    //              chunk.set_status(status);
    //      }
    //      else if constexpr (DataVersion >= 3454) {
    //              chunk.set_status("minecraft:full");
    //      }
    //      else if constexpr (DataVersion >= 1912) {
    //              chunk.set_status("full");
    //      }
    //      else {
    //              chunk.set_status("postprocessed");
    //      }
    // } else {
    //     status = "empty"
    //     pop_tag<ByteTag>(level_tag, "TerrainPopulated", []() { return ByteTag(1); }).value;
    //     if get_layer_obj(data, (
    //         "region",
    //         [("Level", CompoundTag), ("TerrainPopulated", ByteTag)],
    //         ByteTag,
    //     ), pop_last=True):
    //         status = "decorated"
    //     pop_tag<ByteTag>(level_tag, "LightPopulated", []() { return ByteTag(1); }).value;
    //     if get_layer_obj(data, (
    //         "region",
    //         [("Level", CompoundTag), ("LightPopulated", ByteTag)],
    //         ByteTag,
    //     ), pop_last=True):
    //         status = "postprocessed"
    //     chunk.status = status
    // }

    // Inhabited Time TODO
    // pop_tag<LongTag>(level_tag, "InhabitedTime", []() { return LongTag(); }).value;

    // Structures TODO
    // if constexpr (1444 <= DataVersion) {
    //    if constexpr (2844 <= DataVersion) {
    //        // Structures = ("region", [("structures", CompoundTag)], CompoundTag)
    //    } else {
    //        // Structures = (
    //        //     "region",
    //        //     [("Level", CompoundTag), ("Structures", CompoundTag)],
    //        //     CompoundTag,
    //        // )
    //    }
    //    // chunk.misc["structures"] = get_layer_obj(
    //    //     data, Structures, pop_last=True
    //    // )
    //}

    // Move all remaining chunk data into the chunk object.
    auto shared_raw_chunk = std::make_shared<JavaRawChunkType>();
    for (const auto& [k, v] : raw_chunk) {
        shared_raw_chunk->emplace(k, std::make_shared<NamedTag>(v));
    }
    chunk.set_raw_data(std::move(shared_raw_chunk));
}

// Get the default block for this dimension and version.
static BlockStack _get_default_block(
    JavaRawDimension& dimension,
    const VersionRange& version_range)
{
    std::vector<Block> blocks;
    for (const auto& block : dimension.get_default_block().get_blocks()) {
        if (version_range.contains(block.get_platform(), block.get_version())) {
            blocks.push_back(block);
        } else {
            auto converted = get_game_version(block.get_platform(), block.get_version())->get_block_data()->translate("java", version_range.get_max_version(), block);
            std::visit(
                [&blocks](auto&& arg) {
                    using T = std::decay_t<decltype(arg)>;
                    if constexpr (std::is_same_v<T, std::tuple<Block, std::optional<BlockEntity>, bool>>) {
                        blocks.emplace_back(std::get<0>(arg));
                    }
                },
                converted);
        }
    }
    if (blocks.empty()) {
        blocks.emplace_back(
            Block(
                version_range.get_platform(),
                version_range.get_max_version(),
                "minecraft",
                "air"));
    }
    return blocks;
}

static Biome _get_default_biome(
    JavaRawDimension& dimension,
    const VersionRange& version_range)
{
    auto& biome = dimension.get_default_biome();
    if (version_range.contains(biome.get_platform(), biome.get_version())) {
        return biome;
    } else {
        return get_game_version(biome.get_platform(), biome.get_version())->get_biome_data()->translate("java", version_range.get_max_version(), biome);
    }
}

std::unique_ptr<JavaChunk> JavaRawDimension::decode_chunk(
    JavaRawChunk raw_chunk,
    std::int64_t cx,
    std::int64_t cz)
{
    // Get the region compound tag
    CompoundTagPtr region_ptr = [&raw_chunk] {
        const auto& it = raw_chunk.find("region");
        if (it == raw_chunk.end()) {
            throw std::invalid_argument("This chunk does not have a 'region' entry.");
        }
        if (!std::holds_alternative<CompoundTagPtr>(it->second.tag_node)) {
            throw std::invalid_argument("'region' entry is not a CompoundTag.");
        }
        return std::get<CompoundTagPtr>(it->second.tag_node);
    }();
    CompoundTag& region = *region_ptr;

    // Extract the DataVersion
    std::int64_t data_version = pop_tag<IntTag>(
        region,
        "DataVersion",
        []() { return IntTag(-1); }).value;

    VersionNumber version(std::initializer_list<std::int64_t> { data_version });
    auto version_range = std::make_shared<VersionRange>("java", version, version);
    auto default_block = _get_default_block(*this, *version_range);
    auto default_biome = _get_default_biome(*this, *version_range);

    // Make and decode the chunk
    if (2203 <= data_version) {
        auto chunk = std::make_unique<JavaChunk2203>(
            data_version,
            default_block,
            default_biome);

        if (3463 <= data_version) {
            decode_java_chunk<3463>(*chunk, std::move(raw_chunk), region, cx, cz, version, data_version, default_block, default_biome);
            // Status values changed

        } else if (2844 <= data_version) {
            decode_java_chunk<2844>(*chunk, std::move(raw_chunk), region, cx, cz, version, data_version, default_block, default_biome);
            // Note that some of these changes happened in earlier snapshots
            // Chunk restructuring
            // Contents of Level tag moved into root
            // Some tags renamed from PascalCase to snake_case
            //
            // below_zero_retrogen
            //     added to support below zero generation
            // blending_data
            //     added to support blending new world generation with existing chunks
            // block_entities
            //     moved from Level.TileEntities
            // block_ticks
            //     moved from Level.TileTicks and Level.ToBeTicked
            // entities
            //     moved from Level.Entities
            // Heightmaps
            //     moved from Level.Heightmaps
            // InhabitedTime
            //     moved from Level.InhabitedTime
            // isLightOn
            //     moved from Level.isLightOn
            // fluid_ticks
            //     moved from Level.LiquidTicks and Level.LiquidsToBeTicked
            // LastUpdate
            //     moved from Level.LastUpdate
            // PostProcessing
            //     moved from Level.PostProcessing
            // sections
            //     moved from Level.Sections
            // sections[].biomes
            //     moved from Level.Sections[].biomes
            // sections[].block_states
            //     moved from Level.Sections[].block_states
            // Status
            //     moved from Level.Status
            // structures
            //     moved from Level.Structures
            // structures.starts
            //     moved from Level.Structures.Starts
            // xPos
            //     moved from Level.xPos
            // yPos
            //     Added to store the minimum y section in the chunk.
            // zPos
            //     moved from Level.zPos

        } else if (2836 <= data_version) {
            decode_java_chunk<2836>(*chunk, std::move(raw_chunk), region, cx, cz, version, data_version, default_block, default_biome);
            // Level.Sections[].biomes
            //     moved from Level.Biomes
            // Level.CarvingMasks[]
            //     is now long[] instead of byte[]
            // Level.Sections[].block_states
            //     moved from Level.Sections[].BlockStates & Level.Sections[].Palette

        } else if (2709 <= data_version) {
            decode_java_chunk<2709>(*chunk, std::move(raw_chunk), region, cx, cz, version, data_version, default_block, default_biome);
            // Made height bit depth variable to store increased heights
            // Made the biome array size variable to handle the increased height

        } else if (2681 <= data_version) {
            decode_java_chunk<2681>(*chunk, std::move(raw_chunk), region, cx, cz, version, data_version, default_block, default_biome);
            // Entities moved to a different storage layer

        } else if (2529 <= data_version) {
            decode_java_chunk<2529>(*chunk, std::move(raw_chunk), region, cx, cz, version, data_version, default_block, default_biome);
            // Packed long arrays switched to a less dense format
            // Before the long array was just a bit stream but it is now separate longs. The upper bits are unused in some cases.

        } else {
            decode_java_chunk<2203>(*chunk, std::move(raw_chunk), region, cx, cz, version, data_version, default_block, default_biome);
            // Made biomes 3D
        }
        return chunk;

    } else if (1466 <= data_version) {
        auto chunk = std::make_unique<JavaChunk1466>(
            data_version,
            default_block,
            default_biome);
        if (1934 <= data_version) {
            decode_java_chunk<1934>(*chunk, std::move(raw_chunk), region, cx, cz, version, data_version, default_block, default_biome);
            // isLightOn added
            // BlockLight and SkyLight are now optional
        } else if (1912 <= data_version) {
            decode_java_chunk<1912>(*chunk, std::move(raw_chunk), region, cx, cz, version, data_version, default_block, default_biome);
            // Status values changed

        } else if (1908 <= data_version) {
            decode_java_chunk<1908>(*chunk, std::move(raw_chunk), region, cx, cz, version, data_version, default_block, default_biome);
            // Changed height keys again again

        } else if (1901 <= data_version) {
            decode_java_chunk<1901>(*chunk, std::move(raw_chunk), region, cx, cz, version, data_version, default_block, default_biome);
            // Block data in a section is optional

        } else if (1519 <= data_version) {
            decode_java_chunk<1519>(*chunk, std::move(raw_chunk), region, cx, cz, version, data_version, default_block, default_biome);
            // All defined sub-chunks must have a block array

        } else if (1503 <= data_version) {
            decode_java_chunk<1503>(*chunk, std::move(raw_chunk), region, cx, cz, version, data_version, default_block, default_biome);
            // Changed height keys again

        } else if (1484 <= data_version) {
            decode_java_chunk<1484>(*chunk, std::move(raw_chunk), region, cx, cz, version, data_version, default_block, default_biome);
            // Changed height keys

        } else if (1467 <= data_version) {
            decode_java_chunk<1467>(*chunk, std::move(raw_chunk), region, cx, cz, version, data_version, default_block, default_biome);
            // Biomes now stored in an int array

        } else {
            decode_java_chunk<1466>(*chunk, std::move(raw_chunk), region, cx, cz, version, data_version, default_block, default_biome);
            // Added multiple height maps. Now stored in a compound.
        }
        return chunk;

    } else if (1444 <= data_version) {
        auto chunk = std::make_unique<JavaChunk1444>(
            data_version,
            default_block,
            default_biome);
        decode_java_chunk<1444>(*chunk, std::move(raw_chunk), region, cx, cz, version, data_version, default_block, default_biome);
        return chunk;
        // LiquidTicks added
        // LiquidsToBeTicked added
        // PostProcessing added
        // Status added
        //      This replaces TerrainPopulated and LightPopulated
        // Structures added
        // ToBeTicked added

    } else if (0 <= data_version) {
        auto chunk = std::make_unique<JavaChunk0>(
            data_version,
            default_block,
            default_biome);
        decode_java_chunk<0>(*chunk, std::move(raw_chunk), region, cx, cz, version, data_version, default_block, default_biome);
        return chunk;
        // Added the DataVersion tag

    } else {
        auto chunk = std::make_unique<JavaChunkNA>(
            default_block,
            default_biome);
        decode_java_chunk<-1>(*chunk, std::move(raw_chunk), region, cx, cz, version, data_version, default_block, default_biome);
        return chunk;
    }
}

} // namespace Amulet
