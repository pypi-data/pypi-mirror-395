import sys
import requests
from ado_pr_manager.azdo_client import client
from ado_pr_manager.config import settings


def debug_update_pr(pr_id):
    repo_id = settings.AZDO_REPO_ID
    if not repo_id:
        print("Error: AZDO_REPO_ID not set in environment")
        return

    print(f"Attempting to update PR {pr_id} in repo {repo_id}...")

    # Try a simple update (e.g., changing description slightly or just fetching)
    # The user reported error on update, so let's try to replicate the call they might be making.
    # If they are trying to change status, let's try that or just a dummy update.

    # First, get current PR state
    try:
        pr = client.get_pr(pr_id, repo_id)
        print(f"Current PR Status: {pr.get('status')}")
    except Exception as e:
        print(f"Error fetching PR: {e}")
        return

    # Try to update description (safe operation)
    try:
        # We'll append a timestamp or something to description to ensure it's a change
        # But for reproduction, maybe just sending the same data or a known valid update is enough.
        # Let's try to set description to itself for now, or just pass a title.

        # Actually, let's try to reproduce the exact error by calling the client method directly
        # with some dummy data.

        # IMPORTANT: We want to see the response content for the 400 error.
        # The client raises exception, so we need to catch it and inspect response if available.

        # We will manually construct the request here to inspect the response,
        # mirroring what client.update_pr does.

        url = client._get_url(f"git/repositories/{repo_id}/pullrequests/{pr_id}")
        payload = {"description": pr.get("description", "") + "\n\n[Debug update]"}

        print(f"Sending PATCH request to: {url}")
        print(f"Payload: {payload}")

        response = requests.patch(url, headers=client.headers, json=payload)

        print(f"Response Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")

        response.raise_for_status()
        print("Update successful!")

    except Exception as e:
        print(f"Caught exception: {e}")


if __name__ == "__main__":
    debug_update_pr(1673)
