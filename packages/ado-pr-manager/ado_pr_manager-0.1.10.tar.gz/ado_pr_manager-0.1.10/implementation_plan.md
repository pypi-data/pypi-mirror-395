# Implementation Plan - AdoPrManager

## Goal
Create a new MCP server `AdoPrManager` to manage Azure DevOps Pull Requests.

## Proposed Tools
1.  **`create_pr`**
    - `title` (str): Title of the PR.
    - `source_branch` (str): Name of the source branch (e.g., `feature/my-feature`).
    - `target_branch` (str, optional): Name of the target branch (default: `AZDO_DEFAULT_BRANCH`).
    - `repository_id` (str, optional): ID or name of the repository (default: `AZDO_REPO_ID`).
    - `description` (str, optional): Description of the PR.
    - `work_items` (list[int], optional): IDs of work items to link.

2.  **`get_pr`**
    - `pull_request_id` (int): ID of the PR.
    - `repository_id` (str, optional): ID or name of the repository (default: `AZDO_REPO_ID`).

3.  **`list_prs`**
    - `repository_id` (str, optional): ID or name of the repository (default: `AZDO_REPO_ID`).
    - `status` (str, optional): `Active`, `Completed`, `Abandoned` (default: `Active`).
    - `creator_id` (str, optional): Filter by creator.
    - `top` (int, optional): Number of PRs to return.

4.  **`update_pr`**
    - `pull_request_id` (int): ID of the PR.
    - `repository_id` (str, optional): ID or name of the repository (default: `AZDO_REPO_ID`).
    - `title` (str, optional): New title.
    - `description` (str, optional): New description.
    - `status` (str, optional): `Active`, `Completed`, `Abandoned`.

5.  **`add_comment`**
    - `pull_request_id` (int): ID of the PR.
    - `repository_id` (str, optional): ID or name of the repository (default: `AZDO_REPO_ID`).
    - `content` (str): Comment text.
    - `parent_comment_id` (int, optional): ID of comment to reply to.

6.  **`get_pr_comments`**
    - `pull_request_id` (int): ID of the PR.
    - `repository_id` (str, optional): ID or name of the repository (default: `AZDO_REPO_ID`).
    - `sort_by` (str, optional): `newest`, `oldest` (default: `newest`).

7.  **`get_pr_changes`**
    - `pull_request_id` (int): ID of the PR.
    - `repository_id` (str, optional): ID or name of the repository (default: `AZDO_REPO_ID`).
    - Returns a list of changed files and their change type (edit, add, delete).

8.  **`get_file_diff`**
    - `pull_request_id` (int): ID of the PR.
    - `file_path` (str): Path of the file to diff.
    - `repository_id` (str, optional): ID or name of the repository (default: `AZDO_REPO_ID`).
    - Returns the text diff of the file.

## Configuration
- `AZDO_ORG_URL`: Azure DevOps Organization URL.
- `AZDO_PAT`: Personal Access Token.
- `AZDO_PROJECT`: Default project (optional).
- `AZDO_REPO_ID`: Default Repository ID (optional).
- `AZDO_DEFAULT_BRANCH`: Default target branch (optional, e.g., `main`).

## Architecture
- **Language**: Python 3.10+
- **Framework**: `mcp` (FastMCP)
- **Dependencies**: `requests`, `pydantic`, `typer`, `python-dotenv`
- **Testing**: `pytest` with >80% coverage.
