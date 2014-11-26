""" define tools for parsing Dune-style ini files into python

TODO:
- allow values to be lists (as obtained by Dune::FieldVector)
"""

# inspired by http://www.decalage.info/fr/python/configparser

def parse_ini_file(filename, commentChar=("#",), assignment="=", asStrings=False, conversionList=(int, float,)):
    """ parse Dune style .ini files into a dictionary
       
    The parser behaviour can be customized by the keyword arguments of this function.
    The dictionary contains nested dictionaries according to nested subgroups in the
    ini file.
        
    Keyword arguments:
    ------------------
    commentChar: list
        A list of characters that define comments. Everything on a line
        after such character is ignored during the parsing process.
    assignment : string
        A string that separates the key from the value on a line
        containing a key/value pair.
    asStrings : bool
        Whether the values should be treated as strings.
    conversionList : list
        A list of functions to try for converting the parsed strings to other types
        The order of the functions defines the priority of the conversion rules
        (highest priority first). All conversion rules are expected to raise
        a ValueError when they are not applicable.
    """
    result_dict = {}
    f = open(filename)
    current_dict = result_dict
    for line in f:
        # strip the endline character
        line = line.strip("\n")
            
        # strip comments from the line
        for char in commentChar:
            if char in line:
                line, comment = line.split(char, 1)

        # check whether this line specifies a group
        if ("[" in line) and ("]" in line):
            # reset the current dictionary
            current_dict = result_dict
       
            # isolate the group name
            group, bracket = line.split("]", 1)
            bracket, group = group.split("[", 1)
            group = group.strip(" ")

            # process the stack of subgroups given
            while "." in group:
                subgroup, group = group.split(".", 1)
                if subgroup not in current_dict:
                    current_dict[subgroup] = {}
                current_dict = current_dict[subgroup]
                 
            # add a new dictionary for the group name and set the current dict to it
            if group not in current_dict:
                current_dict[group] = {}
            current_dict = current_dict[group]

        # save the current_dict to reset it after each key/value pair evaluation
        # this is necessary to have some subgroup definitions in keys instead of in square brackets.
        group_dict = current_dict

        # check whether this line defines a key/value pair
        # only process if the assignment string is found exactly once
        # 0 => no relevant assignment 2=> this is actually an assignment with a more complicated operator
        if line.count(assignment) is 1:
            # split key from value
            import re
            key, value = re.split(assignment, line)

            # look for additional groups in the key
            key = key.strip()
            while "." in key:
                group, key = key.split(".")
                if group not in current_dict:
                    current_dict[group] = {}
                current_dict = current_dict[group]

            # strip blanks from the value
            value = value.strip()

            # set the dictionary entry for this pair to the default string
            current_dict[key] = value

            # check whether a given conversion applies to this key
            if not asStrings:
                # iterate over the list of conversion functions in reverse priority order
                for rule in [x for x in reversed(conversionList)]:
                    try:
                        current_dict[key] = rule(value)
                    except ValueError:
                        pass

        # restore the current dictionary to the current group
        current_dict = group_dict
                        
    return result_dict
        
