# standard
import subprocess
from unittest.mock import patch

# third party
# custom
from sunwaee_gen.tools.execute_command import execute_command


class TestExecuteCommand:
    def test_execute_command_success(self):
        result = execute_command._execute("echo hello")
        assert "STDOUT:" in result
        assert "hello" in result

    def test_execute_command_no_output(self):
        result = execute_command._execute("true")
        assert result == "Command executed successfully (no output)"

    def test_execute_command_with_stderr(self):
        result = execute_command._execute("ls /nonexistent")
        assert "STDERR:" in result
        assert "RETURN CODE:" in result

    def test_execute_command_timeout(self):
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired("sleep", 60)
            result = execute_command._execute("sleep 100")
            assert "Command timed out after 60 seconds" in result

    def test_execute_command_not_found(self):
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = FileNotFoundError()
            result = execute_command._execute("nonexistent_command")
            assert "Command not found: nonexistent_command" in result

    def test_execute_command_generic_exception(self):
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = Exception("Generic error")
            result = execute_command._execute("some_command")
            assert "Error executing command: Generic error" in result

    def test_execute_command_tool_definition(self):
        assert hasattr(execute_command, "function")
        assert execute_command.function.name == "execute_command"
        assert (
            "Execute a command in the terminal" in execute_command.function.description
        )
        assert "command" in execute_command.function.parameters.properties
