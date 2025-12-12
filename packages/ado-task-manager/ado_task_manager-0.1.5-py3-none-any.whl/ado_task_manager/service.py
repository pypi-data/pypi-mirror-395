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
        original_estimate=fields.get("Microsoft.VSTS.Scheduling.OriginalEstimate"),
        remaining_work=fields.get("Microsoft.VSTS.Scheduling.RemainingWork"),
        completed_work=fields.get("Microsoft.VSTS.Scheduling.CompletedWork"),
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
    assign_to_me: bool = True,
    original_estimate: Optional[float] = None,
    remaining_work: Optional[float] = None,
    completed_work: Optional[float] = None,
) -> Task:
    """Create a new task."""
    config = load_config()

    # If project not passed, try config
    if not project and config.ado_project:
        project = config.ado_project

    if not project:
        raise MCPUserError("Project is required to create a task.")

    with AdoClient(config) as client:
        assigned_to = None
        if assign_to_me:
            user = client.get_current_user()
            # Usually we use the display name or email.
            # 'providerDisplayName' or 'customDisplayName' or 'descriptor'
            # Best is often the email or display name.
            # Let's try providerDisplayName first, then customDisplayName.
            assigned_to = user.get("providerDisplayName") or user.get(
                "customDisplayName"
            )

        data = client.create_task(
            project,
            title,
            description,
            parent_id,
            assigned_to=assigned_to,
            original_estimate=original_estimate,
            remaining_work=remaining_work,
            completed_work=completed_work,
        )
        return _map_to_task(data)


def update_task(
    id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    state: Optional[str] = None,
    assigned_to: Optional[str] = None,
    original_estimate: Optional[float] = None,
    remaining_work: Optional[float] = None,
    completed_work: Optional[float] = None,
) -> Task:
    """Update an existing task."""
    config = load_config()
    ops = []

    if title:
        ops.append({"op": "add", "path": "/fields/System.Title", "value": title})
    if description:
        ops.append(
            {
                "op": "add",
                "path": "/fields/System.Description",
                "value": description,
            }
        )
    if state:
        ops.append({"op": "add", "path": "/fields/System.State", "value": state})
    if assigned_to:
        ops.append(
            {
                "op": "add",
                "path": "/fields/System.AssignedTo",
                "value": assigned_to,
            }
        )
    if original_estimate is not None:
        ops.append(
            {
                "op": "add",
                "path": "/fields/Microsoft.VSTS.Scheduling.OriginalEstimate",
                "value": original_estimate,
            }
        )
    if remaining_work is not None:
        ops.append(
            {
                "op": "add",
                "path": "/fields/Microsoft.VSTS.Scheduling.RemainingWork",
                "value": remaining_work,
            }
        )
    if completed_work is not None:
        ops.append(
            {
                "op": "add",
                "path": "/fields/Microsoft.VSTS.Scheduling.CompletedWork",
                "value": completed_work,
            }
        )

    if not ops:
        return get_task(id)

    with AdoClient(config) as client:
        data = client.update_work_item(id, ops)
        return _map_to_task(data)


def add_comment(id: int, text: str) -> dict:
    """Add a comment to a task."""
    config = load_config()
    with AdoClient(config) as client:
        return client.add_comment(id, text)
