import json
from .state import State

class Trace:
    """
    Minimal reasoning trace container.
    Holds: states + transitions
    """

    def __init__(self):
        self.states = []
        self.transitions = []

    def add_state(self, module_name, content=None):
        state = State(module_name, content)
        self.states.append(state)
        return state

    def add_transition(self, from_state, to_state):
        self.transitions.append((from_state, to_state))

    def to_dict(self):
        return {
            "states": [s.to_dict() for s in self.states],
            "transitions": [
                (fs.module_name, ts.module_name) 
                for (fs, ts) in self.transitions
            ]
        }

    def save(self, path):
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)
