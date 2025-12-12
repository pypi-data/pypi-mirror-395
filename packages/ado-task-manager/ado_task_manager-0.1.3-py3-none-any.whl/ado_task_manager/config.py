"""Configuration helpers for ado-task-manager MCP."""

from __future__ import annotations

import os
from typing import Optional

from dotenv import load_dotenv

from .errors import MissingConfigurationError
from .models import MCPConfig


def load_config() -> MCPConfig:
    """Load configuration from environment variables."""
    
    load_dotenv()
    
    ado_org_url = os.getenv("AZDO_ORG_URL")
    ado_pat = os.getenv("AZDO_PAT")
    
    if not ado_org_url:
        raise MissingConfigurationError("AZDO_ORG_URL is required")
    
    if not ado_pat:
        raise MissingConfigurationError("AZDO_PAT is required")
    
    return MCPConfig(
        ado_org_url=ado_org_url.rstrip("/"),
        ado_pat=ado_pat,
        ado_project=os.getenv("AZDO_PROJECT"),
    )
