import sys
from argparse import Namespace, _SubParsersAction
from pathlib import Path
from rich.console import Console
from ..core import find_projects
from ..clean import clean_project

def register(subparsers: _SubParsersAction):
    """Register the clean command."""
    clean_parser = subparsers.add_parser("clean", help="Recursively remove build artifacts (dist/, build/, __pycache__)")
    clean_parser.add_argument("project_name", help="Name of the project to clean or 'all'", nargs="?", default="all")
    clean_parser.set_defaults(func=execute)

def execute(args: Namespace, console: Console):
    """Execute the clean command."""
    root_path = Path(args.path).resolve()
    all_projects = find_projects(root_path)
    target_projects = []

    if args.project_name == "all":
        target_projects = all_projects
        console.print(f"[bold]Cleaning workspace for {len(target_projects)} projects...[/bold]")
    else:
        target = next((p for p in all_projects if p.name == args.project_name), None)
        if not target:
            console.print(f"[red]Project '{args.project_name}' not found in {root_path}[/red]")
            sys.exit(1)
        target_projects = [target]

    total_cleaned_paths = 0

    for project in target_projects:
        cleaned_paths = clean_project(project)
        if cleaned_paths:
            total_cleaned_paths += len(cleaned_paths)
            console.print(f"[green]Cleaned {project.name}:[/green]")
            for path in cleaned_paths:
                console.print(f"  - {path}")
        else:
            console.print(f"[dim]Nothing to clean for {project.name}[/dim]")

    console.rule("Clean Summary")
    console.print(f"Removed {total_cleaned_paths} artifacts across {len(target_projects)} projects.")
