"""MCP server entrypoint for ado-task-manager."""

from __future__ import annotations

from typing import Optional, List

from mcp.server.fastmcp import FastMCP

from .errors import MCPUserError, AdoRequestError, MissingConfigurationError
from .service import get_task, get_my_tasks, get_task_children, create_task

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
def get_my_tasks_tool() -> List[dict]:
    """
    Fetch all Task work items assigned to the current user.
    """
    try:
        tasks = get_my_tasks()
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
) -> dict:
    """
    Create a new Task work item and link it to a parent.
    
    Args:
        title: The title of the new task.
        parent_id: The ID of the parent work item. Mandatory.
        project: The Azure DevOps project name. If not provided, uses configured default.
        description: Optional description for the task.
    """
    try:
        task = create_task(project=project or "", title=title, parent_id=parent_id, description=description)
        return task.model_dump(by_alias=True)
    except (MCPUserError, MissingConfigurationError) as exc:
        raise ValueError(str(exc)) from exc
    except AdoRequestError as exc:
        raise RuntimeError(f"Azure DevOps error ({exc.status}): {exc}") from exc


def main() -> None:
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
