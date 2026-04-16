import networkx as nx

def classical_path(G, source, target):
    path = nx.shortest_path(G, source, target, weight='weight')
    cost = nx.shortest_path_length(G, source, target, weight='weight')
    return path, cost


def modified_path(G, source, target):
    path = nx.shortest_path(G, source, target, weight='modified_weight')
    cost = nx.shortest_path_length(G, source, target, weight='modified_weight')
    return path, cost
