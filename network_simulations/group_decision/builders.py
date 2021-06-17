import random
from network_simulations.builder import scale_free_network, random_network


def random_init(
    network,
    opinion_a_count,
    opinion_b_count,
    no_opinion,
    opinion_a,
    opinion_b,
    decided,
    undecided,
):
    random_nodes = random.sample(list(network.nodes), len(network.nodes))
    for i_node in random_nodes[:opinion_a_count]:
        network.nodes[i_node]["opinion"] = opinion_a
        network.nodes[i_node]["confidence"] = decided

    for i_node in random_nodes[opinion_a_count : (opinion_a_count + opinion_b_count)]:
        network.nodes[i_node]["opinion"] = opinion_b
        network.nodes[i_node]["confidence"] = decided
    return network


def bias_init(
    network,
    opinion_a_count,
    opinion_b_count,
    no_opinion,
    opinion_a,
    opinion_b,
    decided,
    undecided,
):
    """
    Assign opinion_a to the nodes with the highest degree
    Assign opinion_b to the nodes with the lowest degree
    """
    # reverse=True for a, then reverse=False for b
    for i_node, i_degree in sorted(network.degree, key=lambda x: x[1], reverse=True)[
        :opinion_a_count
    ]:
        network.nodes[i_node]["opinion"] = opinion_a
        network.nodes[i_node]["confidence"] = decided

    for i_node, i_degree in sorted(network.degree, key=lambda x: x[1], reverse=False)[
        :opinion_b_count
    ]:
        network.nodes[i_node]["opinion"] = opinion_b
        network.nodes[i_node]["confidence"] = decided
    return network


def scale_free_with_opinions(
    num_nodes,
    min_neighbors,
    opinion_a_count,
    opinion_b_count,
    no_opinion=0,
    opinion_a=1,
    opinion_b=2,
    decided=0.7,
    undecided=0.3,
    bias=False,
):
    network = scale_free_network(num_nodes, min_neighbors)
    for i_node in network.nodes():
        # initialize all nodes with undecided and no samples
        network.nodes[i_node].update(
            dict(opinion=no_opinion, confidence=undecided, samples=[])
        )

    if bias:
        network = bias_init(
            network,
            opinion_a_count,
            opinion_b_count,
            no_opinion,
            opinion_a,
            opinion_b,
            decided,
            undecided,
        )
    else:
        network = random_init(
            network,
            opinion_a_count,
            opinion_b_count,
            no_opinion,
            opinion_a,
            opinion_b,
            decided,
            undecided,
        )
    return network


def random_network_with_opinions(
    num_nodes,
    min_neighbors,
    opinion_a_count,
    opinion_b_count,
    no_opinion=0,
    opinion_a=1,
    opinion_b=2,
    decided=0.7,
    undecided=0.3,
    bias=False,
):
    network = random_network(num_nodes, min_neighbors)
    for i_node in network.nodes():
        # initialize all nodes with undecided and no samples
        network.nodes[i_node].update(
            dict(opinion=no_opinion, confidence=undecided, samples=[])
        )
    if bias:
        network = bias_init(
            network,
            opinion_a_count,
            opinion_b_count,
            no_opinion,
            opinion_a,
            opinion_b,
            decided,
            undecided,
        )
    else:
        network = random_init(
            network,
            opinion_a_count,
            opinion_b_count,
            no_opinion,
            opinion_a,
            opinion_b,
            decided,
            undecided,
        )
    return network
