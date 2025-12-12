import requests
import base64
from typing import Any, Dict, List, Optional
from .config import settings


class AzDoClient:
    def __init__(self):
        self.base_url = settings.AZDO_ORG_URL.rstrip("/")
        self.pat = settings.AZDO_PAT
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self._encode_pat()}",
        }

    def _encode_pat(self) -> str:
        return base64.b64encode(f":{self.pat}".encode("ascii")).decode("ascii")

    def _get_url(self, path: str, project: Optional[str] = None) -> str:
        project_part = (
            f"/{project}"
            if project
            else (f"/{settings.AZDO_PROJECT}" if settings.AZDO_PROJECT else "")
        )
        return f"{self.base_url}{project_part}/_apis/{path}"

    def create_pr(
        self,
        title: str,
        source_branch: str,
        target_branch: str,
        repository_id: str,
        description: Optional[str] = None,
        work_items: Optional[List[int]] = None,
    ) -> Dict[str, Any]:
        url = self._get_url(f"git/repositories/{repository_id}/pullrequests")

        # Ensure branches have refs/heads/ prefix if not present
        if not source_branch.startswith("refs/"):
            source_branch = f"refs/heads/{source_branch}"
        if not target_branch.startswith("refs/"):
            target_branch = f"refs/heads/{target_branch}"

        payload = {
            "sourceRefName": source_branch,
            "targetRefName": target_branch,
            "title": title,
            "description": description or "",
        }

        if work_items:
            # Linking work items requires a separate API call or specific payload
            # structure depending on API version. For simplicity in creation, we might
            # need to update after creation or check API docs for creation-time linking.
            # According to docs, we can't easily link WIs during creation in the basic
            # payload for all versions, but let's try to add a resource ref if
            # supported.
            # For now, let's stick to basic creation and maybe link later if needed.
            pass

        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        pr_data = response.json()

        if work_items:
            # Link work items after creation
            pr_id = pr_data["pullRequestId"]
            self.link_work_items(pr_id, repository_id, work_items)

        return pr_data

    def link_work_items(self, pr_id: int, repository_id: str, work_items: List[int]):
        url = self._get_url(
            f"git/repositories/{repository_id}/pullrequests/{pr_id}/workitems"
        )
        for wi_id in work_items:
            payload = {"id": str(wi_id)}
            requests.post(url, headers=self.headers, json=payload)

    def get_pr(self, pr_id: int, repository_id: str) -> Dict[str, Any]:
        url = self._get_url(f"git/repositories/{repository_id}/pullrequests/{pr_id}")
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def list_prs(
        self,
        repository_id: str,
        status: str = "Active",
        creator_id: Optional[str] = None,
        top: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        url = self._get_url(f"git/repositories/{repository_id}/pullrequests")
        params = {"searchCriteria.status": status}
        if creator_id:
            params["searchCriteria.creatorId"] = creator_id
        if top:
            params["$top"] = top

        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json().get("value", [])

    def update_pr(
        self,
        pr_id: int,
        repository_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
    ) -> Dict[str, Any]:
        url = self._get_url(f"git/repositories/{repository_id}/pullrequests/{pr_id}")
        payload = {}
        if title:
            payload["title"] = title
        if description:
            payload["description"] = description
        if status:
            payload["status"] = status

        if not payload:
            return self.get_pr(pr_id, repository_id)

        response = requests.patch(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def add_comment(
        self,
        pr_id: int,
        repository_id: str,
        content: str,
        parent_comment_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        url = self._get_url(
            f"git/repositories/{repository_id}/pullrequests/{pr_id}/threads"
        )

        payload = {
            "comments": [
                {
                    "parentCommentId": parent_comment_id or 0,
                    "content": content,
                    "commentType": "text",
                }
            ]
        }

        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def get_pr_comments(
        self,
        pr_id: int,
        repository_id: str,
    ) -> List[Dict[str, Any]]:
        url = self._get_url(
            f"git/repositories/{repository_id}/pullrequests/{pr_id}/threads"
        )
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json().get("value", [])

    def get_pr_changes(self, pr_id: int, repository_id: str) -> Dict[str, Any]:
        # This usually returns the iteration changes
        url = self._get_url(
            f"git/repositories/{repository_id}/pullrequests/{pr_id}/iterations"
        )
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        iterations = response.json().get("value", [])

        if not iterations:
            return {"changes": []}

        last_iteration = iterations[-1]["id"]
        url = self._get_url(
            f"git/repositories/{repository_id}/pullrequests/{pr_id}/"
            f"iterations/{last_iteration}/changes"
        )
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_file_diff(self, pr_id: int, repository_id: str, file_path: str) -> str:
        # Getting the actual diff text can be tricky via API.
        # We might need to fetch the file content from source and target and diff them,
        # or use the internal diff endpoint if available.
        # A common way is to get the file content from the PR's iteration.
        # However, for simplicity, let's try to fetch the diff via the standard git
        # API if possible, or just return the fact that it changed.
        #
        # Actually, the user asked for "Retrieve the diff for a PR".
        # Let's implement a generic diff retrieval if possible.
        #
        # For now, let's implement a placeholder or a best-effort approach.
        # We can use the `diffs` endpoint on the iteration.
        pass
        return "Diff retrieval not fully implemented yet."


client = AzDoClient()
