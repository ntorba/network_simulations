import networkx as nx
import dash
import dash_cytoscape as cyto
import dash_html_components as html

from network_simulations.builder import scale_free_network


def cyto_converter(G):
    positions = nx.nx_agraph.graphviz_layout(G, prog="circo")
    cyto_nodes = []
    cyto_edges = []
    for node in G.nodes:
        current = {
            "data": {"id": node, "label": node,},
            "position": {"x": positions[node][0], "y": positions[node][1]},
        }
        cyto_nodes.append(current)

    for n1, n2 in G.edges:
        current = {"data": {"source": n1, "target": n2}}
        cyto_edges.append(current)

    return cyto_nodes, cyto_edges


G = scale_free_network(100, 3)
nodes, edges = cyto_converter(G)
print(nodes)
app = dash.Dash(__name__)

app.layout = html.Div(
    [
        cyto.Cytoscape(
            id="cytoscape-two-nodes",
            layout={"name": "preset"},
            style={"width": "100%", "height": "500px"},
            elements=nodes + edges,
        )
    ]
)


if __name__ == "__main__":
    app.run_server(debug=True)
