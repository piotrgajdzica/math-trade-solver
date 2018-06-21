from functools import reduce


def flatMap(l):
    flat_map = []
    for el in l:
        if isinstance(el, list):
            flat_map += flatMap(el)
        else:
            flat_map.append(el)
    return flat_map


def parse(filename):

    lines = map(lambda s: "".join(filter(lambda c: c not in ";:", s)), open(filename, encoding='UTF-8').readlines())
    exchanges = {}
    groups = {}
    deep_groups = {}
    user_map = {}
    for line in lines:
        try:
            username, exchange = line.split(")")
            id, *l = exchange.split()
            if username.startswith("("):
                if not id.isdigit():
                    if not all(map(lambda e: e.isdigit(), l)):
                        deep_groups[username + id] = list(map(lambda el: username + el if "%" in el else el, l))
                    else:
                        groups[username + id] = list(map(lambda el: username + el if "%" in el else el, l))
                else:
                    user_map[id] = username[1:]
                    exchanges[id] = list(map(lambda el: username + el if not el.isdigit() else el, l))
        except ValueError:
            pass

    for deep_group in deep_groups.keys():
        for exchange in exchanges.keys():
            while deep_group in exchanges[exchange]:
                exchanges[exchange].remove(deep_group)
                exchanges[exchange] += deep_groups[deep_group]

    id = 100000
    for group in groups.keys():
        id += 1
        for exchange in exchanges.keys():
            while group in exchanges[exchange]:
                exchanges[exchange].remove(group)
                exchanges[exchange].append(str(id))
        exchanges[id] = groups[group]

    for exchange in exchanges.keys():
        exchanges[exchange] = list(filter(lambda el: el.isdigit(), exchanges[exchange]))

    res = ""
    for key in exchanges.keys():
        res += str(key) + "\n"
        res += reduce(lambda acc, next: str(acc) + " " + str(next), exchanges[key], "")[1:] + "\n"
    return res, user_map


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
            res[vertex_id] = set(map(lambda el: int(el), line.split(" ")))
        else:
            res[vertex_id] = []
        vertex = not vertex

    return res
