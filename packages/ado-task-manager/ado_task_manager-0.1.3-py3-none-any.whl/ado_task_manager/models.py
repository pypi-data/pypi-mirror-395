"""Core data models for ado-task-manager."""

from __future__ import annotations

from typing import Optional, Any
from pydantic import BaseModel, ConfigDict, Field


class MCPConfig(BaseModel):
    """Runtime configuration sourced from environment variables."""
    
    model_config = ConfigDict(populate_by_name=True)
    
    ado_org_url: str
    ado_pat: str
    ado_project: Optional[str] = None


class WorkItem(BaseModel):
    """Azure DevOps Work Item."""
    
    model_config = ConfigDict(populate_by_name=True)
    
    id: int
    rev: int
    fields: dict[str, Any]
    url: str


class Task(BaseModel):
    """Task work item model."""
    
    model_config = ConfigDict(populate_by_name=True)
    
    id: int
    title: str
    state: str
    assigned_to: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[int] = None
    url: str
