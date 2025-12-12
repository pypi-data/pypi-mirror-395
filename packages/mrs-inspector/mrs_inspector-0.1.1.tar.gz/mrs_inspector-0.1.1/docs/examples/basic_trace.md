# **5. docs/examples/basic_trace.md**
```markdown
# Basic Trace Example

```python
from mrs_inspector import Inspector

def main():
    return 42

inspector = Inspector()
result, trace = inspector.inspect(main)

trace.save("trace.json")
