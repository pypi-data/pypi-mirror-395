# Usage Guide

This guide shows how to use **MRS-Inspector** to trace functions, capture reasoning flow, and produce structured output.

---

## Basic Inspection

```python
from mrs_inspector import Inspector

inspector = Inspector()

def main():
    return "ok"

result, trace = inspector.inspect(main)
trace.save("trace.json")
```

This produces a JSON trace containing:

- function entry  
- nested calls  
- inputs/outputs  
- exceptions (if any)  
- timing metadata  

---

## Inspecting a Function With Arguments

```python
from mrs_inspector import Inspector

inspector = Inspector()

def add(a, b):
    return a + b

result, trace = inspector.inspect(add, 2, 3)
trace.save("add_trace.json")
```

---

## Using the Decorator Form

```python
from mrs_inspector import Inspector

inspector = Inspector()

@inspector.wrap
def multiply(x, y):
    return x * y

result, trace = inspector.inspect(lambda: multiply(4, 5))
trace.save("multiply_trace.json")
```

---

## Capturing Exceptions

```python
from mrs_inspector import Inspector

inspector = Inspector()

@inspector.wrap
def explode(x):
    return 10 / x   # ZeroDivisionError when x = 0

result, trace = inspector.inspect(lambda: explode(0))
trace.save("exception_trace.json")
```

The trace includes a full exception record: message, type, and call context.

---

## Next Steps

- See **API Reference** for details on Inspector, Trace, and graph utilities.  
- Visit **Examples** for full workflows.
