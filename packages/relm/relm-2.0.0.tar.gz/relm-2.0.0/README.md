<div align="center">
  <img src="https://raw.githubusercontent.com/dhruv13x/relm/main/relm_logo.png" alt="relm logo" width="200"/>
</div>

<div align="center">

<!-- Package Info -->
[![PyPI version](https://img.shields.io/pypi/v/relm.svg)](https://pypi.org/project/relm/)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
![Wheel](https://img.shields.io/pypi/wheel/relm.svg)
[![Release](https://img.shields.io/badge/release-PyPI-blue)](https://pypi.org/project/relm/)

<!-- Build & Quality -->
[![Build status](https://github.com/dhruv13x/relm/actions/workflows/publish.yml/badge.svg)](https://github.com/dhruv13x/relm/actions/workflows/publish.yml)
[![Codecov](https://codecov.io/gh/dhruv13x/relm/graph/badge.svg)](https://codecov.io/gh/dhruv13x/relm)
[![Test Coverage](https://img.shields.io/badge/coverage-90%25%2B-brightgreen.svg)](https://github.com/dhruv13x/relm/actions/workflows/test.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/badge/linting-ruff-yellow.svg)](https://github.com/astral-sh/ruff)

<!-- Usage -->
![Downloads](https://img.shields.io/pypi/dm/relm.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

# relm

**The "Batteries Included" CLI for managing your Python mono-repo or multi-project workspace.**
Automate versioning, git tagging, PyPI releases, and local environment setup with a single tool.

---

## 🚀 Quick Start

### Prerequisites
*   **Python 3.8+**
*   `pip` or `pipx`

### Installation
Install globally with `pipx` (recommended):
```bash
pipx install relm
```
Or with `pip`:
```bash
pip install relm
```

### Usage Example
Manage your projects from the root of your workspace:

```bash
# 1. Discover all projects in the current directory
relm list

# 2. Bulk install all projects in editable mode (Developer Mode)
relm install all

# 3. Check git status across all projects
relm status all

# 4. Run a command across all projects (e.g., tests)
relm run "pytest" all --fail-fast

# 5. Release a patch version for a specific project
relm release my-lib patch
```

> **Note**: `relm` works by finding `pyproject.toml` files. Ensure your projects are standard Python packages.

---

## ✨ Key Features

*   **Automated Discovery**: recursively finds all valid Python projects in your workspace.
*   **Smart Versioning**: Semantically bumps versions (`major`, `minor`, `patch`, `alpha`, `beta`, `rc`) in `pyproject.toml` and `__init__.py`.
*   **Zero-Config Git Ops**: Auto-stages, commits, and tags releases with clean messages.
*   **PyPI Publishing**: Builds wheels/sdist and uploads to PyPI automatically.
*   **Automated Changelog**: **Parses Conventional Commits to automatically generate and update `CHANGELOG.md`.**
*   **Configuration**: Supports `.relm.toml` for global configuration.
*   **Bulk Operations**: **Release, Install, or Check Status of ALL projects at once.**
*   **Task Runner**: Execute any shell command across your entire suite (`relm run "..."`).
*   **Dependency Awareness**: **Automatically topological sorts projects during execution (build `lib-a` before `app-b`).**
*   **Workspace Cleaning**: Quickly remove build artifacts (`dist/`, `build/`, `__pycache__`) with `relm clean`.
*   **PyPI Verification**: **Verify if the locally released version (tag) is available on PyPI with `relm verify`.**
*   **"Changed Since" Detection**: Only list or act on projects modified since a specific git reference using `--since`.
*   **Project Scaffolding**: Generate new standard Python projects instantly with `relm create`.
*   **Developer Friendly**: "Safety checks" prevent running in system roots.

---

## ⚙️ Configuration & Advanced Usage

`relm` is controlled entirely via CLI arguments.

### Global Arguments
| Argument | Default | Description |
| :--- | :--- | :--- |
| `--path` | `.` | Root directory to scan for projects. |

### Commands

#### `list`
Lists all discovered projects, their versions, and paths.
| Argument | Description |
| :--- | :--- |
| `--since` | List only projects changed since the given git ref (e.g., `HEAD~1`, `main`, `v1.0`). |

#### `create`
Generates a new standard Python project structure.
| Argument | Description |
| :--- | :--- |
| `name` | Name of the new project. |
| `path` | Directory to create the project in (default: current directory). |

#### `install`
Installs projects into the current environment.
| Argument | Description |
| :--- | :--- |
| `project_name` | Name of the project or `all`. |
| `--no-editable` | Install in standard mode (default is editable `-e`). |

#### `run`
Executes a shell command in each project's directory.
| Argument | Description |
| :--- | :--- |
| `command_string` | The shell command to execute (e.g., `"ls -la"`). |
| `project_name` | Name of the project or `all` (default: `all`). |
| `--fail-fast` | Stop execution immediately if a command fails. |

#### `status`
Shows the Git branch and dirty/clean status for projects.
| Argument | Description |
| :--- | :--- |
| `project_name` | Name of the project or `all`. |

#### `verify`
Verifies if the locally released version (tag) is available on PyPI.
| Argument | Description |
| :--- | :--- |
| `project_name` | Name of the project or `all`. |

#### `clean`
Recursively removes build artifacts (`dist/`, `build/`, `__pycache__`) from projects.
| Argument | Description |
| :--- | :--- |
| `project_name` | Name of the project or `all`. |

#### `release`
Orchestrates the version bump, build, and publish flow.
| Argument | Description |
| :--- | :--- |
| `project_name` | Name of the project or `all`. |
| `type` | Bump type: `major`, `minor`, `patch`, `alpha`, `beta`, `rc`, `release`. |
| `-y`, `--yes` | Skip confirmation prompts. |
| `-m`, `--message` | Custom commit message template (e.g., `'chore: release {version}'`). |

---

## 🏗️ Architecture

`relm` follows a modular design to keep concerns separated:

```text
src/relm/
├── commands/        # Modular Command Implementations
│   ├── base.py      # Abstract base for commands
│   └── ...          # Individual command modules (list, release, etc.)
├── __init__.py      # Package init
├── banner.py        # ASCII art logo
├── changelog.py     # Changelog generation logic
├── config.py        # Configuration loading (.relm.toml)
├── core.py          # Project discovery & parsing logic
├── git_ops.py       # Git commands (status, commit, tag, push)
├── install.py       # pip installation wrappers
├── main.py          # CLI Entry Point & Argument Parsing
├── release.py       # Release orchestration workflow
├── runner.py        # Subprocess execution for 'run' command
├── verify.py        # PyPI availability verification
└── versioning.py    # Semantic version bumping
```

### Logic Flow
1.  **Discovery**: `main.py` loads configuration and calls `core.py` to map the directory tree.
2.  **Dispatch**: The `argparse` subparser routes execution to the specific module in `src/relm/commands/`.
3.  **Execution**: Command modules orchestrate the logic, calling helpers like `runner.py`, `git_ops.py`, or `changelog.py` to interact with the system.

---

## 🗺️ Roadmap

See [ROADMAP.md](ROADMAP.md) for the detailed vision.

*   [x] Bulk Release Support
*   [x] Task Runner (`relm run`)
*   [x] Project Status (`relm status`)
*   [x] Pre-release Version Support (`alpha`, `beta`, `rc`)
*   [x] Custom Commit Messages
*   [x] Changelog Generation
*   [x] Configuration File Support
*   [x] Dependency Graph Awareness

---

## 🤝 Contributing & License

Contributions are welcome! Please submit a PR or open an issue.

Licensed under **MIT**. See [LICENSE](LICENSE) for details.
