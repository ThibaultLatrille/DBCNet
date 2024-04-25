import os
import pandas as pd
import networkx as nx
from d3graph import d3graph
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
            label = " ".join(row[id_col].split("_")[1:])
            if label.lower() == label:
                label = label.capitalize()
            title = row['Title']
            abstract = row['Abstract']
            color = colors_map[color_idx % 20]
            keywords = []
            if str(row['Keywords']) != "nan":
                keywords = row['Keywords'].replace("\n", ", ").replace(";", ", ").split(",")
                keywords = [k.strip() for k in keywords if len(k.strip()) > 0]
            link = row['Link']
            G.add_node(row[id_col], label=label, title=title, abstract=abstract, color=color, keywords=keywords,
                       link=link)
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


def save_d3(G):
    # Initialize from adjacency matrix (obtained from G)
    d3 = d3graph(support=True)
    d3.graph(nx.to_pandas_adjacency(G))

    # Node properties
    nodelist = d3.adjmat.columns.tolist()
    node_labels = [G.nodes[n]['label'] for n in nodelist]
    node_colors = [G.nodes[n]['color'] for n in nodelist]
    node_tooltips = [G.nodes[n]['title'] for n in nodelist]

    d3.set_node_properties(label=node_labels, color=node_colors, tooltip=node_tooltips,
                           size=4, opacity=1.0, fontsize=6)

    outpath = 'DBCNetwork.html'
    d3.show(filepath=f'./{outpath}', showfig=False, show_slider=False)
    print(f'Graph saved in {outpath}')


def save_nx(G):
    plt.figure(figsize=(10, 10))
    pos = nx.spring_layout(G)
    node_colors = [G.nodes[n]['color'] for n in G.nodes]
    labels = {n: G.nodes[n]['label'] for n in G.nodes}
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=1000, edge_color='k', linewidths=1,
            font_size=10, font_color='black', font_weight='bold', alpha=0.7, edgecolors='k', labels=labels)
    plt.axis('off')
    plt.savefig('DBCNetwork.pdf')


if __name__ == '__main__':
    graph = build_graph()
    save_nx(graph)
    save_d3(graph)
