#include <cstdint>
#include <map>
#include <memory>
#include <stdexcept>

#include <amulet/nbt/tag/array.hpp>
#include <amulet/nbt/tag/compound.hpp>
#include <amulet/nbt/tag/named_tag.hpp>

#include <amulet/core/chunk/chunk.hpp>

#include <amulet/game/game.hpp>
#include <amulet/game/java/version.hpp>

#include "chunk.hpp"
#include "long_array.hpp"
#include "raw_dimension.hpp"

using namespace Amulet::NBT;
using namespace Amulet::game;

namespace Amulet {

template <typename tagT>
tagT setdefault_tag(CompoundTag& compound, std::string name, std::function<tagT()> get_default)
{
    auto it = compound.find(name);
    if (it == compound.end() || !std::holds_alternative<tagT>(it->second)) {
        it = compound.insert_or_assign(name, get_default()).first;
    }
    return std::get<tagT>(it->second);
}

template <int DataVersion, typename ChunkT>
JavaRawChunk encode_java_chunk(
    ChunkT& chunk,
    std::int64_t cx,
    std::int64_t cz,
    std::int64_t min_y,
    std::int64_t max_y)
{
    // Extract the unhandled data from the chunk
    JavaRawChunk raw_chunk;
    for (auto& [k, v] : *chunk.get_raw_data()) {
        raw_chunk.emplace(std::move(k), std::move(*v));
    }

    // Populate the region tag
    CompoundTag& region_tag = [&raw_chunk]() -> CompoundTag& {
        auto it = raw_chunk.find("region");
        if (it == raw_chunk.end()) {
            it = raw_chunk.emplace("region", NamedTag("", std::make_shared<CompoundTag>())).first;
        } else {
            auto& region_named_tag = it->second;
            region_named_tag.name = "";
            auto& node = region_named_tag.tag_node;
            if (!std::holds_alternative<CompoundTagPtr>(node)) {
                node = std::make_shared<CompoundTag>();
            }
        }
        return *std::get<CompoundTagPtr>(it->second.tag_node);
    }();

    // Populate the Level tag.
    // In newer versions this is just the root tag.
    CompoundTag& level_tag = [&region_tag]() -> CompoundTag& {
        if constexpr (DataVersion >= 2844) {
            return region_tag;
        } else {
            return *setdefault_tag<CompoundTagPtr>(
                region_tag,
                "Level",
                []() { return std::make_shared<CompoundTag>(); });
        }
    }();

    auto floor_cy = min_y >> 4;
    auto ceil_cy = max_y >> 4;
    auto height_cy = ceil_cy - floor_cy;

    // LongArrayDense = DataVersion < 2529

    // Version tag
    if constexpr (0 <= DataVersion) {
        region_tag.insert_or_assign(
            "DataVersion",
            IntTag(static_cast<std::int32_t>(chunk.get_data_version())));
    } else {
        // TODO: Pull this from the chunk
        level_tag.insert_or_assign("V", ByteTag(1));
    }

    // # Coords
    level_tag.insert_or_assign("xPos", IntTag(static_cast<std::int32_t>(cx)));
    level_tag.insert_or_assign("zPos", IntTag(static_cast<std::int32_t>(cz)));
    if constexpr (2844 <= DataVersion) {
        level_tag.insert_or_assign("yPos", IntTag(static_cast<std::int32_t>(floor_cy)));
    }

    // Extract sections tag into a more usable format.
    std::map<std::int64_t, CompoundTagPtr> sections_map;
    {
        // Extract sections tag from unhandled data.
        auto sections_node = [&level_tag]() {
            if constexpr (2844 <= DataVersion) {
                return level_tag.extract("sections");
            } else {
                return level_tag.extract("Sections");
            }
        }();
        if (sections_node && std::holds_alternative<ListTagPtr>(sections_node.mapped())) {
            auto& sections_tag = *std::get<ListTagPtr>(sections_node.mapped());
            if (std::holds_alternative<CompoundListTag>(sections_tag)) {
                auto& compound_sections_tag = std::get<CompoundListTag>(sections_tag);
                for (auto& section_tag : compound_sections_tag) {
                    auto y_it = section_tag->find("Y");
                    if (y_it != section_tag->end() && std::holds_alternative<ByteTag>(y_it->second)) {
                        auto cy = std::get<ByteTag>(y_it->second).value;
                        sections_map.insert_or_assign(cy, section_tag);
                    }
                }
            }
        }
    }

    auto get_section = [&sections_map](std::int64_t cy) -> CompoundTag& {
        if (!(-127 <= cy && cy < 128)) {
            throw std::runtime_error("Section " + std::to_string(cy) + " is out of bounds. It must be between -127 and 128.");
        }
        const auto& it = sections_map.find(cy);
        if (it == sections_map.end()) {
            auto& section_tag = *sections_map.emplace(cy, std::make_shared<CompoundTag>()).first->second;
            section_tag.emplace("Y", ByteTag(static_cast<std::int8_t>(cy)));
            return section_tag;
        } else {
            return *it->second;
        }
    };

    std::shared_ptr<JavaGameVersion> game_version = get_java_game_version(VersionNumber({ chunk.get_data_version() }));

    // Encode block data
    {
        auto block_component = chunk.get_block_storage_ptr();
        auto& block_palette = block_component->get_palette();
        auto& block_sections = block_component->get_sections();
        auto version_block_data = game_version->get_block_data();
        for (auto& [cy, block_array_ptr] : block_sections.get_arrays()) {
            if (!(floor_cy <= cy && cy < ceil_cy)) {
                continue;
            }
            if constexpr (1444 <= DataVersion) {
                if (block_array_ptr->get_shape() != SectionShape(16, 16, 16)) {
                    throw std::runtime_error("Unsupported sub-chunk shape.");
                }
                auto block_array = block_array_ptr->get_span();

                // create a lut from chunk palette index to encoded palette index
                std::map<size_t, std::uint16_t> lut;
                for (size_t index = 0; index < 4096; index++) {
                    lut.emplace(
                        block_array[index],
                        static_cast<std::uint16_t>(lut.size()));
                }

                // Pack waterlogging. Some states may encode to the same state.
                std::list<Block> encoded_blocks;
                std::map<Block, std::uint16_t> encoded_block_to_index;
                for (auto& [src_index, dst_index] : lut) {
                    auto block = [&]() -> Block {
                        auto& block_stack = block_palette.index_to_block_stack(src_index);
                        auto& base_block = block_stack.at(0);
                        switch (version_block_data->is_waterloggable(
                            base_block.get_namespace(),
                            base_block.get_base_name())) {
                        case Waterloggable::Yes: {
                            auto properties = base_block.get_properties();
                            if (1 < block_stack.size()) {
                                // Has an extra block
                                auto& extra_block = block_stack.at(1);
                                if (
                                    extra_block.get_namespace() == "minecraft"
                                    && extra_block.get_base_name() == "water") {
                                    properties.insert_or_assign("waterlogged", StringTag("true"));
                                } else {
                                    properties.insert_or_assign("waterlogged", StringTag("false"));
                                }
                            }
                            return Block(
                                base_block.get_platform(),
                                base_block.get_version(),
                                base_block.get_namespace(),
                                base_block.get_base_name(),
                                std::move(properties));
                        }
                        default:
                            return base_block;
                        }
                    }();
                    encoded_blocks.emplace_back(block);
                    dst_index = encoded_block_to_index
                                    .emplace(
                                        block,
                                        static_cast<std::uint16_t>(encoded_block_to_index.size()))
                                    .first->second;
                }

                if constexpr (DataVersion < 2844) {
                    if (encoded_blocks.size() == 1
                        && encoded_blocks.front().get_namespace() == "minecraft"
                        && encoded_blocks.front().get_base_name() == "air") {
                        // Skip saving the blocks if it only contains air.
                        // TODO: Do we need to save this in 2844+?
                        // TODO: What if the default block is not air?
                        continue;
                    }
                }

                // Encode the palette
                CompoundListTag block_tags;
                block_tags.reserve(encoded_blocks.size());
                for (const auto& block : encoded_blocks) {
                    auto properties = std::make_shared<CompoundTag>();
                    for (const auto& [k, v] : block.get_properties()) {
                        if (std::holds_alternative<StringTag>(v)) {
                            properties->emplace(k, std::get<StringTag>(v));
                        }
                    }
                    auto block_tag = std::make_shared<CompoundTag>();
                    block_tag->emplace("Name", StringTag(block.get_namespace() + ":" + block.get_base_name()));
                    if (!properties->empty()) {
                        block_tag->emplace("Properties", std::move(properties));
                    }
                    block_tags.emplace_back(std::move(block_tag));
                }

                auto encode_block_array = [&block_array, &lut, &block_tags]() -> LongArrayTagPtr {
                    // Convert and pack the array
                    std::vector<std::uint16_t> converted_block_array;
                    converted_block_array.reserve(4096);
                    for (size_t y = 0; y < 16; y++) {
                        for (size_t z = 0; z < 16; z++) {
                            for (size_t x = 0; x < 16; x++) {
                                converted_block_array.emplace_back(
                                    lut.at(block_array[x * 256 + y * 16 + z]));
                            }
                        }
                    }
                    auto bits_per_entry = std::max<std::uint8_t>(4, std::bit_width(block_tags.size() - 1));
                    bool dense = DataVersion < 2529;
                    auto packed_array = std::make_shared<LongArrayTag>(encoded_long_array_size(4096, bits_per_entry, dense));
                    std::span<std::uint64_t> packed_span(reinterpret_cast<std::uint64_t*>(packed_array->data()), packed_array->size());
                    encode_long_array<std::uint16_t>(
                        converted_block_array,
                        packed_span,
                        bits_per_entry,
                        dense);
                    return packed_array;
                };

                auto& section = get_section(cy);

                if constexpr (2844 <= DataVersion) {
                    auto block_states_tag = std::make_shared<CompoundTag>();
                    if (1 < block_tags.size()) {
                        block_states_tag->emplace("data", encode_block_array());
                    }
                    block_states_tag->emplace("palette", std::make_shared<ListTag>(std::move(block_tags)));
                    section.insert_or_assign("block_states", std::move(block_states_tag));
                } else {
                    section.insert_or_assign("Palette", std::make_shared<ListTag>(std::move(block_tags)));
                    section.insert_or_assign("BlockStates", encode_block_array());
                }
            } else {
                throw std::runtime_error("NotImplementedError");
                //            block_sub_array = palette[
                //                numpy.transpose(
                //                    chunk.blocks.get_sub_chunk(cy), (1, 2, 0)
                //                ).ravel()  # XYZ -> YZX
                //            ]

                //            data_sub_array = block_sub_array[:, 1]
                //            block_sub_array = block_sub_array[:, 0]
                //            # if not numpy.any(block_sub_array) and not numpy.any(data_sub_array):
                //            #     return False
                //            sections[cy]["Blocks"] = ByteArrayTag(block_sub_array.astype("uint8"))
                //            sections[cy]["Data"] = ByteArrayTag(world_utils.to_nibble_array(data_sub_array))
            }
        }
    }

    // if 2844 <= DataVersion:
    //     BlockEntities = ("region", [("block_entities", ListTag)], ListTag)
    // else:
    //     BlockEntities = (
    //         "region",
    //         [("Level", CompoundTag), ("TileEntities", ListTag)],
    //         ListTag,
    //     )
    // encoded_block_entities = []
    // for entity in chunk.block_entities:
    //     nbt = self._encode_block_entity(
    //         entity,
    //         EntityIDType.namespace_str_id,
    //         EntityCoordType.xyz_int,
    //     )
    //     if nbt is not None:
    //         encoded_block_entities.append(nbt.compound)
    // set_layer_obj(
    //     data,
    //     BlockEntities,
    //     ListTag(encoded_block_entities)
    //)

    // if amulet.entity_support:
    //     entities = chunk.entities
    // else:
    //     entities = chunk._native_entities

    // def _encode_entity_list(entities: Iterable["Entity"]) -> ListTag:
    //     entities_out = []
    //     for entity in entities:
    //         nbt = self._encode_entity(
    //             entity,
    //             EntityIDType.namespace_str_id,
    //             EntityCoordType.Pos_list_double,
    //         )
    //         if nbt is not None:
    //             entities_out.append(nbt.compound)

    //    return ListTag(entities_out)

    // encoded_entities = _encode_entity_list(entities)
    // if 2681 <= DataVersion:
    //     # TODO: it is possible the entity data version does not match the chunk data version
    //     Entities = (
    //         "entities",
    //         [("Entities", ListTag)],
    //         ListTag,
    //     )
    //     EntitiesDataVersion = (
    //         "entities",
    //         [("DataVersion", IntTag)],
    //         IntTag,
    //     )

    //    try:
    //        platform, version = chunk._native_version
    //    except:
    //        data.pop(EntitiesDataVersion[0], None)
    //    else:
    //        if platform == "java" and isinstance(version, int):
    //            set_layer_obj(
    //                data,
    //                Entities,
    //                encoded_entities,
    //            )
    //            set_layer_obj(data, EntitiesDataVersion, IntTag(version))
    //        else:
    //            data.pop(EntitiesDataVersion[0], None)
    // else:
    //    Entities = (
    //        "region",
    //        [("Level", CompoundTag), ("Entities", ListTag)],
    //        ListTag,
    //    )
    //    set_layer_obj(
    //        data,
    //        Entities,
    //        encoded_entities,
    //    )

    // if 2844 <= DataVersion:
    //     BlockTicks = ("region", [("block_ticks", ListTag)], ListTag)
    // else:
    //     BlockTicks = (
    //         "region",
    //         [("Level", CompoundTag), ("TileTicks", ListTag)],
    //         ListTag,
    //     )
    // set_layer_obj(
    //     data, BlockTicks, _encode_ticks(chunk.misc.get("block_ticks", {}))
    //)

    // if 1444 <= DataVersion < 2844:
    //     ToBeTicked = (
    //         "region",
    //         [("Level", CompoundTag), ("ToBeTicked", ListTag)],
    //         ListTag,
    //     )
    //     set_layer_obj(
    //         data,
    //         ToBeTicked,
    //         _encode_to_be_ticked(
    //             chunk.misc.get("to_be_ticked"), floor_cy, height_cy
    //         ),
    //     )

    // if 1444 <= DataVersion:
    //     if 2844 <= DataVersion:
    //         LiquidTicks = ("region", [("fluid_ticks", ListTag)], ListTag)
    //     else:
    //         LiquidTicks = (
    //             "region",
    //             [("Level", CompoundTag), ("LiquidTicks", ListTag)],
    //             ListTag,
    //         )
    //     set_layer_obj(
    //         data,
    //         LiquidTicks,
    //         _encode_ticks(chunk.misc.get("fluid_ticks", {})),
    //     )

    // if 1444 <= DataVersion < 2844:
    //     LiquidsToBeTicked = (
    //         "region",
    //         [("Level", CompoundTag), ("LiquidsToBeTicked", ListTag)],
    //         ListTag,
    //     )
    //     set_layer_obj(
    //         data,
    //         LiquidsToBeTicked,
    //         _encode_to_be_ticked(
    //             chunk.misc.get("liquids_to_be_ticked"), floor_cy, height_cy
    //         ),
    //     )

    // if 1444 <= DataVersion:
    //     if 2844 <= DataVersion:
    //         PostProcessing = ("region", [("PostProcessing", ListTag)], ListTag)
    //     else:
    //         PostProcessing = (
    //             "region",
    //             [("Level", CompoundTag), ("PostProcessing", ListTag)],
    //             ListTag,
    //         )
    //     set_layer_obj(
    //         data,
    //         PostProcessing,
    //         _encode_to_be_ticked(
    //             chunk.misc.get("post_processing"), floor_cy, height_cy
    //         ),
    //     )

    // if 2844 <= DataVersion:
    //     chunk.biomes.convert_to_3d()
    //     for cy in chunk.biomes.sections:
    //         if floor_cy <= cy < ceil_cy:
    //             biome_sub_array = numpy.transpose(
    //                 chunk.biomes.get_section_ptr(cy), (1, 2, 0)
    //             ).ravel()

    //            sub_palette_, biome_sub_array = numpy.unique(
    //                biome_sub_array, return_inverse=True
    //            )
    //            sub_palette = ListTag([StringTag(entry) for entry in chunk.biome_palette[sub_palette_]])
    //            biomes = sections[cy]["biomes"] = CompoundTag({"palette": sub_palette})
    //            if len(sub_palette) != 1:
    //                biomes["data"] = LongArrayTag(
    //                    encode_long_array(biome_sub_array, dense=LongArrayDense)
    //                )

    // elif 2203 <= DataVersion:
    //     Biomes = (
    //         "region",
    //         [("Level", CompoundTag), ("Biomes", IntArrayTag)],
    //         None,
    //     )
    //     if chunk.status.value > -0.7:
    //         chunk.biomes.convert_to_3d()
    //         set_layer_obj(
    //             data,
    //             Biomes,
    //             IntArrayTag(
    //                 numpy.transpose(
    //                     numpy.asarray(
    //                         chunk.biomes[
    //                             :, floor_cy * 4 : ceil_cy * 4, :
    //                         ]
    //                     ).astype(numpy.uint32),
    //                     (1, 2, 0),
    //                 ).ravel()  # YZX -> XYZ
    //             ),
    //         )
    // elif 1467 <= DataVersion:
    //     Biomes = (
    //         "region",
    //         [("Level", CompoundTag), ("Biomes", IntArrayTag)],
    //         None,
    //     )
    //     if chunk.status.value > -0.7:
    //         chunk.biomes.convert_to_2d()
    //         set_layer_obj(
    //             data,
    //             Biomes,
    //             IntArrayTag(chunk.biomes.astype(dtype=numpy.uint32).ravel()),
    //         )
    // else:
    //     Biomes = (
    //         "region",
    //         [("Level", CompoundTag), ("Biomes", ByteArrayTag)],
    //         None,
    //     )
    //     chunk.biomes.convert_to_2d()
    //     set_layer_obj(
    //         data,
    //         Biomes,
    //         ByteArrayTag(chunk.biomes.astype(dtype=numpy.uint8).ravel()),
    //     )

    // if 1934 <= DataVersion:
    //     if 2844 <= DataVersion:
    //         isLightOn = ("region", [("isLightOn", ByteTag)], ByteTag)
    //     else:
    //         isLightOn = ("region", [("Level", CompoundTag), ("isLightOn", ByteTag)], ByteTag)
    //     is_light_on = bool(chunk.misc.pop("isLightOn", None))
    //     set_layer_obj(data, isLightOn, ByteTag(is_light_on))

    // def _pack_light(
    //     feature_key: str,
    //     section_key: str,
    //):
    //     light_container = chunk.misc.get(feature_key, {})
    //     if not isinstance(light_container, dict):
    //         light_container = {}
    //     for cy, section in sections.items():
    //         light = light_container.get(cy, None)
    //         if (
    //             isinstance(light, numpy.ndarray)
    //             and numpy.issubdtype(light.dtype, numpy.integer)
    //             and light.shape == (16, 16, 16)
    //         ):
    //             light = light.ravel() % 16
    //             section[section_key] = ByteArrayTag(light[::2] + (light[1::2] << 4))
    //         elif DataVersion < 1934:
    //             # light is optional after 1934
    //             section[section_key] = ByteArrayTag(
    //                 numpy.full(2048, 255, dtype=numpy.uint8)
    //             )

    //_pack_light("block_light", "BlockLight")
    //_pack_light("sky_light", "SkyLight")

    // if 1466 <= DataVersion:
    //     if 2844 <= DataVersion:
    //         Heightmaps = ("region", [("Heightmaps", CompoundTag)], CompoundTag)
    //     else:
    //         Heightmaps = (
    //             "region",
    //             [("Level", CompoundTag), ("Heightmaps", CompoundTag)],
    //             CompoundTag,
    //         )
    //     maps = [
    //         "WORLD_SURFACE_WG",
    //         "OCEAN_FLOOR_WG",
    //         "MOTION_BLOCKING",
    //         "MOTION_BLOCKING_NO_LEAVES",
    //         "OCEAN_FLOOR",
    //     ]
    //     if 1908 <= DataVersion:
    //         maps.append("WORLD_SURFACE")
    //     elif 1503 <= DataVersion:
    //         maps.append("LIGHT_BLOCKING")
    //         maps.append("WORLD_SURFACE")
    //     elif 1484 <= DataVersion:
    //         maps.append("LIGHT_BLOCKING")
    //     else:
    //         maps = ("LIQUID", "SOLID", "LIGHT", "RAIN")
    //     heightmaps_temp: dict[str, numpy.ndarray] = chunk.misc.get("height_mapC", {})
    //     heightmaps = CompoundTag()
    //     for heightmap in maps:
    //         if (
    //                 heightmap in heightmaps_temp
    //                 and isinstance(heightmaps_temp[heightmap], numpy.ndarray)
    //                 and heightmaps_temp[heightmap].size == 256
    //         ):
    //             heightmaps[heightmap] = LongArrayTag(
    //                 encode_long_array(
    //                     heightmaps_temp[heightmap].ravel() - (floor_cy << 4),
    //                     (height_cy << 4).bit_length(),
    //                     LongArrayDense,
    //                 )
    //             )
    //     set_layer_obj(data, Heightmaps, heightmaps)
    // else:
    //     HeightMap = (
    //         "region",
    //         [("Level", CompoundTag), ("HeightMap", IntArrayTag)],
    //         IntArrayTag,
    //     )
    //     height = chunk.misc.get("height_map256IA", None)
    //     if (
    //         isinstance(height, numpy.ndarray)
    //         and numpy.issubdtype(height.dtype, numpy.integer)
    //         and height.shape == (16, 16)
    //     ):
    //         set_layer_obj(
    //             data,
    //             HeightMap,
    //             IntArrayTag(numpy.zeros(256, dtype=numpy.uint32)),
    //         )
    //     elif self._features["height_map"] == "256IARequired":
    //         set_layer_obj(data, HeightMap, IntArrayTag(height.ravel()))

    // if 2844 <= DataVersion:
    //     LastUpdate = ("region", [("LastUpdate", LongTag)], LongTag)
    // else:
    //     LastUpdate = (
    //         "region",
    //         [("Level", CompoundTag), ("LastUpdate", LongTag)],
    //         LongTag,
    //     )
    // set_layer_obj(
    //     data, LastUpdate, LongTag(chunk.misc.get("last_update", 0))
    //)

    // if 1444 <= DataVersion:
    //     if 2844 <= DataVersion:
    //         Status = ("region", [("Status", StringTag)], StringTag("full"))
    //     else:
    //         Status = (
    //             "region",
    //             [("Level", CompoundTag), ("Status", StringTag)],
    //             StringTag("full"),
    //         )
    //     # Order the float value based on the order they would be run. Newer replacements for the same come just after
    //     # to save back find the next lowest valid value.
    //     status = chunk.status.as_type(self._features["status"])
    //     set_layer_obj(data, Status, StringTag(status))
    // else:
    //     LightPopulated = (
    //         "region",
    //         [("Level", CompoundTag), ("LightPopulated", ByteTag)],
    //         ByteTag,
    //     )
    //     TerrainPopulated = (
    //         "region",
    //         [("Level", CompoundTag), ("TerrainPopulated", ByteTag)],
    //         ByteTag,
    //     )
    //     status = chunk.status.as_type(StatusFormats.Raw)
    //     set_layer_obj(data, TerrainPopulated, ByteTag(int(status > -0.3)))
    //     set_layer_obj(data, LightPopulated, ByteTag(int(status > -0.2)))

    // if 2844 <= DataVersion:
    //     InhabitedTime = ("region", [("InhabitedTime", LongTag)], LongTag)
    // else:
    //     InhabitedTime = (
    //         "region",
    //         [("Level", CompoundTag), ("InhabitedTime", LongTag)],
    //         LongTag,
    //     )
    // set_layer_obj(
    //     data, InhabitedTime, LongTag(chunk.misc.get("inhabited_time", 0))
    //)

    // if 1444 <= DataVersion:
    //     if 2844 <= DataVersion:
    //         Structures = ("region", [("structures", CompoundTag)], CompoundTag)
    //     else:
    //         Structures = (
    //             "region",
    //             [("Level", CompoundTag), ("Structures", CompoundTag)],
    //             CompoundTag,
    //         )
    //     set_layer_obj(
    //         data,
    //         Structures,
    //         chunk.misc.get(
    //             "structures",
    //             CompoundTag(
    //                 {
    //                     "References": CompoundTag(),
    //                     "Starts": CompoundTag(),
    //                 }
    //             ),
    //         ),
    //     )

    // # TODO: What is going on here?
    // #  This is implemented incorrectly
    // if DataVersion < 1901:
    //     Sections = (
    //         "region",
    //         [("Level", CompoundTag), ("Sections", ListTag)],
    //         ListTag,
    //     )
    //     if 1519 <= DataVersion:
    //         sections = get_layer_obj(data, Sections)
    //         for section_index in range(len(sections) - 1, -1, -1):
    //             if (
    //                     "BlockStates" not in sections[section_index]
    //                     or "Palette" not in sections[section_index]
    //             ):
    //                 del sections[section_index]
    //     else:
    //         # Strip out all empty sections
    //         sections = get_layer_obj(data, Sections)
    //         if sections:
    //             for i in range(len(sections) - 1, -1, -1):
    //                 section = sections[i]
    //                 if "Blocks" not in section or "Data" not in section:
    //                     # in 1.12 if a section exists, Blocks and Data must exist
    //                     sections.pop(i)
    //         if not sections:
    //             # if no sections remain we can remove the sections data
    //             get_layer_obj(data, Sections, pop_last=True)

    // if 2844 <= DataVersion:
    //     OldLevel = ("region", [("Level", CompoundTag)], CompoundTag)
    //     get_layer_obj(data, OldLevel, pop_last=True)

    // Pack sections tag back into the data
    {
        CompoundListTag sections_tag;
        sections_tag.reserve(sections_map.size());
        for (auto& [_, section_tag] : sections_map) {
            sections_tag.emplace_back(std::move(section_tag));
        }
        if constexpr (2844 <= DataVersion) {
            level_tag.insert_or_assign(
                "sections",
                std::make_shared<ListTag>(std::move(sections_tag)));
        } else {
            level_tag.insert_or_assign(
                "Sections",
                std::make_shared<ListTag>(std::move(sections_tag)));
        }
    }

    return raw_chunk;
}

JavaRawChunk JavaRawDimension::encode_chunk(
    JavaChunk& chunk,
    std::int64_t cx,
    std::int64_t cz)
{
    auto min_y = get_bounds().min_y();
    auto max_y = get_bounds().max_y();

    // See the decoder for version documentation.
    if (auto* chunk_ = dynamic_cast<JavaChunk2203*>(&chunk)) {
        auto data_version = chunk_->get_data_version();
        if (3463 <= data_version) {
            return encode_java_chunk<3463>(*chunk_, cx, cz, min_y, max_y);
        } else if (2844 <= data_version) {
            return encode_java_chunk<2844>(*chunk_, cx, cz, min_y, max_y);
        } else if (2836 <= data_version) {
            return encode_java_chunk<2836>(*chunk_, cx, cz, min_y, max_y);
        } else if (2709 <= data_version) {
            return encode_java_chunk<2709>(*chunk_, cx, cz, min_y, max_y);
        } else if (2681 <= data_version) {
            return encode_java_chunk<2681>(*chunk_, cx, cz, min_y, max_y);
        } else if (2529 <= data_version) {
            return encode_java_chunk<2529>(*chunk_, cx, cz, min_y, max_y);
        } else {
            return encode_java_chunk<2203>(*chunk_, cx, cz, min_y, max_y);
        }
    } else if (auto* chunk_ = dynamic_cast<JavaChunk1466*>(&chunk)) {
        auto data_version = chunk_->get_data_version();
        if (1934 <= data_version) {
            return encode_java_chunk<1934>(*chunk_, cx, cz, min_y, max_y);
        } else if (1912 <= data_version) {
            return encode_java_chunk<1912>(*chunk_, cx, cz, min_y, max_y);
        } else if (1908 <= data_version) {
            return encode_java_chunk<1908>(*chunk_, cx, cz, min_y, max_y);
        } else if (1901 <= data_version) {
            return encode_java_chunk<1901>(*chunk_, cx, cz, min_y, max_y);
        } else if (1519 <= data_version) {
            return encode_java_chunk<1519>(*chunk_, cx, cz, min_y, max_y);
        } else if (1503 <= data_version) {
            return encode_java_chunk<1503>(*chunk_, cx, cz, min_y, max_y);
        } else if (1484 <= data_version) {
            return encode_java_chunk<1484>(*chunk_, cx, cz, min_y, max_y);
        } else if (1467 <= data_version) {
            return encode_java_chunk<1467>(*chunk_, cx, cz, min_y, max_y);
        } else {
            return encode_java_chunk<1466>(*chunk_, cx, cz, min_y, max_y);
        }
    } else if (auto* chunk_ = dynamic_cast<JavaChunk1444*>(&chunk)) {
        return encode_java_chunk<1444>(*chunk_, cx, cz, min_y, max_y);
    } else if (auto* chunk_ = dynamic_cast<JavaChunk0*>(&chunk)) {
        return encode_java_chunk<0>(*chunk_, cx, cz, min_y, max_y);
    } else if (auto* chunk_ = dynamic_cast<JavaChunkNA*>(&chunk)) {
        return encode_java_chunk<-1>(*chunk_, cx, cz, min_y, max_y);
    } else {
        throw std::invalid_argument("Unsupported Java chunk class: " + chunk.get_chunk_id());
    }
}

} // namespace Amulet
