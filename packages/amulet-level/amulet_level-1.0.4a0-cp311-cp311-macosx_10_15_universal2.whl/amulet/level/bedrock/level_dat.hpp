#pragma once

#include <filesystem>
#include <memory>
#include <string>
#include <string_view>

#include <amulet/nbt/tag/named_tag.hpp>

#include <amulet/level/dll.hpp>

namespace Amulet {

class BedrockLevelDat {
private:
    std::uint32_t _version;
    std::shared_ptr<NBT::NamedTag> _named_tag;

public:
    AMULET_LEVEL_EXPORT BedrockLevelDat();

    // Construct with the level.dat version and named tag
    AMULET_LEVEL_EXPORT BedrockLevelDat(std::uint32_t version, std::shared_ptr<NBT::NamedTag> named_tag);
    AMULET_LEVEL_EXPORT BedrockLevelDat(std::uint32_t version, const NBT::NamedTag& named_tag);

    AMULET_LEVEL_EXPORT BedrockLevelDat(const BedrockLevelDat&);
    AMULET_LEVEL_EXPORT BedrockLevelDat(BedrockLevelDat&&);
    AMULET_LEVEL_EXPORT BedrockLevelDat& operator=(const BedrockLevelDat&);
    AMULET_LEVEL_EXPORT BedrockLevelDat& operator=(BedrockLevelDat&&);

    AMULET_LEVEL_EXPORT ~BedrockLevelDat();

    AMULET_LEVEL_EXPORT std::uint32_t get_version() const;
    AMULET_LEVEL_EXPORT void set_version(std::uint32_t);

    AMULET_LEVEL_EXPORT NBT::NamedTag& get_named_tag();
    AMULET_LEVEL_EXPORT const NBT::NamedTag& get_named_tag() const;
    AMULET_LEVEL_EXPORT std::shared_ptr<NBT::NamedTag> get_named_tag_ptr();
    
    AMULET_LEVEL_EXPORT void set_named_tag(std::shared_ptr<NBT::NamedTag>);
    AMULET_LEVEL_EXPORT void set_named_tag(const NBT::NamedTag&);

    // Construct from the binary data
    AMULET_LEVEL_EXPORT static BedrockLevelDat from_binary(std::string_view);

    // Construct from the give path.
    AMULET_LEVEL_EXPORT static BedrockLevelDat from_file(std::filesystem::path path);

    // Convert to binary.
    AMULET_LEVEL_EXPORT std::string to_binary() const;

    // Encode and write to the file.
    AMULET_LEVEL_EXPORT void save_to(std::filesystem::path path) const;

    AMULET_LEVEL_EXPORT BedrockLevelDat deep_copy() const;
};

} // namespace Amulet
