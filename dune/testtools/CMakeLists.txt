# both targets do not work with global venv
# add_subdirectory(test)
# add_subdirectory(tutorial)

install(FILES gridconstruction.hh
              outputtree.hh
        DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/dune/testtools)



