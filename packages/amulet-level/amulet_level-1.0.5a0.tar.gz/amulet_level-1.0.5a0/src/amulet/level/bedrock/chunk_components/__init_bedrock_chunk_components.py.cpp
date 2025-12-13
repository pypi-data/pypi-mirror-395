#include <pybind11/pybind11.h>

#include <amulet/pybind11_extensions/py_module.hpp>

namespace py = pybind11;

void init_bedrock_raw_chunk_component(py::module);

void init_bedrock_chunk_components(py::module m_parent)
{
    auto m = Amulet::pybind11_extensions::def_subpackage(m_parent, "chunk_components");
    init_bedrock_raw_chunk_component(m);
}
