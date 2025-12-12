from .tracer import Trace
from .utils import timestamp

class Inspector:
    """
    Wraps a function call with reasoning trace capture.
    """

    def __init__(self):
        self.trace = Trace()

    def inspect(self, fn, *args, **kwargs):
        entry = self.trace.add_state("entry", {"time": timestamp()})

        result = fn(*args, **kwargs)

        exit_state = self.trace.add_state("exit", {"time": timestamp()})
        self.trace.add_transition(entry, exit_state)

        return result, self.trace
