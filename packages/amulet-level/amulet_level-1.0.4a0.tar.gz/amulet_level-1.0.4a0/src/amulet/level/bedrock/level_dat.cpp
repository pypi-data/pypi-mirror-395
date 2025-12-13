#include <fstream>

#include <amulet/io/binary_reader.hpp>
#include <amulet/io/binary_writer.hpp>

#include <amulet/nbt/nbt_encoding/binary.hpp>
#include <amulet/nbt/string_encoding/string_encoding.hpp>
#include <amulet/nbt/tag/compound.hpp>
#include <amulet/nbt/tag/copy.hpp>

#include "level_dat.hpp"

namespace Amulet {

BedrockLevelDat::BedrockLevelDat()
    : _version()
    , _named_tag(std::make_shared<NBT::NamedTag>("", std::make_shared<NBT::CompoundTag>()))
{
}

BedrockLevelDat::BedrockLevelDat(std::uint32_t version, std::shared_ptr<NBT::NamedTag> named_tag)
    : _version(version)
    , _named_tag(std::move(named_tag))
{
}

BedrockLevelDat::BedrockLevelDat(std::uint32_t version, const NBT::NamedTag& named_tag)
    : _version(version)
    , _named_tag(std::make_shared<NBT::NamedTag>(named_tag))
{
}

BedrockLevelDat::BedrockLevelDat(const BedrockLevelDat&) = default;
BedrockLevelDat::BedrockLevelDat(BedrockLevelDat&&) = default;
BedrockLevelDat& BedrockLevelDat::operator=(const BedrockLevelDat&) = default;
BedrockLevelDat& BedrockLevelDat::operator=(BedrockLevelDat&&) = default;
BedrockLevelDat::~BedrockLevelDat() = default;

std::uint32_t BedrockLevelDat::get_version() const
{
    return _version;
}

void BedrockLevelDat::set_version(std::uint32_t version)
{
    _version = version;
}

NBT::NamedTag& BedrockLevelDat::get_named_tag()
{
    return *_named_tag;
}

const NBT::NamedTag& BedrockLevelDat::get_named_tag() const
{
    return *_named_tag;
}

std::shared_ptr<NBT::NamedTag> BedrockLevelDat::get_named_tag_ptr()
{
    return _named_tag;
}

void BedrockLevelDat::set_named_tag(std::shared_ptr<NBT::NamedTag> named_tag)
{
    _named_tag = named_tag;
}

void BedrockLevelDat::set_named_tag(const NBT::NamedTag& named_tag)
{
    _named_tag = std::make_shared<NBT::NamedTag>(named_tag);
}

// Construct from the binary data
BedrockLevelDat BedrockLevelDat::from_binary(std::string_view buffer)
{
    BinaryReader reader(buffer, 0, std::endian::little, NBT::utf8_to_utf8_escape);
    auto version = reader.read_numeric<std::uint32_t>();
    auto size = reader.read_numeric<std::uint32_t>();
    auto named_tag = NBT::decode_nbt(reader);

    return { version, named_tag };
}

// Construct from the give path.
BedrockLevelDat BedrockLevelDat::from_file(std::filesystem::path path)
{
    if (!std::filesystem::is_regular_file(path)) {
        throw std::invalid_argument(path.string() + " is not a file path.");
    }
    std::ifstream file(path, std::ios::binary);
    if (!file) {
        throw std::runtime_error("Failed to open file: " + path.string());
    }

    file.seekg(0, std::ios::end);
    size_t size = file.tellg();
    file.seekg(0, std::ios::beg);

    std::string buffer(size, 0);
    if (size) {
        file.read(buffer.data(), size);
    }

    return from_binary(buffer);
}

// Convert to binary.
std::string BedrockLevelDat::to_binary() const
{
    std::string buffer;
    BaseBinaryWriter writer(buffer, std::endian::little, NBT::utf8_escape_to_utf8);
    writer.write_numeric<std::uint32_t>(_version);
    writer.write_numeric<std::uint32_t>(0); // size
    NBT::encode_nbt(writer, *_named_tag);

    // Write the size to the end
    writer.write_numeric<std::uint32_t>(writer.get_buffer().size() - 8);
    // Copy it to the correct location
    std::memcpy(&buffer[4], &buffer[buffer.size() - 4], 4);
    // Crop off the end value
    buffer.resize(buffer.size() - 4);

    return buffer;
}

static void write_to_file(std::filesystem::path path, std::string_view buffer)
{
    std::ofstream file(path, std::ios::binary);
    if (!file) {
        throw std::runtime_error("Failed to open " + path.string());
    }

    file.write(buffer.data(), buffer.size());
    if (!file) {
        throw std::runtime_error("Failed to write to " + path.string());
    }
}

// Encode and write to the file.
void BedrockLevelDat::save_to(std::filesystem::path path) const
{
    auto buffer = to_binary();

    std::filesystem::path old_path = path;
    old_path += "_old";

    if (std::filesystem::exists(path)) {
        std::filesystem::rename(path, old_path);
    }

    try {
        write_to_file(path, buffer);
    } catch (...) {
        if (std::filesystem::exists(old_path)) {
            std::filesystem::rename(old_path, path);
        }
        throw;
    }
}

BedrockLevelDat BedrockLevelDat::deep_copy() const
{
    return BedrockLevelDat(_version, NBT::deep_copy(_named_tag));
}

} // namespace Amulet
