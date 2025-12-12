import pytest
from unittest.mock import patch
from ado_pr_manager.server import (
    create_pr,
    get_pr,
    list_prs,
    update_pr,
    add_comment,
    get_pr_comments,
    get_pr_changes,
    get_file_diff,
)
from ado_pr_manager.config import settings


@pytest.fixture(autouse=True)
def mock_settings():
    settings.AZDO_REPO_ID = "test-repo"
    settings.AZDO_DEFAULT_BRANCH = "main"


@pytest.fixture
def mock_client():
    with patch("ado_pr_manager.server.client") as mock:
        yield mock


def test_create_pr(mock_client):
    mock_client.create_pr.return_value = {
        "url": "http://azdo/pr/1",
        "pullRequestId": 1,
        "title": "Test PR",
        "status": "Active",
    }
    result = create_pr("Test PR", "feature/1")
    assert "ID: 1" in result
    assert "Title: Test PR" in result
    mock_client.create_pr.assert_called_once_with(
        title="Test PR",
        source_branch="feature/1",
        target_branch="main",
        repository_id="test-repo",
        description=None,
        work_items=None,
    )


def test_get_pr(mock_client):
    mock_client.get_pr.return_value = {
        "pullRequestId": 1,
        "title": "Test PR",
        "status": "Active",
    }
    result = get_pr(1)
    assert "ID: 1" in result
    assert "Title: Test PR" in result
    mock_client.get_pr.assert_called_once_with(1, "test-repo")


def test_list_prs(mock_client):
    mock_client.list_prs.return_value = [
        {"pullRequestId": 1, "title": "PR 1", "status": "Active"},
        {"pullRequestId": 2, "title": "PR 2", "status": "Active"},
    ]
    result = list_prs()
    assert "ID: 1" in result
    assert "ID: 2" in result
    mock_client.list_prs.assert_called_once_with("test-repo", "Active", None, False)


def test_update_pr(mock_client):
    mock_client.update_pr.return_value = {
        "pullRequestId": 1,
        "title": "Test PR",
        "status": "Abandoned",
    }
    result = update_pr(1, action="abandon")
    assert "ID: 1" in result
    assert "Status: Abandoned" in result
    mock_client.update_pr.assert_called_once_with(1, "test-repo", None, None, "abandon")


def test_add_comment(mock_client):
    mock_client.add_comment.return_value = {
        "comments": [{"id": 100, "content": "Nice code"}]
    }
    result = add_comment(1, "Nice code")
    assert "ID: 100" in result
    assert "Content: Nice code" in result
    mock_client.add_comment.assert_called_once_with(1, "test-repo", "Nice code", None)


def test_get_pr_comments(mock_client):
    mock_client.get_pr_comments.return_value = [
        {"id": 10, "comments": [{"id": 100, "content": "Nice code"}]}
    ]
    result = get_pr_comments(1)
    assert "Thread ID: 10" in result
    assert "ID: 100" in result
    assert "Content: Nice code" in result
    mock_client.get_pr_comments.assert_called_once_with(1, "test-repo")


def test_get_pr_changes(mock_client):
    mock_client.get_pr_changes.return_value = {
        "changeEntries": [{"changeType": "edit", "item": {"path": "/foo.py"}}]
    }
    result = get_pr_changes(1)
    assert "Type: edit" in result
    assert "Path: /foo.py" in result
    mock_client.get_pr_changes.assert_called_once_with(1, "test-repo")


def test_get_file_diff(mock_client):
    mock_client.get_file_diff.return_value = "diff content"
    result = get_file_diff(1, "file.txt")
    assert "diff content" in result
    mock_client.get_file_diff.assert_called_once_with(1, "test-repo", "file.txt")
