"""Tests for ado-task-manager."""

import pytest
from unittest.mock import Mock, patch
from ado_task_manager.service import get_task, get_my_tasks, get_task_children, create_task
from ado_task_manager.models import Task, MCPConfig
from ado_task_manager.errors import MCPUserError

@pytest.fixture
def mock_config():
    with patch("ado_task_manager.service.load_config") as mock:
        mock.return_value = MCPConfig(
            ado_org_url="https://dev.azure.com/test",
            ado_pat="test-pat",
            ado_project="test-project"
        )
        yield mock

@pytest.fixture
def mock_client():
    with patch("ado_task_manager.service.AdoClient") as mock:
        client_instance = Mock()
        mock.return_value.__enter__.return_value = client_instance
        yield client_instance

def test_get_task(mock_config, mock_client):
    mock_client.get_work_item.return_value = {
        "id": 1,
        "fields": {
            "System.WorkItemType": "Task",
            "System.Title": "Test Task",
            "System.State": "New",
            "System.AssignedTo": {"displayName": "User"},
            "System.Description": "Desc"
        },
        "url": "http://url"
    }
    
    task = get_task(1)
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.assigned_to == "User"

def test_get_task_not_task_type(mock_config, mock_client):
    mock_client.get_work_item.return_value = {
        "id": 1,
        "fields": {
            "System.WorkItemType": "Bug",
        }
    }
    
    with pytest.raises(MCPUserError):
        get_task(1)

def test_get_my_tasks(mock_config, mock_client):
    mock_client.get_my_tasks.return_value = [
        {
            "id": 1,
            "fields": {
                "System.WorkItemType": "Task",
                "System.Title": "Task 1",
                "System.State": "New"
            },
            "url": "http://url"
        }
    ]
    
    tasks = get_my_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == "Task 1"

def test_get_task_children(mock_config, mock_client):
    mock_client.get_work_item_children.return_value = [
        {
            "id": 2,
            "fields": {
                "System.WorkItemType": "Task",
                "System.Title": "Child Task"
            },
            "url": "http://url"
        },
        {
            "id": 3,
            "fields": {
                "System.WorkItemType": "Bug", # Should be filtered out
                "System.Title": "Child Bug"
            },
            "url": "http://url"
        }
    ]
    
    tasks = get_task_children(1)
    assert len(tasks) == 1
    assert tasks[0].id == 2

def test_create_task(mock_config, mock_client):
    mock_client.create_task.return_value = {
        "id": 4,
        "fields": {
            "System.WorkItemType": "Task",
            "System.Title": "New Task",
            "System.State": "New"
        },
        "url": "http://url",
        "relations": [
            {"rel": "System.LinkTypes.Hierarchy-Reverse", "url": "http://url/1"}
        ]
    }
    
    task = create_task(project="p", title="New Task", parent_id=1)
    assert task.id == 4
    assert task.parent_id == 1
