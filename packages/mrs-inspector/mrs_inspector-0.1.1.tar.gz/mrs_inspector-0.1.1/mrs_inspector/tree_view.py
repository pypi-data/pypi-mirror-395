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


# mrs_inspector/tree_view.py

import json

def render_tree(path: str):
    with open(path, "r") as f:
        events = json.load(f)

    # Build mapping: parent_id -> list of children
    children = {}
    root = None
    for e in events:
        pid = e["parent_id"]
        children.setdefault(pid, []).append(e)
        if pid is None:
            root = e

    def walk(node, indent=""):
        print(f"{indent}{node['module_name']} (depth {node['depth']})")
        for child in children.get(node["id"], []):
            walk(child, indent + "    ")

    if root:
        walk(root)
    else:
        print("No root event found.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m mrs_inspector.tree_view <trace.json>")
        sys.exit(1)

    path = sys.argv[1]
    render_tree(path)
