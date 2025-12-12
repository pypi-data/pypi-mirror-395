#!/usr/bin/env python
import argparse
import sys
from dataclasses import dataclass
from datetime import timedelta, timezone
from typing import Dict, Iterator

from pygit2 import BlameHunk, Oid, Repository

DEFAULT_WIDTH = 78
DEFAULT_CONTEXT = 3


@dataclass
class FileFuzzies:
    repo: Repository
    file_path: str
    diffs: list[dict]


def get_fuzzy_entries(repo: Repository, file_id: Oid) -> Iterator[int]:
    try:
        pofile = repo.get(file_id).data.decode("utf-8")
    except KeyError:
        print("Unknown file in current revision.")
        return
    for i, line in enumerate(pofile.splitlines()):
        if line.startswith("#,") and "fuzzy" in line:
            yield i + 1


def get_commit_patches(repo: Repository, commit: Oid, file_path: str):
    for patch in repo.diff(commit.id):
        content = patch.data.decode("utf-8").split("\n")
        if file_path in content[0]:
            yield content


def is_good_diff(patchline: str, linenum: int) -> bool:
    if not patchline.startswith("@@"):
        return False
    final_lines = patchline.split("+")[1].split("@")[0]
    final_start = int(final_lines.split(",")[0])
    final_end = final_start + int(final_lines.split(",")[1])
    return final_start <= linenum <= final_end


def get_line_start_old(patch: list[str], linenum: int) -> int:
    """return line number of old version start"""
    orig_start_line = -int(patch[0].split(",")[0].split("@")[-1])
    final_start_line = int(patch[0].split("+")[1].split(",")[0])
    for line in patch[1:]:
        if line.startswith("+"):
            final_start_line += 1
        elif line.startswith("-"):
            orig_start_line += 1
        else:
            final_start_line += 1
            orig_start_line += 1
        if final_start_line == linenum:
            return orig_start_line - 1
    raise IndexError("Cannot find start line in old version")


def get_msgid_at_linenum(repo: Repository, file_id: Oid, linenum: int) -> str:
    content = repo.get(file_id).data.decode("utf-8").split("\n")
    result = ""
    capture = False
    for line in content[linenum:]:
        if line.startswith("msgstr"):
            return result
        if line.startswith("msgid"):
            capture = True
            if line != 'msgid ""':
                return str(line[6:])
        elif capture:
            result += str(line[1:-1])
    return result


def get_old_version(
    repo: Repository, file_path: str, linenum: int, blame: BlameHunk
) -> str | None:
    """get version of orig_commit_id, from linenum"""
    try:
        old_commit = repo.get(blame.final_commit_id).parents[0]
        for file_patch in get_commit_patches(repo, old_commit, file_path):
            for i, line in enumerate(file_patch):
                if is_good_diff(line, linenum):
                    line_start_old = get_line_start_old(file_patch[i:], linenum)
                    commit = repo.get(old_commit.id)
                    file_id = commit.tree[file_path].id
                    msgid = get_msgid_at_linenum(repo, file_id, line_start_old)
                    return msgid
    except KeyError as e:
        print(
            f"{file_path} not found in old tree ({blame.orig_commit_id}): {e}",
            file=sys.stderr,
        )
    return None


def populate(
    repo: Repository, filename: str, file_id: Oid, cur_diff: Dict
) -> tuple[int, BlameHunk, str, str, timezone]:
    """Searching in git is expensive.
    Do a lazy search and cache the result in the dict"""
    linenum = cur_diff["linenum"]
    blame = cur_diff.setdefault(
        "blame",
        repo.blame(filename, min_line=linenum, max_line=linenum)[0],
    )
    current = cur_diff.setdefault(
        "current",
        get_msgid_at_linenum(repo, file_id, linenum),
    )
    old = cur_diff.setdefault(
        "old",
        get_old_version(repo, filename, linenum, blame),
    )
    minutes = cur_diff.setdefault("committer", blame.final_committer).offset
    tzinfo = timezone(timedelta(minutes=minutes))
    return linenum, blame, current, old, tzinfo


def core_parser(desc: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        "--repo",
        type=str,
        default=".",
        help="path to the repository (default: current directory)",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=DEFAULT_WIDTH,
        help="width of lines (default: %(default)s)",
    )
    parser.add_argument(
        "--context",
        type=int,
        default=DEFAULT_CONTEXT,
        help="lines of context (default: %(default)s)",
    )
    return parser
