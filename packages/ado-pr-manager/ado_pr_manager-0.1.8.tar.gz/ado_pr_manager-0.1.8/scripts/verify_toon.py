from ado_pr_manager.server import format_pr, format_comment

# Dummy Data
mock_pr = {
    "pullRequestId": 101,
    "title": "Fix login bug",
    "status": "Active",
    "createdBy": {"displayName": "Alice Developer"},
    "url": "https://dev.azure.com/org/proj/_git/repo/pullrequest/101",
    "description": (
        "This PR fixes the issue where users could not login with special characters."
    ),
}

mock_comment = {
    "id": 505,
    "author": {"displayName": "Bob Reviewer"},
    "content": "Looks good to me, but can we add a test case?",
}

print("--- PR FORMAT (TOON) ---")
print(format_pr(mock_pr))
print("\n--- COMMENT FORMAT (TOON) ---")
print(format_comment(mock_comment))
