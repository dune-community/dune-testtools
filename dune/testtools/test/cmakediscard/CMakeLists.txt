set(MYPARAM 0)
set(MYOTHERPARAM 1)

dune_add_system_test(SOURCE test.cc
                     INIFILE discard.mini
                     BASENAME dt1
                     CREATED_TARGETS ct1
                    )

dune_assert(LIST_LENGTH ct1 1 MESSAGE "Error in discard test 1")

set(MYOTHERPARAM 0)

dune_add_system_test(SOURCE test.cc
                     INIFILE discard2.mini
                     BASENAME dt2
                     CREATED_TARGETS ct2
                    )

dune_assert(LIST_LENGTH ct2 0 MESSAGE "Error in discard test 2")
