import pytest
import subprocess # Add this line
from unittest.mock import patch, MagicMock
from appscriptz.core import (
    generate_schedule,
    run_applescript,
    Notes,
    Reminder,
    Calulate,
    Display,
    ShortCut
)

# Mock external dependencies
@pytest.fixture(autouse=True)
def mock_external_dependencies():
    with patch('appscriptz.core.BianXieAdapter') as MockBianXieAdapter, \
         patch('appscriptz.core.PromptManager') as MockPromptManager, \
         patch('appscriptz.core.PromptRepository') as MockPromptRepository:
        
        # Configure MockBianXieAdapter
        mock_llm_instance = MagicMock()
        mock_llm_instance.product.return_value = "Generated Schedule"
        MockBianXieAdapter.return_value = mock_llm_instance

        # Configure MockPromptManager
        mock_prompt_manager_instance = MagicMock()
        mock_prompt_manager_instance.get_prompt.return_value.format.return_value = "Formatted Prompt"
        MockPromptManager.return_value = mock_prompt_manager_instance

        yield

@patch('appscriptz.core.subprocess.run')
def test_run_applescript(mock_subprocess_run):
    mock_subprocess_run.return_value.stdout.decode.return_value = "script output\n"
    result = run_applescript("some applescript")
    mock_subprocess_run.assert_called_once_with(['osascript', '-e', 'some applescript'], capture_output=True, check=False)
    assert result == "script output"

def test_generate_schedule():
    result = generate_schedule("test text", "test habit")
    assert result == "Generated Schedule"

@patch('appscriptz.core.run_applescript')
def test_notes_write(mock_run_applescript):
    mock_run_applescript.return_value = "Note created"
    content = "My test note\n- [ ] item1"
    result = Notes.write(content)
    assert "tell application \"Notes\"" in mock_run_applescript.call_args[0][0]
    assert "My test note, item1" in mock_run_applescript.call_args[0][0]
    assert result == "Note created"

@patch('appscriptz.core.run_applescript')
def test_reminder_write_reminder(mock_run_applescript):
    mock_run_applescript.return_value = "Reminder created"

    # Test with minimal parameters
    result = Reminder.write_reminder(None, content="Buy groceries")
    assert "tell application \"Reminders\"" in mock_run_applescript.call_args[0][0]
    assert 'name:"Buy groceries"' in mock_run_applescript.call_args[0][0]
    assert result == "Reminder created"

    # Test with all parameters
    result = Reminder.write_reminder(
        None,
        content="Meeting with John",
        list_name="Work",
        due_date="2025年7月3日10:00",
        priority=1,
        notes="Discuss project status"
    )
    script_content = mock_run_applescript.call_args[0][0]
    assert 'name:"Meeting with John"' in script_content
    assert 'list "Work"' in script_content
    assert 'due date:(date "2025年7月3日10:00")' in script_content
    assert 'priority:1' in script_content
    assert 'body:"Discuss project status"' in script_content
    assert result == "Reminder created"

@patch('appscriptz.core.run_applescript')
def test_calulate_update(mock_run_applescript):
    mock_run_applescript.return_value = "Event updated"
    result = Calulate.update(None, start_date="2025年7月3日9:00", end_date="2025年7月3日10:00", event_name="Daily Standup")
    script_content = mock_run_applescript.call_args[0][0]
    assert 'tell application "Calendar"' in script_content
    assert 'set theStartDate to date "2025年7月3日9:00"' in script_content
    assert 'set theEndDate to date "2025年7月3日10:00"' in script_content
    assert 'set theSummary to "Daily Standup"' in script_content
    assert result == "Event updated"

@patch('appscriptz.core.run_applescript')
def test_calulate_delete(mock_run_applescript):
    mock_run_applescript.return_value = "Event deleted"
    result = Calulate.delete(None, event_name="Old Meeting")
    script_content = mock_run_applescript.call_args[0][0]
    assert 'tell application "Calendar"' in script_content
    assert 'set eventNameToRemove to "Old Meeting"' in script_content
    assert 'delete ev' in script_content
    assert result == "Event deleted"


@patch('appscriptz.core.subprocess.run')
@patch('sys.platform', new='darwin')
def test_display_multiple_selection_boxes_user_cancels(mock_subprocess_run):
    mock_subprocess_run.side_effect = subprocess.CalledProcessError(
        returncode=1, cmd=['osascript'], stderr="-128"
    )
    options = ["Option A", "Option B"]
    result = Display.multiple_selection_boxes(None, options=options)
    assert result is None

@patch('appscriptz.core.subprocess.run')
def test_display_get_multi_level_selection_simple(mock_subprocess_run):
    mock_subprocess_run.return_value.stdout.strip.return_value = "Action:Warehouse:Title:Description"
    warehouse_list = ["Warehouse A", "Warehouse B"]
    action_list = ["Action X", "Action Y"]
    result = Display.get_multi_level_selection_simple(None, warehouse_list, action_list)
    assert result == "Action:Warehouse:Title:Description"
    script_content = mock_subprocess_run.call_args[0][0][2]
    assert 'choose from list {"Warehouse A", "Warehouse B"}' in script_content
    assert 'choose from list {"Action X", "Action Y"}' in script_content

@patch('appscriptz.core.subprocess.run')
def test_display_display_dialog(mock_subprocess_run):
    mock_subprocess_run.return_value.stdout = "button returned:OK\n"
    result = Display.display_dialog(None, "Test Title", "Test Text")
    assert result == "OK"
    script_content = mock_subprocess_run.call_args[0][0][2]
    assert 'display dialog "Test Text" with title "Test Title"' in script_content

@patch('appscriptz.core.run_applescript')
def test_shortcut_run_shortcut(mock_run_applescript):
    mock_run_applescript.return_value = "Shortcut executed"
    result = ShortCut.run_shortcut(None, "My Shortcut", "param_value")
    script_content = mock_run_applescript.call_args[0][0]
    assert 'run shortcut "My Shortcut" with input "param_value"' in script_content
    assert result == "Shortcut executed"

@patch('appscriptz.core.run_applescript')
def test_shortcut_applescript(mock_run_applescript):
    mock_run_applescript.return_value = "AppleScript executed"
    result = ShortCut.applescript()
    script_content = mock_run_applescript.call_args[0][0]
    assert 'tell application "System Events"' in script_content
    assert result == "AppleScript executed"