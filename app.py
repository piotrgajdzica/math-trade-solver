import argparse
import json

from flask import Flask, request

from solver.ilp import build_ilp, solve
from solver.trade_solver import solve_trade, build_graph
from solver.graph_api_parser import parse
import solver.settings as settings

app = Flask(__name__)

secret_token = "MathandelSecret$!"
@app.route('/solve/', methods=['POST'])
def api_solve():

    try:
        token = request.headers['Authorization'].split("Bearer ")[1]
        print(token)
        if token != secret_token:
            return "", 401
    except (KeyError, IndexError):
        return "", 401
    string_graph = parse(request.json)
    G = build_graph(string_graph)
    model = build_ilp(G)
    result = solve(model)

    d = {}

    for var in result.variables():
        if var.varValue == 1:
            print(var.name)
            _, vertex1, vertex2 = var.name.split("_")
            d[vertex1] = vertex2

    ret_json = []
    for key in filter(lambda el: el.startswith(settings.element_prefix), d.keys()):
        el = d[key]
        while el.startswith(settings.group_prefix):
            el = d[el]
        ret_json.append({"receiver": key[len(settings.element_prefix):], "sender": el[len(settings.element_prefix):]})
    return json.dumps(ret_json)

@app.route('/', methods=['GET'])
def hello():
    return "hello"


if __name__ == '__main__':
    app.run(host='0.0.0.0')
