import matplotlib.pyplot as plt
import networkx as nx

def draw_graph(G, path=None, title="Graph"):
    pos = nx.spring_layout(G)

    edge_labels = nx.get_edge_attributes(G, 'weight')

    nx.draw(G, pos, with_labels=True, node_color='lightblue')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    if path:
        edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color='red', width=3)

    plt.title(title)
    plt.show()
