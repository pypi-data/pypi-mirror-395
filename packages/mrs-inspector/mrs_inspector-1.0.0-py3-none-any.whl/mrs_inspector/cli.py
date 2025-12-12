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

import argparse
from .inspector import Inspector

def main():
    parser = argparse.ArgumentParser(
        description="Run a function under MRS trace inspection."
    )
    parser.add_argument("script", help="Path to script to run")
    parser.add_argument("--out", default="trace.json", help="Output trace path")

    args = parser.parse_args()

    inspector = Inspector()

    namespace = {}
    with open(args.script, "r") as f:
        code = f.read()
        exec(code, namespace)

    if "main" not in namespace:
        raise ValueError("Script must define a main() function")

    result, trace = inspector.inspect(namespace["main"])

    trace.save(args.out)
