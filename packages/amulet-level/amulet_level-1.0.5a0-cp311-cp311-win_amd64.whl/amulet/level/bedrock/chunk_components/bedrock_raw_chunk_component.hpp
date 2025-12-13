#pragma once

#include <cstdint>
#include <map>
#include <memory>
#include <optional>
#include <stdexcept>
#include <string>

#include <amulet/level/bedrock/raw_chunk.hpp>

#include <amulet/level/dll.hpp>

namespace Amulet {

class BedrockRawChunkComponent {
private:
    std::optional<std::shared_ptr<BedrockRawChunk>> _raw_data;

protected:
    // Null constructor
    BedrockRawChunkComponent() { }
    // Default constructor
    void init()
    {
        _raw_data = std::make_shared<BedrockRawChunk>();
    }
    // Argument constructor
    void init(std::shared_ptr<BedrockRawChunk> raw_data)
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
    std::shared_ptr<BedrockRawChunk> get_raw_data()
    {
        if (!_raw_data) {
            throw std::runtime_error("BedrockRawChunkComponent has not been loaded.");
        }
        return *_raw_data;
    }
    void set_raw_data(std::shared_ptr<BedrockRawChunk> raw_data)
    {
        if (!_raw_data) {
            throw std::runtime_error("BedrockRawChunkComponent has not been loaded.");
        }
        _raw_data = raw_data;
    }
};
}
