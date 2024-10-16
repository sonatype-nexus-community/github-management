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
import os

from github import Auth, Github
from github.Repository import Repository

from github_standards.standards import check_and_apply_standard_properties_to_repo

GH_ORG_NAME = 'sonatype-nexus-community'
EXCLUDED_REPO_NAMES = ['.github']


def apply_standards_to_repo(repo: Repository, do_actual_work: bool = False) -> None:
    if repo.name not in EXCLUDED_REPO_NAMES:
        print(f'Reviewing Repo: {repo.name}...')

        if repo.custom_properties.get('Auto-Apply-Standards', 'false') == 'false':
            print(f'    Skipping {repo.name} as not part of standards management (yet!)')

        print(f'    Assessing Standards for {repo.name}')
        check_and_apply_standard_properties_to_repo(repo, do_actual_work)

        main_branch = repo.default_branch
        if main_branch != 'main':
            print(f'    WARNING: {repo.name}\'s default branch is not called main it is: {main_branch}')

        if do_actual_work:
            main_b = repo.get_branch(main_branch)

            if main_b:
                main_b.edit_protection(
                    allow_deletions=False,
                    allow_force_pushes=False,
                    require_code_owner_reviews=True,
                    required_approving_review_count=1,
                )
                main_b.add_required_signatures()

                # @todo: Status Checks as this relies upon GitHub actions being present
                # main_b.edit_required_status_checks(strict=True, contexts=[
                #
                # ])
            else:
                print(f'There is no branch {main_branch} in {repo.name}')

        # print(dir(repo.permissions))


def main() -> None:
    gh_token = os.getenv('GH_TOKEN', None)

    if not gh_token:
        print(f'GH_TOKEN environment variable not set.')
        exit(1)

    with Github(auth=Auth.Token(gh_token)) as gh:
        gh_org = gh.get_organization(GH_ORG_NAME)

        repo = gh_org.get_repo('github-management')
        apply_standards_to_repo(repo=repo, do_actual_work=True)

        # List all Repos
        # for repo in gh_org.get_repos():
        #     if repo.custom_properties.get('Auto-Apply-Standards', 'false') != 'false':
        #         apply_standards_to_repo(repo=repo, do_actual_work=True)
        #     else:
        #         print(f'Skipping {repo.name} as Auto-Apply-Standards is not true')


if __name__ == "__main__":
    main()
