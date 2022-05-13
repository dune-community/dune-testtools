include(DunePythonCommonMacros)
add_subdirectory(dune)
add_subdirectory(scripts)
add_subdirectory(wrapper)

configure_file(setup.py.in setup.py)
