from __future__ import absolute_import
from .parser import CommandToApply
from .metaini import expand_meta_ini
from .cmakeoutput import printForCMake
from .command import apply_commands, CommandType
from .uniquenames import *
import sys
import argparse


def extract_static_info(metaini):
    static_section = expand_meta_ini(metaini, whiteFilter=("__static", "__exec_suffix"), addNameKey=False)

    # make the found exec suffixes unique
    if "__exec_suffix" not in static_section[0]:
        static_section[0]["__exec_suffix"] = ""
    cmd = [CommandToApply(name="unique", args=[], key="__exec_suffix")]
    apply_commands(static_section, cmd)

    # construct a dictionary from the static information. This can be passed to CMake
    static = {}
    # we need a list of extracted compile definitions names
    static["__COMPILE_DEFINITIONS"] = []
    # The special key __CONFIGS holds a list of configuration names
    static["__CONFIGS"] = []

    # extract the data from the configurations
    for conf in static_section:
        static["__CONFIGS"].append(conf["__exec_suffix"])

        # copy the entire data
        if "__static" in conf:
            for key in conf["__static"]:
                if key not in static["__COMPILE_DEFINITIONS"]:
                    static["__COMPILE_DEFINITIONS"].append(key)

            static[conf["__exec_suffix"]] = conf["__static"]

    return static


if __name__ == "__main__":
    # read command line options
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ini', help='The meta-inifile to expand', required=True)
    args = vars(parser.parse_args())

    # call the macro
    static = extract_static_info(args["ini"])

    # print to CMake
    printForCMake(static)