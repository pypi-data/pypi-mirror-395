# Graph Output Example

MRS-Inspector can render a visual call graph from any captured trace.  
This example shows how to generate the trace, build the graph, and export it as a PNG.

---

## Example: Producing a Graph Image

```python
from mrs_inspector import Inspector
from mrs_inspector.graph import GraphBuilder

def main():
    return "done"

# Step 1 — capture trace
inspector = Inspector()
result, trace = inspector.inspect(main)

# Step 2 — build graph structure
gb = GraphBuilder()
graph = gb.build(trace)

# Step 3 — export to PNG
gb.save_png("graph.png")

print("Trace result:", result)
print("Graph image written to graph.png")
```

---

## What This Demonstrates

- You can generate a call graph from *any* inspected workflow.  
- The PNG output shows:
  - nodes for functions / call steps  
  - edges for execution flow  
  - optional metadata encoded in the JSON trace  
- This is ideal for debugging, documentation, or visual reasoning analysis.

For full customization options, see the GraphBuilder class in the API reference.
