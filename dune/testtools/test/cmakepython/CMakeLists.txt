# This is a configure test for the Python CMake interface

execute_process(COMMAND ${CMAKE_BINARY_DIR}/gdt-run-in-dune-env python ${CMAKE_CURRENT_SOURCE_DIR}/testdata.py ${CMAKE_CURRENT_BINARY_DIR}/interface.log
                )

include(ParsePythonData)
parse_python_data(PREFIX TESTPREFIX FILE ${CMAKE_CURRENT_BINARY_DIR}/interface.log)

if(NOT "${TESTPREFIX_3}" STREQUAL "5")
  message(FATAL_ERROR "Fatal error in Python - CMake interface! TESTPREFIX_3 not parsed correctly")
endif()

if(NOT "${TESTPREFIX_2}" STREQUAL "17")
  message("TESTPREFIX_2: ${TESTPREFIX_2}")
  message(FATAL_ERROR "Fatal error in Python - CMake interface! TESTPREFIX_2 not parsed correctly")
endif()

if(NOT "${TESTPREFIX_8}" STREQUAL "4;something")
  message(FATAL_ERROR "Fatal error in Python - CMake interface! TESTPREFIX_8 not parsed correctly")
endif()

if(NOT "${TESTPREFIX_mykey}" STREQUAL "bla;blubb")
  message(FATAL_ERROR "Fatal error in Python - CMake interface! TESTPREFIX_mykey not parsed correctly")
endif()

if(NOT "${TESTPREFIX_nested_bla}" STREQUAL "val")
  message(FATAL_ERROR "Fatal error in Python - CMake interface! TESTPREFIX_nested_bla not parsed correctly")
endif()

if(NOT "${TESTPREFIX_nested_5_deeper}" STREQUAL "wow!")
  message(FATAL_ERROR "Fatal error in Python - CMake interface! TESTPREFIX_nested_5_deeper not parsed correctly")
endif()

if(${DEBUG_MACRO_TESTS})
  message("All configure tests for the Python CMake interface have been run...")
endif()
