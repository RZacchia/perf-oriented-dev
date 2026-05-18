cmake_minimum_required(VERSION 3.10)
project(perf_oriented_prog_samples)

set_property(GLOBAL PROPERTY C_STANDARD 11)

if(MSVC)
  add_compile_options(/W4 /WX)
else()
  add_compile_options(-Wall -Wextra -Wpedantic -Werror -O2)
endif()


add_executable(delannoy delannoy.c)
add_executable(delannoy_memoized delannoy_memoized.c)
add_executable(delannoy_tabulated delannoy_tabulated.c)

