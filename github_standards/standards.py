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
from typing import Optional

from github import Repository, Branch, GithubException
from github.BranchProtection import BranchProtection


def check_and_apply_standard_properties_to_repo(repo: Repository, do_actual_work: bool = False) -> str:
    # check if repo is already in spec
    standard_props = {
        'allow_auto_merge': False,
        'allow_merge_commit': True,
        'allow_rebase_merge': False,
        'allow_squash_merge': True,
        'allow_update_branch': True,
        'delete_branch_on_merge': True,
        'has_discussions': True,
        'has_issues': True,
        'has_projects': False,
        'has_wiki': False,
        'web_commit_signoff_required': True
    }

    props_not_as_per_standards = ''
    for prop, val in standard_props.items():
        if getattr(repo, prop) != val:
            print(f'        {prop} is not set to {val} in {repo.name}')
            if props_not_as_per_standards != '':
                props_not_as_per_standards = f'{props_not_as_per_standards},'
            props_not_as_per_standards = props_not_as_per_standards + prop

    if props_not_as_per_standards != '':
        print(f'    Setting Standards for {repo.name} - missing {props_not_as_per_standards}')
        if do_actual_work:
            repo.edit(**standard_props)
            print(f'        Repo Standards applied')

    return props_not_as_per_standards


def check_and_apply_standard_properties_to_branch(repo, branch: Branch, do_actual_work: bool = False) -> str:
    branch_protection: Optional[BranchProtection] = None
    try:
        branch_protection = branch.get_protection()
    except GithubException as e:
        # GH returns a 404 when Branch Protection is not yet enabled for the branch in question
        print(f'    Branch {branch} is not protected in {repo.name}')

    # check if branch is already in spec
    standard_branch_protection = {
        'allow_deletions': False,
        'allow_force_pushes': False,
    }
    props_not_as_per_standards = ''
    if branch_protection is not None:
        for prop, val in standard_branch_protection.items():
            if getattr(branch_protection, prop) != val:
                print(f'        {prop} is not set to {val} in {repo.name}')
                if props_not_as_per_standards != '':
                    props_not_as_per_standards = f'{props_not_as_per_standards},'
                props_not_as_per_standards = props_not_as_per_standards + prop

    if branch_protection is None or props_not_as_per_standards != '':
        print(f'    Setting Standards for {repo.name} - missing {props_not_as_per_standards}')
        if do_actual_work:
            branch.edit_protection(**standard_branch_protection)
            print(f'        Branch Standards applied')

    standard_pull_request_reviews = {
        'require_code_owner_reviews': True,
        'required_approving_review_count': 1,  # Perhaps we should allow this to be greater than 1?
    }
    missing_pr_standards = ''
    for prop, val in standard_pull_request_reviews.items():
        if getattr(branch.get_required_pull_request_reviews(), prop) != val:
            print(f'        {prop} is not set to {val} in {repo.name}')
            if missing_pr_standards != '':
                missing_pr_standards = f'{missing_pr_standards},'
            missing_pr_standards = missing_pr_standards + prop

    if missing_pr_standards != '':
        print(f'    Setting Standards for {repo.name} - missing {missing_pr_standards}')
        if do_actual_work:
            branch.edit_protection(**standard_pull_request_reviews)
            print(f'        Branch Standards applied')

    if not branch.get_required_signatures():
        print(f'        required_signatures is not set to True in {repo.name}')
        if missing_pr_standards != '':
            missing_pr_standards = f'{missing_pr_standards},'
        missing_pr_standards = missing_pr_standards + 'required_signatures'
        if do_actual_work:
            branch.add_required_signatures()
            print(f'        Branch required signatures applied')

    if missing_pr_standards != '':
        props_not_as_per_standards = f'{props_not_as_per_standards},'

    return props_not_as_per_standards + missing_pr_standards
