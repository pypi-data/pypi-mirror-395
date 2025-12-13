#include <map>
#include <memory>

#include <amulet/utils/bytes.hpp>

#include <amulet/nbt/nbt_encoding/binary.hpp>
#include <amulet/nbt/tag/copy.hpp>

#include "raw_chunk.hpp"

namespace Amulet {

BedrockRawChunk::BedrockRawChunk() = default;
BedrockRawChunk::BedrockRawChunk(
    std::map<Bytes, Bytes> data,
    std::vector<std::shared_ptr<NBT::NamedTag>> entity_actors)
    : _data(data)
    , _actors(entity_actors)
{
}

// Copy
BedrockRawChunk::BedrockRawChunk(const BedrockRawChunk& other)
    : _data(other._data)
    , _actors([&other] {
        std::vector<std::shared_ptr<NBT::NamedTag>> actors;
        for (const auto& actor : other._actors) {
            actors.emplace_back(NBT::deep_copy(actor));
        }
        return actors;
    }()) {};

BedrockRawChunk& BedrockRawChunk::operator=(const BedrockRawChunk& other)
{
    _data = other._data;
    _actors.clear();
    for (const auto& actor : other._actors) {
        _actors.emplace_back(NBT::deep_copy(actor));
    }
    return *this;
};

// Move
BedrockRawChunk::BedrockRawChunk(BedrockRawChunk&&) = default;
BedrockRawChunk& BedrockRawChunk::operator=(BedrockRawChunk&&) = default;

BedrockRawChunk::~BedrockRawChunk() = default;

void BedrockRawChunk::serialise(BaseBinaryWriter& writer) const
{
    // Version
    writer.write_numeric<std::uint8_t>(1);

    // Write data
    writer.write_numeric<std::uint64_t>(_data.size());
    for (const auto& [k, v] : _data) {
        writer.write_size_and_bytes(k);
        writer.write_size_and_bytes(v);
    }

    // Write actors
    writer.write_numeric<std::uint64_t>(_actors.size());
    for (const auto& actor : _actors) {
        NBT::encode_nbt(writer, *actor);
    }
}

BedrockRawChunk BedrockRawChunk::deserialise(BinaryReader& reader)
{
    auto version_number = reader.read_numeric<std::uint8_t>();
    switch (version_number) {
    case 1: {
        BedrockRawChunk chunk;

        // Read data
        auto data_count = reader.read_numeric<std::uint64_t>();
        for (std::uint64_t i = 0; i < data_count; i++) {
            auto k = reader.read_size_and_bytes();
            auto v = reader.read_size_and_bytes();
            chunk._data.emplace(std::move(k), std::move(v));
        }

        // Read actors
        auto actor_count = reader.read_numeric<std::uint64_t>();
        for (std::uint64_t i = 0; i < actor_count; i++) {
            chunk._actors.emplace_back(std::make_shared<NBT::NamedTag>(NBT::decode_nbt(reader)));
        }

        return chunk;
    }
    default:
        throw std::invalid_argument("Unsupported BedrockRawChunk version " + std::to_string(version_number));
    }
}

std::map<Bytes, Bytes>& BedrockRawChunk::get_data()
{
    return _data;
}

const std::map<Bytes, Bytes>& BedrockRawChunk::get_data() const
{
    return _data;
}

std::vector<std::shared_ptr<NBT::NamedTag>>& BedrockRawChunk::get_actors()
{
    return _actors;
}

const std::vector<std::shared_ptr<NBT::NamedTag>>& BedrockRawChunk::get_actors() const
{
    return _actors;
}

} // namespace Amulet
