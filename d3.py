import os
import pandas as pd
from d3graph import d3graph
import networkx as nx
import matplotlib.pyplot as plt


def build_graph():
    G = nx.Graph()

    c_map = plt.get_cmap('tab20')
    colors_map = {i: c_map(i) for i in range(20)}
    colors_map = {i: f"#{int(c[0] * 255):02x}{int(c[1] * 255):02x}{int(c[2] * 255):02x}" for i, c in colors_map.items()}

    color_idx = 0
    for p in os.listdir('data'):
        if not p.startswith('nodes') or p.startswith('.'):
            continue
        df_node = pd.read_csv(f'data/{p}')
        id_col = "Manuscript Id"
        assert id_col in df_node.columns, "Id column not found"
        assert "Title" in df_node.columns, "Title column not found"
        group_nodes = []
        for i, row in df_node.iterrows():
            label = " ".join(row[id_col].split("_")[1:]).capitalize()
            title = row['Title']
            abstract = row['Abstract']
            color = colors_map[color_idx % 20]
            G.add_node(row[id_col], label=label, title=title, abstract=abstract, color=color)
            for node in group_nodes:
                G.add_edge(row[id_col], node, label="Inner")
            group_nodes.append(row[id_col])
        color_idx += 1
    nodes = set(G.nodes)

    df_links = pd.read_csv('data/links.csv')
    for i, row in df_links.iterrows():
        if row['Id 1'] not in nodes:
            print(f"Source {row['Id 1']} not found in nodes")
            continue
        if row['Id 2'] not in nodes:
            print(f"Target {row['Id 2']} not found in nodes")
            continue
        G.add_edge(row['Id 1'], row['Id 2'], label="Outer")

    # Obtain adjacency matrix
    return G


def show_graph(G):
    # Initialize from adjacency matrix (obtained from G)
    d3 = d3graph()
    d3.graph(nx.to_pandas_adjacency(G))

    # Node properties
    nodelist = d3.adjmat.columns.tolist()
    node_labels = [G.nodes[n]['label'] for n in nodelist]
    node_colors = [G.nodes[n]['color'] for n in nodelist]
    node_tooltips = [G.nodes[n]['title'] for n in nodelist]
    d3.set_node_properties(label=node_labels, color=node_colors, tooltip=node_tooltips)

    # Plot
    outpath = 'd3graph.html'
    d3.show(filepath=f'./{outpath}', showfig=False, show_slider=False)
    print(f'Graph saved in {outpath}')
    # Remove the sentence below to remove adds
    r = "<script async src='https://media.ethicalads.io/media/client/ethicalads.min.js'></script>"
    with open(outpath, 'r') as f:
        lines = f.readlines()
        lines = [l for l in lines if r not in l]
    with open(outpath, 'w') as f:
        f.writelines(lines)


if __name__ == '__main__':
    graph = build_graph()
    show_graph(graph)
