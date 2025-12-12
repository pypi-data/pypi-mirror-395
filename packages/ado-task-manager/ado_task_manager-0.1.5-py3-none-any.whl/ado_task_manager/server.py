"""MCP server entrypoint for ado-task-manager."""

from __future__ import annotations

from typing import Optional, List

from mcp.server.fastmcp import FastMCP

from .errors import MCPUserError, AdoRequestError, MissingConfigurationError
from .service import (
    get_task,
    get_my_tasks,
    get_task_children,
    create_task,
    update_task,
    add_comment,
)

mcp = FastMCP("AdoTaskManager")


@mcp.tool()
def get_task_tool(id: int) -> dict:
    """
    Fetch a Task work item by its ID.

    Args:
        id: The ID of the task to fetch.
    """
    try:
        task = get_task(id)
        return task.model_dump(by_alias=True)
    except (MCPUserError, MissingConfigurationError) as exc:
        raise ValueError(str(exc)) from exc
    except AdoRequestError as exc:
        raise RuntimeError(f"Azure DevOps error ({exc.status}): {exc}") from exc


@mcp.tool()
def get_my_tasks_tool(include_closed: bool = False) -> List[dict]:
    """
    Fetch all Task work items assigned to the current user.

    Args:
        include_closed: If True, includes Closed, Removed, Done, Resolved.
                        Otherwise defaults to New, Active, Committed, etc.
    """
    try:
        tasks = get_my_tasks(include_closed=include_closed)
        return [t.model_dump(by_alias=True) for t in tasks]
    except (MCPUserError, MissingConfigurationError) as exc:
        raise ValueError(str(exc)) from exc
    except AdoRequestError as exc:
        raise RuntimeError(f"Azure DevOps error ({exc.status}): {exc}") from exc


@mcp.tool()
def get_task_children_tool(id: int) -> List[dict]:
    """
    Fetch all child Task work items for a given parent work item ID.

    Args:
        id: The ID of the parent work item.
    """
    try:
        tasks = get_task_children(id)
        return [t.model_dump(by_alias=True) for t in tasks]
    except (MCPUserError, MissingConfigurationError) as exc:
        raise ValueError(str(exc)) from exc
    except AdoRequestError as exc:
        raise RuntimeError(f"Azure DevOps error ({exc.status}): {exc}") from exc


@mcp.tool()
def create_task_tool(
    title: str,
    parent_id: int,
    project: Optional[str] = None,
    description: Optional[str] = None,
    assign_to_me: bool = True,
    original_estimate: Optional[float] = None,
    remaining_work: Optional[float] = None,
    completed_work: Optional[float] = None,
) -> dict:
    """
    Create a new Task work item and link it to a parent.

    Args:
        title: The title of the new task.
        parent_id: The ID of the parent work item. Mandatory.
        project: The Azure DevOps project name. If not provided, uses default.
        description: Optional description for the task.
        assign_to_me: If True, assigns the task to the creator (default: True).
        original_estimate: Initial estimate in hours.
        remaining_work: Remaining work in hours.
        completed_work: Completed work in hours.
    """
    try:
        task = create_task(
            project=project or "",
            title=title,
            parent_id=parent_id,
            description=description,
            assign_to_me=assign_to_me,
            original_estimate=original_estimate,
            remaining_work=remaining_work,
            completed_work=completed_work,
        )
        return task.model_dump(by_alias=True)
    except (MCPUserError, MissingConfigurationError) as exc:
        raise ValueError(str(exc)) from exc
    except AdoRequestError as exc:
        raise RuntimeError(f"Azure DevOps error ({exc.status}): {exc}") from exc


@mcp.tool()
def update_task_tool(
    id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    state: Optional[str] = None,
    assigned_to: Optional[str] = None,
    original_estimate: Optional[float] = None,
    remaining_work: Optional[float] = None,
    completed_work: Optional[float] = None,
) -> dict:
    """
    Update an existing Task work item.

    Args:
        id: The ID of the task to update.
        title: New title.
        description: New description.
        state: New state (e.g., 'Active', 'Closed').
        assigned_to: Display name of the user to assign to.
        original_estimate: Update original estimate.
        remaining_work: Update remaining work.
        completed_work: Update completed work.
    """
    try:
        task = update_task(
            id=id,
            title=title,
            description=description,
            state=state,
            assigned_to=assigned_to,
            original_estimate=original_estimate,
            remaining_work=remaining_work,
            completed_work=completed_work,
        )
        return task.model_dump(by_alias=True)
    except (MCPUserError, MissingConfigurationError) as exc:
        raise ValueError(str(exc)) from exc
    except AdoRequestError as exc:
        raise RuntimeError(f"Azure DevOps error ({exc.status}): {exc}") from exc


@mcp.tool()
def add_comment_tool(id: int, text: str) -> dict:
    """
    Add a comment to a work item.

    Args:
        id: The ID of the work item.
        text: The comment text.
    """
    try:
        return add_comment(id, text)
    except (MCPUserError, MissingConfigurationError) as exc:
        raise ValueError(str(exc)) from exc
    except AdoRequestError as exc:
        raise RuntimeError(f"Azure DevOps error ({exc.status}): {exc}") from exc


def main() -> None:
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
