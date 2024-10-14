# Sonatype Community GitHub Management

<!-- Badges Section -->
[![shield_gh-workflow-test]][link_gh-workflow-test]
[![shield_license]][license_file]
<!-- Add other badges or shields as appropriate -->

---

This project is here to enforce our [GitHub Standards](https://contribute.sonatype.com/docs/standards/github-repository/) for Sonatype Open Source Community Projects.

- [Usage](#usage)
- [Development](#development)
- [The Fine Print](#the-fine-print)

## Usage

### Running Locally

You will need:
- Python 3.12
- Poetry >= 1.8.1

1. Clone this repository
2. Install dependencies by running `poetry install`
3. Set your `GH_TOKEN` environment variable (see below) and then run `python -m github_standards`

## GitHub Token Requirements

You will need a GitHub Personal Access (Fine Grained) Token with the following permissions:

- Repository Access: All Repositories
- Repository Permissions:
  - Administration: Read + Write
  - Contents: Read Only
  - Custom Properties: Read Only
  - Metadata: Read Only (Mandatory)

## Development

See [CONTRIBUTING.md](./CONTRIBUTING.md) for details.

## The Fine Print

Remember:

This project is part of the [Sonatype Nexus Community](https://github.com/sonatype-nexus-community) organization, which is not officially supported by Sonatype. Please review the latest pull requests, issues, and commits to understand this project's readiness for contribution and use.

* File suggestions and requests on this repo through GitHub Issues, so that the community can pitch in
* Use or contribute to this project according to your organization's policies and your own risk tolerance
* Don't file Sonatype support tickets related to this project— it won't reach the right people that way

Last but not least of all - have fun!

<!-- Links Section -->
[shield_gh-workflow-test]: https://img.shields.io/github/actions/workflow/status/sonatype-nexus-community/github-management/apply-standards.yaml?branch=main&logo=GitHub&logoColor=white "build"
[shield_license]: https://img.shields.io/github/license/sonatype-nexus-community/github-management?logo=open%20source%20initiative&logoColor=white "license"

[link_gh-workflow-test]: https://github.com/sonatype-nexus-community/github-management/actions/workflows/apply-standards.yaml?query=branch%3Amain
[license_file]: https://github.com/sonatype-nexus-community/github-management/blob/main/LICENSE