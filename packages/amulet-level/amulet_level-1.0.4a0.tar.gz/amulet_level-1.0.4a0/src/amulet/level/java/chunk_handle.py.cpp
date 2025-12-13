#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <amulet/pybind11_extensions/collections.hpp>

#include "chunk_handle.hpp"

namespace py = pybind11;

py::module init_java_chunk_handle(py::module m_parent)
{
    auto m = m_parent.def_submodule("chunk_handle");

    py::classh<Amulet::JavaChunkHandle, Amulet::ChunkHandle>
        JavaChunkHandle(m, "JavaChunkHandle");

    JavaChunkHandle.attr("get_chunk") = py::cpp_function(
        [](Amulet::JavaChunkHandle& self, std::optional<Amulet::pybind11_extensions::collections::Iterable<std::string>> py_component_ids) {
            std::optional<std::set<std::string>> component_ids;
            if (py_component_ids) {
                component_ids = std::set<std::string>(py_component_ids->begin(), py_component_ids->end());
            }
            py::gil_scoped_release nogil;
            return self.get_java_chunk(std::move(component_ids));
        },
        py::name("get_chunk"),
        py::is_method(JavaChunkHandle),
        py::arg("component_ids") = py::none(),
        py::doc("Get a unique copy of the chunk data."));
    JavaChunkHandle.def(
        "set_chunk",
        &Amulet::JavaChunkHandle::set_java_chunk,
        py::arg("chunk"),
        py::prepend(),
        py::call_guard<py::gil_scoped_release>(),
        py::doc(
            "Overwrite the chunk data.\n"
            "You must acquire the chunk lock before setting.\n"
            "If you want to edit the chunk, use :meth:`edit` instead.\n"
            "\n"
            ":param chunk: The chunk data to set."));
    // This is here to appease mypy.
    JavaChunkHandle.def(
        "set_chunk",
        &Amulet::JavaChunkHandle::set_chunk,
        py::arg("chunk"),
        py::call_guard<py::gil_scoped_release>(),
        py::doc(
            "Overwrite the chunk data.\n"
            "You must acquire the chunk lock before setting.\n"
            "If you want to edit the chunk, use :meth:`edit` instead.\n"
            "\n"
            ":param chunk: The chunk data to set."));

    return m;
}
