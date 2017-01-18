cmake_minimum_required(VERSION 2.8.12)
project(dune-testtools CXX)

if(NOT (dune-common_DIR OR dune-common_ROOT OR
      "${CMAKE_PREFIX_PATH}" MATCHES ".*dune-common.*"))
    string(REPLACE  ${CMAKE_PROJECT_NAME} dune-common dune-common_DIR
      ${PROJECT_BINARY_DIR})
endif()

#find dune-common and set the module path
find_package(dune-common REQUIRED)
list(APPEND CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake/modules"
  ${dune-common_MODULE_PATH})

#include the dune macros
include(DuneMacros)

# start a dune project with information from dune.module
dune_project()
dune_enable_all_packages()

set(DUNE_TESTTOOLS_PATH ${PROJECT_SOURCE_DIR})

dune_install_python_package(PATH python)
add_python_test_command(COMMAND python -m pytest
                        WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}/python
                        REQUIRED_PACKAGES pytest)
add_python_test_command(COMMAND python -m pytest --pep8
                        WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}/python
                        REQUIRED_PACKAGES pytest pytest-pep8)

add_subdirectory("dune")
add_subdirectory("doc")
add_subdirectory("cmake/modules")

# Use a custom section to export testtool module path for downstream modules.
set(DUNE_CUSTOM_PKG_CONFIG_SECTION "
set(DUNE_TESTTOOLS_PATH \"${PROJECT_SOURCE_DIR}\")
")

# finalize the dune project, e.g. generating config.h etc.
finalize_dune_project(GENERATE_CONFIG_H_CMAKE)
