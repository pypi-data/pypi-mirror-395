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

from mrs_inspector.inspector import Inspector

def test_wrap_basic():
    inspector = Inspector()

    @inspector.wrap
    def add(a, b):
        return a + b

    result = add(2, 3)
    assert result == 5

    trace = inspector.trace.states
    assert len(trace) == 1
    assert trace[0].module_name == "add"
    assert trace[0].outputs == 5


def test_wrap_exception():
    inspector = Inspector()

    @inspector.wrap
    def explode():
        return 1 / 0   # ZeroDivisionError

    try:
        explode()
    except ZeroDivisionError:
        pass

    trace = inspector.trace.states
    assert len(trace) == 1
    assert trace[0].exception is not None
    assert trace[0].exception["type"] == "ZeroDivisionError"


def test_phase_context():
    inspector = Inspector()

    with inspector.phase("setup"):
        x = 10

    trace = inspector.trace.states
    assert len(trace) == 1
    assert trace[0].module_name == "setup"
    assert trace[0].outputs == {"done": True}

