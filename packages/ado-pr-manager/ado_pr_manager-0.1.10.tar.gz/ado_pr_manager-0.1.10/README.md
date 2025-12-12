# AdoPrManager

A Model Context Protocol (MCP) server for managing Azure DevOps Pull Requests.

## Features

- **Create PR**: Create new pull requests with title, description, and linked work items.
- **Get PR**: Retrieve detailed information about a specific PR.
- **List PRs**: List PRs created by you (default) or where you are a reviewer.
- **Update PR**: Update PR details or perform actions (abandon, draft, publish, reactivate).
- **Comments**: Add and retrieve comments on PR threads.
- **Diffs**: View file diffs and changed files in a PR.

## Quick Start

### Prerequisites

- Python 3.10+
- Azure DevOps Personal Access Token (PAT) with **Code (Read & Write)** and **Pull Request Threads (Read & Write)** scopes.

### Installation

Install via `pip` or `uv`:

```bash
pip install ado-pr-manager
# or
uv pip install ado-pr-manager
```

### Configuration

Set the following environment variables in a `.env` file:

- `AZDO_ORG_URL`: Organization URL (e.g., `https://dev.azure.com/myorg`)
- `AZDO_PAT`: Personal Access Token (Requires **Code** and **Pull Request** Read/Write access)
- `AZDO_PROJECT`: (Optional) Default project name
- `AZDO_REPO_ID`: (Optional) Default repository name or ID (can also use `AZDO_REPO`)
- `AZDO_DEFAULT_BRANCH`: (Optional) Default target branch (default: `main`)

### Usage with Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "ado-pr-manager": {
      "command": "python3",
      "args": ["-m", "ado_pr_manager.server"],
      "env": {
        "AZDO_ORG_URL": "https://dev.azure.com/myorg",
        "AZDO_PAT": "your-token",
        "AZDO_PROJECT": "my-project",
        "AZDO_REPO_ID": "my-repo"
      }
    }
  }
}
```

## Development

1.  **Clone & Install**:
    ```bash
    git clone https://github.com/om-surushe/ado-pr-manager.git
    cd ado-pr-manager
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -e .[dev]
    ```

2.  **Test**:
    ```bash
    pytest
    ```
