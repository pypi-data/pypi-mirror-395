# Copyright 2025 RJ Sabouhi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import networkx as nx
import matplotlib.pyplot as plt

class GraphBuilder:
    """
    Builds a graph representation of a Trace object and can export it to PNG.
    """

    def __init__(self, trace):
        self.trace = trace

    def build(self):
        """Convert the trace into a NetworkX graph object."""
        G = nx.DiGraph()

        # Each state becomes a node
        for idx, state in enumerate(self.trace.states):
            label = f"{idx}: {state.phase or 'root'}"
            G.add_node(idx, label=label)

        # Edges follow chronological ordering
        for i in range(len(self.trace.states) - 1):
            G.add_edge(i, i + 1)

        return G

    def save_png(self, path: str):
        """Build the graph and save as a PNG file."""
        G = self.build()

        plt.figure(figsize=(8, 6))
        pos = nx.spring_layout(G)

        labels = nx.get_node_attributes(G, "label")

        nx.draw(
            G,
            pos,
            with_labels=True,
            labels=labels,
            node_color="lightblue",
            node_size=1200,
            font_size=8,
            arrows=True
        )

        plt.savefig(path, format="png", dpi=300)
        plt.close()

