import pytest
import os
from unittest.mock import patch
from ado_task_manager.config import load_config
from ado_task_manager.errors import MissingConfigurationError

def test_load_config_success():
    with patch.dict(os.environ, {
        "AZDO_ORG_URL": "https://dev.azure.com/org",
        "AZDO_PAT": "pat",
        "AZDO_PROJECT": "project"
    }):
        config = load_config()
        assert config.ado_org_url == "https://dev.azure.com/org"
        assert config.ado_pat == "pat"
        assert config.ado_project == "project"

def test_load_config_missing():
    with patch("ado_task_manager.config.load_dotenv"), \
         patch.dict(os.environ, {}, clear=True):
        with pytest.raises(MissingConfigurationError):
            load_config()
