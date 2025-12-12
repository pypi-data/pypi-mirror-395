"""Simple reusable GitHub Issue Creator.

Usage:
    from github_issue_creator import create_issue
    resp = create_issue(
        repo_owner="org",
        repo_name="repo",
        title="Issue title",
        body="Issue body",
        assignees=["user"],
        labels=["bug"]
    )
"""
from github import Github
import os
from typing import List, Optional, Dict, Any
try:
    # internal helper; if not present, fall back to a simple dict response
    from util.api_util import response_code
except Exception:
    class _RC:
        @staticmethod
        def success():
            return {"code": 200, "message": "success"}
        @staticmethod
        def internalError():
            return {"code": 500, "message": "internal_error"}
    response_code = _RC()

GITHUB_TOKEN = os.getenv("GITHUB_ISSUE_CREATION_TOKEN")

def create_issue(
    repo_owner: str,
    repo_name: str,
    title: str,
    body: str = "",
    assignees: Optional[List[str]] = None,
    labels: Optional[List[str]] = None,
    token: Optional[str] = None
) -> Dict[str, Any]:
    """Create an issue on GitHub.

    If `token` is provided, it overrides the environment variable.
    Returns a dict with success or error details.
    """
    token = token or GITHUB_TOKEN
    if not token:
        return {"status": "error", "message": "GitHub token not provided (set GITHUB_ISSUE_CREATION_TOKEN)"}

    try:
        g = Github(token)
        repo = g.get_repo(f"{repo_owner}/{repo_name}")
        new_issue = repo.create_issue(
            title=title,
            body=body,
            assignees=assignees or [],
            labels=labels or [],
        )

        # Build response using response_code helper if available
        resp = response_code.success()
        resp.update({
            "issue_url": new_issue.html_url,
            "issue_number": new_issue.number,
            "issue_title": new_issue.title,
        })
        return resp

    except Exception as e:
        resp = response_code.internalError()
        resp.update({"error": str(e)})
        return resp
