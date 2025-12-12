from datetime import timedelta, timezone
from unittest import TestCase

from pygit2 import Repository

from pofuzzy_helper.core import (
    get_commit_patches,
    get_fuzzy_entries,
    get_line_start_old,
    get_old_version,
    populate,
)


class RepoObj(object):
    pass


class MockRepository(Repository):
    def __init__(self):
        self.entries = []

    def get(self, id: int):
        if id == 1:  # current.po
            result = RepoObj()
            with open("tests/current.po", "rb") as f:
                result.data = f.read(9999999)
            return result
        elif id == 2:  # last commit_id
            result = RepoObj()
            old_commit = RepoObj()
            old_commit.commit_time = 12346578
            old_commit.id = 3
            result.parents = [
                old_commit,
            ]
            return result
        elif id == 3:  # old_commit_id
            result = RepoObj()
            old_file = RepoObj()
            old_file.id = 4
            result.tree = {"tests/current.po": old_file}
            return result
        elif id == 4:
            result = RepoObj()
            with open("tests/old.po", "rb") as f:
                result.data = f.read(9999999)
            return result

    def diff(self, commit_id: int):
        if commit_id == 3:
            result = RepoObj()
            with open("tests/diff.txt", "rb") as f:
                result.data = f.read(9999999)
            return [
                result,
            ]

    def blame(self, filename, min_line=None, max_line=None) -> list:
        assert filename == "tests/current.po"
        result = RepoObj()
        result.final_commit_id = 2
        final_committer = RepoObj()
        final_committer.offset = 60
        result.final_committer = final_committer
        return [
            result,
        ]


class Test(TestCase):
    def setUp(self):
        self.repo = MockRepository()
        self.file_id = 1
        self.file_path = "tests/current.po"
        self.blamehunk = RepoObj()
        self.blamehunk.final_commit_id = 2

    def test_get_fuzzy_entries(self):
        fuzzies = list(get_fuzzy_entries(self.repo, self.file_id))
        self.assertEqual([28, 51], fuzzies)

    def test_get_commit_patches(self):
        commit = RepoObj()
        commit.id = 3
        commit_patches = list(get_commit_patches(self.repo, commit, self.file_path))
        self.assertEqual(len(commit_patches), 1)

    def test_get_line_start_old(self):
        commit = RepoObj()
        commit.id = 3
        commit_patch = list(get_commit_patches(self.repo, commit, self.file_path))[0]
        result = get_line_start_old(commit_patch[4:], 28)
        self.assertEqual(25, result)

    def test_get_old_version(self):
        result = get_old_version(self.repo, self.file_path, 28, self.blamehunk)
        self.assertEqual("This is the old entry msgid", result[:27])
        result = get_old_version(self.repo, self.file_path, 51, self.blamehunk)
        self.assertEqual("This is another entry msgid", result[:27])

    def test_populate(self):
        cur_diff = {
            "linenum": 28,
            "repo": self.repo,
        }
        result = populate(self.repo, self.file_path, 1, cur_diff)
        self.assertEqual(result[0], 28)
        self.assertEqual(result[1].final_commit_id, 2)
        self.assertEqual("This is the new entry msgid", result[2][:27])
        self.assertEqual("This is the old entry msgid", result[3][:27])
        self.assertEqual(result[4], timezone(timedelta(seconds=3600)))
