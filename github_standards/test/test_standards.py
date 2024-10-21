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

from github import GithubException
from github.Branch import Branch
from github.BranchProtection import BranchProtection
from github.Repository import Repository
from github.Requester import Requester
from github.RequiredPullRequestReviews import RequiredPullRequestReviews

from github_standards import standards

MOCK_REPO_URL = 'https://mygithuburl.git'


class TestStandardProps(unittest.TestCase):
    def test_props_in_spec_makes_no_change(self):
        # noinspection PyTypeChecker
        repo = Repository(requester='', headers='',
                          attributes={"url": MOCK_REPO_URL,
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
                          attributes={"url": MOCK_REPO_URL,
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
        result = standards.check_and_apply_standard_properties_to_repo(repo, True)

        self.assertEqual(result, "has_projects")  # add assertion here
        repo.edit.assert_called_with(allow_auto_merge=False,
                                     allow_merge_commit=True,
                                     allow_rebase_merge=False,
                                     allow_squash_merge=True,
                                     allow_update_branch=True,
                                     delete_branch_on_merge=True,
                                     has_discussions=True,
                                     has_issues=True,
                                     has_projects=False,  # this is the only change
                                     has_wiki=False,
                                     web_commit_signoff_required=True)

    def test_props_out_of_spec_makes_many_changes(self):
        # noinspection PyTypeChecker
        repo = Repository(requester='', headers='',
                          attributes={"url": MOCK_REPO_URL,
                                      "name": "myrepo",
                                      "allow_auto_merge": False,
                                      "allow_merge_commit": True,
                                      "allow_rebase_merge": False,
                                      "allow_squash_merge": False,  # this is change 1
                                      "allow_update_branch": True,
                                      "delete_branch_on_merge": True,
                                      "has_discussions": True,
                                      "has_issues": True,
                                      "has_projects": True,  # this is change 2
                                      "has_wiki": False,
                                      "web_commit_signoff_required": True},
                          completed='')
        repo.edit = MagicMock()
        result = standards.check_and_apply_standard_properties_to_repo(repo, True)

        self.assertEqual(result, "allow_squash_merge,has_projects")  # add assertion here
        repo.edit.assert_called_with(allow_auto_merge=False,
                                     allow_merge_commit=True,
                                     allow_rebase_merge=False,
                                     allow_squash_merge=True,  # this is change 1
                                     allow_update_branch=True,
                                     delete_branch_on_merge=True,
                                     has_discussions=True,
                                     has_issues=True,
                                     has_projects=False,  # this is change 2
                                     has_wiki=False,
                                     web_commit_signoff_required=True)

    @staticmethod
    def create_mock_repo():
        # noinspection PyTypeChecker
        repo = Repository(requester='', headers='', attributes={"url": MOCK_REPO_URL, "name": "myrepo"},
                          completed='')
        return repo

    @staticmethod
    def create_mock_requester():
        # noinspection PyTypeChecker
        requester = Requester('', MOCK_REPO_URL, '', user_agent='', per_page=0, verify=False, retry=0,
                              pool_size=0)
        requester.requestJsonAndCheck = MagicMock()
        requester.requestJsonAndCheck.return_value = [None, None]
        return requester

    def test_props_in_spec_branch_makes_no_change(self):
        repo = self.create_mock_repo()

        requester = self.create_mock_requester()
        # noinspection PyTypeChecker
        branch = Branch(requester='', headers='', attributes={}, completed='')
        branch.get_protection = MagicMock()
        # noinspection PyTypeChecker
        bp = BranchProtection(requester=requester, headers='', attributes={"url": MOCK_REPO_URL,
                                                                           "allow_deletions": {"enabled": False},
                                                                           "allow_force_pushes": {"enabled": False}},
                              completed='')
        branch.get_protection.return_value = bp

        branch.get_required_pull_request_reviews = MagicMock()
        # noinspection PyTypeChecker
        rprr = RequiredPullRequestReviews(requester=requester, headers='', attributes={"url": MOCK_REPO_URL,
                                                                                       'require_code_owner_reviews': True,
                                                                                       'required_approving_review_count': 1},
                                          completed='')
        branch.get_required_pull_request_reviews.return_value = rprr

        branch.get_required_signatures = MagicMock()
        branch.get_required_signatures.return_value = True

        result = standards.check_and_apply_standard_properties_to_branch(repo, branch)

        self.assertEqual(result, "")

    def test_props_out_of_spec_branch_makes_a_change_no_branch_protection(self):
        repo = self.create_mock_repo()

        requester = self.create_mock_requester()
        # noinspection PyTypeChecker
        branch = Branch(requester='', headers='', attributes={}, completed='')
        branch.get_protection = MagicMock()
        # noinspection PyTypeChecker
        ghe = GithubException(status=404, data=None)
        branch.get_protection.side_effect = ghe

        branch.edit_protection = MagicMock()

        branch.get_required_pull_request_reviews = MagicMock()
        # noinspection PyTypeChecker
        rprr = RequiredPullRequestReviews(requester=requester, headers='', attributes={"url": MOCK_REPO_URL,
                                                                                       'require_code_owner_reviews': True,
                                                                                       'required_approving_review_count': 1},
                                          completed='')
        branch.get_required_pull_request_reviews.return_value = rprr

        branch.get_required_signatures = MagicMock()
        branch.get_required_signatures.return_value = True

        result = standards.check_and_apply_standard_properties_to_branch(repo, branch, True)

        self.assertEqual(result, "")
        branch.edit_protection.assert_called_once_with(allow_deletions=False,
                                                       allow_force_pushes=False)  # this is the only change

    def test_props_out_of_spec_branch_makes_a_change(self):
        repo = self.create_mock_repo()

        requester = self.create_mock_requester()
        # noinspection PyTypeChecker
        branch = Branch(requester='', headers='', attributes={}, completed='')
        branch.get_protection = MagicMock()
        # noinspection PyTypeChecker
        bp = BranchProtection(requester=requester, headers='', attributes={"url": MOCK_REPO_URL,
                                                                           "allow_deletions": {"enabled": False},
                                                                           "allow_force_pushes": {"enabled": True}},
                              # this is the only change
                              completed='')
        branch.get_protection.return_value = bp

        branch.edit_protection = MagicMock()

        branch.get_required_pull_request_reviews = MagicMock()
        # noinspection PyTypeChecker
        rprr = RequiredPullRequestReviews(requester=requester, headers='', attributes={"url": MOCK_REPO_URL,
                                                                                       'require_code_owner_reviews': True,
                                                                                       'required_approving_review_count': 1},
                                          completed='')
        branch.get_required_pull_request_reviews.return_value = rprr

        branch.get_required_signatures = MagicMock()
        branch.get_required_signatures.return_value = True

        result = standards.check_and_apply_standard_properties_to_branch(repo, branch, True)

        self.assertEqual(result, "allow_force_pushes")  # add assertion here
        branch.edit_protection.assert_called_once_with(allow_deletions=False,
                                                       allow_force_pushes=False)  # this is the only change

    def test_props_out_of_spec_branch_makes_many_changes(self):
        repo = self.create_mock_repo()

        requester = self.create_mock_requester()
        # noinspection PyTypeChecker
        branch = Branch(requester='', headers='', attributes={}, completed='')
        branch.get_protection = MagicMock()
        # noinspection PyTypeChecker
        bp = BranchProtection(requester=requester, headers='', attributes={"url": MOCK_REPO_URL,
                                                                           "allow_deletions": {"enabled": False},
                                                                           "allow_force_pushes": {"enabled": True}},
                              # change 1
                              completed='')
        branch.get_protection.return_value = bp

        branch.edit_protection = MagicMock()

        branch.get_required_pull_request_reviews = MagicMock()
        # noinspection PyTypeChecker
        rprr = RequiredPullRequestReviews(requester=requester, headers='', attributes={"url": MOCK_REPO_URL,
                                                                                       'require_code_owner_reviews': True,
                                                                                       'required_approving_review_count': 0},
                                          # change 2
                                          completed='')
        branch.get_required_pull_request_reviews.return_value = rprr

        branch.get_required_signatures = MagicMock()
        branch.get_required_signatures.return_value = False  # change 3

        branch.add_required_signatures = MagicMock()

        result = standards.check_and_apply_standard_properties_to_branch(repo, branch, True)

        self.assertEqual(result,
                         "allow_force_pushes,required_approving_review_count,required_signatures")
        branch.edit_protection.assert_any_call(allow_deletions=False,
                                               allow_force_pushes=False)
        branch.edit_protection.assert_called_with(require_code_owner_reviews=True,
                                                  required_approving_review_count=1)
        branch.add_required_signatures.assert_called()


if __name__ == '__main__':
    unittest.main()
