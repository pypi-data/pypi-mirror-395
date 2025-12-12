# Azure DevOps Task Manager MCP

An MCP server to manage Task work items in Azure DevOps.

## Features

- **Get Task**: Fetch details of a specific task by ID.
- **Get My Tasks**: List tasks assigned to the current user.
- **Get Child Tasks**: List child tasks for a given parent task.
- **Create Task**: Create a new task and link it to a parent.

## Configuration

Set the following environment variables in `.env`:

```bash
AZDO_ORG_URL=https://dev.azure.com/your-org
AZDO_PAT=your-pat-token
```

## Installation

```bash
pip install -e .
```

## Usage

### MCP Server

```bash
mcp dev src/ado_task_manager/server.py
```
