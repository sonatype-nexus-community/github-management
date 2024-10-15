from github import Repository


def check_and_apply_standard_properties_to_repo(repo: Repository) -> str:
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
    applied_props = ""
    for prop, val in standard_props.items():
        if getattr(repo, prop) != val:
            print(f'        {prop} is not set to {val} in {repo.name}')
            if applied_props != "":
                applied_props = applied_props + ","
            applied_props = applied_props + prop

    if applied_props != "":
        print(f'    Setting Standards for {repo.name}')
        repo.edit(
            allow_auto_merge=False,
            allow_merge_commit=True,
            allow_rebase_merge=False,
            allow_squash_merge=True,
            allow_update_branch=True,
            delete_branch_on_merge=True,
            has_discussions=True,
            has_issues=True,
            has_projects=False,
            has_wiki=False,
            web_commit_signoff_required=True
        )
        print(f'        Repo Standards applied')

    return applied_props
