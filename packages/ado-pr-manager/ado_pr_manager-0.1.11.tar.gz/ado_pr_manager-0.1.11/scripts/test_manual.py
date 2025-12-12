from ado_pr_manager.azdo_client import client
from ado_pr_manager.config import settings


def main():
    print("Testing AdoPrManager against real API...")

    repo_id = settings.AZDO_REPO_ID
    if not repo_id:
        print("Error: AZDO_REPO_ID (or AZDO_REPO) not set in environment")
        return

    try:
        print(f"Listing PRs for repo {repo_id}...")
        prs = client.list_prs(repository_id=repo_id, top=5)
        print(f"Found {len(prs)} PRs")
        for pr in prs:
            print(f"- {pr.get('pullRequestId')}: {pr.get('title')}")

        if prs:
            pr_id = prs[0]["pullRequestId"]
            print(f"\nGetting details for PR {pr_id}...")
            pr = client.get_pr(pr_id, repo_id)
            print(f"Title: {pr.get('title')}")
            print(f"Status: {pr.get('status')}")

            print(f"\nGetting comments for PR {pr_id}...")
            comments = client.get_pr_comments(pr_id, repo_id)
            print(f"Found {len(comments)} threads")

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
