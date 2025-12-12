#!/usr/bin/env python3
"""Find and display diffs for fuzzy entries in pofile.
diff are displayed in the order of the pofile.
"""
import argparse
import sys
import textwrap
from datetime import datetime
from difflib import ndiff
from itertools import repeat
from typing import Dict

from pygit2 import Oid, Repository

from .core import core_parser, get_fuzzy_entries, populate

NO_COLOR = "\033[0m"
YELLOW = "\033[93m"
RED = "\033[91m"
GREEN = "\033[92m"


def color_diff(diff):
    """print diff using colors"""
    for line in diff:
        if line.startswith("+ "):
            print(GREEN + line + NO_COLOR)
        elif line.startswith("- "):
            print(RED + line + NO_COLOR)
        elif line.startswith("? "):
            print(YELLOW + line + NO_COLOR)
        else:
            print(line)


def display(
    args: argparse.Namespace, repo: Repository, file_id: Oid, cur_diff: Dict
) -> None:
    """print one diff according to cli arguments"""
    linenum, blame, current, old, tzinfo = populate(
        repo, args.filename, file_id, cur_diff
    )
    print(
        f"{blame.final_commit_id} {datetime.fromtimestamp(blame.final_committer.time, tzinfo)} "
        f"by {blame.final_committer.name}"
    )
    print(f"line: {linenum}")
    diff = ndiff(
        textwrap.fill(old, args.width).split("\n"),
        textwrap.fill(current, args.width).split("\n"),
    )
    if args.no_color:
        print("\n".join(l for l in diff))
    else:
        color_diff(diff)
    print()


def parse_args():
    """add special parameters for cli"""
    parser = core_parser(__doc__)
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="interactive mode",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="do not color diff",
    )
    parser.add_argument("filename", help="relative path to file to parse")

    return parser.parse_args()


def main():
    args = parse_args()
    repo = Repository(args.repo)
    try:
        file_id = repo.get(repo.head.target).tree[args.filename].id
    except KeyError as e:
        print(f"{args.filename} not found in {repo.path}: {e}", file=sys.stderr)
        sys.exit(1)
    diffs = [{"linenum": linenum} for linenum in get_fuzzy_entries(repo, file_id)]
    nb_diffs = len(diffs)
    if not args.interactive:
        if len(diffs) > 0:
            for d in diffs:
                display(args, repo, file_id, d)
        else:
            print(f"No fuzzy entry in {args.filename}", file=sys.stderr)
    else:
        index = 0
        while True:
            display(args, repo, file_id, diffs[index])
            while True:
                resp = input(
                    f"diff {index+1}/{nb_diffs} -> (N)ext - (P)rev - (W)idth - (Q)uit ? [N]"
                ).upper()
                if resp == "Q":
                    sys.exit(0)
                elif resp in ("", "N") and index < len(diffs) - 1:
                    index += 1
                    break
                elif resp == "P" and index > 0:
                    index -= 1
                    break
                elif resp == "W":
                    while True:
                        width = input(f"enter new width (current: {args.width}): ")
                        if width == "":
                            break
                        try:
                            args.width = int(width)
                            break
                        except ValueError:
                            pass
                    break


if __name__ == "__main__":
    main()
