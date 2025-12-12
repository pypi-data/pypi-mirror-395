"""CLI for ado-task-manager."""

from __future__ import annotations

import json
from typing import Optional
import typer

from .service import get_task, get_my_tasks, get_task_children, create_task
from .errors import MCPUserError, AdoRequestError, MissingConfigurationError

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
def mine():
    """Fetch tasks assigned to me."""
    try:
        tasks = get_my_tasks()
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
):
    """Create a new task."""
    try:
        task = create_task(project=project or "", title=title, parent_id=parent_id, description=description)
        print(json.dumps(task.model_dump(by_alias=True), indent=2))
    except Exception as e:
        print(f"Error: {e}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
