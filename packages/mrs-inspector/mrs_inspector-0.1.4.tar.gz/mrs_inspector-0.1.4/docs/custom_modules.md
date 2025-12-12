# Custom Modules Example

MRS-Inspector is intentionally unopinionated:  
you can build *your own* mini-modules, steps, or reasoning units, and the inspector will trace them exactly as they execute.

This example shows how to combine multiple custom functions into a composed workflow while capturing a unified trace.

---

## Example: Custom Steps / Mini-Modules

```python
from mrs_inspector import Inspector

# Define your own reasoning steps
def step_a():
    return "a"

def step_b(x):
    return f"{x} + b"

inspector = Inspector()

# Compose your steps into a workflow
def workflow():
    return step_b(step_a())

# Inspect and capture the full trace
result, trace = inspector.inspect(workflow)

trace.save("custom_modules_trace.json")

print("Result:", result)
print("Trace saved to custom_modules_trace.json")
```

---

## What This Demonstrates

- You can create arbitrary functions ("modules") and chain them freely.  
- Every step — call, input, output, timing — is captured automatically.  
- The exported trace is fully compatible with graph building, manual inspection, or custom visualization.

This pattern scales naturally to larger reasoning systems and nested pipelines.
