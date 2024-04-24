import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

G = nx.Graph()
color_map = []

color_idx = 0
for p in os.listdir('.'):
    if not p.startswith('data_nodes') or p.startswith('.'):
        continue
    df_node = pd.read_csv(p)
    id_col = "Manuscript Id"
    assert id_col in df_node.columns, "Id column not found"
    assert "Title" in df_node.columns, "Title column not found"
    group_nodes = []
    for i, row in df_node.iterrows():
        G.add_node(row[id_col], label=row['Title'])
        color_map.append(color_idx)
        for node in group_nodes:
            G.add_edge(row[id_col], node)
        group_nodes.append(row[id_col])
    color_idx += 1
nodes = set(G.nodes)

df_links = pd.read_csv('data_links.csv')
for i, row in df_links.iterrows():
    assert row['Id 1'] in nodes, f"Source {row['Id 1']} not found in nodes"
    assert row['Id 2'] in nodes, f"Target {row['Id 2']} not found in nodes"
    G.add_edge(row['Id 1'], row['Id 2'])


nx.draw(G, nx.spring_layout(G, seed=7), with_labels=True, node_color=color_map)
plt.savefig('graph.pdf')
