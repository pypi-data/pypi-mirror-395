import subprocess
from pathlib import Path
from rich.console import Console

console = Console()

def run_project_command(project_path: Path, command: str) -> bool:
    """
    Runs a shell command in the project directory, allowing direct output to stdout/stderr.
    Returns True if successful (exit code 0), False otherwise.
    """
    try:
        result = subprocess.run(
            command,
            cwd=project_path,
            shell=True,
            check=False
        )
        return result.returncode == 0
    except Exception as e:
        console.print(f"[red]Error executing command: {e}[/red]")
        return False
