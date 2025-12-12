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

# mrs_inspector/validator.py


class TraceValidationError(Exception):
    """Raised when a trace fails structural validation."""
    pass




def validate_trace(states):
    """
    Strict validator for a list of TraceState objects.
    Ensures:
        - IDs are unique
        - parent_id refers to earlier element
        - depth is parent.depth + 1 (except root)
        - timestamps are non-decreasing
        - module_name, phase are non-empty
    """


    seen_ids = set()
    id_to_state = {}


    # --- pass 1: basic shape checks ---
    last_timestamp = None


    for index, state in enumerate(states):


        # Unique IDs
        if state.id in seen_ids:
            raise TraceValidationError(
                f"Duplicate ID found at index {index}: {state.id}"
            )
        seen_ids.add(state.id)
        id_to_state[state.id] = state


        # Required fields
        if not state.module_name:
            raise TraceValidationError(f"Missing module_name at index {index}")


        if not state.phase:
            raise TraceValidationError(f"Missing phase at index {index}")


        # Timestamp ordering
        if last_timestamp and state.timestamp < last_timestamp:
            raise TraceValidationError(
                f"Timestamps not ordered at index {index}: "
                f"{state.timestamp} < {last_timestamp}"
            )
        last_timestamp = state.timestamp


    # --- pass 2: parent/child structure ---
    for index, state in enumerate(states):


        if state.parent_id is None:
            # root depth must be 0
            if state.depth != 0:
                raise TraceValidationError(
                    f"Root node at index {index} must have depth 0"
                )
            continue


        if state.parent_id not in id_to_state:
            raise TraceValidationError(
                f"parent_id {state.parent_id} at index {index} does not exist"
            )


        parent = id_to_state[state.parent_id]


        # Depth check
        if state.depth != parent.depth + 1:
            raise TraceValidationError(
                f"Incorrect depth at index {index}: got {state.depth}, "
                f"expected {parent.depth + 1}"
            )

