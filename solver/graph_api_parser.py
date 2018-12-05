from functools import reduce
import solver.settings as settings
from solver.exceptions import ApiException


def replace_inner_groups(groups, group, depth, max_depth):
    if depth < max_depth:
        again = False
        new_groups = []
        for index in range(len(group["groups"])):

            preference_group_id = group["groups"][index]
            preference_group = next(x for x in groups if str(x["id"]) == str(preference_group_id))
            group["single_preferences"] += preference_group["single_preferences"]
            new_groups += preference_group["groups"]
            again = True
        group["groups"] = list(set(new_groups))
        group["single_preferences"] = list(set(group["single_preferences"]))

        if again:
            replace_inner_groups(groups, group, depth + 1, max_depth)


def parse(json):
    try:
        groups = json["named_groups"]
        preferences = json["preferences"]
    except KeyError as e:
        groups = []
        preferences = []
    for group in groups:
        try:
            replace_inner_groups(groups, group, 0, 3)
        except StopIteration:
            raise ApiException("wrong group id given in named groups")
    try:
        res = ""
        for el in preferences:
            res += settings.element_prefix + str(el["id"]) + "\n"
            res += reduce(lambda acc, next: str(acc) + " " + settings.element_prefix + str(next), el["single_preferences"], "")[1:]
            res += reduce(lambda acc, next: str(acc) + " " + settings.group_prefix + str(next), el["groups"], "") + "\n"

        for el in groups:
            res += settings.group_prefix + str(el["id"]) + "\n"
            res += reduce(lambda acc, next: str(acc) + " " + settings.element_prefix + str(next), el["single_preferences"], "")[1:] + "\n"
    except KeyError as e:
        raise ApiException("missing key in json: " + str(e))
    print(res)
    return res


def build_graph(input):
    # print(input)
    res = {}
    vertex = True
    vertex_id = None
    for line in input.split("\n"):
        if vertex and line:
            vertex_id = int(line)
        elif vertex:
            continue
        elif line:
            res[vertex_id] = set(map(lambda el: el, line.split(" ")))
        else:
            res[vertex_id] = []
        vertex = not vertex

    return res
