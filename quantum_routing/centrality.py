import networkx as nx

def compute_centrality(G):
    return nx.betweenness_centrality(G, normalized=True)

def normalize_centrality(C):
    min_c = min(C.values())
    max_c = max(C.values())

    norm = {}
    for node in C:
        if max_c - min_c == 0:
            norm[node] = 0
        else:
            norm[node] = (C[node] - min_c) / (max_c - min_c)
    return norm
