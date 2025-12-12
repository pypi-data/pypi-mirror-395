import pytest
from unittest.mock import MagicMock, patch
from ado_task_manager.client import AdoClient
from ado_task_manager.models import MCPConfig

@pytest.fixture
def config():
    return MCPConfig(
        ado_org_url="https://dev.azure.com/org",
        ado_pat="pat",
        ado_project="project"
    )

@pytest.fixture
def client(config):
    return AdoClient(config)

def test_client_context_manager(config):
    with patch("requests.Session") as MockSession:
        with AdoClient(config) as client:
            assert client.session is not None
        
        MockSession.return_value.close.assert_called_once()

def test_client_error_handling(client):
    with patch.object(client.session, "get") as mock_get:
        mock_get.return_value.ok = False
        mock_get.return_value.status_code = 404
        mock_get.return_value.text = "Not Found"
        mock_get.return_value.json.side_effect = ValueError
        
        from ado_task_manager.errors import AdoRequestError
        with pytest.raises(AdoRequestError) as exc:
            client.get_work_item(1)
        assert "Not Found" in str(exc.value)

    with patch.object(client.session, "post") as mock_post:
        mock_post.return_value.ok = False
        mock_post.return_value.status_code = 500
        mock_post.return_value.json.return_value = {"message": "Internal Error"}
        
        from ado_task_manager.errors import AdoRequestError
        with pytest.raises(AdoRequestError) as exc:
            client.create_task("p", "t")
        assert "Internal Error" in str(exc.value)

    with patch.object(client.session, "patch") as mock_patch:
        mock_patch.return_value.ok = False
        mock_patch.return_value.status_code = 400
        
        from ado_task_manager.errors import AdoRequestError
        with pytest.raises(AdoRequestError):
            client.update_work_item(1, [])

def test_get_current_user(client):
    with patch.object(client.session, "get") as mock_get:
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = {
            "authenticatedUser": {"providerDisplayName": "Test User"}
        }
        
        user = client.get_current_user()
        assert user["providerDisplayName"] == "Test User"
        mock_get.assert_called_once()

def test_create_task(client):
    with patch.object(client.session, "post") as mock_post:
        mock_post.return_value.ok = True
        mock_post.return_value.json.return_value = {"id": 1}
        
        client.create_task(
            project="p",
            title="t",
            assigned_to="u",
            original_estimate=1.0
        )
        
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        assert call_args[1]["json"][0]["path"] == "/fields/System.Title"
        # Check if assigned_to and estimate were added
        paths = [op["path"] for op in call_args[1]["json"]]
        assert "/fields/System.AssignedTo" in paths
        assert "/fields/Microsoft.VSTS.Scheduling.OriginalEstimate" in paths

def test_update_work_item(client):
    with patch.object(client.session, "patch") as mock_patch:
        mock_patch.return_value.ok = True
        mock_patch.return_value.json.return_value = {"id": 1}
        
        client.update_work_item(1, [{"op": "add", "path": "/f", "value": "v"}])
        
        mock_patch.assert_called_once()

def test_add_comment(client):
    with patch.object(client.session, "post") as mock_post:
        mock_post.return_value.ok = True
        mock_post.return_value.json.return_value = {"id": 1}
        
        client.add_comment(1, "comment")
        
        mock_post.assert_called_once()
