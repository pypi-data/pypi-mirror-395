from mcp.server.fastmcp import FastMCP
from typing import List, Optional
from .azdo_client import client
from .config import settings

mcp = FastMCP("ado-pr-manager")


@mcp.tool()
def create_pr(
    title: str,
    source_branch: str,
    target_branch: Optional[str] = None,
    repository_id: Optional[str] = None,
    description: Optional[str] = None,
    work_items: Optional[List[int]] = None,
) -> str:
    """Create a new Pull Request."""
    repo_id = repository_id or settings.AZDO_REPO_ID
    if not repo_id:
        return "Error: repository_id is required (arg or env AZDO_REPO_ID)"

    tgt_branch = target_branch or settings.AZDO_DEFAULT_BRANCH
    if not tgt_branch:
        return "Error: target_branch is required (arg or env AZDO_DEFAULT_BRANCH)"

    try:
        pr = client.create_pr(
            title=title,
            source_branch=source_branch,
            target_branch=tgt_branch,
            repository_id=repo_id,
            description=description,
            work_items=work_items,
        )
        return f"PR Created: {pr.get('url')} (ID: {pr.get('pullRequestId')})"
    except Exception as e:
        return f"Error creating PR: {str(e)}"


@mcp.tool()
def get_pr(
    pull_request_id: int,
    repository_id: Optional[str] = None,
) -> str:
    """Get details of a Pull Request."""
    repo_id = repository_id or settings.AZDO_REPO_ID
    if not repo_id:
        return "Error: repository_id is required"

    try:
        pr = client.get_pr(pull_request_id, repo_id)
        return str(pr)
    except Exception as e:
        return f"Error getting PR: {str(e)}"


@mcp.tool()
def list_prs(
    repository_id: Optional[str] = None,
    status: str = "Active",
    creator_id: Optional[str] = None,
    top: Optional[int] = None,
) -> str:
    """List Pull Requests."""
    repo_id = repository_id or settings.AZDO_REPO_ID
    if not repo_id:
        return "Error: repository_id is required"

    try:
        prs = client.list_prs(repo_id, status, creator_id, top)
        return str(prs)
    except Exception as e:
        return f"Error listing PRs: {str(e)}"


@mcp.tool()
def update_pr(
    pull_request_id: int,
    repository_id: Optional[str] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    status: Optional[str] = None,
) -> str:
    """Update a Pull Request."""
    repo_id = repository_id or settings.AZDO_REPO_ID
    if not repo_id:
        return "Error: repository_id is required"

    try:
        pr = client.update_pr(pull_request_id, repo_id, title, description, status)
        return f"PR Updated: {pr.get('pullRequestId')}"
    except Exception as e:
        return f"Error updating PR: {str(e)}"


@mcp.tool()
def add_comment(
    pull_request_id: int,
    content: str,
    repository_id: Optional[str] = None,
    parent_comment_id: Optional[int] = None,
) -> str:
    """Add a comment to a Pull Request."""
    repo_id = repository_id or settings.AZDO_REPO_ID
    if not repo_id:
        return "Error: repository_id is required"

    try:
        comment = client.add_comment(
            pull_request_id, repo_id, content, parent_comment_id
        )
        return f"Comment added: {comment.get('id')}"
    except Exception as e:
        return f"Error adding comment: {str(e)}"


@mcp.tool()
def get_pr_comments(
    pull_request_id: int,
    repository_id: Optional[str] = None,
) -> str:
    """Get comments for a Pull Request."""
    repo_id = repository_id or settings.AZDO_REPO_ID
    if not repo_id:
        return "Error: repository_id is required"

    try:
        comments = client.get_pr_comments(pull_request_id, repo_id)
        return str(comments)
    except Exception as e:
        return f"Error getting comments: {str(e)}"


@mcp.tool()
def get_pr_changes(
    pull_request_id: int,
    repository_id: Optional[str] = None,
) -> str:
    """Get changes in a Pull Request."""
    repo_id = repository_id or settings.AZDO_REPO_ID
    if not repo_id:
        return "Error: repository_id is required"

    try:
        changes = client.get_pr_changes(pull_request_id, repo_id)
        return str(changes)
    except Exception as e:
        return f"Error getting changes: {str(e)}"


@mcp.tool()
def get_file_diff(
    pull_request_id: int,
    file_path: str,
    repository_id: Optional[str] = None,
) -> str:
    """Get diff for a file in a Pull Request."""
    repo_id = repository_id or settings.AZDO_REPO_ID
    if not repo_id:
        return "Error: repository_id is required"

    try:
        diff = client.get_file_diff(pull_request_id, repo_id, file_path)
        return diff
    except Exception as e:
        return f"Error getting diff: {str(e)}"


def main():
    mcp.run()


if __name__ == "__main__":
    main()
