# Global Variable List
the = {'seed': 937162211,
       'bins': 16,
       'cliffs': 0.147,
       'd': 0.35,
       'file': '../../etc/data/project/auto93.csv',
       'Far': 0.95,
       'go': 'all',
       'help': False,
       'Halves': 512,
       'min': 0.5,
       'Max': 512,
       'p': 2,
       'rest': 4,
       'Reuse': True}
# the help description
help = """
script.py : an example script with help text and a test suite
USAGE:   script.py  [OPTIONS] [-g ACTION]
OPTIONS:
  -b  --bins    initial number of bins       = 16
  -c  --cliffs  cliff's delta threshold      = .147
  -d  --d       different is over sd*d       = .35
  -f  --file    data file                    = ../../etc/data/auto93.csv
  -F  --Far     distance to distant          = .95
  -g  --go      start-up action              = nothing
  -h  --help    show help                    = false
  -H  --Halves  search space for clustering  = 512
  -m  --min     size of smallest cluster     = .5
  -M  --Max     numbers                      = 512
  -p  --p       dist coefficient             = 2
  -r  --rest    how many of rest to sample   = 4
  -R  --Reuse   child splits reuse a parent pole = true
  -s  --seed    random number seed           = 937162211
ACTIONS:
"""
# Test cases
egs = {}
