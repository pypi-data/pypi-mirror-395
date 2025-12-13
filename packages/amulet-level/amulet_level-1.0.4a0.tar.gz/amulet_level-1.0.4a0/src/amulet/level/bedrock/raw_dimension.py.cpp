#include <pybind11/pybind11.h>

#include "raw_dimension.hpp"

namespace py = pybind11;

class PyBedrockChunkCoordIterator {
    Amulet::BedrockChunkCoordIterator _it;
    bool _init;

public:
    PyBedrockChunkCoordIterator(Amulet::BedrockChunkCoordIterator it)
        : _it(std::move(it))
        , _init(false)
    {
    }

    std::pair<std::int32_t, std::int32_t> next()
    {
        if (!_it.is_vaild()) {
            throw py::stop_iteration();
        }
        if (_init) {
            if (!_it.seek_to_next()) {
                throw py::stop_iteration();
            }
        } else {
            _init = true;
            if (!_it.seek_to_first()) {
                throw py::stop_iteration();
            }
        }
        return _it.get_coord();
    }
};

py::module init_bedrock_raw_dimension(py::module m_parent)
{
    auto m = m_parent.def_submodule("raw_dimension");

    py::classh<PyBedrockChunkCoordIterator>
        BedrockChunkCoordIterator(m, "BedrockChunkCoordIterator", py::release_gil_before_calling_cpp_dtor());
    BedrockChunkCoordIterator.def(
        "__iter__",
        [](py::object self) { return self; });
    BedrockChunkCoordIterator.def(
        "__next__",
        &PyBedrockChunkCoordIterator::next);

    py::classh<Amulet::BedrockRawDimension>
        BedrockRawDimension(m, "BedrockRawDimension", py::release_gil_before_calling_cpp_dtor());
    BedrockRawDimension.def_property_readonly(
        "lock",
        &Amulet::BedrockRawDimension::get_mutex,
        py::keep_alive<0, 1>(),
        py::doc("The public lock\n"
                "Thread safe."));
    BedrockRawDimension.def_property_readonly(
        "dimension_id",
        &Amulet::BedrockRawDimension::get_dimension_id,
        py::doc("The identifier for this dimension. eg. \"minecraft:overworld\".\n"
                "Thread safe."));
    BedrockRawDimension.def_property_readonly(
        "internal_dimension_id",
        &Amulet::BedrockRawDimension::get_internal_dimension_id,
        py::doc("The internal identifier for this dimension. eg 0, 1 or 2\n"
                "Thread safe."));
    BedrockRawDimension.def_property_readonly(
        "bounds",
        &Amulet::BedrockRawDimension::get_bounds,
        py::doc("The selection box that fills the whole world.\n"
                "Thread safe."));
    BedrockRawDimension.def_property_readonly(
        "default_block",
        &Amulet::BedrockRawDimension::get_default_block,
        py::doc("The default block for this dimension.\n"
                "Thread safe."));
    BedrockRawDimension.def_property_readonly(
        "default_biome",
        &Amulet::BedrockRawDimension::get_default_biome,
        py::doc("The default biome for this dimension.\n"
                "Thread safe."));
    BedrockRawDimension.def_property_readonly(
        "all_chunk_coords",
        [](const Amulet::BedrockRawDimension& self) {
            return PyBedrockChunkCoordIterator(self.all_chunk_coords());
        },
        py::doc("An iterator of all chunk coordinates in the dimension.\n"
                "External Read:SharedReadWrite lock required.\n"
                "External Read:SharedReadOnly lock optional."));
    BedrockRawDimension.def(
        "has_chunk",
        &Amulet::BedrockRawDimension::has_chunk,
        py::arg("cx"),
        py::arg("cz"),
        py::doc("Does the chunk exist in this dimension.\n"
                "External Read:SharedReadWrite lock required.\n"
                "External Read:SharedReadOnly lock optional."));
    BedrockRawDimension.def(
        "delete_chunk",
        &Amulet::BedrockRawDimension::delete_chunk,
        py::arg("cx"),
        py::arg("cz"),
        py::doc("Delete the chunk from this dimension.\n"
                "External ReadWrite:SharedReadWrite lock required."));
    BedrockRawDimension.def(
        "get_raw_chunk",
        &Amulet::BedrockRawDimension::get_raw_chunk,
        py::arg("cx"),
        py::arg("cz"),
        py::doc("Get the raw chunk from this dimension.\n"
                "External Read:SharedReadWrite lock required."));
    BedrockRawDimension.def(
        "set_raw_chunk",
        &Amulet::BedrockRawDimension::set_raw_chunk,
        py::arg("cx"),
        py::arg("cz"),
        py::arg("chunk"),
        py::doc("Set the chunk in this dimension from raw data.\n"
                "External ReadWrite:SharedReadWrite lock required."));
    BedrockRawDimension.def(
        "decode_chunk",
        [](
            Amulet::BedrockRawDimension& self,
            const Amulet::BedrockRawChunk& raw_chunk,
            std::int64_t cx,
            std::int64_t cz) {
            return self.decode_chunk(raw_chunk, cx, cz);
        },
        py::arg("raw_chunk"),
        py::arg("cx"),
        py::arg("cz"),
        py::doc("Decode a raw chunk to a chunk object.\n"
                "TODO: thread safety"));
    BedrockRawDimension.def(
        "encode_chunk",
        &Amulet::BedrockRawDimension::encode_chunk,
        py::arg("chunk"),
        py::arg("cx"),
        py::arg("cz"),
        py::doc("Encode a chunk object to its raw data.\n"
                "This will mutate the chunk data.\n"
                "TODO: thread safety"));
    BedrockRawDimension.def(
        "get_chunk",
        &Amulet::BedrockRawDimension::get_chunk,
        py::arg("cx"),
        py::arg("cz"),
        py::doc("Get and decode the chunk.\n"
                "TODO: thread safety"));
    BedrockRawDimension.def(
        "set_chunk",
        &Amulet::BedrockRawDimension::set_chunk,
        py::arg("cx"),
        py::arg("cz"),
        py::arg("chunk"),
        py::doc("Encode and set the chunk.\n"
                "This will mutate the chunk data.\n"
                "TODO: thread safety"));
    BedrockRawDimension.def(
        "destroy",
        &Amulet::BedrockRawDimension::destroy,
        py::call_guard<py::gil_scoped_release>(),
        py::doc("Destroy the instance.\n"
                "Calls made after this will fail.\n"
                "This may only be called by the owner of the instance.\n"
                "External ReadWrite:Unique lock required."));
    BedrockRawDimension.def(
        "is_destroyed",
        &Amulet::BedrockRawDimension::is_destroyed,
        py::doc("Has the instance been destroyed.\n"
                "If this is false, other calls will fail.\n"
                "External Read:SharedReadWrite lock required."));

    return m;
}
