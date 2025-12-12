import networkx as nx

class GraphBuilder:
    """
    Build a simple directed graph from a Trace.
    """

    def __init__(self):
        self.g = nx.DiGraph()

    def build(self, trace):
        for state in trace.states:
            self.g.add_node(state.module_name)

        for (f, t) in trace.transitions:
            self.g.add_edge(f.module_name, t.module_name)

        return self.g

    def save_png(self, path):
        import matplotlib.pyplot as plt

        pos = nx.spring_layout(self.g)
        nx.draw(self.g, pos, with_labels=True, node_size=1500)
        plt.savefig(path, dpi=300)
        plt.close()
