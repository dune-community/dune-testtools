add_executable(onemacrodyntest1 source.cc)
add_executable(onemacrodyntest2 source.cc)
set_property(TARGET onemacrodyntest2 APPEND PROPERTY COMPILE_DEFINITIONS "SWITCH=ON")

dune_add_system_test(TARGET onemacrodyntest1 onemacrodyntest2 INIFILE dynamictest.mini ${DEBUG_MACRO_TESTS})
dune_assert(TEST_EXISTS onemacrodyntest1_1_0000 MESSAGE "dynamicvariants: A test called onemacrodyntest1_1_0000 should exist")
dune_assert(TEST_EXISTS onemacrodyntest1_1_0001 MESSAGE "dynamicvariants: A test called onemacrodyntest1_1_0001 should exist")
dune_assert(TEST_EXISTS onemacrodyntest1_2_0000 MESSAGE "dynamicvariants: A test called onemacrodyntest1_2_0000 should exist")
dune_assert(TEST_EXISTS onemacrodyntest1_2_0001 MESSAGE "dynamicvariants: A test called onemacrodyntest1_2_0001 should exist")
dune_assert(TEST_EXISTS onemacrodyntest1_3_0000 MESSAGE "dynamicvariants: A test called onemacrodyntest1_3_0000 should exist")
dune_assert(TEST_EXISTS onemacrodyntest1_3_0001 MESSAGE "dynamicvariants: A test called onemacrodyntest1_3_0001 should exist")
dune_assert(TEST_EXISTS onemacrodyntest2_1_0000 MESSAGE "dynamicvariants: A test called onemacrodyntest2_1_0000 should exist")
dune_assert(TEST_EXISTS onemacrodyntest2_1_0001 MESSAGE "dynamicvariants: A test called onemacrodyntest2_1_0001 should exist")
dune_assert(TEST_EXISTS onemacrodyntest2_2_0000 MESSAGE "dynamicvariants: A test called onemacrodyntest2_2_0000 should exist")
dune_assert(TEST_EXISTS onemacrodyntest2_2_0001 MESSAGE "dynamicvariants: A test called onemacrodyntest2_2_0001 should exist")
dune_assert(TEST_EXISTS onemacrodyntest2_3_0000 MESSAGE "dynamicvariants: A test called onemacrodyntest2_3_0000 should exist")
dune_assert(TEST_EXISTS onemacrodyntest2_3_0001 MESSAGE "dynamicvariants: A test called onemacrodyntest2_3_0001 should exist")
