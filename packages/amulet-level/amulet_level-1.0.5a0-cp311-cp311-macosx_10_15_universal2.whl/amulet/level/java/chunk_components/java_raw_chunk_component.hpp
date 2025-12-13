#pragma once

#include <cstdint>
#include <map>
#include <memory>
#include <optional>
#include <stdexcept>
#include <string>

#include <amulet/nbt/tag/named_tag.hpp>

#include <amulet/level/dll.hpp>

namespace Amulet {
typedef std::map<std::string, std::shared_ptr<Amulet::NBT::NamedTag>> JavaRawChunkType;

class JavaRawChunkComponent {
private:
    std::optional<std::shared_ptr<JavaRawChunkType>> _raw_data;

protected:
    // Null constructor
    JavaRawChunkComponent() { }
    // Default constructor
    void init()
    {
        _raw_data = std::make_shared<JavaRawChunkType>();
    }
    // Argument constructor
    void init(std::shared_ptr<JavaRawChunkType> raw_data)
    {
        _raw_data = std::move(raw_data);
    }
    
    // Serialise the component data
    AMULET_LEVEL_EXPORT std::optional<std::string> serialise() const;
    // Deserialise the component
    AMULET_LEVEL_EXPORT void deserialise(std::optional<std::string>);

public:
    AMULET_LEVEL_EXPORT static const std::string ComponentID;

    // This is subject to change as data gets moved into the chunk class.
    // Do not rely on data in here existing.
    std::shared_ptr<JavaRawChunkType> get_raw_data()
    {
        if (!_raw_data) {
            throw std::runtime_error("JavaRawChunkComponent has not been loaded.");
        }
        return *_raw_data;
    }
    void set_raw_data(std::shared_ptr<JavaRawChunkType> raw_data)
    {
        if (!_raw_data) {
            throw std::runtime_error("JavaRawChunkComponent has not been loaded.");
        }
        _raw_data = raw_data;
    }
};
}
