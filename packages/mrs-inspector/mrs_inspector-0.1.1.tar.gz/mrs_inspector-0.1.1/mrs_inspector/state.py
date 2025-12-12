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

# state.py
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, List
from datetime import datetime
import uuid

def now_iso():
    return datetime.utcnow().isoformat()

@dataclass
class State:
    """
    A single reasoning event captured during an MRS run.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    module_name: str = ""              # name of the module/function
    phase: str = "step"                # expand | prune | verify | commit | step
    content: Any = None                # arbitrary data (string, dict, etc.)
    inputs: Dict[str, Any] = field(default_factory=dict)
    outputs: Dict[str, Any] = field(default_factory=dict)
    depth: int = 0                     # nested reasoning depth
    parent_id: Optional[str] = None    # for hierarchical graph construction
    exception: Any = None               # exception data if any
   
    timestamp: str = field(default_factory=now_iso)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "module_name": self.module_name,
            "phase": self.phase,
            "content": self.content,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "depth": self.depth,
            "parent_id": self.parent_id,
            "timestamp": self.timestamp,
        }
