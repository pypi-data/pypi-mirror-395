import subprocess
from typing import List

def run_command(command: List[str]) -> subprocess.CompletedProcess:
    """
    A robust wrapper around subprocess.run with logging and error handling.

    Args:
        command: A list of strings representing the command to execute.

    Returns:
        A CompletedProcess instance.

    Raises:
        subprocess.CalledProcessError: If the command returns a non-zero exit code.
    """
    print(f"Running command: {' '.join(command)}")
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
        )
        print(f"Command output: {result.stdout}")
        return result
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}:\n{e.stderr}")
        raise