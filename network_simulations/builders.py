"""
Module to create different types of networkx graphs
"""
import random
import networkx as nx


def scale_free_network(num_nodes, min_neighbors):
    """
    From http://networksciencebook.com/chapter/5#barabasi-model
        We start with m0 nodes, the links between which are chosen arbitrarily, as long as each node has at least one link. The network develops following two steps

        Growth
            At each timestep we add a new node with m (≤ m0) links that connect the new node to m nodes already in the network. Preferential attachment
            The probability Π(k) that a link of the new node connects to node i depends on the degree ki as  Π(ki)=ki∑jkj

        We must have at least min_neighbor nodes to start, with arbitrary connections between them
    """

    G = nx.complete_graph(
        min_neighbors
    )  # TODO: confirm this is an appropriate intializer (the definition says the links here aren't important)
    for i_new_node in range(min_neighbors, num_nodes):
        G.add_node(i_new_node)
        selection_list = []
        for i_candidate in G.nodes():
            # Add more possible choices because it has more neighbors
            # simulating result of preferential attachment
            selection_list.extend([i_candidate] * G.degree[i_candidate])

        # scale-free linking
        while G.degree[i_new_node] < min_neighbors:
            random_neighbor = random.choice(selection_list)
            G.add_edge(i_new_node, random_neighbor)
    return G


def random_network(num_nodes, min_neighbors):
    G = nx.Graph(name="random graph")
    G.add_node(0)
    for i_node in range(0, num_nodes):
        G.add_node(i_node)

    for i_node in G.nodes:
        while G.degree[i_node] < min_neighbors:
            random_neighbor = random.choice(list(G.nodes))
            G.add_edge(i_node, random_neighbor)
    return G

