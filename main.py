import argparse
import time

from core.orchestrator import Orchestrator
from system import get_monitor


def main():
    parser = argparse.ArgumentParser(description="Resource-aware AI plugin runtime")
    parser.add_argument("input", nargs="?", default="Hello from main")
    parser.add_argument("--watch", type=float, metavar="SECONDS",
                        help="re-evaluate resources and run every N seconds")
    args = parser.parse_args()

    orchestrator = Orchestrator()
    while True:
        status = get_monitor().status()
        print("System:", status)
        print("Result:", orchestrator.run(args.input, status))
        if not args.watch:
            break
        time.sleep(args.watch)


if __name__ == "__main__":
    main()
