from graph_parser import *
from ilp import build_ilp, solve
import time


def print_time(t, message):
    now = time.time()
    print(message + " took " + str(now - t) + "s")
    return now


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filename", type=str,
                    help="increase output verbosity", default="mathandel_30.txt")
args = parser.parse_args()

start = time.time()
string_graph = parse(args.filename)
t = print_time(start, "parsing graph")
G = build_graph(string_graph)
t = print_time(t, "building graph")
model = build_ilp(G)
t = print_time(t, "building ilp")
result = solve(model)
t = print_time(t, "solving ilp")
print_time(start, "whole program")

print("\n\nOptimal results: \n")

d = {}

for var in result.variables():
    if var.varValue == 1:
        _, vertex1, vertex2 = var.name.split("_")
        d[vertex1] = vertex2

for key in filter(lambda el: int(el) < 100000, d.keys()):
    el = d[key]
    while int(el) > 100000:
        el = d[el]
    print(key + " receives " + el)
