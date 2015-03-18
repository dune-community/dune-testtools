from metaIni import *

def test_metaini1():
    configs = expand_meta_ini("./tests/metaini1.mini")
    assert(len(configs) == 72)

    configs = expand_meta_ini("./tests/metaini1.mini", filterKeys=("g",))
    assert(len(configs) == 12)
    
    configs = expand_meta_ini("./tests/metaini1.mini", filterKeys=("g", "a"))
    assert(len(configs) == 24)
    
# TODO fails, but I think it should not!
#     configs = expand_meta_ini("./tests/metaini1.mini", filterKeys=("a",))
#     assert(len(configs) == 2)

    configs = expand_meta_ini("./tests/metaini1.mini", assignment="=1=")
    # Nota bene: With =1= being the assignment, nothing gets expanded, so its only 1 config!
    assert(len(configs) == 1)

def test_metaini2():
    configs = expand_meta_ini("./tests/metaini2.mini")
    assert(len(configs) == 24)