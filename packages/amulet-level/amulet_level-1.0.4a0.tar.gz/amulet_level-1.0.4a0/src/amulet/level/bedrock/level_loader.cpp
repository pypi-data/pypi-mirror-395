#include <memory>

#include <amulet/level/loader.hpp>

#include "level.hpp"

namespace Amulet {

static std::unique_ptr<Level> load_bedrock_level(const LevelLoaderToken& token)
{
    if (const LevelLoaderPathToken* path_token = dynamic_cast<const LevelLoaderPathToken*>(&token)) {
        return BedrockLevel::load(path_token->path);
    }
    throw std::runtime_error("token is not a path token.");
}

static LevelLoaderRegister bedrock_loader(std::make_shared<LevelLoader>("BedrockLevel", load_bedrock_level));

}
