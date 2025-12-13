#include <optional>
#include <stdexcept>

#include <amulet/io/binary_reader.hpp>
#include <amulet/io/binary_writer.hpp>

#include <amulet/nbt/nbt_encoding/binary.hpp>

#include <amulet/level/bedrock/chunk_components/bedrock_raw_chunk_component.hpp>
#include <amulet/level/dll.hpp>

namespace Amulet {
const std::string BedrockRawChunkComponent::ComponentID = "Amulet::BedrockRawChunkComponent";

std::optional<std::string> BedrockRawChunkComponent::serialise() const
{
    if (_raw_data) {
        std::string buffer;
        BaseBinaryWriter writer(buffer);
        (**_raw_data).serialise(writer);
        return buffer;
    } else {
        return std::nullopt;
    }
}

void BedrockRawChunkComponent::deserialise(std::optional<std::string> data)
{
    if (data) {
        _raw_data = std::make_shared<BedrockRawChunk>(
            Amulet::deserialise<BedrockRawChunk>(data.value()));
    } else {
        _raw_data = std::nullopt;
    }
}
}
