#include <pybind11/pybind11.h>

#include <amulet/core/chunk/component/block_component.hpp>
#include <amulet/core/chunk/component/block_entity_component.hpp>

#include "chunk.hpp"

#include "chunk_components/bedrock_raw_chunk_component.hpp"

namespace py = pybind11;

void init_bedrock_chunk(py::module m_parent)
{
    auto m = m_parent.def_submodule("chunk");

    py::classh<Amulet::BedrockChunk, Amulet::Chunk>
        BedrockChunk(m, "BedrockChunk");

    py::classh<
        Amulet::BedrockChunk0,
        Amulet::BedrockChunk,
        Amulet::BedrockRawChunkComponent,
        Amulet::BlockComponent,
        Amulet::BlockEntityComponent>
        BedrockChunk0(m, "BedrockChunk0");

    py::classh<
        Amulet::BedrockChunk1,
        Amulet::BedrockChunk,
        Amulet::BedrockRawChunkComponent,
        Amulet::BlockComponent,
        Amulet::BlockEntityComponent>
        BedrockChunk1(m, "BedrockChunk1");

    py::classh<
        Amulet::BedrockChunk118,
        Amulet::BedrockChunk,
        Amulet::BedrockRawChunkComponent,
        Amulet::BlockComponent,
        Amulet::BlockEntityComponent>
        BedrockChunk118(m, "BedrockChunk118");
}
