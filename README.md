# DBCNet

### This code repository:
https://tinyurl.com/DBCNet2024

### The collaborative spreadsheet:
https://docs.google.com/spreadsheets/d/1YzLqlKZBrjSAjGZ1VwzpoAemwn04uZNlmVhsGsmBPuk/edit#gid=0

- Sheet `LINKS` contains the links between manuscripts, this is where we will collaboratively build the network.
- Sheet `Bergamnn`, `Ciriello`, `Dessimoz`, `Fasshauer`, `Kutalik`, `Malaspinas` and `Salamin` already contains the list of manuscripts (you can add a row if you want).

### The graph of the network:
https://thibaultlatrille.github.io/DBCNet/

## Done:
- Nodes are already defined and grouped (by PI, thanks to *volunteers*).
- PDFs are already downloaded (in the `PDF` column of each sheet).
- Links within groups are already defined (based on abstract similarity).
- Convert the spreadsheet into a graph (using Python/networkx).
- Display the graph on a webpage (using [d3.js](https://d3js.org/), thanks to [Clément Train](https://github.com/F4llis)).

## To do:
- Create links between groups in the spreadsheet (`LINKS`), this is the goal of the workshop.

## How to contribute
- Add rows in the sheet `LINKS` as links between manuscripts.
- Write your name in the first column (so that other people know who is working on each line).
- Use the `Manuscript ID` (e.g. `B_pathway`) to refer to a manuscript in the spreadsheet.
- Write the reason for the link in the `Relationship` column, this can be because the manuscript shares a similar topic, a similar method, dataset, or whatever you think is relevant.
- Write any comment in the `Comment` column if you wish too (optional).
- It is possible to have several rows for the same pair of manuscripts (reasons will be concatenated).
- If you are part of joint lab-meeting, seek link both inside and outside of these joint meetings.
- As many as you can, the more links the better!