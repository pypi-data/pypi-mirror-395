#include <pybind11/pybind11.h>

// #include <amulet/core/biome/biome.hpp>
// #include <amulet/core/block/block.hpp>
// #include <amulet/core/chunk/chunk.hpp>
// #include <amulet/core/chunk/component/block_component.hpp>

// #include "chunk_components/bedrock_raw_chunk_component.hpp"
#include "chunk.hpp"

namespace py = pybind11;

void init_bedrock_chunk(py::module m_parent)
{
    auto m = m_parent.def_submodule("chunk");

    py::classh<Amulet::BedrockChunk, Amulet::Chunk>
        BedrockChunk(m, "BedrockChunk");

    py::classh<
        Amulet::BedrockChunk118,
        Amulet::BedrockChunk,
        Amulet::BedrockRawChunkComponent,
        Amulet::BlockComponent>
        BedrockChunk118(m, "BedrockChunk118");
}
