# MRS-Inspector v1.0 — Structured Reasoning Trace Engine
*A companion module to the Modular Recursion Scaffold (MRS), providing full visibility into reasoning steps, execution flow, and exceptions.*

## Overview
MRS-Inspector records *every step* of a function’s execution — calls, nested calls, phases, inputs, outputs, and exceptions — into a structured trace object.  
It is designed to work alongside **Modular Recursion Scaffold (MRS)** as its interpretability and debugging layer.

Where MRS provides **structure**,  
MRS-Inspector provides **visibility**.

You can use MRS-Inspector to:

- instrument any Python function
- view internal reasoning flow
- collect nested call hierarchies
- capture exceptions with full traceback
- export traces to JSON
- reload traces for offline analysis or visualization

This enables research-grade transparency for small models, agents, recursive systems, or any code where reasoning steps matter.

---

# 1. Core Concepts

## 1.1 State Nodes
Every recorded event is a **State** — a dataclass containing:

- `id` (UUID)
- `module_name`
- `phase` (“call”, “phase”, “root”)
- `inputs`
- `outputs`
- `exception`
- `parent_id`
- `depth`
- `timestamp`

States form a **tree** that mirrors actual execution.

---

## 1.2 Trace Object
The `Trace` class stores all states and provides:

- ordered state list  
- lookup by ID  
- JSON save/load  
- compatibility with visualization tools

---

## 1.3 Call Stack Model
A lightweight stack keeps track of active states.  
Nested calls automatically become **children** of their callers.

---

# 2. Instrumentation Modes

## 2.1 `@inspector.wrap` — Function Instrumentation
Wrap any function to automatically record:

- its inputs  
- its output  
- nested calls inside it  
- exceptions  

Example:

```python
@inspector.wrap
def compute(x):
    return x * 2
```

Nested functions wrapped with `.wrap` automatically chain into the same trace.

---

## 2.2 Phases — `with inspector.phase(name)`
Phases are logical reasoning segments inside a function.

```python
with inspector.phase("retrieve"):
    docs = index.search(query)
```

Each phase becomes its own State node, allowing **semantic segmentation** of reasoning.

---

## 2.3 Root Execution — `inspector.inspect(fn)`
Runs a top-level function and returns `(result, trace)`:

```python
result, trace = inspector.inspect(main_fn)
```

This creates the root of the trace tree.

---

# 3. Exception Capture

All exceptions — including nested ones — are captured with:

- type  
- message  
- full traceback  

Example stored format:

```json
{
    "type": "ZeroDivisionError",
    "message": "division by zero",
    "traceback": "Traceback (most recent call last)..."
}
```

Exceptions **do not break the trace**.  
They become part of it.

---

# 4. JSON Export / Import

Save any trace:

```python
trace.save_json("trace.json")
```

Load a trace:

```python
loaded = Trace.load_json("trace.json")
```

Useful for:

- offline analysis  
- visualization tools  
- interpretability experiments  
- dataset generation  

---

# 5. Minimal Example

```python
from mrs_inspector import Inspector

inspector = Inspector()

@inspector.wrap
def squared(x):
    return x * x

def main():
    with inspector.phase("setup"):
        value = squared(3)
    return value + 1

result, trace = inspector.inspect(main)
trace.save_json("trace.json")
```

Resulting trace will contain:

- root execution  
- setup phase  
- call to `squared`  
- returned values  
- timestamps and structure  

---

# 6. What MRS-Inspector Enables

### Interpretability
A structured understanding of how a model, agent, or recursive system produced its output.

### Debugging
Exact reproduction of:

- the call structure  
- intermediate values  
- exceptions  
- execution order  

### Reasoning Analysis
Turn any function (or agent) into a *transparent reasoning pipeline*.

### Reusability & Offline Work
Share traces across systems or store them as part of datasets.

---

# 7. Roadmap

### v1.0 (Current)
- full call tracing  
- nested call support  
- exception recording  
- phases  
- JSON export/import  
- stable state tree representation  

### v1.1
- performance profiling  
- time-delta metrics  
- per-state memory footprint  

### v2.0
- graph visualization tools  
- HTML trace viewer  
- integration with MRS advanced recursion mode  

---

# License
Apache 2.0

# Citation
RJ Sabouhi (2025). MRS-Inspector v1.0 — Structured Reasoning Trace Engine.

