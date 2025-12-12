"""
# fedkit CLI

Usage: fedkit [command] [options]

command: query
    Query a fediverse actor or activity

"""

import sys
import argparse

def main():
    args = argparse.ArgumentParser()
    args.add_argument("command", choices=["query"], help="The command to execute")
    args.add_argument("actor_or_activity", help="The actor or activity to query")
    args = args.parse_args()

    if args.command == "query":
        print(f"Querying {args.actor_or_activity}")
        from tasks.fetch import BaseFetch
        BaseFetch(args.actor_or_activity)

if __name__ == "__main__":
    sys.exit(main())
