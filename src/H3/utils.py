import re
import sys
import config
from csv import reader


def eg(key, str, fun):
    config.egs[key] = fun
    config.help += "  -g  {}\t{}\n".format(key, str)


def coerce(s: str):
    try:
        # check if boolean true
        if s.lower() == 'true':
            return True
        # check if boolean false
        elif s.lower() == 'false':
            return False
        try:
            # cast to int
            return int(s)
        except Exception as e:
            try:
                # cast to float
                return float(s)
            except Exception as e:
                # remove whitespaces
                return s.strip()
    except Exception as e:
        # any other exception, return as is
        return s


def settings(s):
    t = {}
    result = re.findall("[\n]\s*[-]\S+\s*[-][-](\S+)[^=]*[=]\s*(\S+)", s)
    for k, v in result:
        t[k] = v
    return t


# update key,val in `t` from command-line flags


def cli(options):
    for k, v in options.items():
        for n, x in enumerate(sys.argv):
            # If the command line argument equals to the option
            if x == "-" + k[0] or x == "--" + k:
                if v == "false":
                    v = "true"
                elif v == "true":
                    v = "false"
                else:
                    v = sys.argv[n + 1]
        options[k] = coerce(v)
    return options


# Read a csv file and apply the function 'fun' to the rowTable
def csv(sFilename, fun):
    src = open(sFilename, 'r')
    r = reader(src)
    for row in r:
        # For each cell in the row, clean it with coerce and append it to the rowTable
        rowTable = [coerce(cell) for cell in row]
        fun(rowTable)
    src.close()


# prints the tree generated from `DATA:tree`
def show(node, what, cols, nPlaces, lvl=None):
    if node:
        lvl = lvl or 0
        if "left" not in node or lvl == 0:
            print("| " * lvl + str(len(node["data"].rows)) + " ", end="")
            print(node["data"].stats("mid", node["data"].cols.y, nPlaces))
        else:
            print("| " * lvl + str(len(node["data"].rows)) + " ")
            
        if "left" in node:
            show(node["left"], what, cols, nPlaces, lvl + 1)

        if "right" in node:
            show(node["right"], what, cols, nPlaces, lvl + 1)


def returnHandler(value, n=1):
    # for None
    if value is None:
        return [None]*n

    # for list, set, dict, tuple
    if type(value) in [list, set, dict, tuple]:
        values_to_return = []
        remaining = n
        if n <= len(value):
            values_to_return = [value]
            remaining -= 1

        if remaining != 0:
            while remaining != 0:
                values_to_return.append(None)
                remaining -= 1

        return values_to_return

    values_to_return = [value]
    remaining = n-1
    # for others (int,str,etc)
    if remaining != 0:
        while remaining != 0:
            values_to_return.append(None)
            remaining -= 1
