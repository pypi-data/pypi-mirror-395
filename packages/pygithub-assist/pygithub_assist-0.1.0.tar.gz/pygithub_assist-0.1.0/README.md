# github_issue_creator

Version: 0.1.0

## Overview

A lightweight internal Python package to create GitHub issues using PyGithub.
Designed for private distribution inside your company.

## Installation (from git)
```bash
pip install git+https://github.com/your-company/github_issue_creator.git
```

## Quick example
```python
from github_issue_creator import create_issue

resp = create_issue(
    repo_owner="Lokesh-techy",
    repo_name="django-testing",
    title="Automated Issue Creation Test",
    body="Issue body text",
    assignees=["Lokesh-techy"],
    labels=["bug"],
)
print(resp)
```

## Token
Set the GitHub token as an environment variable:
```bash
export GITHUB_ISSUE_CREATION_TOKEN=ghp_...
```

## Notes
- This package depends on `PyGithub`.
- For internal distribution, push this repo to a private GitHub or upload the built wheel to your private PyPI.
