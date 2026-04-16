import networkx as nx

def create_graph():
    G = nx.Graph()

    edges = [
        (0,1,2),(1,2,3),(2,3,2),(0,4,1),
        (4,5,2),(5,3,3),(3,6,5),(6,7,2),
        (2,7,3)
    ]

    for u,v,w in edges:
        G.add_edge(u, v, weight=w)

    return G
