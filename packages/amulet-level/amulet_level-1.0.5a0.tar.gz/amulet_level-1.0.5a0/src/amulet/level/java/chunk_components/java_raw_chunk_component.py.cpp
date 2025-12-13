#include <pybind11/operators.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/typing.h>

#include <memory>

#include <amulet/pybind11_extensions/collections.hpp>
#include <amulet/pybind11_extensions/mutable_mapping.hpp>

#include <amulet/nbt/tag/named_tag.hpp>

#include <amulet/level/java/chunk_components/java_raw_chunk_component.hpp>

namespace py = pybind11;
namespace pyext = Amulet::pybind11_extensions;

void init_java_raw_chunk_component(py::module m)
{
    py::class_<Amulet::JavaRawChunkComponent, std::shared_ptr<Amulet::JavaRawChunkComponent>>
        JavaRawChunkComponent(m, "JavaRawChunkComponent");

    JavaRawChunkComponent.def_readonly_static(
        "ComponentID",
        &Amulet::JavaRawChunkComponent::ComponentID);
    JavaRawChunkComponent.def_property(
        "raw_data",
        [](
            Amulet::JavaRawChunkComponent& self) -> Amulet::pybind11_extensions::collections::MutableMapping<std::string, Amulet::NBT::NamedTag> {
            auto raw_data_ptr = self.get_raw_data();
            Amulet::JavaRawChunkType& raw_data = *raw_data_ptr;
            return pyext::make_mutable_mapping(raw_data, std::move(raw_data_ptr));
        },
        [](
            Amulet::JavaRawChunkComponent& self, Amulet::pybind11_extensions::collections::Mapping<std::string, Amulet::NBT::NamedTag> py_raw_data) {
            auto raw_data = std::make_shared<Amulet::JavaRawChunkType>();
            for (auto it = py_raw_data.begin(); it != py_raw_data.end(); it++) {
                raw_data->insert_or_assign(
                    it->cast<std::string>(),
                    py_raw_data.attr("__getitem__")(*it).cast<std::shared_ptr<Amulet::NBT::NamedTag>>());
            }
            self.set_raw_data(raw_data);
        },
        py::doc(
            "This is subject to change as data gets moved into the chunk class.\n"
            "Do not rely on data in here existing."));
}
