import pytest
from unittest.mock import MagicMock, patch
from ado_task_manager.service import create_task, update_task, add_comment
from ado_task_manager.models import Task

@pytest.fixture
def mock_client():
    with patch("ado_task_manager.service.AdoClient") as MockClient:
        client_instance = MockClient.return_value
        client_instance.__enter__.return_value = client_instance
        yield client_instance

@pytest.fixture
def mock_config():
    with patch("ado_task_manager.service.load_config") as mock_load:
        mock_load.return_value = MagicMock(
            ado_org_url="https://dev.azure.com/org",
            ado_pat="pat",
            ado_project="project",
        )
        yield mock_load

def test_create_task_with_assignment(mock_config, mock_client):
    mock_client.get_current_user.return_value = {"providerDisplayName": "Test User"}
    mock_client.create_task.return_value = {
        "id": 1,
        "fields": {
            "System.Title": "Task 1",
            "System.AssignedTo": {"displayName": "Test User"},
        },
        "url": "http://url",
    }

    task = create_task(
        project="p",
        title="Task 1",
        parent_id=1,
        assign_to_me=True,
        original_estimate=5.0
    )

    mock_client.get_current_user.assert_called_once()
    mock_client.create_task.assert_called_with(
        "p", "Task 1", None, 1,
        assigned_to="Test User",
        original_estimate=5.0,
        remaining_work=None,
        completed_work=None
    )
    assert task.assigned_to == "Test User"
    assert task.original_estimate is None # Response didn't include it, but call did

def test_update_task(mock_config, mock_client):
    mock_client.update_work_item.return_value = {
        "id": 1,
        "fields": {
            "System.Title": "Updated Task",
            "Microsoft.VSTS.Scheduling.OriginalEstimate": 10.0
        },
        "url": "http://url",
    }

    task = update_task(
        id=1,
        title="Updated Task",
        original_estimate=10.0
    )

    mock_client.update_work_item.assert_called_once()
    ops = mock_client.update_work_item.call_args[0][1]
    assert len(ops) == 2
    assert ops[0]["path"] == "/fields/System.Title"
    assert ops[1]["path"] == "/fields/Microsoft.VSTS.Scheduling.OriginalEstimate"
    assert task.title == "Updated Task"
    assert task.original_estimate == 10.0

def test_add_comment(mock_config, mock_client):
    mock_client.add_comment.return_value = {"id": 1, "text": "Comment"}
    
    result = add_comment(1, "Comment")
    
    mock_client.add_comment.assert_called_with(1, "Comment")
    assert result["text"] == "Comment"
