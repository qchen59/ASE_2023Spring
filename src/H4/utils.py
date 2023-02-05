import re
import sys
import config
from csv import reader
from lists import Lists
import re
import json
import data

l = Lists()

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

            # Orders data from (Lbs-, Acc+, Mpg+) to (Acc+, Lbs-, Mpg+)
            myDict = node["data"].stats("mid", node["data"].cols.y, nPlaces)
            myKeys = list(myDict.keys())
            myKeys.sort()
            sorted_dict = {i: myDict[i] for i in myKeys}
            print(sorted_dict)
        else:
            print("| " * lvl + str(len(node["data"].rows)) + " ")

        if "left" in node:
            show(node["left"], what, cols, nPlaces, lvl + 1)
        if "right" in node:
            show(node["right"], what, cols, nPlaces, lvl + 1)

def processLua(file):
    f = open(file, "r")
    # skip first line
    f.readline()
    f.readline()
    fs = f.read()
    fs = re.sub("\'", "\"", fs)
    fs = re.sub("=", ":", fs)
    fs = re.sub("{", "[", fs)
    fs = re.sub("}", "]", fs)
    fs = re.sub("_", "null", fs)
    fs = re.sub("\n]", "", fs)
    fs = re.sub("domain", "\"domain\"", fs)
    fs = re.sub("cols", "\"cols\"", fs)
    fs = re.sub("rows", "\"rows\"", fs)
    fs = "{" + fs + "}"
    # print(fs)
    fs = json.loads(fs)
    # print(fs)
    return fs

processLua("../../etc/data/repgrid1.csv")


def transpose(t):
    u = []
    for i in range(len(t[0])):
        u.append([])
        for j in range(len(t)):
            u[i].append(t[j][i])
    return u


def repRows(t, rows):
    rows = l.copy(rows)
    for j, s in enumerate(rows[-1]):
        rows[0][j] = rows[0][j]+':'+s
    rows[-1] = None
    for n, row in enumerate(rows):
        if n == 0:
            row.append("thingX")
        else:
            u = t.rows[len(t.rows) - n + 1]
            row.append(u[-1])

def repCols(cols):
    cols = l.copy(cols)
    for col in cols:
        col[-1] = str(col[0]) + ":" + str(col[-1])
        for j in range(1, len(col)-1):
            col[j-1] = col[j]

    def numPlusStr(k, v):
        return "Num" + str(k), None
    #insert into the cols table using helper function
    cols.insert(0, list(l.kap(cols[0], numPlusStr).values())[:-1]) # Need another way to insert() into list of cols
    cols[0][len(cols[0]) - 1] = "thingX"
    return data.Data(cols)


def repPlace( data, n, g, max_x, max_y, x, y, c):
    n, g = 20, {}
    g = [ [' ' for j in range(n+1)] for i in range(n+1)]
    max_y = 0
    print('')

    for r, row in enumerate(data['rows']):
        c = chr(64 + r)
        print(c, row['cells'][-1])
        x, y = int(row['x'] * n), int(row['y'] * n)
        max_y = max(max_y, y + 1)
        g[y + 1][x + 1] = c
    print('')

    for y in range(max_y):
        print(g[y])


def repGrid(sFile, table):
    # table = doFile(sFile)  -- Require a parsing function in utils.py that reads the repgrid1.csv file into a dict
    rows = repRows(table, transpose(table.cols))
    cols = repCols(table.cols)
    show(rows.cluster())
    show(cols.cluster())

    repPlace(rows)