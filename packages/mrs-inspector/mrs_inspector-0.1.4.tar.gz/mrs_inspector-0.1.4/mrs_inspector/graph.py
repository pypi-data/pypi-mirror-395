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
    def __init__(self, trace):
        self.trace = trace

    def build(self, path):
        """
        Render trace graph to PNG or save intermediate structure.
        """
        import graphviz

        dot = graphviz.Digraph(comment="MRS Execution Graph")

        # Add nodes
        for node in self.trace:
            dot.node(node.id, label=node.label)

        # Add edges
        for node in self.trace:
            for child in node.children:
                dot.edge(node.id, child.id)

        # Save file
        dot.render(path, format="png", cleanup=True)

        return path + ".png"


