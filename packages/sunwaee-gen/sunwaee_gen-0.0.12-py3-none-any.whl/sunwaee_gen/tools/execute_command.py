# standard
import subprocess

# third party
# custom
from sunwaee_gen.tool import T


@T()
def execute_command(command: str) -> str:
    """Execute a command in the terminal and return the output.

    command: The command to execute (e.g., 'ls -la', 'echo hello', 'wc file.txt')
    """

    try:
        # run
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60,
        )

        # output
        output = ""
        if result.stdout:
            output += f"STDOUT:\n{result.stdout}"
        if result.stderr:
            output += f"\nSTDERR:\n{result.stderr}"

        if result.returncode != 0:
            output += f"\nRETURN CODE: {result.returncode}"

        return output or "Command executed successfully (no output)"

    except subprocess.TimeoutExpired:
        return f"Command timed out after 60 seconds"
    except FileNotFoundError:
        return f"Command not found: {command.split()[0]}"
    except Exception as e:
        return f"Error executing command: {str(e)}"
