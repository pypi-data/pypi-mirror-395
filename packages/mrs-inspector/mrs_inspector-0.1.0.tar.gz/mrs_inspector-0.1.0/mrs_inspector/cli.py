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
