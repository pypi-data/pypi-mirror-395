#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl/filesystem.h>

#include <amulet/pybind11_extensions/builtins.hpp>

#include "level_dat.hpp"

namespace py = pybind11;
namespace pyext = Amulet::pybind11_extensions;

static std::shared_ptr<Amulet::NBT::NamedTag> get_named_tag_ptr(pyext::PyObjectCpp<Amulet::NBT::NamedTag> named_tag)
{
    try {
        return named_tag.cast<std::shared_ptr<Amulet::NBT::NamedTag>>();
    } catch (const std::runtime_error&) {
        return std::make_shared<Amulet::NBT::NamedTag>(named_tag.cast<Amulet::NBT::NamedTag&>());
    }
}

py::module init_bedrock_level_dat(py::module m_parent)
{
    auto m = m_parent.def_submodule("level_dat");

    py::classh<Amulet::BedrockLevelDat>
        BedrockLevelDat(m, "BedrockLevelDat");

    BedrockLevelDat.def(py::init<>());

    BedrockLevelDat.def(
        py::init([](std::uint32_t version, pyext::PyObjectCpp<Amulet::NBT::NamedTag> named_tag) {
            return Amulet::BedrockLevelDat(version, get_named_tag_ptr(named_tag));
        }),
        py::arg("version"),
        py::arg("named_tag"));

    BedrockLevelDat.def_static(
        "from_binary",
        [](py::bytes buffer) {
            return Amulet::BedrockLevelDat::from_binary(buffer.cast<std::string>());
        },
        py::arg("buffer"));

    BedrockLevelDat.def_static(
        "from_file",
        &Amulet::BedrockLevelDat::from_file,
        py::arg("path"));

    BedrockLevelDat.def(
        "to_binary",
        [](const Amulet::BedrockLevelDat& self) {
            return py::bytes(self.to_binary());
        });

    BedrockLevelDat.def(
        "save_to",
        &Amulet::BedrockLevelDat::save_to,
        py::arg("path"));

    BedrockLevelDat.def_property(
        "version",
        &Amulet::BedrockLevelDat::get_version,
        py::cpp_function(
            &Amulet::BedrockLevelDat::set_version,
            py::is_method(BedrockLevelDat),
            py::arg("version")));

    BedrockLevelDat.def_property(
        "named_tag",
        &Amulet::BedrockLevelDat::get_named_tag_ptr,
        [](Amulet::BedrockLevelDat& self, pyext::PyObjectCpp<Amulet::NBT::NamedTag> tag) {
            self.set_named_tag(get_named_tag_ptr(tag));
        });

    BedrockLevelDat.def(
        "__repr__",
        [](const Amulet::BedrockLevelDat& self) {
            return "BedrockLevelDat("
                + std::to_string(self.get_version()) + ", "
                + py::repr(py::cast(self.get_named_tag(), py::return_value_policy::reference)).cast<std::string>() + ")";
        });

    BedrockLevelDat.def(
        "__copy__",
        [](const Amulet::BedrockLevelDat& self) {
            return self;
        });

    BedrockLevelDat.def(
        "__deepcopy__",
        [](const Amulet::BedrockLevelDat& self, py::dict) {
            return self.deep_copy();
        },
        py::arg("memo"));

    return m;
}
