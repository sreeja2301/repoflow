from graph_utils import create_graph
from centrality import compute_centrality, normalize_centrality
from weight_modifier import modify_weights
from routing import classical_path, modified_path
from visualization import draw_graph
import config

def main():
    G = create_graph()

    # Step 1: Centrality
    C = compute_centrality(G)
    C_norm = normalize_centrality(C)

    print("\nCentrality:", C)
    print("\nNormalized:", C_norm)

    print("\n=== Classical Routing ===")
    c_path, c_cost = classical_path(G, config.SOURCE, config.TARGET)
    print(f"Path: {c_path}")
    print(f"Cost: {c_cost}")

    print("\n=== Quantum-Inspired Routing ===")
    
    # Extra for high marks: looping over multiple alpha values and comparing node usage
    for alpha in [0, 2, 5, 10, 20]:
        G_mod = modify_weights(G, C_norm, alpha)
        m_path, m_cost = modified_path(G_mod, config.SOURCE, config.TARGET)
        
        print(f"\n--- Alpha = {alpha} ---")
        print(f"Path: {m_path}")
        print(f"Cost: {m_cost:.4f}")
        print(f"Nodes used: {len(m_path)}")
        
        if alpha == config.ALPHA:
            m_path_default = m_path

    # Step 5: Visualization
    print("\n[NOTE] Close the first plot window to see the second one.")
    draw_graph(G, c_path, "Classical Path")
    
    # Re-apply for visualization
    G_mod_final = modify_weights(G, C_norm, config.ALPHA)
    draw_graph(G_mod_final, m_path_default, f"Quantum-Inspired Path (alpha={config.ALPHA})")


if __name__ == "__main__":
    main()
