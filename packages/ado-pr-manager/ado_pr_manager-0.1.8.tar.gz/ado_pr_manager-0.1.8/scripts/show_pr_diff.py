from ado_pr_manager.azdo_client import client
from ado_pr_manager.config import settings


def show_diff(pr_id):
    repo_id = settings.AZDO_REPO_ID
    if not repo_id:
        print("Error: AZDO_REPO_ID not set in environment")
        return

    print(f"Fetching PR {pr_id} details...")
    try:
        pr = client.get_pr(pr_id, repo_id)
        print(f"PR Found: {pr.get('title')} (Status: {pr.get('status')})")
    except Exception as e:
        print(f"Error fetching PR: {e}")
        return

    print(f"Fetching changes for PR {pr_id} in repo {repo_id}...")
    try:
        changes = client.get_pr_changes(pr_id, repo_id)

        change_entries = changes.get("changeEntries", [])
        if not change_entries:
            print("No changes found in response.")
            print(f"Raw response: {changes}")
            return

        for change in change_entries:
            item = change.get("item", {})
            path = item.get("path")
            change_type = change.get("changeType")

            print(f"\n--- File: {path} ({change_type}) ---")

            if change_type == "edit":
                diff = client.get_file_diff(pr_id, repo_id, path)
                print(diff)
            else:
                print(f"(Diff not shown for change type: {change_type})")

    except Exception as e:
        print(f"Error fetching changes: {e}")


if __name__ == "__main__":
    show_diff(1673)
