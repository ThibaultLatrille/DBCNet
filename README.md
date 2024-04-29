# DBCNet


Specs
==================
- 2/3 viewport for d3.js graph (left side)
- 1/3 viewport for information (right side)
Graph:
Undirected force field graph, can be dragged and zoomed
- Nodes: 
  - "Name": Id of the manuscript 
  - "Title": Manuscript's title
  - "Authors": Manuscript's authors
  - "Keywords": Manuscript's keywords
  - "Abstract": Manuscript's abstract
  - "DOI": Manuscript's DOI
  - Color: Inherited from the DBC's group
- Edges:
  - "source": Id of the source node
  - "target": Id of the target node
  - "sourceTitle": Title of the source node
  - "targetTitle": Title of the target node
  - "Relationship": Relationship between the source and the target
  
Information:
- Legend for group color and name
- Callback on node click: display the node's information:
    - "Title"
    - "Authors"
    - "DOI" (as a link, open in a new tab with target="_blank")
    - "Keywords"
    - "Abstract"
- Callback on node unclick: hide the node's information
- Callback on edge click: display the edge's information:
    - "Link between" (source node's title and target node's title as links, open in a new tab with target="_blank") 
    - "Relationship"
- Callback on edge unclick: hide the edge's information

Optional:
- Callback on node hover: highlight the node and its edges
- Callback on node unhover: unhighlight the node and its edges
- Callback on edge hover: highlight the edge and its end nodes
- Callback on edge unhover: unhighlight the edge and its end nodes
- Bootstrap for the layout
- Favicon with the DBC's logo
