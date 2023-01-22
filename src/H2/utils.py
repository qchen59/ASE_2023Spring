import re
import sys
from config import egs, help


def eg(key, str, fun):
    global help
    egs[key] = fun
    help += "  -g  {}\t{}\n".format(key, str)


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
    reader = csv.reader(src)
    for row in reader:
        # For each cell in the row, clean it with coerce and append it to the rowTable 
        rowTable = [coerce(cell) for cell in row]
        fun(rowTable)
    src.close()
    
