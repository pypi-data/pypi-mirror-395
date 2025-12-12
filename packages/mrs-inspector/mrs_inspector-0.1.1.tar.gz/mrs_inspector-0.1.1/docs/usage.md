# **3. docs/usage.md**
```markdown
# Usage

## Basic Inspection

```python
from mrs_inspector import Inspector

def main():
    return "ok"

inspector = Inspector()
result, trace = inspector.inspect(main)

trace.save("trace.json")
