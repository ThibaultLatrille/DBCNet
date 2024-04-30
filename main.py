import os
import pandas as pd
import networkx as nx
from d3graph import d3graph
import matplotlib.pyplot as plt
import json
import textdistance


def build_graph():
    G = nx.Graph()

    c_map = plt.get_cmap('tab20')
    colors_map = {i: c_map(i) for i in range(20)}
    colors_map = {i: f"#{int(c[0] * 255):02x}{int(c[1] * 255):02x}{int(c[2] * 255):02x}" for i, c in colors_map.items()}
    color_idx = 0
    for p in os.listdir('data'):
        if not p.startswith('nodes') or p.startswith('.'):
            continue
        group_name = p.split("_")[1].replace(".csv", "").capitalize()
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
            authors = row['Authors']
            color = colors_map[color_idx % 20]
            keywords = []
            if str(row['Keywords']) != "nan":
                keywords = row['Keywords'].replace("\n", ", ").replace(";", ", ").split(",")
                keywords = [k.strip() for k in keywords if len(k.strip()) > 0]
            link = row['Link']
            G.add_node(row[id_col], label=label, title=title, abstract=abstract, color=color, keywords=keywords,
                       doi=link, authors=authors, group=group_name)
            for node in group_nodes:
                abstract_similarity = textdistance.jaccard.normalized_similarity(abstract, G.nodes[node]['abstract'])
                G.add_edge(row[id_col], node, label="Inner", relationship=f"Group {group_name}",
                           weight=abstract_similarity)
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
        G.add_edge(row['Id 1'], row['Id 2'], label="Outer", relationship=row['Relationship'], weight=1)

    # Obtain adjacency matrix
    return G


def save_json(G):
    # Save graph as JSON for D3.js
    # Nodes:
    # - "id": Id of the manuscript
    # - "name": Display name of the manuscript
    # - "title": Manuscript's title
    # - "authors": Manuscript's authors
    # - "keywords": Manuscript's keywords
    # - "abstract": Manuscript's abstract
    # - "doi": Manuscript's DOI
    # - "group": DBC's group
    # - "color": Inherited from the DBC's group
    # Edges:
    # - "source": Id of the source node
    # - "target": Id of the target node
    # - "label": Label of the edge
    # - "value": Weight of the edge
    # - "source_title": Title of the source node
    # - "source_doi": DOI of the source node
    # - "target_title": Title of the target node
    # - "target_doi": DOI of the target node
    # - "relationship": Relationship between the source and the target
    nodes = []
    for n in G.nodes:
        node = G.nodes[n]
        nodes.append(
            {"id": n, "name": node['label'], "title": node['title'], "authors": node['authors'], "group": node['group'],
             "keywords": node['keywords'], "abstract": node['abstract'], "doi": node['doi'], "color": node['color']})
    links = []
    for e in G.edges:
        source = e[0]
        target = e[1]
        edge = G.edges[e]
        links.append(
            {"source": source, "target": target, "label": edge['label'], "value": edge['weight'],
             "source_title": G.nodes[source]['title'], "source_doi": G.nodes[source]['doi'],
             "target_title": G.nodes[target]['title'], "target_doi": G.nodes[target]['doi'],
             "relationship": edge['relationship']})

    # Writing to sample.json
    with open("DBCNetwork.json", "w") as outfile:
        # Serializing json
        json_object = json.dumps({"nodes": nodes, "links": links}, indent=2)
        outfile.write(json_object)

    # Writing to DBCNetwork.js
    # A js dictionary named "groups" is created with the group name as key and the color as value
    with open("DBCNetwork.js", "w") as outfile:
        groups = dict()
        for n in G.nodes:
            groups[G.nodes[n]['group']] = G.nodes[n]['color']
        outfile.write("var groups = ")
        outfile.write(json.dumps(groups, indent=2))


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
    save_json(graph)
    save_nx(graph)
    save_d3(graph)
