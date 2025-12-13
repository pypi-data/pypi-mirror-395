#include <functional>
#include <limits>
#include <map>
#include <memory>
#include <stdexcept>
#include <string>

#include "chunk.hpp"

namespace Amulet {

const std::string BedrockChunk0::ChunkID = "Amulet::BedrockChunk0";
const std::string BedrockChunk1::ChunkID = "Amulet::BedrockChunk1";
const std::string BedrockChunk118::ChunkID = "Amulet::BedrockChunk118";

std::string BedrockChunk0::get_chunk_id() const { return ChunkID; }
std::string BedrockChunk1::get_chunk_id() const { return ChunkID; }
std::string BedrockChunk118::get_chunk_id() const { return ChunkID; }

BedrockChunk0::BedrockChunk0(
    const BlockStack& default_block,
    const Biome& default_biome)
    : ChunkComponentHelper()
{
    BedrockRawChunkComponent::init();
    BlockComponent::init(
        VersionRange(
            "bedrock",
            VersionNumber({ -1 }),
            VersionNumber({ -1 })),
        SectionShape(
            static_cast<std::uint16_t>(16),
            static_cast<std::uint16_t>(16),
            static_cast<std::uint16_t>(16)),
        default_block);
}

BedrockChunk1::BedrockChunk1(
    const BlockStack& default_block,
    const Biome& default_biome)
    : ChunkComponentHelper()
{
    BedrockRawChunkComponent::init();
    BlockComponent::init(
        VersionRange(
            "bedrock",
            VersionNumber({ -1 }),
            VersionNumber({ 4294967295 })),
        SectionShape(
            static_cast<std::uint16_t>(16),
            static_cast<std::uint16_t>(16),
            static_cast<std::uint16_t>(16)),
        default_block);
}

BedrockChunk118::BedrockChunk118(
    const BlockStack& default_block,
    const Biome& default_biome)
    : ChunkComponentHelper()
{
    BedrockRawChunkComponent::init();
    BlockComponent::init(
        VersionRange(
            "bedrock",
            VersionNumber({ -1 }),
            VersionNumber({ 4294967295 })),
        SectionShape(
            static_cast<std::uint16_t>(16),
            static_cast<std::uint16_t>(16),
            static_cast<std::uint16_t>(16)),
        default_block);
}

static const ChunkNullConstructor<BedrockChunk0> _bc0;
static const ChunkNullConstructor<BedrockChunk1> _bc1;
static const ChunkNullConstructor<BedrockChunk118> _bc118;

static std::map<std::string, std::function<std::unique_ptr<BedrockChunk>()>> bedrock_chunk_constructors = {
    { BedrockChunk0::ChunkID, []() { return std::make_unique<BedrockChunk0>(); } },
    { BedrockChunk1::ChunkID, []() { return std::make_unique<BedrockChunk1>(); } },
    { BedrockChunk118::ChunkID, []() { return std::make_unique<BedrockChunk118>(); } },
};

namespace detail {
    std::unique_ptr<BedrockChunk> get_bedrock_null_chunk(const std::string& chunk_id)
    {
        auto it = bedrock_chunk_constructors.find(chunk_id);
        if (it == bedrock_chunk_constructors.end()) {
            throw std::runtime_error("Unknown chunk_id " + chunk_id);
        }
        return it->second();
    }
    std::string get_bedrock_chunk_id(const BedrockChunk& chunk)
    {
        std::string chunk_id = chunk.get_chunk_id();
        if (!bedrock_chunk_constructors.contains(chunk_id)) {
            throw std::runtime_error("Unknown chunk_id " + chunk_id);
        }
        return chunk_id;
    }
} // namespace detail

} // namespace Amulet
