## HW 2

- Re-wrote data.lua into multiple Python files found in this [directory](../src/H2/main.py).
- The entry point of HW2 is the [main.py](../src/H2/main.py) file.
- Ran 4 test cases to see if functionality in python implementation matches lua script
- Created git workflow to run test cases and organized our github repository


### File structure

|File | Description |
|------|-------|
|col.py   | Generates NUM or SYM from column names as well as update columns with row details |
|config.py   | Houses global variable lists and the help string |
|data.py | Holder for Rows described as NUMs or SYMs |
|lists.py  | Has table adjustment methods like applying a function to a table or sorting the table |
|main.py | Runs the program and launches tests |
|num.py | Holds calculations to store, high/low numbers, average, standard deviation, and obtain a random number |
|numerics.py | Holds calculations to obtain a random number using a predefined seed |
|row.py | Representation of a record |
|sym.py | Holds light calculations for symbol attributes like average, diversity, and count |
|test.py | Has test functions to test our class functionality |
|utils.py | Misc. functions that describe cli functionality, csv reading, and casting strings to different types |

### Dataset

- We used [the following dataset](https://github.com/qchen59/ASE_2023Spring/blob/main/etc/data/auto93.csv) in our program
- This data represents vehicle data through attributes like cylinders, weight, acceleration, miles-per-gallon, volume, etc. 
- Attribute headers may also describe optimality based on the last character. Ex) Lbs- indicates Lbs should be minimized
