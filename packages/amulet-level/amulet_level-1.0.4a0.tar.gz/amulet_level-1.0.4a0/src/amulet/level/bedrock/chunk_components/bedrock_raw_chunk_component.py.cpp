#include <pybind11/operators.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/typing.h>

#include <memory>

#include <amulet/pybind11_extensions/collections.hpp>
#include <amulet/pybind11_extensions/mutable_mapping.hpp>

#include <amulet/nbt/tag/named_tag.hpp>

#include "bedrock_raw_chunk_component.hpp"

namespace py = pybind11;
namespace pyext = Amulet::pybind11_extensions;

void init_bedrock_raw_chunk_component(py::module m)
{
    py::class_<Amulet::BedrockRawChunkComponent, std::shared_ptr<Amulet::BedrockRawChunkComponent>>
        BedrockRawChunkComponent(m, "BedrockRawChunkComponent");

    BedrockRawChunkComponent.def_readonly_static(
        "ComponentID",
        &Amulet::BedrockRawChunkComponent::ComponentID);
    BedrockRawChunkComponent.def_property(
        "raw_data",
        &Amulet::BedrockRawChunkComponent::get_raw_data,
        &Amulet::BedrockRawChunkComponent::set_raw_data,
        py::doc(
            "This is subject to change as data gets moved into the chunk class.\n"
            "Do not rely on data in here existing."));
}
