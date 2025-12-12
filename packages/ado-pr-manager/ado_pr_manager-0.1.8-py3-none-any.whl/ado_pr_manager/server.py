from mcp.server.fastmcp import FastMCP
from typing import List, Optional
from .azdo_client import client
from .config import settings

mcp = FastMCP("ado-pr-manager")


def format_pr(pr: dict) -> str:
    """Format a PR dictionary into a concise string."""
    return (
        f"ID: {pr.get('pullRequestId')}\n"
        f"Title: {pr.get('title')}\n"
        f"Status: {pr.get('status')}\n"
        f"Creator: {pr.get('createdBy', {}).get('displayName')}\n"
        f"Url: {pr.get('url')}\n"
        f"Description: {pr.get('description', '')[:100]}..."
    )


def format_comment(comment: dict) -> str:
    """Format a comment dictionary into a concise string."""
    return (
        f"ID: {comment.get('id')}\n"
        f"Author: {comment.get('author', {}).get('displayName')}\n"
        f"Content: {comment.get('content')}\n"
    )


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
        return format_pr(pr)
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
        return format_pr(pr)
    except Exception as e:
        return f"Error getting PR: {str(e)}"


@mcp.tool()
def list_prs(
    repository_id: Optional[str] = None,
    status: str = "Active",
    top: Optional[int] = None,
    include_reviewer: bool = False,
) -> str:
    """List Pull Requests. Defaults to PRs created by the current user.

    Args:
        repository_id: Repository ID or Name.
        status: Filter by status (Active, Completed, Abandoned, All).
        top: Limit number of results.
        include_reviewer: If True, also include PRs where the user is a reviewer.
    """
    repo_id = repository_id or settings.AZDO_REPO_ID
    if not repo_id:
        return "Error: repository_id is required"

    try:
        prs = client.list_prs(repo_id, status, top, include_reviewer)
        return "\n---\n".join([format_pr(pr) for pr in prs])
    except Exception as e:
        return f"Error listing PRs: {str(e)}"


@mcp.tool()
def update_pr(
    pull_request_id: int,
    repository_id: Optional[str] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    action: Optional[str] = None,
) -> str:
    """Update a Pull Request.

    Args:
        pull_request_id: ID of the PR.
        repository_id: Repository ID or Name.
        title: New title.
        description: New description.
        action: Action to perform: 'abandon', 'draft', 'publish', or 'reactivate'.
    """
    repo_id = repository_id or settings.AZDO_REPO_ID
    if not repo_id:
        return "Error: repository_id is required"

    try:
        pr = client.update_pr(pull_request_id, repo_id, title, description, action)
        return format_pr(pr)
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
        return format_comment(comment.get("comments", [{}])[0])
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
        formatted_threads = []
        for thread in comments:
            thread_comments = thread.get("comments", [])
            if not thread_comments:
                continue
            formatted_thread = "\n".join([format_comment(c) for c in thread_comments])
            formatted_threads.append(
                f"Thread ID: {thread.get('id')}\n{formatted_thread}"
            )
        return "\n---\n".join(formatted_threads)
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
        formatted_changes = []
        for change in changes.get("changeEntries", []):
            item = change.get("item", {})
            formatted_changes.append(
                f"Type: {change.get('changeType')}\n" f"Path: {item.get('path')}\n"
            )
        return "\n---\n".join(formatted_changes)
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
