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
from github import Repository


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
