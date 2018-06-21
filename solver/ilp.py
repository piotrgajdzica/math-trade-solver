

from functools import reduce
from pulp import *
from collections import defaultdict


def build_ilp(G):

    model = LpProblem("solver", LpMaximize)

    vertex_in = defaultdict(lambda: None)
    vertex_out = defaultdict(lambda: None)
    vertex_diff = defaultdict(lambda: None)
    max_sum = None
    for vertex1 in G.keys():
        for vertex2 in G[vertex1]:
            e = LpVariable("e_" + str(vertex1) + "_" + str(vertex2), cat="Binary")
            vertex_out[vertex1] += e
            vertex_in[vertex2] += e
            vertex_diff[vertex1] += e
            vertex_diff[vertex2] -= e
            if vertex2 < 100000:
                max_sum += e

    for vertex in G.keys():
        if vertex_in[vertex]:
            model += vertex_in[vertex] <= 1
        if vertex_out[vertex]:
            model += vertex_out[vertex] <= 1
        if vertex_diff[vertex]:
            model += vertex_diff[vertex] == 0
    model += max_sum

    return model

def solve(model):

    # choose an algorithm to solve
    # model.solve()
    # these require installation
    model.solve(GLPK())
    # model.solve(CPLEX())

    # print(LpStatus[model.status])
    #
    # print(value(model.objective))
    #
    # print(LpStatus[model.status])

    return model