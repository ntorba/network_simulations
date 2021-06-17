"""
This module is based on ideas from https://thetinkerpoint.com/2019/02/11/why-the-world-has-gone-crazy/ and code Alex Lamb shared with me: https://github.com/alexlamb/groupdecision via twitter dm.


I attempted to do this in a more functional style, as inspired by my recent watching of https://www.youtube.com/watch?v=vK1DazRK_a0... we'll see how it goes.
"""

from collections import Counter
import random


def add_influence(graph, node, influence_node, min_samples=3):
    """
    Add the opinion of the influence_node to the current_node (arg: node).
    Then, update the opinion of the current node based on the new sample. First, add the sample, then, get the opinion with the most samples, then, if a random number comes back higher than the current confidence, and there is a new winner, change opinion to the current consensus opinion in the current nodes samples.

    Args:
        graph (nx.Graph): networkx graph object holding both nodes
        node (int): node to have influence (opinion) added from influence_node
        influence_node (int): this node has it's opinion added to the first node
        min_sample (int): Node must have at least min_samples samples to make a consensus change
    """
    node = graph.nodes[node]
    node["samples"].append(graph.nodes[influence_node]["opinion"])

    node_counter = Counter(node["samples"])
    consensus, count = node_counter.most_common(1)[
        0
    ]  # returns a list of tuples of (opinion, count)
    if (
        len(node["samples"]) > min_samples
        and consensus > 0
        and random.random() > node["confidence"]
    ):
        node["opinion"] = consensus
        node["confidence"] = 0.7

    # node["samples"] = []


def is_converged(network, states):
    num_nodes = len(network.nodes)
    if num_nodes in states[-1]:
        return True
    else:
        return False


def get_opinions(network):
    opinions = [0, 0, 0]
    for i_node in network.nodes:
        opinions[network.nodes[i_node]["opinion"]] += 1
    return opinions


def all_nodes_update_state(network):
    # First version, ensures we update every node on each step
    # The differences between state steps will be much larger...
    # Simulations will converge much faster
    for i_node in network.nodes:
        b = random.choice(list(network.neighbors(i_node)))
        add_influence(network, i_node, b)
        add_influence(network, b, i_node)
    return network


def random_update(network):
    a = random.choice(list(network.nodes))
    b = random.choice(list(network.neighbors(a)))

    add_influence(network, a, b, min_samples=6)
    add_influence(network, b, a, min_samples=6)
    return network


def run(network, update_network, extract_state, converged, num_steps):
    """
    network (networkx.graph): graph of nodes to run sim on
    update_network (func): receives network, runs a single update step
    extract_state (func): receives network, returns the current state from network that you want added to the returned states from the experiment run
    converged (func): receives network, return True if network has converged, False otherwise
    num_steps (int): number of simulation steps to run
    """
    states = []
    states.append(extract_state(network))
    for i in range(num_steps):
        network = update_network(network)
        state = extract_state(network)
        states.append(state)
        if converged(network, states):
            break
    return states

