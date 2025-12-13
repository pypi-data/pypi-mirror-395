#include <cstdint>
#include <optional>

#include <amulet/io/binary_reader.hpp>
#include <amulet/io/binary_writer.hpp>

#include <amulet/level/dll.hpp>
#include <amulet/level/java/chunk_components/data_version_component.hpp>

namespace Amulet {
const std::string DataVersionComponent::ComponentID = "Amulet::DataVersionComponent";

std::optional<std::string> DataVersionComponent::serialise() const
{
    if (_data_version) {
        std::string buffer;
        TemplateBaseBinaryWriter<StaticLittleEndian, false> writer(buffer);
        writer.write_numeric<std::int64_t>(_data_version.value());
        return buffer;
    } else {
        return std::nullopt;
    }
}
void DataVersionComponent::deserialise(std::optional<std::string> data)
{
    if (data) {
        TemplateBinaryReader<StaticLittleEndian, false> reader(data.value());
        _data_version = reader.read_numeric<std::int64_t>();
    } else {
        _data_version = std::nullopt;
    }
}
}
