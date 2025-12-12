# **7. docs/examples/custom_modules.md**
```markdown
# Custom Modules Example

The trace structure is unopinionated and can be extended.

```python
from mrs_inspector import Inspector

def step_a():
    return "a"

def step_b(x):
    return f"{x} + b"

inspector = Inspector()

entry, trace = inspector.inspect(lambda: step_b(step_a()))
trace.save("steps.json")
