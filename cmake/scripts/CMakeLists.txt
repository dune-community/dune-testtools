configure_file(gdt-run-in-dune-env.sh.in ${CMAKE_BINARY_DIR}/gdt-run-in-dune-env @ONLY)

install(PROGRAMS gdt-run-in-dune-env.sh.in DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/dune/cmake/scripts)
install(PROGRAMS ${CMAKE_BINARY_DIR}/gdt-run-in-dune-env DESTINATION ${CMAKE_INSTALL_BINDIR})
