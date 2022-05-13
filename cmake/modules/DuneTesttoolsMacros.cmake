# .. cmake_module::
#
#    The CMake code to execute whenever a module requires or suggests dune-testtools.
#
#    A summary of what is done:
#
#    * Requirements on the Python interpreter are formulated
#    * The API for Dune-style system tests is included.
#
# .. cmake_variable:: DEBUG_MACRO_TESTS
#
#    If turned on, the configure time unit tests of dune-testtools
#    have verbose output. This is mainly useful if you are developing
#    and debugging dune-testtools.
#


# Generate a string containing "DEBUG" if we want to debug macros
if(DEBUG_MACRO_TESTS)
  set(DEBUG_MACRO_TESTS DEBUG)
else()
  set(DEBUG_MACRO_TESTS)
endif()

include(DuneCMakeAssertion)
include(ParsePythonData)
include(DuneSystemtests)
include(ExpandMetaIni)

function(testtools_add_python_targets base)
include(DuneSymlinkOrCopy)
if(PROJECT_SOURCE_DIR STREQUAL PROJECT_BINARY_DIR)
  message(WARNING "Source and binary dir are the same, skipping symlink!")
else()
  foreach(file ${ARGN})
    dune_symlink_to_source_files(FILES ${file}.py)
  endforeach()
endif()
endfunction()