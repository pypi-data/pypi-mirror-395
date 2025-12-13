#include <pybind11/pybind11.h>

#include <amulet/pybind11_extensions/py_module.hpp>

namespace py = pybind11;

py::module init_bedrock_level_dat(py::module);
void init_bedrock_raw_chunk(py::module);
void init_bedrock_chunk_components(py::module);
void init_bedrock_chunk(py::module);
py::module init_bedrock_raw_dimension(py::module);
py::module init_bedrock_raw_level(py::module);
py::module init_bedrock_chunk_handle(py::module);
py::module init_bedrock_dimension(py::module);
py::module init_bedrock_level(py::module);

py::module init_bedrock(py::module m_parent)
{
    auto m = Amulet::pybind11_extensions::def_subpackage(m_parent, "bedrock");

    m.attr("BedrockLevelDat") = init_bedrock_level_dat(m).attr("BedrockLevelDat");

    init_bedrock_raw_chunk(m);
    init_bedrock_chunk_components(m);
    init_bedrock_chunk(m);

    auto raw_dimension = init_bedrock_raw_dimension(m);
    m.attr("BedrockRawDimension") = raw_dimension.attr("BedrockRawDimension");

    auto raw_level = init_bedrock_raw_level(m);
    m.attr("BedrockRawLevel") = raw_level.attr("BedrockRawLevel");

    auto chunk_handle = init_bedrock_chunk_handle(m);
    m.attr("BedrockChunkHandle") = chunk_handle.attr("BedrockChunkHandle");

    auto dimension = init_bedrock_dimension(m);
    m.attr("BedrockInternalDimensionID") = dimension.attr("BedrockInternalDimensionID");
    m.attr("BedrockDimension") = dimension.attr("BedrockDimension");

    auto level = init_bedrock_level(m);
    m.attr("BedrockLevel") = level.attr("BedrockLevel");

    return m;
}
