#include <optional>
#include <stdexcept>

#include <amulet/io/binary_reader.hpp>
#include <amulet/io/binary_writer.hpp>

#include <amulet/nbt/nbt_encoding/binary.hpp>

#include <amulet/level/dll.hpp>
#include <amulet/level/java/chunk_components/java_raw_chunk_component.hpp>

namespace Amulet {
const std::string JavaRawChunkComponent::ComponentID = "Amulet::JavaRawChunkComponent";

std::optional<std::string> JavaRawChunkComponent::serialise() const
{
    if (_raw_data) {
        std::string buffer;
        BaseBinaryWriter writer(buffer);
        writer.write_numeric<std::uint8_t>(1);
        const auto& raw_data = _raw_data.value();
        writer.write_numeric<std::uint64_t>(raw_data->size());
        for (const auto& [k, v] : *raw_data) {
            writer.write_size_and_bytes(k);
            Amulet::NBT::encode_nbt(writer, *v);
        }
        return buffer;
    } else {
        return std::nullopt;
    }
}
void JavaRawChunkComponent::deserialise(std::optional<std::string> data)
{
    if (data) {
        BinaryReader reader(data.value());
        auto version = reader.read_numeric<std::uint8_t>();
        switch (version) {
        case 1: {
            auto raw_data = std::make_shared<Amulet::JavaRawChunkType>();
            auto count = reader.read_numeric<std::uint64_t>();
            for (auto i = 0; i < count; i++) {
                auto key = reader.read_size_and_bytes();
                auto tag = std::make_shared<Amulet::NBT::NamedTag>(Amulet::NBT::decode_nbt(reader));
                raw_data->emplace(key, tag);
            }
            _raw_data = raw_data;
        } break;
        default:
            throw std::invalid_argument("Unsupported JavaRawChunkComponent version " + std::to_string(version));
        }
    } else {
        _raw_data = std::nullopt;
    }
}
}
