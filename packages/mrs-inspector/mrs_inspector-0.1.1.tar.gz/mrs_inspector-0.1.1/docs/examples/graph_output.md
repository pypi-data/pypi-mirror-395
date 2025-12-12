# **6. docs/examples/graph_output.md**
```markdown
# Graph Output Example

```python
from mrs_inspector.graph import GraphBuilder
from mrs_inspector import Inspector

def main():
    return "done"

inspector = Inspector()
result, trace = inspector.inspect(main)

gb = GraphBuilder()
g = gb.build(trace)
gb.save_png("graph.png")
