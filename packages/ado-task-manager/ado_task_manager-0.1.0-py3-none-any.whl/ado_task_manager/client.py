"""Client for Azure DevOps API."""

from __future__ import annotations

from typing import Any, Dict, Optional, List
import requests
import base64

from .errors import AdoRequestError
from .models import MCPConfig


class AdoClient:
    """HTTP client for Azure DevOps API."""
    
    def __init__(self, config: MCPConfig) -> None:
        self.config = config
        self.session = requests.Session()
        
        # ADO PAT auth requires base64 encoding of ":<PAT>"
        auth_str = f":{config.ado_pat}"
        b64_auth = base64.b64encode(auth_str.encode()).decode()
        
        self.session.headers.update({
            "Authorization": f"Basic {b64_auth}",
            "Content-Type": "application/json",
        })
        self.base_url = f"{config.ado_org_url}/{config.ado_project}/_apis" if config.ado_project else f"{config.ado_org_url}/_apis"
        # Note: Some calls might need project-level or org-level URLs. 
        # Work items are usually project-scoped but can be accessed via org URL if ID is known.
        # However, creating a work item requires a project.
        # We will assume project is in config or passed in.
        
    def __enter__(self) -> "AdoClient":
        return self
    
    def __exit__(self, *args: Any) -> None:
        self.session.close()
    
    def _handle_error(self, response: requests.Response) -> None:
        if not response.ok:
            try:
                error_data = response.json()
                message = error_data.get("message", response.text)
            except ValueError:
                message = response.text
            raise AdoRequestError(
                f"Azure DevOps API Error: {message}",
                status=response.status_code,
            )

    def get_work_item(self, id: int) -> Dict[str, Any]:
        """Fetch a work item by ID."""
        # Using org-level URL for fetching by ID is safer if project is unknown, 
        # but config usually has project.
        # Let's use the configured base URL.
        url = f"{self.config.ado_org_url}/_apis/wit/workitems/{id}?api-version=7.1"
        response = self.session.get(url)
        self._handle_error(response)
        return response.json()

    def get_my_tasks(self) -> List[Dict[str, Any]]:
        """Fetch tasks assigned to the current user."""
        # WIQL query
        query = """
        SELECT [System.Id]
        FROM WorkItems
        WHERE [System.WorkItemType] = 'Task'
        AND [System.AssignedTo] = @Me
        """
        
        # WIQL endpoint is usually project-scoped or org-scoped (collection).
        # We'll try project-scoped if project is set, else org-scoped (might fail if cross-project query not allowed without specific permissions).
        # But @Me usually works.
        if self.config.ado_project:
             url = f"{self.config.ado_org_url}/{self.config.ado_project}/_apis/wit/wiql?api-version=7.1"
        else:
             # Fallback to org level (might need collection?)
             # Usually https://dev.azure.com/{org}/_apis/wit/wiql
             url = f"{self.config.ado_org_url}/_apis/wit/wiql?api-version=7.1"

        response = self.session.post(url, json={"query": query})
        self._handle_error(response)
        
        result = response.json()
        work_items = result.get("workItems", [])
        
        if not work_items:
            return []
            
        # Fetch details
        ids = [str(wi["id"]) for wi in work_items]
        # Batch get
        # https://dev.azure.com/{org}/_apis/wit/workitems?ids={ids}&api-version=7.1
        ids_str = ",".join(ids)
        url_batch = f"{self.config.ado_org_url}/_apis/wit/workitems?ids={ids_str}&api-version=7.1"
        
        response_batch = self.session.get(url_batch)
        self._handle_error(response_batch)
        return response_batch.json().get("value", [])

    def get_work_item_children(self, id: int) -> List[Dict[str, Any]]:
        """Fetch child work items."""
        url = f"{self.config.ado_org_url}/_apis/wit/workitems/{id}?$expand=relations&api-version=7.1"
        response = self.session.get(url)
        self._handle_error(response)
        
        data = response.json()
        relations = data.get("relations", [])
        
        child_ids = []
        for rel in relations:
            if rel.get("rel") == "System.LinkTypes.Hierarchy-Forward":
                # URL is like .../_apis/wit/workitems/123
                child_url = rel.get("url", "")
                if child_url:
                    parts = child_url.split("/")
                    try:
                        child_ids.append(parts[-1])
                    except IndexError:
                        pass
        
        if not child_ids:
            return []
            
        ids_str = ",".join(child_ids)
        url_batch = f"{self.config.ado_org_url}/_apis/wit/workitems?ids={ids_str}&api-version=7.1"
        
        response_batch = self.session.get(url_batch)
        self._handle_error(response_batch)
        return response_batch.json().get("value", [])

    def create_task(self, project: str, title: str, description: Optional[str] = None, parent_id: Optional[int] = None) -> Dict[str, Any]:
        """Create a new Task."""
        url = f"{self.config.ado_org_url}/{project}/_apis/wit/workitems/$Task?api-version=7.1"
        
        patch_doc = [
            {
                "op": "add",
                "path": "/fields/System.Title",
                "value": title
            }
        ]
        
        if description:
            patch_doc.append({
                "op": "add",
                "path": "/fields/System.Description",
                "value": description
            })
            
        if parent_id:
            # To add a parent link during creation, we add a relation
            patch_doc.append({
                "op": "add",
                "path": "/relations/-",
                "value": {
                    "rel": "System.LinkTypes.Hierarchy-Reverse",
                    "url": f"{self.config.ado_org_url}/_apis/wit/workitems/{parent_id}",
                    "attributes": {
                        "comment": "Parent task"
                    }
                }
            })
            
        response = self.session.post(
            url, 
            json=patch_doc, 
            headers={"Content-Type": "application/json-patch+json"}
        )
        self._handle_error(response)
        return response.json()
