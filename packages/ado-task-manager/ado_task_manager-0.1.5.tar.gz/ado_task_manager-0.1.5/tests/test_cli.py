import pytest
from typer.testing import CliRunner
from unittest.mock import patch
from ado_task_manager.cli import app
from ado_task_manager.models import Task

runner = CliRunner()

@pytest.fixture
def mock_service():
    with patch("ado_task_manager.cli.create_task") as mock_create, \
         patch("ado_task_manager.cli.update_task") as mock_update, \
         patch("ado_task_manager.cli.add_comment") as mock_comment, \
         patch("ado_task_manager.cli.get_task") as mock_get, \
         patch("ado_task_manager.cli.get_my_tasks") as mock_mine, \
         patch("ado_task_manager.cli.get_task_children") as mock_children:
        yield {
            "create": mock_create,
            "update": mock_update,
            "comment": mock_comment,
            "get": mock_get,
            "mine": mock_mine,
            "children": mock_children
        }

def test_create_command(mock_service):
    mock_service["create"].return_value = Task(id=1, title="t", url="u", state="New")
    result = runner.invoke(app, ["create", "t", "1"])
    assert result.exit_code == 0
    assert "id" in result.stdout

def test_update_command(mock_service):
    mock_service["update"].return_value = Task(id=1, title="t", url="u", state="New")
    result = runner.invoke(app, ["update", "1", "--title", "new"])
    assert result.exit_code == 0
    assert "id" in result.stdout

def test_comment_command(mock_service):
    mock_service["comment"].return_value = {"id": 1, "text": "c"}
    result = runner.invoke(app, ["comment", "1", "--text", "c"])
    assert result.exit_code == 0
    assert "text" in result.stdout

def test_fetch_command(mock_service):
    mock_service["get"].return_value = Task(id=1, title="t", url="u", state="New")
    result = runner.invoke(app, ["fetch", "1"])
    assert result.exit_code == 0
    assert "id" in result.stdout

def test_mine_command(mock_service):
    mock_service["mine"].return_value = [Task(id=1, title="t", url="u", state="New")]
    result = runner.invoke(app, ["mine"])
    assert result.exit_code == 0
    assert "id" in result.stdout

def test_children_command(mock_service):
    mock_service["children"].return_value = [Task(id=1, title="t", url="u", state="New")]
    result = runner.invoke(app, ["children", "1"])
    assert result.exit_code == 0
    assert "id" in result.stdout

def test_cli_error_handling(mock_service):
    mock_service["create"].side_effect = Exception("error")
    result = runner.invoke(app, ["create", "t", "1"])
    assert result.exit_code == 1
    assert "Error: error" in result.stdout

    mock_service["update"].side_effect = Exception("error")
    result = runner.invoke(app, ["update", "1"])
    assert result.exit_code == 1
    assert "Error: error" in result.stdout

    mock_service["comment"].side_effect = Exception("error")
    result = runner.invoke(app, ["comment", "1", "--text", "c"])
    assert result.exit_code == 1
    assert "Error: error" in result.stdout
