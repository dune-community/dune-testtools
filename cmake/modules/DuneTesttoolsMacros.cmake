# .. cmake_module::
#
#    The cmake code to execute whenever a module requires or suggests dune-testtools.
#
#    A summary of what is done:
#
#    * Requirements on the python interpreter are formulated
#    * The API for dune-style system tests is included.
#
# .. cmake_variable:: DEBUG_MACRO_TESTS
#
#    If turned on, the configure time unit tests of dune-testtools
#    have verbose output. This is mainly useful if you are developing
#    and debugging dune-testtools.
#

dune_require_python_version(2.7)
#TODO: What is our minimum python3.x requirement?

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
