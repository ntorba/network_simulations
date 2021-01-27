import random
from multiprocessing import Pool
import os

NO_OPINION = 0
OPINION_A = 1
OPINION_B = 2
DECIDED = 0.7
UNDECIDED = 0.3

NUM_NODE_INTERACTIONS = 150


class Environment:
    def __init__(
        self,
        agent_count,
        opinion_a_count,
        opinion_b_count,
        sample_size,
        bias,
        builder,
        min_neighbors,
    ):
        if opinion_a_count + opinion_b_count > agent_count:
            raise Exception(
                "opinion_a_count and opinion_b_count combine to total more than agent_count. Please pass new values. "
            )
        self.agent_count = agent_count
        self.opinion_a_count = opinion_a_count
        self.opinion_b_count = opinion_b_count
        self.builder = builder
        # Return a networkx graph built with some specific strategy
        self.network = self.builder(num_nodes=agent_count, min_neighbors=min_neighbors)

        if bias:  # In this case, we bias influential nodes towards opinion_a
            for i_node, i_degree in sorted(
                self.network.degree, key=lambda x: x[1], reverse=True
            )[: self.opinion_a_count]:
                self.network.nodes[i_node]["opinion"] = OPINION_A
                self.network.nodes[i_node]["confidence"] = DECIDED

            for i_node, i_degree in sorted(
                self.network.degree, key=lambda x: x[1], reverse=False
            )[: self.opinion_b_count]:
                self.network.nodes[i_node]["opinion"] = OPINION_B
                self.network.nodes[i_node]["confidence"] = DECIDED

        else:  # randomly assigning opions to all nodes
            random_nodes = random.sample(
                list(self.network.nodes), len(self.network.nodes)
            )
            opinion_a_group = []
            for i_node in random_nodes[: self.opinion_a_count]:
                self.network.nodes[i_node]["opinion"] = OPINION_A
                self.network.nodes[i_node]["confidence"] = DECIDED

            for i_node in random_nodes[
                self.opinion_a_count : (self.opinion_a_count + self.opinion_b_count)
            ]:
                self.network.nodes[i_node]["opinion"] = OPINION_B
                self.network.nodes[i_node]["confidence"] = DECIDED

    def advance(self):
        """
        Randomly select nodes to add samples from each other
        This is how nodes influence each other
        """
        a = random.choice(list(self.network.nodes))
        b = random.choice(list(self.network.neighbors(a)))

        add_influence(self.network, a, b)
        add_influence(self.network, b, a)

    @staticmethod
    def run_experiment(env):
        for _ in range(NUM_NODE_INTERACTIONS):
            for i_node in env.network.nodes:
                b = random.choice(list(env.network.neighbors(i_node)))
                add_influence(env.network, i_node, b)
                add_influence(env.network, b, i_node)
            if env.is_converged():
                break
        return env.is_converged()

    def run_experiments(self, num_experiments):
        results = [0, 0, 0]
        with Pool(os.cpu_count()) as p:
            for i in p.imap_unordered(
                self.run_experiment,
                [self] * num_experiments,
                chunksize=num_experiments // os.cpu_count(),
            ):
                results[i] += 1
        return results

    def is_converged(self):
        results = [0, 0, 0]
        for i_node in self.network.nodes:
            results[self.network.nodes[i_node]["opinion"]] += 1

        count = 0
        max_ = 0
        max_val = 0
        for index, i in enumerate(results):
            if i == 0:
                count += 1
            elif i > max_val:
                max_ = index
                max_val = i
        result = 0
        if count == 2:
            result = max_
        return result


def add_influence(graph, node, influence_node):
    """
    Args:
        graph (nx.Graph): networkx graph object holding both nodes
        node (int): node to have influence (opinion) added from influence_node
        influence_node (int): this node has it's opinion added to the first node
    """
    node = graph.nodes[node]
    node["samples"].append(graph.nodes[influence_node]["opinion"])

    if len(node["samples"]) >= 3:
        scores = [0, 0, 0]
        for i_sample in node["samples"]:
            scores[i_sample] += 1
        max_ = 0
        maxVal = 0
        for i in range(len(scores)):
            if scores[i] > maxVal:
                max_ = i
                maxVal = scores[i]
        consensus = max_
        # breakpoint() if 2 in node["samples"] else None
        if consensus > 0 and random.random() > node["confidence"]:
            node["opinion"] = consensus
            node["confidence"] = 0.7
        node["samples"] = []
