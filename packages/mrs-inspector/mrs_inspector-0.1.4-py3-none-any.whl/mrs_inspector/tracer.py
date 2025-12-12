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


import json
from dataclasses import asdict

from .state import State


class Trace:
    def __init__(self):
        self.states = []

    def add(self, state):
        self.states.append(state)

    def save_json(self, path):
        data = [asdict(s) for s in self.states]
        with open(path, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def load_json(path):
        """
        Load a saved JSON trace file back into a Trace object.
        """
        trace = Trace()

        with open(path, "r") as f:
            data = json.load(f)

        for item in data:
            state = State(
                id=item["id"],
                module_name=item["module_name"],
                phase=item["phase"],
                content=item.get("content"),
                inputs=item.get("inputs"),
                outputs=item.get("outputs"),
                exception=item.get("exception"),
                depth=item["depth"],
                parent_id=item["parent_id"],
                timestamp=item["timestamp"]
            )
            trace.add(state)

        return trace

