# math-trade-solver

## Description

Solver for Math Trade problem. As input it takes a file with list of preferences link in example
and returns list of preferences to output file.

## Requirements

Python 3

## Dependencies Installation

```
pip install pulp
```

## Usage

from command line:
```
python trade_solver.py [-h] [-f FILENAME] [-v {0,1,2}]

optional arguments:
  -h, --help            show this help message and exit
  -f FILENAME, --filename FILENAME
                        trade preferences file
  -v {0,1,2}, --verbosity {0,1,2}
                        increase output verbosity
```
as a server:
```
pip install flask
flask run
```
server will be deployed on http://127.0.0.1:5000/