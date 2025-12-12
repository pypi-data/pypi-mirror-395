# Basic Trace Example

This example shows the simplest use of **MRS-Inspector**: capturing a trace of a function execution and exporting it to JSON.

---

## Example: Tracing a Simple Function

```python
from mrs_inspector import Inspector

def main():
    return 42

inspector = Inspector()

# Run with tracing enabled
result, trace = inspector.inspect(main)

# Save the full execution trace
trace.save("basic_trace.json")

print("Result:", result)
print("Trace saved to basic_trace.json")
```

---

## What You Get

The generated `basic_trace.json` includes:

- function entry and exit  
- timing data  
- return values  
- full call record  
- structure suitable for graph building or custom inspection  

This is the minimal workflow for using the inspector.
