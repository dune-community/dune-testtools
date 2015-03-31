"""Test for the convergence test metaini python module"""
from convergencetest_metaini import *

def test_extract_convergence_test_info():
    tests = extract_convergence_test_info("./tests/convtest.ini")
    # the meta ini file should yield 4 different convergence tests
    assert(len(tests) == 4)
    for configuration in tests:
        # each having a list of four different configurations (e.g. 4 refinements)
        assert(len(configuration) == 4)
