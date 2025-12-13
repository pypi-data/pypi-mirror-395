import sys
from argparse import Namespace, _SubParsersAction
from pathlib import Path
from rich.console import Console
from ..core import find_projects, sort_projects_by_dependency
from ..runner import run_project_command

def register(subparsers: _SubParsersAction):
    """Register the run command."""
    run_parser = subparsers.add_parser("run", help="Run a shell command across projects")
    run_parser.add_argument("command_string", help="The shell command to execute")
    run_parser.add_argument("project_name", nargs="?", default="all", help="Name of the project to run on or 'all'")
    run_parser.add_argument("--fail-fast", action="store_true", help="Stop execution if a command fails")
    run_parser.set_defaults(func=execute)

def execute(args: Namespace, console: Console):
    """Execute the run command."""
    root_path = Path(args.path).resolve()
    all_projects = find_projects(root_path)
    target_projects = []

    if args.project_name == "all":
        try:
            target_projects = sort_projects_by_dependency(all_projects)
        except ValueError as e:
            console.print(f"[red]Dependency sorting failed: {e}[/red]")
            sys.exit(1)

        console.print(f"[bold]Running command '{args.command_string}' on {len(target_projects)} projects...[/bold]")
    else:
        target = next((p for p in all_projects if p.name == args.project_name), None)
        if not target:
            console.print(f"[red]Project '{args.project_name}' not found in {root_path}[/red]")
            sys.exit(1)
        target_projects = [target]

    results = {"success": [], "failed": []}

    for project in target_projects:
        console.rule(f"Running on {project.name}")
        success = run_project_command(project.path, args.command_string)
        if success:
            results["success"].append(project.name)
        else:
            results["failed"].append(project.name)
            if args.fail_fast:
                console.print(f"[red]Fail-fast enabled. Stopping execution.[/red]")
                break

    console.rule("Execution Summary")
    if results["success"]:
        console.print(f"[green]Success: {len(results['success'])}[/green] {results['success']}")
    if results["failed"]:
        console.print(f"[red]Failed:  {len(results['failed'])}[/red] {results['failed']}")
        sys.exit(1)
