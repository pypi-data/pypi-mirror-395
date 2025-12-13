#include <pybind11/pybind11.h>

#include <amulet/core/biome/biome.hpp>
#include <amulet/core/block/block.hpp>
#include <amulet/core/chunk/chunk.hpp>
#include <amulet/core/chunk/component/block_component.hpp>

#include "chunk_components/data_version_component.hpp"
#include "chunk_components/java_raw_chunk_component.hpp"
#include "chunk.hpp"

namespace py = pybind11;

void init_java_chunk(py::module m_parent)
{
    auto m = m_parent.def_submodule("chunk");

    py::classh<
        Amulet::JavaChunk,
        Amulet::Chunk>
        JavaChunk(m, "JavaChunk");

    py::classh<
        Amulet::JavaChunkNA,
        Amulet::JavaChunk,
        Amulet::JavaRawChunkComponent,
        Amulet::DataVersionComponent,
        // Amulet::LastUpdateComponent,
        // Amulet::JavaLegacyVersionComponent,
        Amulet::BlockComponent //,
        // Amulet::BlockEntityComponent,
        // Amulet::EntityComponent,
        // Amulet::Biome2DComponent,
        // Amulet::Height2DComponent,
        >
        JavaChunkNA(m, "JavaChunkNA");

    JavaChunkNA.def(
        py::init<
            const Amulet::BlockStack&,
            const Amulet::Biome&>(),
        py::arg("default_block"),
        py::arg("default_biome"));

    py::classh<
        Amulet::JavaChunk0,
        Amulet::JavaChunk,
        Amulet::JavaRawChunkComponent,
        Amulet::DataVersionComponent,
        // Amulet::LastUpdateComponent,
        // Amulet::TerrainPopulatedComponent,
        // Amulet::LightPopulatedComponent,
        Amulet::BlockComponent //,
        // Amulet::BlockEntityComponent,
        // Amulet::EntityComponent,
        // Amulet::Biome2DComponent,
        // Amulet::Height2DComponent,
        >
        JavaChunk0(m, "JavaChunk0");

    JavaChunk0.def(
        py::init<
            std::int64_t,
            const Amulet::BlockStack&,
            const Amulet::Biome&>(),
        py::arg("data_version"),
        py::arg("default_block"),
        py::arg("default_biome"));

    py::classh<
        Amulet::JavaChunk1444,
        Amulet::JavaChunk,
        Amulet::JavaRawChunkComponent,
        Amulet::DataVersionComponent,
        // Amulet::LastUpdateComponent,
        // Amulet::StatusStringComponent,
        Amulet::BlockComponent //,
        // Amulet::BlockEntityComponent,
        // Amulet::EntityComponent,
        // Amulet::Biome2DComponent,
        // Amulet::Height2DComponent,
        >
        JavaChunk1444(m, "JavaChunk1444");

    JavaChunk1444.def(
        py::init<
            std::int64_t,
            const Amulet::BlockStack&,
            const Amulet::Biome&>(),
        py::arg("data_version"),
        py::arg("default_block"),
        py::arg("default_biome"));

    py::classh<
        Amulet::JavaChunk1466,
        Amulet::JavaChunk,
        Amulet::JavaRawChunkComponent,
        Amulet::DataVersionComponent,
        // Amulet::LastUpdateComponent,
        // Amulet::StatusStringComponent,
        Amulet::BlockComponent //,
        // Amulet::BlockEntityComponent,
        // Amulet::EntityComponent,
        // Amulet::Biome2DComponent,
        // Amulet::NamedHeight2DComponent,
        >
        JavaChunk1466(m, "JavaChunk1466");

    JavaChunk1466.def(
        py::init<
            std::int64_t,
            const Amulet::BlockStack&,
            const Amulet::Biome&>(),
        py::arg("data_version"),
        py::arg("default_block"),
        py::arg("default_biome"));

    py::classh<
        Amulet::JavaChunk2203,
        Amulet::JavaChunk,
        Amulet::JavaRawChunkComponent,
        Amulet::DataVersionComponent,
        // Amulet::LastUpdateComponent,
        // Amulet::StatusStringComponent,
        Amulet::BlockComponent //,
        // Amulet::BlockEntityComponent,
        // Amulet::EntityComponent,
        // Amulet::Biome3DComponent,
        // Amulet::NamedHeight2DComponent,
        >
        JavaChunk2203(m, "JavaChunk2203");

    JavaChunk2203.def(
        py::init<
            std::int64_t,
            const Amulet::BlockStack&,
            const Amulet::Biome&>(),
        py::arg("data_version"),
        py::arg("default_block"),
        py::arg("default_biome"));
}
