if (NOT TARGET amulet_level)
    message(STATUS "Finding amulet_level")

    find_package(amulet_io CONFIG REQUIRED)
    find_package(amulet_leveldb CONFIG REQUIRED)
    find_package(amulet_utils CONFIG REQUIRED)
    find_package(amulet_nbt CONFIG REQUIRED)
    find_package(amulet_core CONFIG REQUIRED)
    find_package(amulet_game CONFIG REQUIRED)
    find_package(amulet_anvil CONFIG REQUIRED)

    set(amulet_level_INCLUDE_DIR "${CMAKE_CURRENT_LIST_DIR}/../..")
    find_library(amulet_level_LIBRARY NAMES amulet_level PATHS "${CMAKE_CURRENT_LIST_DIR}")
    message(STATUS "amulet_level_LIBRARY: ${amulet_level_LIBRARY}")

    add_library(amulet_level_bin SHARED IMPORTED)
    set_target_properties(amulet_level_bin PROPERTIES
        IMPORTED_IMPLIB "${amulet_level_LIBRARY}"
    )

    add_library(amulet_level INTERFACE)
    target_link_libraries(amulet_level INTERFACE amulet_io)
    target_link_libraries(amulet_level INTERFACE leveldb)
    target_link_libraries(amulet_level INTERFACE amulet_utils)
    target_link_libraries(amulet_level INTERFACE amulet_nbt)
    target_link_libraries(amulet_level INTERFACE amulet_core)
    target_link_libraries(amulet_level INTERFACE amulet_game)
    target_link_libraries(amulet_level INTERFACE amulet_anvil)
    target_link_libraries(amulet_level INTERFACE amulet_level_bin)
    target_include_directories(amulet_level INTERFACE ${amulet_level_INCLUDE_DIR})
endif()
