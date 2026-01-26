import matplotlib.pyplot as plt
import networkx as nx
import re
import sys
import os

def parse_nam_file(filename):
    edges = []
    # This searches for the flags anywhere in the 'l' (link) line.
    s_re = re.compile(r"-s\s+(\d+)") # -s is the source node
    d_re = re.compile(r"-d\s+(\d+)") # -d is the destination node
    r_re = re.compile(r"-r\s+(\d+)") # -r is the bandwidth in bits per second
    D_re = re.compile(r"-D\s+([\d\.]+)") # -D is the delay in seconds

    if not os.path.exists(filename):
        print(f"Error: Could not find '{filename}'.")
        return []

    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('l '):
                s_match = s_re.search(line)
                d_match = d_re.search(line)
                r_match = r_re.search(line)
                D_match = D_re.search(line)
                
                if s_match and d_match:
                    src = s_match.group(1)
                    dst = d_match.group(1)
                    
                    label = ""
                    if r_match and D_match:
                        rate_mbps = int(r_match.group(1)) / 1_000_000
                        delay_ms = float(D_match.group(1)) * 1000
                        label = f"{int(rate_mbps)}Mbps\n{int(delay_ms)}ms"
                    
                    edge = tuple(sorted([f"n{src}", f"n{dst}"]))
                    edges.append((edge[0], edge[1], {'label': label}))
    
    # Remove duplicates from bi-directional link entries
    unique_edges = list({(e[0], e[1]): e for e in edges}.values())
    return unique_edges

def draw_topology_from_nam(nam_file, output_file="topology.png"):
    edges = parse_nam_file(nam_file)
    
    if not edges:
        print(f"Error: No topology data found in {nam_file}. Check if the file is empty.")
        return

    G = nx.Graph()
    G.add_edges_from(edges)

    # Use a fixed layout or shell layout to better approximate your diagram
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, k=1.0, iterations=100)

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=3000, node_color='white', edgecolors='black', linewidths=2)
    nx.draw_networkx_labels(G, pos, font_size=14, font_weight='bold')

    # Draw edges
    nx.draw_networkx_edges(G, pos, width=2, edge_color='black')
    
    # Draw edge labels (Bandwidth/Delay)
    edge_labels = {(u, v): d['label'] for u, v, d in G.edges(data=True) if 'label' in d}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, font_color='blue')

    plt.title(f"Generated Network Topology", pad=20, fontsize=16)
    plt.axis('off')
    
    # Save in the same directory as the input NAM file
    output_path = os.path.join(os.path.dirname(os.path.abspath(nam_file)), output_file)
    plt.tight_layout()
    plt.savefig(output_path)
    print(f"Success! Diagram saved to: {output_path}")

if __name__ == "__main__":
    nam_path = sys.argv[1] if len(sys.argv) > 1 else "out.nam"
    draw_topology_from_nam(nam_path)