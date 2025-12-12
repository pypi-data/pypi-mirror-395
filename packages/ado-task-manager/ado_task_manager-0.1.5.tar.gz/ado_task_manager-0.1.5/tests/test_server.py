import pytest
from unittest.mock import patch
from ado_task_manager.server import (
    create_task_tool,
    update_task_tool,
    add_comment_tool,
    get_task_tool,
    get_my_tasks_tool,
    get_task_children_tool
)
from ado_task_manager.models import Task

@pytest.fixture
def mock_service():
    with patch("ado_task_manager.server.create_task") as mock_create, \
         patch("ado_task_manager.server.update_task") as mock_update, \
         patch("ado_task_manager.server.add_comment") as mock_comment, \
         patch("ado_task_manager.server.get_task") as mock_get, \
         patch("ado_task_manager.server.get_my_tasks") as mock_mine, \
         patch("ado_task_manager.server.get_task_children") as mock_children:
        yield {
            "create": mock_create,
            "update": mock_update,
            "comment": mock_comment,
            "get": mock_get,
            "mine": mock_mine,
            "children": mock_children
        }

def test_create_task_tool(mock_service):
    mock_service["create"].return_value = Task(id=1, title="t", url="u", state="New")
    
    result = create_task_tool("t", 1)
    
    assert result["id"] == 1
    mock_service["create"].assert_called_once()

def test_update_task_tool(mock_service):
    mock_service["update"].return_value = Task(id=1, title="t", url="u", state="New")
    
    result = update_task_tool(1, title="new")
    
    assert result["id"] == 1
    mock_service["update"].assert_called_once()

def test_add_comment_tool(mock_service):
    mock_service["comment"].return_value = {"id": 1}
    
    result = add_comment_tool(1, "c")
    
    assert result["id"] == 1
    mock_service["comment"].assert_called_once()

def test_get_task_tool(mock_service):
    mock_service["get"].return_value = Task(id=1, title="t", url="u", state="New")
    result = get_task_tool(1)
    assert result["id"] == 1

def test_get_my_tasks_tool(mock_service):
    mock_service["mine"].return_value = [Task(id=1, title="t", url="u", state="New")]
    result = get_my_tasks_tool()
    assert len(result) == 1

def test_get_task_children_tool(mock_service):
    mock_service["children"].return_value = [Task(id=1, title="t", url="u", state="New")]
    result = get_task_children_tool(1)
    assert len(result) == 1

def test_server_error_handling(mock_service):
    from ado_task_manager.errors import MCPUserError, AdoRequestError
    
    mock_service["create"].side_effect = MCPUserError("error")
    with pytest.raises(ValueError):
        create_task_tool("t", 1)
        
    mock_service["create"].side_effect = AdoRequestError("error", 500)
    with pytest.raises(RuntimeError):
        create_task_tool("t", 1)

    mock_service["update"].side_effect = MCPUserError("error")
    with pytest.raises(ValueError):
        update_task_tool(1, title="t")

    mock_service["update"].side_effect = AdoRequestError("error", 500)
    with pytest.raises(RuntimeError):
        update_task_tool(1, title="t")

    mock_service["comment"].side_effect = MCPUserError("error")
    with pytest.raises(ValueError):
        add_comment_tool(1, "c")

    mock_service["comment"].side_effect = AdoRequestError("error", 500)
    with pytest.raises(RuntimeError):
        add_comment_tool(1, "c")

    mock_service["get"].side_effect = MCPUserError("error")
    with pytest.raises(ValueError):
        get_task_tool(1)

    mock_service["get"].side_effect = AdoRequestError("error", 500)
    with pytest.raises(RuntimeError):
        get_task_tool(1)

    mock_service["mine"].side_effect = MCPUserError("error")
    with pytest.raises(ValueError):
        get_my_tasks_tool()

    mock_service["mine"].side_effect = AdoRequestError("error", 500)
    with pytest.raises(RuntimeError):
        get_my_tasks_tool()

    mock_service["children"].side_effect = MCPUserError("error")
    with pytest.raises(ValueError):
        get_task_children_tool(1)

    mock_service["children"].side_effect = AdoRequestError("error", 500)
    with pytest.raises(RuntimeError):
        get_task_children_tool(1)
