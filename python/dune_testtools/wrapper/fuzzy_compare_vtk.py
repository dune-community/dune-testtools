""" A module for fuzzy comparing VTK files.

This module provides methods to compare two VTK files. Applicable
for all VTK style formats like VTK files. Fuzzy compares numbers by
using absolute and/or relative difference comparison.

"""
from __future__ import absolute_import
import argparse
import xml.etree.ElementTree as ET
from operator import attrgetter, itemgetter
import sys
from six.moves import range
from six.moves import zip


# fuzzy compare VTK tree from VTK strings
def compare_vtk(vtk1, vtk2, absolute=1e-9, relative=1e-2, verbose=True):
    """ take two vtk files and compare them. Returns an exit key as returnvalue.

    Arguments:
    ----------
    vtk1, vtk2 : string
        The filenames of the vtk files to compare

    Keyword Arguments:
    ------------------
    absolute : float
        The epsilon used for comparing numbers with an absolute criterion
    relative: float
        The epsilon used for comparing numbers with an relative criterion
    """

    # construct element tree from vtk file
    root1 = ET.fromstring(open(vtk1).read())
    root2 = ET.fromstring(open(vtk2).read())

    # sort the vtk file in case nodes appear in different positions
    # e.g. because of minor changes in the output code
    sortedroot1 = sort_vtk(root1)
    sortedroot2 = sort_vtk(root2)

    if verbose:
        print("Comparing {} and {}".format(vtk1, vtk2))

    # sort the vtk file so that the comparison is independent of the
    # index numbering (coming e.g. from different grid managers)
    sortedroot1, sortedroot2 = sort_vtk_by_coordinates(sortedroot1, sortedroot2, verbose)

    # do the fuzzy compare
    if is_fuzzy_equal_node(sortedroot1, sortedroot2, absolute, relative, verbose):
        return 0
    else:
        return 1


# fuzzy compare of VTK nodes
def is_fuzzy_equal_node(node1, node2, absolute, relative, verbose=True):

    is_equal = True
    for node1child, node2child in zip(node1.iter(), node2.iter()):
        if node1.tag != node2.tag:
            if verbose:
                print('The name of the node differs in: {} and {}'.format(node1.tag, node2.tag))
                is_equal = False
            else:
                return False
        if list(node1.attrib.items()) != list(node2.attrib.items()):
            if verbose:
                print('Attributes differ in node: {}'.format(node1.tag))
                is_equal = False
            else:
                return False
        if len(list(node1.iter())) != len(list(node2.iter())):
            if verbose:
                print('Number of children differs in node: {}'.format(node1.tag))
                is_equal = False
            else:
                return False
        if node1child.text or node2child.text:
            if not is_fuzzy_equal_text(node1child.text, node2child.text, node1child.attrib["Name"], absolute, relative, verbose):
                if node1child.attrib["Name"] == node2child.attrib["Name"]:
                    if verbose:
                        print('Data differs in parameter: {}'.format(node1child.attrib["Name"]))
                        is_equal = False
                    else:
                        return False
                else:
                    if verbose:
                        print('Comparing different parameters: {} and {}'.format(node1child.attrib["Name"], node2child.attrib["Name"]))
                        is_equal = False
                    else:
                        return False
    return is_equal


# fuzzy compare of text (in the xml sense) consisting of whitespace separated numbers
def is_fuzzy_equal_text(text1, text2, parameter, absolute, relative, verbose=True):
    list1 = text1.split()
    list2 = text2.split()
    # difference only in whitespace?
    if (list1 == list2):
        return True
    # compare number by number
    is_equal = True
    max_relative_difference = 0.0
    max_absolute_difference = 0.0
    for number1, number2 in zip(list1, list2):
        number1 = float(number1)
        number2 = float(number2)
        if not number2 == 0.0:
            # check for the relative difference
            if abs(abs(number1 / number2) - 1.0) > relative and not abs(number1 - number2) < absolute:
                if verbose:
                    # print('Relative difference is too large between: {} and {}'.format(number1, number2))
                    max_relative_difference = max(max_relative_difference, abs(abs(number1 / number2) - 1.0))
                    is_equal = False
                else:
                    return False
        else:
            # check for the absolute difference
            if abs(number1 - number2) > absolute:
                if verbose:
                    # print('Absolute difference is too large between: {} and {}'.format(number1, number2))
                    max_absolute_difference = max(max_absolute_difference, abs(number1 - number2))
                    is_equal = False
                else:
                    return False
    if verbose:
        if max_absolute_difference != 0.0:
            print('Maximum absolute difference for parameter {}: {}'.format(parameter, max_absolute_difference))
        if max_relative_difference != 0.0:
            print('Maximum relative difference for parameter {}: {:.2%}'.format(parameter, max_relative_difference))
    return is_equal


def sort_by_name(elem):
    name = elem.get('Name')
    if name:
        try:
            return str(name)
        except ValueError:
            return ''
    return ''


# sorts attributes of an item and returns a sorted item
def sort_attributes(item, sorteditem):
    attrkeys = sorted(item.keys())
    for key in attrkeys:
        sorteditem.set(key, item.get(key))


def sort_elements(items, newroot):
    items = sorted(items, key=sort_by_name)
    items = sorted(items, key=attrgetter('tag'))

    # Once sorted, we sort each of the items
    for item in items:
        # Create a new item to represent the sorted version
        # of the next item, and copy the tag name and contents
        newitem = ET.Element(item.tag)
        if item.text and item.text.isspace() == False:
            newitem.text = item.text

        # Copy the attributes (sorted by key) to the new item
        sort_attributes(item, newitem)

        # Copy the children of item (sorted) to the new item
        sort_elements(list(item), newitem)

        # Append this sorted item to the sorted root
        newroot.append(newitem)


# has to sort all Cell and Point Data after the attribute "Name"!
def sort_vtk(root):
    if(root.tag != "VTKFile"):
        print('Format is not a VTKFile. Sorting will most likely fail!')
    # create a new root for the sorted tree
    newroot = ET.Element(root.tag)
    # create the sorted copy
    # (after the idea of Dale Lane's xmldiff.py)
    sort_attributes(root, newroot)
    sort_elements(list(root), newroot)
    # return the sorted element tree
    return newroot


# sorts the data by point coordinates so that it is independent of index numbering
def sort_vtk_by_coordinates(root1, root2, verbose=True):
    if not is_fuzzy_equal_node(root1.find(".//Points/DataArray"), root2.find(".//Points/DataArray"), 1e-2, 1e-9, False):
        if verbose:
            print("Sorting vtu by coordinates...")
        for root in [root1, root2]:
            # parse all DataArrays in a dictionary
            pointDataArrays = []
            cellDataArrays = []
            dataArrays = {}
            numberOfComponents = {}
            for dataArray in root.findall(".//PointData/DataArray"):
                pointDataArrays.append(dataArray.attrib["Name"])
            for dataArray in root.findall(".//CellData/DataArray"):
                cellDataArrays.append(dataArray.attrib["Name"])
            for dataArray in root.findall(".//DataArray"):
                dataArrays[dataArray.attrib["Name"]] = dataArray.text
                numberOfComponents[dataArray.attrib["Name"]] = dataArray.attrib["NumberOfComponents"]

            vertexArray = []
            coords = dataArrays["Coordinates"].split()
            # group the coordinates into coordinate tuples
            dim = int(numberOfComponents["Coordinates"])
            for i in range(len(coords) // dim):
                vertexArray.append([float(c) for c in coords[i * dim: i * dim + dim]])

            # obtain a vertex index map
            vMap = []
            for idx, coords in enumerate(vertexArray):
                vMap.append((idx, coords))
            sortedVMap = sorted(vMap, key=itemgetter(1))
            vertexIndexMap = {}
            for idxNew, idxOld in enumerate(sortedVMap):
                vertexIndexMap[idxOld[0]] = idxNew

            # group the cells into vertex index tuples
            cellArray = []
            offsets = dataArrays["offsets"].split()
            connectivity = dataArrays["connectivity"].split()
            vertex = 0
            for cellIdx, offset in enumerate(offsets):
                cellArray.append([])
                for v in range(vertex, int(offset)):
                    cellArray[cellIdx].append(int(connectivity[v]))
                    vertex += 1

            # replace all vertex indices in the cellArray by the new indices
            for cell in cellArray:
                for idx, vertexIndex in enumerate(cell):
                    cell[idx] = vertexIndexMap[vertexIndex]

            # sort all data arrays
            for name, text in list(dataArrays.items()):
                # split the text
                items = text.split()
                # convert if vector
                num = int(numberOfComponents[name])
                newitems = []
                for i in range(len(items) // num):
                    newitems.append([i for i in items[i * num: i * num + num]])
                items = newitems
                # sort the items: we have either vertex or cell data
                if name in pointDataArrays:
                    sortedItems = [j for (i, j) in sorted(zip(vertexArray, items), key=itemgetter(0))]
                elif name in cellDataArrays or name == "types":
                    sortedItems = [j for (i, j) in sorted(zip(cellArray, items), key=itemgetter(0))]
                elif name == "offsets":
                    sortedItems = []
                    counter = 0
                    for cell in sorted(cellArray):
                        counter += len(cell)
                        sortedItems.append([str(counter)])
                elif name == "Coordinates":
                    sortedItems = sorted(vertexArray)
                elif name == "connectivity":
                    sortedItems = sorted(cellArray)

                # convert the sorted arrays to a xml text
                dataArrays[name] = ""
                for i in sortedItems:
                    for j in i:
                        dataArrays[name] += str(j) + " "

            # do the replacement in the actual elements
            for dataArray in root.findall(".//DataArray"):
                dataArray.text = dataArrays[dataArray.attrib["Name"]]

    return (root1, root2)


# main program if called as script return appropriate error codes
if __name__ == "__main__":
    # handle arguments and print help message
    parser = argparse.ArgumentParser(description='Fuzzy compare of two VTK\
        (Visualization Toolkit) files. The files are accepted if for every\
        value the difference is below the absolute error or below the\
        relative error or below both.')
    parser.add_argument('vtk_file_1', type=str, help='first file to compare')
    parser.add_argument('vtk_file_2', type=str, help='second file to compare')
    parser.add_argument('-r', '--relative', type=float, default=1e-2, help='maximum relative error (default=1e-2)')
    parser.add_argument('-a', '--absolute', type=float, default=1e-9, help='maximum absolute error (default=1e-9)')
    parser.add_argument('-v', '--verbose', type=bool, default=True, help='verbosity of the script')
    args = vars(parser.parse_args())

    sys.exit(compare_vtk(args["vtk_file_1"], args["vtk_file_2"], args["absolute"], args["relative"], args["verbose"]))
