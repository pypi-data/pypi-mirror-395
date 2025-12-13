#include <pybind11/pybind11.h>

#include "dimension.hpp"

namespace py = pybind11;

py::module init_bedrock_dimension(py::module m_parent)
{
    auto m = m_parent.def_submodule("dimension");

    m.attr("BedrockInternalDimensionID") = py::module::import("builtins").attr("str");

    py::classh<Amulet::BedrockDimension, Amulet::Dimension>
        BedrockDimension(m, "BedrockDimension");
    BedrockDimension.attr("get_chunk_handle") = py::cpp_function(
        &Amulet::BedrockDimension::get_bedrock_chunk_handle,
        py::name("get_chunk_handle"),
        py::is_method(BedrockDimension),
        py::arg("cx"),
        py::arg("cz"),
        py::call_guard<py::gil_scoped_release>(),
        py::doc(
            "Get the chunk handle for the given chunk in this dimension.\n"
            "Thread safe.\n"
            "\n"
            ":param cx: The chunk x coordinate to load.\n"
            ":param cz: The chunk z coordinate to load."));

    return m;
}
