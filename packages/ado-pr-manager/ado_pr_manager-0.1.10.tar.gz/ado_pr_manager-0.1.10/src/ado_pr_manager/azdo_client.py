import requests
import base64
from typing import Any, Dict, List, Optional
import difflib
from .config import settings


class AzDoClient:
    def __init__(self):
        self.base_url = settings.AZDO_ORG_URL.rstrip("/")
        self.pat = settings.AZDO_PAT
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self._encode_pat()}",
        }
        self._current_user_id: Optional[str] = None

    def get_current_user_id(self) -> str:
        if self._current_user_id:
            return self._current_user_id

        url = f"{self.base_url}/_apis/connectionData"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        self._current_user_id = response.json()["authenticatedUser"]["id"]
        return self._current_user_id

    def _encode_pat(self) -> str:
        return base64.b64encode(f":{self.pat}".encode("ascii")).decode("ascii")

    def _get_url(self, path: str, project: Optional[str] = None) -> str:
        project_part = (
            f"/{project}"
            if project
            else (f"/{settings.AZDO_PROJECT}" if settings.AZDO_PROJECT else "")
        )
        return f"{self.base_url}{project_part}/_apis/{path}?api-version=7.1"

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
        top: Optional[int] = None,
        include_reviewer: bool = False,
    ) -> List[Dict[str, Any]]:
        url = self._get_url(f"git/repositories/{repository_id}/pullrequests")
        current_user_id = self.get_current_user_id()

        # Fetch PRs created by current user
        params_creator = {
            "searchCriteria.status": status,
            "searchCriteria.creatorId": current_user_id,
        }
        if top:
            params_creator["$top"] = top

        response_creator = requests.get(
            url, headers=self.headers, params=params_creator
        )
        response_creator.raise_for_status()
        prs = response_creator.json().get("value", [])

        if include_reviewer:
            # Fetch PRs where current user is a reviewer
            params_reviewer = {
                "searchCriteria.status": status,
                "searchCriteria.reviewerId": current_user_id,
            }
            if top:
                params_reviewer["$top"] = top

            response_reviewer = requests.get(
                url, headers=self.headers, params=params_reviewer
            )
            response_reviewer.raise_for_status()
            reviewer_prs = response_reviewer.json().get("value", [])

            # Merge lists, avoiding duplicates
            seen_ids = {pr["pullRequestId"] for pr in prs}
            for pr in reviewer_prs:
                if pr["pullRequestId"] not in seen_ids:
                    prs.append(pr)

        return prs

    def update_pr(
        self,
        pr_id: int,
        repository_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        action: Optional[str] = None,
    ) -> Dict[str, Any]:
        url = self._get_url(f"git/repositories/{repository_id}/pullrequests/{pr_id}")
        payload = {}
        if title:
            payload["title"] = title
        if description:
            payload["description"] = description

        if action:
            action = action.lower()
            if action == "abandon":
                payload["status"] = "abandoned"
            elif action == "draft":
                payload["isDraft"] = True
            elif action == "publish":
                payload["isDraft"] = False
            elif action == "reactivate":
                payload["status"] = "active"
            else:
                raise ValueError(
                    f"Invalid action: {action}. "
                    "Must be 'abandon', 'draft', 'publish', or 'reactivate'."
                )

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
        # Get PR details to find source and target refs
        pr = self.get_pr(pr_id, repository_id)
        source_ref = pr["sourceRefName"]
        target_ref = pr["targetRefName"]

        # Helper to fetch file content
        def get_content(ref_name: str) -> str:
            url = self._get_url(
                f"git/repositories/{repository_id}/items",
                project=pr.get("repository", {}).get("project", {}).get("name"),
            )
            params = {
                "path": file_path,
                "versionDescriptor.version": ref_name.replace("refs/heads/", ""),
                "versionDescriptor.versionType": "branch",
                "includeContent": "true",
            }
            try:
                response = requests.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                return response.text
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    return ""  # File might not exist in this ref
                raise

        source_content = get_content(source_ref)
        target_content = get_content(target_ref)

        diff = difflib.unified_diff(
            target_content.splitlines(),
            source_content.splitlines(),
            fromfile=f"a/{file_path}",
            tofile=f"b/{file_path}",
            lineterm="",
        )
        return "\n".join(diff)


client = AzDoClient()
