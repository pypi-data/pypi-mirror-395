"""Service layer for ado-task-manager."""

from __future__ import annotations

from typing import List, Optional

from .client import AdoClient
from .config import load_config
from .models import Task
from .errors import MCPUserError


def _map_to_task(data: dict) -> Task:
    """Map raw ADO work item to Task model."""
    fields = data.get("fields", {})

    # We no longer strictly enforce "Task" type here, allowing other work item types.
    # But we still map to our 'Task' model which is generic enough.

    # Find parent ID from relations if available
    parent_id = None
    relations = data.get("relations", [])
    for rel in relations:
        if rel.get("rel") == "System.LinkTypes.Hierarchy-Reverse":
            # Parent
            url = rel.get("url", "")
            try:
                parent_id = int(url.split("/")[-1])
            except (ValueError, IndexError):
                pass
            break

    return Task(
        id=data["id"],
        title=fields.get("System.Title", ""),
        state=fields.get("System.State", ""),
        assigned_to=(
            fields.get("System.AssignedTo", {}).get("displayName")
            if isinstance(fields.get("System.AssignedTo"), dict)
            else fields.get("System.AssignedTo")
        ),
        description=fields.get("System.Description"),
        parent_id=parent_id,
        url=data.get("url", ""),
    )


def get_task(id: int) -> Task:
    """Fetch a task by ID."""
    config = load_config()
    with AdoClient(config) as client:
        data = client.get_work_item(id)
        # Relaxed: No longer checking if it is a "Task" type.
        return _map_to_task(data)


def get_my_tasks(include_closed: bool = False) -> List[Task]:
    """
    Fetch tasks assigned to me.

    Args:
        include_closed: If True, includes Closed, Removed, Done, Resolved.
                        Otherwise defaults to New, Active, Committed, etc.
    """
    config = load_config()
    with AdoClient(config) as client:
        items = client.get_my_tasks(include_closed=include_closed)
        return [_map_to_task(item) for item in items]


def get_task_children(id: int) -> List[Task]:
    """Fetch child tasks."""
    config = load_config()
    with AdoClient(config) as client:
        # Verify parent exists and is a task?
        # User requirement: "if i give it a task and ask to pull related task,
        # should pull all the children"
        # Doesn't strictly say parent must be a Task, but we are a Task Manager.
        # Let's allow fetching children of any work item, but filter children to be
        # Tasks?
        # "should pull all the children" - implies all.
        # But our model is `Task`.
        # Let's filter for Tasks.

        items = client.get_work_item_children(id)
        # Relaxed: Return all children regardless of type
        return [_map_to_task(item) for item in items]


def create_task(
    project: str,
    title: str,
    parent_id: int,
    description: Optional[str] = None,
) -> Task:
    """Create a new task."""
    config = load_config()

    # If project not passed, try config
    if not project and config.ado_project:
        project = config.ado_project

    if not project:
        raise MCPUserError("Project is required to create a task.")

    with AdoClient(config) as client:
        # Verify parent exists? API will fail if not.
        data = client.create_task(project, title, description, parent_id)
        return _map_to_task(data)
