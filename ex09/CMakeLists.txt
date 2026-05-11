cmake_minimum_required(VERSION 3.16)

project(container_benchmark LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type" FORCE)
endif()

add_executable(container_benchmark
  container_benchmark.cpp
)

target_compile_options(container_benchmark PRIVATE
  $<$<CONFIG:Release>:-O2>
  -Wall
  -Wextra
  -Wpedantic
)
