#pragma once

#include <map>

#include <amulet/io/binary_reader.hpp>
#include <amulet/io/binary_writer.hpp>

#include <amulet/nbt/tag/named_tag.hpp>

#include <amulet/utils/bytes.hpp>

#include <amulet/level/dll.hpp>

namespace Amulet {

class BedrockRawChunk {
private:
    // LevelDB keys and values (keys have the dimension and coord stripped)
    std::map<Bytes, Bytes> _data;
    std::vector<std::shared_ptr<NBT::NamedTag>> _actors;

public:
    // Constructors
    AMULET_LEVEL_EXPORT BedrockRawChunk();
    AMULET_LEVEL_EXPORT BedrockRawChunk(
        std::map<Bytes, Bytes>,
        std::vector<std::shared_ptr<NBT::NamedTag>>);

    // Copy
    AMULET_LEVEL_EXPORT BedrockRawChunk(const BedrockRawChunk&);
    AMULET_LEVEL_EXPORT BedrockRawChunk& operator=(const BedrockRawChunk&);

    // Move
    AMULET_LEVEL_EXPORT BedrockRawChunk(BedrockRawChunk&&);
    AMULET_LEVEL_EXPORT BedrockRawChunk& operator=(BedrockRawChunk&&);

    // Destructor
    AMULET_LEVEL_EXPORT ~BedrockRawChunk();

    AMULET_LEVEL_EXPORT void serialise(BaseBinaryWriter&) const;
    AMULET_LEVEL_EXPORT static BedrockRawChunk deserialise(BinaryReader&);

    AMULET_LEVEL_EXPORT std::map<Bytes, Bytes>& get_data();
    AMULET_LEVEL_EXPORT const std::map<Bytes, Bytes>& get_data() const;
    AMULET_LEVEL_EXPORT std::vector<std::shared_ptr<NBT::NamedTag>>& get_actors();
    AMULET_LEVEL_EXPORT const std::vector<std::shared_ptr<NBT::NamedTag>>& get_actors() const;
};

} // namespace Amulet
