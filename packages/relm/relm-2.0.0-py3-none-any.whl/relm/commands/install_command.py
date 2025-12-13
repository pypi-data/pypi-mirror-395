import sys
from argparse import Namespace, _SubParsersAction
from pathlib import Path
from rich.console import Console
from ..core import find_projects, sort_projects_by_dependency
from ..install import install_project

def register(subparsers: _SubParsersAction):
    """Register the install command."""
    install_parser = subparsers.add_parser("install", help="Install projects into the current environment")
    install_parser.add_argument("project_name", help="Name of the project to install or 'all'")
    install_parser.add_argument("--no-editable", action="store_true", help="Install in standard mode instead of editable")
    install_parser.set_defaults(func=execute)

def execute(args: Namespace, console: Console):
    """Execute the install command."""
    root_path = Path(args.path).resolve()
    all_projects = find_projects(root_path)
    target_projects = []

    if args.project_name == "all":
        try:
            target_projects = sort_projects_by_dependency(all_projects)
        except ValueError as e:
            console.print(f"[red]Dependency sorting failed: {e}[/red]")
            sys.exit(1)

        console.print(f"[bold]Bulk Installing {len(target_projects)} projects...[/bold]")
    else:
        target = next((p for p in all_projects if p.name == args.project_name), None)
        if not target:
            console.print(f"[red]Project '{args.project_name}' not found in {root_path}[/red]")
            sys.exit(1)
        target_projects = [target]

    results = {"installed": [], "failed": []}
    editable_mode = not args.no_editable

    for project in target_projects:
        success = install_project(project, editable=editable_mode)
        if success:
            results["installed"].append(project.name)
        else:
            results["failed"].append(project.name)

    if args.project_name == "all":
        console.rule("Bulk Install Summary")
        console.print(f"[green]Installed: {len(results['installed'])}[/green] {results['installed']}")
        if results["failed"]:
            console.print(f"[red]Failed:    {len(results['failed'])}[/red] {results['failed']}")
