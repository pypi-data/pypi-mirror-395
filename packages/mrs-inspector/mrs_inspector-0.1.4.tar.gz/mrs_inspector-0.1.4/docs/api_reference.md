# API Reference

This document provides the complete public API for **MRS-Inspector**.

---

## Inspector

The core entry point for tracing execution.

```python
from mrs_inspector import Inspector

inspector = Inspector()
```

### **inspect(fn, *args, **kwargs) → (result, Trace)**

Executes the function while recording a full reasoning trace.

```python
result, trace = inspector.inspect(fn, *args, **kwargs)
```

Captures:

- function entry/exit  
- nested calls  
- arguments + return values  
- timing metadata  
- exceptions (if thrown)  

---

## Decorator: `@inspector.wrap`

Wraps a function so every call is automatically traced.

```python
@inspector.wrap
def step(x):
    return x * 2
```

Works for deeply nested calls and pipelines.

---

## Trace Object

`Trace` represents the full execution history.

### **trace.save(path: str)**  
Exports the trace to JSON.

```python
trace.save("trace.json")
```

Output includes call tree, steps, timing, and exception details.

---

## GraphBuilder

Optional utility to turn a trace into a PNG call graph.

```python
from mrs_inspector.graph import GraphBuilder
```

### **GraphBuilder().build(trace)**  
Converts a trace into a directed graph structure.

### **GraphBuilder().save_png(path: str)**  
Renders the graph to an image file.

```python
gb = GraphBuilder()
g = gb.build(trace)
gb.save_png("graph.png")
```

Uses `networkx` and `matplotlib` under the hood.

---

## Exceptions

All exceptions raised during execution are captured and stored in the trace:

- exception type  
- message  
- call context  

They never crash tracing unless explicitly re-raised by user code.

---

## Modules

### `mrs_inspector.state`  
Internal state container for function call records.

### `mrs_inspector.trace`  
Implements the `Trace` class and JSON export.

### `mrs_inspector.graph`  
GraphBuilder and visualization helpers.

---

End of API specification.
