#include <pybind11/pybind11.h>

#include <amulet/pybind11_extensions/mutable_mapping.hpp>
#include <amulet/pybind11_extensions/mutable_sequence.hpp>

#include <amulet/utils/bytes.py.hpp>

#include "raw_chunk.hpp"

namespace py = pybind11;
namespace pyext = Amulet::pybind11_extensions;

void init_bedrock_raw_chunk(py::module m_parent)
{
    auto m = m_parent.def_submodule("raw_chunk");

    py::classh<Amulet::BedrockRawChunk>
        BedrockRawChunk(m, "BedrockRawChunk");

    BedrockRawChunk.def_property_readonly(
        "data",
        [](Amulet::BedrockRawChunk& self) {
            return pyext::make_mutable_mapping(self.get_data());
        },
        py::keep_alive<0, 1>());

    BedrockRawChunk.def_property_readonly(
        "actors",
        [](Amulet::BedrockRawChunk& self) {
            return pyext::make_mutable_sequence(self.get_actors());
        },
        py::keep_alive<0, 1>());
}
