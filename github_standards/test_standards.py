# -*-: coding: utf-8

#
# Copyright 2023-Present Sonatype Inc.
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
#
import unittest

from unittest.mock import MagicMock
from github.Repository import Repository

from github_standards import standards


class TestStandardProps(unittest.TestCase):
    def test_props_in_spec_makes_no_change(self):
        # noinspection PyTypeChecker
        repo = Repository(requester='', headers='',
                          attributes={"url": "https://mygithuburl.git",
                                      "name": "myrepo",
                                      "allow_auto_merge": False,
                                      "allow_merge_commit": True,
                                      "allow_rebase_merge": False,
                                      "allow_squash_merge": True,
                                      "allow_update_branch": True,
                                      "delete_branch_on_merge": True,
                                      "has_discussions": True,
                                      "has_issues": True,
                                      "has_projects": False,
                                      "has_wiki": False,
                                      "web_commit_signoff_required": True},
                          completed='')
        result = standards.check_and_apply_standard_properties_to_repo(repo)

        self.assertEqual(result, "")

    def test_props_out_of_spec_makes_a_change(self):
        # noinspection PyTypeChecker
        repo = Repository(requester='', headers='',
                          attributes={"url": "https://mygithuburl.git",
                                      "name": "myrepo",
                                      "allow_auto_merge": False,
                                      "allow_merge_commit": True,
                                      "allow_rebase_merge": False,
                                      "allow_squash_merge": True,
                                      "allow_update_branch": True,
                                      "delete_branch_on_merge": True,
                                      "has_discussions": True,
                                      "has_issues": True,
                                      "has_projects": True,  # this is the only change
                                      "has_wiki": False,
                                      "web_commit_signoff_required": True},
                          completed='')
        repo.edit = MagicMock()
        result = standards.check_and_apply_standard_properties_to_repo(repo)

        self.assertEqual(result, "has_projects")  # add assertion here
        repo.edit.assert_called_with(allow_auto_merge=False,
                                     allow_merge_commit=True,
                                     allow_rebase_merge=False,
                                     allow_squash_merge=True,
                                     allow_update_branch=True,
                                     delete_branch_on_merge=True,
                                     has_discussions=True,
                                     has_issues=True,
                                     has_projects=False,   # this is the only change
                                     has_wiki=False,
                                     web_commit_signoff_required=True)

    def test_props_out_of_spec_makes_many_changes(self):
        # noinspection PyTypeChecker
        repo = Repository(requester='', headers='',
                          attributes={"url": "https://mygithuburl.git",
                                      "name": "myrepo",
                                      "allow_auto_merge": False,
                                      "allow_merge_commit": True,
                                      "allow_rebase_merge": False,
                                      "allow_squash_merge": False, # this is change 1
                                      "allow_update_branch": True,
                                      "delete_branch_on_merge": True,
                                      "has_discussions": True,
                                      "has_issues": True,
                                      "has_projects": True,  # this is change 2
                                      "has_wiki": False,
                                      "web_commit_signoff_required": True},
                          completed='')
        repo.edit = MagicMock()
        result = standards.check_and_apply_standard_properties_to_repo(repo)

        self.assertEqual(result, "allow_squash_merge,has_projects")  # add assertion here
        repo.edit.assert_called_with(allow_auto_merge=False,
                                     allow_merge_commit=True,
                                     allow_rebase_merge=False,
                                     allow_squash_merge=True,  # this is change 1
                                     allow_update_branch=True,
                                     delete_branch_on_merge=True,
                                     has_discussions=True,
                                     has_issues=True,
                                     has_projects=False,   # this is change 2
                                     has_wiki=False,
                                     web_commit_signoff_required=True)


if __name__ == '__main__':
    unittest.main()
