#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl/filesystem.h>

#include <amulet/level/abc/level.hpp>

#include "level.hpp"

namespace py = pybind11;

py::module init_bedrock_level(py::module m_parent)
{
    auto m = m_parent.def_submodule("level");

    py::classh<
        Amulet::BedrockLevel,
        Amulet::Level,
        Amulet::CompactibleLevel,
        Amulet::DiskLevel,
        Amulet::ReloadableLevel>
        BedrockLevel(m, "BedrockLevel");
    BedrockLevel.def_static(
        "load",
        &Amulet::BedrockLevel::load,
        py::arg("path"),
        py::call_guard<py::gil_scoped_release>(),
        py::doc("Load an existing Bedrock level from the given directory.\n"
                "Thread safe."));
    //    BedrockLevel.def_static(
    //        "create",
    //        [](const Amulet::BedrockCreateArgsV1& args) {
    //            return Amulet::BedrockLevel::create(args);
    //        },
    //        py::arg("args"),
    //        py::call_guard<py::gil_scoped_release>(),
    //        py::doc("Create a new Bedrock level at the given directory.\n"
    //                "Thread safe."));
    BedrockLevel.def_property_readonly(
        "raw_level",
        &Amulet::BedrockLevel::get_raw_level,
        py::keep_alive<0, 1>(),
        py::doc(
            "Access the raw level instance.\n"
            "Before calling any mutating functions, the caller must call :meth:`purge` (optionally saving before)\n"
            "External ReadWrite:Unique lock required."));
    BedrockLevel.attr("get_dimension") = py::cpp_function(
        &Amulet::BedrockLevel::get_bedrock_dimension,
        py::name("get_dimension"),
        py::is_method(BedrockLevel),
        py::arg("dimension_id"),
        py::doc("Get a dimension.\n"
                "External Read:SharedReadWrite lock required.\n"
                "External ReadWrite:SharedReadWrite lock required when calling code in Dimension (and its children) that need write permission."));

    return m;
}
