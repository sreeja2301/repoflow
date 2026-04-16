def modify_weights(G, C_norm, alpha):
    G_mod = G.copy()

    for u, v, data in G_mod.edges(data=True):
        original_weight = data['weight']
        penalty = alpha * (C_norm[v] ** 2)

        data['modified_weight'] = original_weight + penalty

    return G_mod
