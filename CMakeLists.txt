cmake_minimum_required(VERSION 3.10.0)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

project(gamjam)

find_package(SDL2 REQUIRED)

file(GLOB SOURCES
    src/*.c
    src/lib/*.c
    src/lib/*.h
    include/*.h
)

include_directories(${CMAKE_SOURCE_DIR}/lib)
link_directories(${CMAKE_SOURCE_DIR}/build)

add_executable(gamjam ${SOURCES})
target_include_directories(
    gamjam
    PUBLIC
    ${SDL2_INCLUDE_DIRS}
    src
    include
    src/lib
)
set(CMAKE_C_FLAGS "-g")

target_link_libraries(gamjam PRIVATE SDL2::SDL2-static)
