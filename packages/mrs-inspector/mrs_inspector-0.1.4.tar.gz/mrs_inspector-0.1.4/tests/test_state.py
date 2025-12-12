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

from mrs_inspector.state import State

def test_state_creation():
    s = State(
        id="123",
        module_name="test",
        phase="call",
        inputs={"x": 1},
        outputs=None,
        parent_id=None,
        depth=0,
        timestamp="2025-01-01T00:00:00",
        exception=None,
    )

    assert s.id == "123"
    assert s.module_name == "test"
    assert s.phase == "call"
    assert s.inputs == {"x": 1}
    assert s.outputs is None
    assert s.exception is None

