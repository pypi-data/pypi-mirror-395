"""CLI for ado-task-manager."""

from __future__ import annotations

import json
from typing import Optional
import typer

from .service import (
    get_task,
    get_my_tasks,
    get_task_children,
    create_task,
    update_task,
    add_comment,
)

app = typer.Typer(no_args_is_help=True)


@app.command()
def fetch(id: int):
    """Fetch a task by ID."""
    try:
        task = get_task(id)
        print(json.dumps(task.model_dump(by_alias=True), indent=2))
    except Exception as e:
        print(f"Error: {e}")
        raise typer.Exit(code=1)


@app.command()
def server():
    """Run the MCP server."""
    from .server import main as server_main

    server_main()


@app.command()
def mine(
    closed: bool = typer.Option(False, "--closed", help="Include closed/inactive tasks")
):
    """Fetch tasks assigned to me."""
    try:
        tasks = get_my_tasks(include_closed=closed)
        print(json.dumps([t.model_dump(by_alias=True) for t in tasks], indent=2))
    except Exception as e:
        print(f"Error: {e}")
        raise typer.Exit(code=1)


@app.command()
def children(id: int):
    """Fetch child tasks."""
    try:
        tasks = get_task_children(id)
        print(json.dumps([t.model_dump(by_alias=True) for t in tasks], indent=2))
    except Exception as e:
        print(f"Error: {e}")
        raise typer.Exit(code=1)


@app.command()
def create(
    title: str,
    parent_id: int,
    project: Optional[str] = typer.Option(None, help="Project name"),
    description: Optional[str] = typer.Option(None, help="Task description"),
    assign_to_me: bool = typer.Option(True, help="Assign task to me (default: True)"),
    original_estimate: Optional[float] = typer.Option(
        None, help="Original estimate in hours"
    ),
    remaining_work: Optional[float] = typer.Option(
        None, help="Remaining work in hours"
    ),
    completed_work: Optional[float] = typer.Option(
        None, help="Completed work in hours"
    ),
):
    """Create a new task."""
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
        print(json.dumps(task.model_dump(by_alias=True), indent=2))
    except Exception as e:
        print(f"Error: {e}")
        raise typer.Exit(code=1)


@app.command()
def update(
    id: int,
    title: Optional[str] = typer.Option(None, help="New title"),
    description: Optional[str] = typer.Option(None, help="New description"),
    state: Optional[str] = typer.Option(None, help="New state"),
    assigned_to: Optional[str] = typer.Option(None, help="Assign to user"),
    original_estimate: Optional[float] = typer.Option(None, help="Original estimate"),
    remaining_work: Optional[float] = typer.Option(None, help="Remaining work"),
    completed_work: Optional[float] = typer.Option(None, help="Completed work"),
):
    """Update an existing task."""
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
        print(json.dumps(task.model_dump(by_alias=True), indent=2))
    except Exception as e:
        print(f"Error: {e}")
        raise typer.Exit(code=1)


@app.command()
def comment(
    id: int,
    text: str = typer.Option(..., help="Comment text"),
):
    """Add a comment to a task."""
    try:
        result = add_comment(id, text)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
