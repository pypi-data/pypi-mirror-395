#include <pybind11/chrono.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl/filesystem.h>

// #include <memory>

#include <amulet/utils/event.py.hpp>

// #include <amulet/core/version/version.hpp>

#include "raw_level.hpp"

namespace py = pybind11;

py::module init_bedrock_raw_level(py::module m_parent)
{
    auto m = m_parent.def_submodule("raw_level");
    //
    //    py::classh<Amulet::BedrockCreateArgsV1>
    //        BedrockCreateArgsV1(m, "BedrockCreateArgsV1");
    //    BedrockCreateArgsV1.def(
    //        py::init<bool, const std::string&, const Amulet::VersionNumber&, const std::string&>(),
    //        py::arg("overwrite"),
    //        py::arg("path"),
    //        py::arg("version"),
    //        py::arg("level_name"));
    //    BedrockCreateArgsV1.def_readonly(
    //        "overwrite",
    //        &Amulet::BedrockCreateArgsV1::overwrite);
    //    BedrockCreateArgsV1.def_property_readonly(
    //        "path",
    //        [](const Amulet::BedrockCreateArgsV1& self) {
    //            return self.path.string();
    //        });
    //    BedrockCreateArgsV1.def_readonly(
    //        "version",
    //        &Amulet::BedrockCreateArgsV1::version);
    //    BedrockCreateArgsV1.def_readonly(
    //        "level_name",
    //        &Amulet::BedrockCreateArgsV1::level_name);
    //
    py::classh<Amulet::BedrockRawLevel>
        BedrockRawLevel(m, "BedrockRawLevel", py::release_gil_before_calling_cpp_dtor());
    BedrockRawLevel.def_static(
        "load",
        &Amulet::BedrockRawLevel::load,
        py::arg("path"),
        py::call_guard<py::gil_scoped_release>(),
        py::doc("Load an existing Bedrock level from the given directory.\n"
                "Thread safe."));
    //    BedrockRawLevel.def_static(
    //        "create",
    //        [](const Amulet::BedrockCreateArgsV1& args) {
    //            return Amulet::BedrockRawLevel::create(args);
    //        },
    //        py::arg("args"),
    //        py::call_guard<py::gil_scoped_release>(),
    //        py::doc("Create a new Bedrock level at the given directory.\n"
    //                "Thread safe."));
    BedrockRawLevel.def_property_readonly(
        "lock",
        &Amulet::BedrockRawLevel::get_mutex,
        py::keep_alive<0, 1>(),
        py::doc("The public lock\n"
                "Thread safe."));
    BedrockRawLevel.def(
        "is_open",
        &Amulet::BedrockRawLevel::is_open,
        py::call_guard<py::gil_scoped_release>(),
        py::doc("Is the level open.\n"
                "External Read:SharedReadWrite lock required."));
    BedrockRawLevel.def(
        "reload_metadata",
        &Amulet::BedrockRawLevel::reload_metadata,
        py::call_guard<py::gil_scoped_release>(),
        py::doc("Reload the metadata. This can only be called when the level is closed.\n"
                "External ReadWrite:Unique lock required."));
    Amulet::def_event(
        BedrockRawLevel,
        "opened",
        &Amulet::BedrockRawLevel::opened);
    BedrockRawLevel.def(
        "open",
        &Amulet::BedrockRawLevel::open,
        py::call_guard<py::gil_scoped_release>(),
        py::doc("Open the level.\n"
                "opened event will be emitted when complete.\n"
                "External ReadWrite:Unique lock required."));
    Amulet::def_event(
        BedrockRawLevel,
        "closed",
        &Amulet::BedrockRawLevel::closed);
    BedrockRawLevel.def(
        "close",
        &Amulet::BedrockRawLevel::close,
        py::call_guard<py::gil_scoped_release>(),
        py::doc("Close the level.\n"
                "closed event will be emitted when complete.\n"
                "External ReadWrite:Unique lock required."));
    Amulet::def_event(
        BedrockRawLevel,
        "reloaded",
        &Amulet::BedrockRawLevel::reloaded);
    BedrockRawLevel.def(
        "reload",
        &Amulet::BedrockRawLevel::reload,
        py::call_guard<py::gil_scoped_release>(),
        py::doc("Reload the level.\n"
                "This is like closing and re-opening without releasing the session.lock file.\n"
                "External ReadWrite:Unique lock required."));
    BedrockRawLevel.def_property_readonly(
        "path",
        [](const Amulet::BedrockRawLevel& self) {
            return self.get_path().string();
        },
        py::doc("The path to the level directory.\n"
                "Thread safe."));
    BedrockRawLevel.def_property(
        "level_dat",
        py::cpp_function(
            &Amulet::BedrockRawLevel::get_level_dat,
            py::call_guard<py::gil_scoped_release>()),
        py::cpp_function(
            &Amulet::BedrockRawLevel::set_level_dat,
            py::call_guard<py::gil_scoped_release>()),
        py::doc("Getter:\n"
                "The NamedTag stored in the level.dat file. Returns a unique copy.\n"
                "External Read:SharedReadWrite lock required.\n"
                "\n"
                "Setter:\n"
                "Set the level.dat NamedTag\n"
                "This calls :meth:`reload` if the data version changed.\n"
                "External ReadWrite:Unique lock required."));
    BedrockRawLevel.def_property_readonly(
        "platform",
        &Amulet::BedrockRawLevel::get_platform,
        py::doc("The platform identifier. \"bedrock\"\n"
                "Thread safe."));
    BedrockRawLevel.def_property(
        "last_opened_version",
        &Amulet::BedrockRawLevel::get_last_opened_version,
        py::cpp_function(
            &Amulet::BedrockRawLevel::set_last_opened_version,
            py::call_guard<py::gil_scoped_release>()),
        py::doc("Getter:\n"
                "The game version that the level was last opened in.\n"
                "External Read:SharedReadWrite lock required.\n"
                "\n"
                "Setter:\n"
                "Set the maximum game version.\n"
                "If the game version is different this will call :meth:`reload`.\n"
                "External ReadWrite:SharedReadWrite lock required."));
    BedrockRawLevel.def(
        "is_supported",
        &Amulet::BedrockRawLevel::is_supported,
        py::doc(
            "Is this level a supported version.\n"
            "This is true for all versions we support and false for snapshots and unsupported newer versions.\n"
            "TODO: thread safety"));
    BedrockRawLevel.def_property_readonly(
        "thumbnail",
        &Amulet::BedrockRawLevel::get_thumbnail,
        py::doc("Get the thumbnail for the level.\n"
                "Thread safe."));
    BedrockRawLevel.def_property_readonly(
        "modified_time",
        py::cpp_function(
            &Amulet::BedrockRawLevel::get_modified_time,
            py::call_guard<py::gil_scoped_release>()),
        py::doc("The time when the level was lasted edited.\n"
                "External Read:SharedReadWrite lock required."));
    BedrockRawLevel.def_property(
        "level_name",
        py::cpp_function(
            &Amulet::BedrockRawLevel::get_level_name,
            py::call_guard<py::gil_scoped_release>()),
        py::cpp_function(
            &Amulet::BedrockRawLevel::set_level_name,
            py::call_guard<py::gil_scoped_release>()),
        py::doc("Getter:\n"
                "The name of the level.\n"
                "External Read:SharedReadWrite lock required.\n"
                "\n"
                "Setter:\n"
                "Set the level name.\n"
                "External ReadWrite:Unique lock required."));
    BedrockRawLevel.def_property_readonly(
        "dimension_ids",
        py::cpp_function(
            &Amulet::BedrockRawLevel::get_dimension_ids,
            py::call_guard<py::gil_scoped_release>()),
        py::doc("The identifiers for all dimensions in this level.\n"
                "External Read:SharedReadWrite lock required.\n"
                "External Read:SharedReadOnly lock optional."));
    BedrockRawLevel.def(
        "get_dimension",
        [](Amulet::BedrockRawLevel& self, std::variant<Amulet::DimensionId, Amulet::BedrockInternalDimensionID> dimension_id) {
            return std::visit(
                [&](auto&& arg) {
                    return self.get_dimension(arg);
                },
                dimension_id);
        },
        py::arg("dimension_id"),
        py::call_guard<py::gil_scoped_release>(),
        py::doc("Get the raw dimension object for a specific dimension.\n"
                "External Read:SharedReadWrite lock required."));
    BedrockRawLevel.def(
        "compact",
        &Amulet::BedrockRawLevel::compact,
        py::call_guard<py::gil_scoped_release>(),
        py::doc("Compact the level.\n"
                "External Read:SharedReadWrite lock required."));
    BedrockRawLevel.def_property_readonly(
        "block_id_override",
        &Amulet::BedrockRawLevel::get_block_id_override,
        py::call_guard<py::gil_scoped_release>(),
        py::doc("Overridden block ids.\n"
                "External Read:SharedReadWrite lock required."));
    BedrockRawLevel.def_property_readonly(
        "biome_id_override",
        &Amulet::BedrockRawLevel::get_biome_id_override,
        py::call_guard<py::gil_scoped_release>(),
        py::doc("Overridden biome ids.\n"
                "External Read:SharedReadWrite lock required."));
    BedrockRawLevel.def_property_readonly(
        "leveldb",
        &Amulet::BedrockRawLevel::get_leveldb,
        py::doc("Get the LevelDB database.\n"
                "External Read::SharedReadWrite lock required."));

    return m;
}
