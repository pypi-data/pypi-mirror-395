# Copyright 2025 RJ Sabouhi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import uuid
import traceback
from .state import State
from .tracer import Trace
from .utils import timestamp




class Inspector:
    """
    Core inspector that records structured reasoning traces.


    Features:
    - @wrap decorator for automatic instrumentation
    - phase(name) context manager
    - parent-child linking via call stack
    - full exception capture with traceback
    """


    def __init__(self):
        self.trace = Trace()
        self.call_stack = []   # stack of active State IDs


    # ---------------------------------------------------------
    # Internal helper: enter a new state
    # ---------------------------------------------------------
    def _begin_state(self, module_name, phase, inputs=None):
        parent_id = self.call_stack[-1] if self.call_stack else None


        state = State(
            id=str(uuid.uuid4()),
            module_name=module_name,
            phase=phase,
            inputs=inputs or {},
            outputs=None,
            exception=None,                    # <--- stores exception info
            parent_id=parent_id,
            depth=len(self.call_stack),
            timestamp=timestamp()
        )


        self.call_stack.append(state.id)
        self.trace.add(state)
        return state


    # ---------------------------------------------------------
    # Internal helper: finish a state
    # ---------------------------------------------------------
    def _end_state(self, state, outputs=None, exception=None):
        state.outputs = outputs
        state.exception = exception
        self.call_stack.pop()


    # ---------------------------------------------------------
    # PUBLIC API: decorator for automatic instrumentation
    # ---------------------------------------------------------
    def wrap(self, fn):
        """
        Example:


        @inspector.wrap
        def compute(x):
            return x + 1
        """


        module_name = fn.__name__


        def wrapped_fn(*args, **kwargs):
            inputs = {"args": args, "kwargs": kwargs}
            state = self._begin_state(module_name, phase="call", inputs=inputs)


            try:
                result = fn(*args, **kwargs)
                self._end_state(state, outputs=result)
                return result


            except Exception as e:
                tb = traceback.format_exc()
                exc_data = {
                    "type": type(e).__name__,
                    "message": str(e),
                    "traceback": tb
                }


                self._end_state(state, outputs=None, exception=exc_data)


                # IMPORTANT:
                # MRS Inspector does NOT crash the caller.
                # It records the failure and returns None.
                return None


        return wrapped_fn


    # ---------------------------------------------------------
    # PUBLIC API: context manager for phases
    # ---------------------------------------------------------
    class PhaseContext:
        def __init__(self, inspector, name):
            self.inspector = inspector
            self.name = name
            self.state = None


        def __enter__(self):
            self.state = self.inspector._begin_state(
                self.name, phase="phase", inputs={}
            )
            return self


        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_type:
                tb = traceback.format_exc()
                exc_data = {
                    "type": exc_type.__name__,
                    "message": str(exc_val),
                    "traceback": tb
                }
                self.inspector._end_state(
                    self.state, outputs=None, exception=exc_data
                )
                return False  # do not suppress
            else:
                self.inspector._end_state(
                    self.state, outputs={"done": True}
                )
                return False


    def phase(self, name):
        """Usage:  with inspector.phase("init"): ..."""
        return Inspector.PhaseContext(self, name)


    # ---------------------------------------------------------
    # Run a root function & produce the final trace
    # ---------------------------------------------------------
    def inspect(self, fn):
        state = self._begin_state(fn.__name__, phase="root", inputs={})


        try:
            result = fn()
            self._end_state(state, outputs=result)
            return result, self.trace


        except Exception as e:
            tb = traceback.format_exc()
            exc_data = {
                "type": type(e).__name__,
                "message": str(e),
                "traceback": tb
            }
            self._end_state(state, outputs=None, exception=exc_data)
            return None, self.trace

