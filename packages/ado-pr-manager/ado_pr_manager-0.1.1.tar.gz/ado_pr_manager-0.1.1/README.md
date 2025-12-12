# AdoPrManager

An MCP server to manage Azure DevOps Pull Requests.

## Features

- **Create PR**: Create new pull requests with title, description, and linked work items.
- **Get PR**: Retrieve detailed information about a specific PR.
- **List PRs**: List PRs with filtering by status, creator, and repository.
- **Update PR**: Update PR status (e.g., abandon, complete) or details.
- **Comments**: Add and retrieve comments on PR threads.
- **Diffs**: View file diffs and changed files in a PR.

## Requirements

- Python 3.10+
- Azure DevOps Personal Access Token (PAT) with **Code (Read & Write)** and **Pull Request Threads (Read & Write)** scopes.

## Installation

### Local Development

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    cd ado-pr-manager
    ```

2.  Create and activate a virtual environment:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  Install dependencies:
    ```bash
    pip install -e .
    ```

4.  Configure environment variables:
    ```bash
    cp .env.example .env
    # Edit .env with your Azure DevOps details
    ```

## Configuration

The server is configured via environment variables (in `.env` or passed directly):

- `AZDO_ORG_URL`: Your Azure DevOps organization URL (e.g., `https://dev.azure.com/myorg`).
- `AZDO_PAT`: Your Personal Access Token.
- `AZDO_REPO_ID` (or `AZDO_REPO`): Default repository ID or name.
- `AZDO_DEFAULT_BRANCH`: Default target branch for new PRs (default: `main`).
- `AZDO_PROJECT`: Default project name (optional).

## Usage

### Running the Server

You can run the MCP server directly:

```bash
python -m ado_pr_manager.server
```

### Using with MCP Client

Add the server to your MCP client configuration (e.g., `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "ado-pr-manager": {
      "command": "python",
      "args": [
        "-m",
        "ado_pr_manager.server"
      ],
      "env": {
        "AZDO_ORG_URL": "https://dev.azure.com/myorg",
        "AZDO_PAT": "my-token",
        "AZDO_REPO_ID": "my-repo"
      }
    }
  }
}
```

### Manual Verification

A script is provided to manually verify the server against the real Azure DevOps API:

```bash
python scripts/test_manual.py
```

## Development

- **Install dev dependencies**:
    ```bash
    pip install -e .[dev]
    ```
    (Or manually: `pip install pytest pytest-mock black flake8 pre-commit build twine`)

- **Run tests**:
    ```bash
    pytest
    ```

- **Run linting**:
    ```bash
    pre-commit run --all-files
    ```

- **Publish to PyPI**:
    ```bash
    ./scripts/publish.sh
    ```
