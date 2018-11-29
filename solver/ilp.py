from pulp import *
from collections import defaultdict
import solver.settings as settings
from collections import defaultdict

from pulp import *


def build_ilp(G, predicate = lambda vertex: vertex.startswith(settings.element_prefix)):
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
            if predicate(vertex2):
                max_sum += e

    for vertex in G.keys():
        if vertex_in[vertex]:
            model += vertex_in[vertex] <= 1
        if vertex_out[vertex]:
            model += vertex_out[vertex] <= 1
        if vertex_diff[vertex]:
            model += vertex_diff[vertex] == 0
    print(type(max_sum))
    model += max_sum

    return model


def solve(model):
    model.solve()
    # model.solve(GLPK())
    # model.solve(CPLEX())
    return model
