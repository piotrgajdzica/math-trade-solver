from solver.graph_parser import *
from solver.ilp import build_ilp, solve
import time
import argparse


def print_time(t, message, verbosity):
    now = time.time()
    if verbosity >= 2:
        print(message + " took " + str(now - t) + "s")
    return now


def solve_trade(filename, verbosity):
    ret = ""
    start = time.time()
    string_graph, user_map = parse(filename)
    t = print_time(start, "parsing graph", verbosity)
    G = build_graph(string_graph)
    t = print_time(t, "building graph", verbosity)
    model = build_ilp(G)
    t = print_time(t, "building ilp", verbosity)
    result = solve(model)
    t = print_time(t, "solving ilp", verbosity)
    print_time(start, "whole program", verbosity)

    print("\n\nOptimal results: \n")

    d = {}

    for var in result.variables():
        if var.varValue == 1:
            _, vertex1, vertex2 = var.name.split("_")
            d[vertex1] = vertex2

    output = open(filename.split(".")[0] + "_output.txt", 'w')
    for key in filter(lambda el: int(el) < 100000, d.keys()):
        el = d[key]
        while int(el) > 100000:
            el = d[el]
        if verbosity >= 1:
            print(user_map[key] + " receives " + el + " from " + user_map[el])
            ret += user_map[key] + " receives " + el + " from " + user_map[el] + "\n"
        output.write(user_map[key] + " receives " + el + " from " + user_map[el] + "\n")
    return ret


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", type=str,
                        help="trade preferences file", default=r"C:\Users\piotrek\Desktop\inf\inżynierka\math-trade-solver\example_preferences\mathandel_30.txt")
    parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2],
                        help="increase output verbosity", default=2)
    args = parser.parse_args()
    solve_trade(args.filename, args.verbosity)
