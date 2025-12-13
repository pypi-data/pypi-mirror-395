<div align="center">
  <img src="https://raw.githubusercontent.com/dhruv13x/jules-cli/main/jules-cli_logo.png" alt="jules-cli logo" width="200"/>
</div>

<div align="center">

<!-- Package Info -->
[![PyPI version](https://img.shields.io/pypi/v/jules-cli.svg)](https://pypi.org/project/jules-cli/)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
![Wheel](https://img.shields.io/pypi/wheel/jules-cli.svg)
[![Release](https://img.shields.io/badge/release-PyPI-blue)](https://pypi.org/project/jules-cli/)

<!-- Build & Quality -->
[![Build status](https://github.com/dhruv13x/jules-cli/actions/workflows/publish.yml/badge.svg)](https://github.com/dhruv13x/jules-cli/actions/workflows/publish.yml)
[![Codecov](https://codecov.io/gh/dhruv13x/jules-cli/graph/badge.svg)](https://codecov.io/gh/dhruv13x/jules-cli)
[![Test Coverage](https://img.shields.io/badge/coverage-90%25%2B-brightgreen.svg)](https://github.com/dhruv13x/jules-cli/actions/workflows/test.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/badge/linting-ruff-yellow.svg)](https://github.com/astral-sh/ruff)
![Security](https://img.shields.io/badge/security-CodeQL-blue.svg)

<!-- Usage -->
![Downloads](https://img.shields.io/pypi/dm/jules-cli.svg)
[![PyPI Downloads](https://img.shields.io/pypi/dm/jules-cli.svg)](https://pypistats.org/packages/jules-cli)
![OS](https://img.shields.io/badge/os-Linux%20%7C%20macOS%20%7C%20Windows-blue.svg)
[![Python Versions](https://img.shields.io/pypi/pyversions/jules-cli.svg)](https://pypi.org/project/jules-cli/)

<!-- License -->
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

# jules-cli

A fully automated **developer assistant CLI** built on the **Jules API** (Google’s experimental code automation system).  
`jules-cli` lets you run tests, fix bugs, apply patches, refactor code, and even create GitHub pull requests — all from your terminal.

Designed for real-world workflows, CI pipelines, and local debugging sessions.

---

## 🚀 Quick Start (User View)

### Prerequisites
- Python 3.8+
- `pip`

### One-command installation
```bash
pip install jules-cli
```

### Usage Example
```bash
# Initialize and setup API keys
jules init

# Fix tests automatically
jules auto
```

---

## ✨ Key Features

- **God Level: Proactive Suggestions**: `jules suggest` scans your codebase to identify security holes, missing tests, and technical debt before they become problems.
- **God Level: Automated Test Fixer**: `jules auto` runs pytest, sends failures to the API, and autonomously applies fixes.
 - **Flaky Test Detection**: Automatically detects flaky tests by re-running failures (`jules auto --detect-flaky`).
- **God Level: Intelligent Test Generation**: `jules testgen` generates comprehensive tests for your code (`jules testgen src/utils.py`).
- **AI-Powered Refactoring**: Perform repository-wide refactors with natural language instructions (`jules refactor "Migrate to Python 3.11"`).
- **Development Assistant**: Issue arbitrary tasks like bug fixes or feature additions (`jules task "Add a retry mechanism to the HTTP client"`).
- **Stateful Interactive REPL**: Chat with your codebase in real-time (`jules interact`).
- **TUI Dashboard**: Launch a rich terminal interface for a visual experience (`jules tui`).
- **Workspace Automation**: Run commands across multiple repositories defined in a workspace (`jules workspace run`).
- **Multi-Platform PR/MR Support**: Create Pull Requests/Merge Requests for GitHub, GitLab, and Bitbucket (`jules pr create`).
- **Git Hooks**: Install pre-commit hooks to run jules checks automatically (`jules hooks install`).
- **Session Management**: Track, review, and resume your interactive sessions (`jules session list`, `jules history view`).
- **Interactive Staging**: Selectively stage changes with a user-friendly interface (`jules stage`).
- **Environment Doctor**: Validate your setup and dependencies (`jules doctor`).
- **Secure Credential Storage**: Safely stores API keys in your system keyring (`jules auth login`) instead of plain text files.
- **Self-Update Mechanism**: Keep your CLI up-to-date with `jules upgrade`.
- **Shell Completion**: Native tab-completion support for Bash, Zsh, and Fish shells (`jules --install-completion`).

---

## ⚙️ Configuration & Advanced Usage (Dev View)

### Environment Variables
- `JULES_API_KEY`: Your Jules API key.
- `GITHUB_TOKEN`: Your GitHub token for PR creation.

### CLI/API Table

| Command | Description | Arguments | Options |
| --- | --- | --- | --- |
| `init` | Interactive setup wizard. | | |
| `auth login` | Interactively set API keys securely. | | |
| `config get/set`| Manage configuration values. | `key`, `value` | |
| `config list` | List all configuration. | | |
| `auto` | Run tests and auto-fix failures. | | `--runner` (`-r`), `--detect-flaky` |
| `testgen` | Generate tests for a given file. | `file_path` | `--type` (`-t`) |
| `refactor` | Run a repository-wide refactor. | `instruction` | |
| `task` | Ask Jules to perform an arbitrary dev task. | `prompt` | |
| `suggest` | Proactively scan and suggest improvements. | | `--focus` (`-f`), `--security`, `--tests`, `--chore` |
| `interact` | Start an interactive chat session. | `prompt` | |
| `tui` | Launch the Jules TUI. | | |
| `workspace run` | Run command across multiple repos. | `command` | |
| `approve` | Approve the plan for the current session. | `session_id` | |
| `reject` | Reject the plan for the current session. | `session_id` | |
| `session list` | List active sessions. | | |
| `session show` | Show active session details. | `session_id` | |
| `history list` | List all past sessions. | | |
| `history view` | View details of a past session. | `session_id` | |
| `apply` | Apply last patch received. | | |
| `commit` | Commit & create branch after apply. | | `--message` (`-m`), `--type` (`-t`) |
| `push` | Push branch to origin. | | |
| `pr create` | Create a PR/MR (GitHub/GitLab/Bitbucket). | | `--title`, `--body`, `--draft`, `--labels`, `--reviewers`, `--assignees`, `--issue` |
| `hooks install` | Install Jules pre-commit hooks. | | |
| `stage` | Interactively stage changes. | | |
| `doctor` | Run environment validation checks. | | |
| `upgrade` | Self-update the Jules CLI. | | |

**Global Options:**
- `--debug`: Enable debug logging.
- `--verbose`: Enable verbose logging.
- `--no-color`: Disable colored output.
- `--json`: Output in JSON format.
- `--pretty`: Pretty-print JSON output.

---

## 🏗️ Architecture

```
jules-cli/
│
├── src/
│   └── jules_cli/
│       ├── commands/      # Individual command modules (auto.py, task.py, etc.)
│       ├── core/          # Jules API interaction
│       ├── git/           # Git utilities
│       ├── patch/         # Patch application logic
│       ├── testing/       # Test runner integration
│       ├── utils/         # Shared helpers (logging, config)
│       ├── cli.py         # Main entry point (Typer app)
│       └── ...
│
├── tests/                 # Test suite
├── config.toml            # Configuration file
├── pyproject.toml         # Project metadata and dependencies
└── README.md              # Documentation
```

The `jules-cli` is a Python-based command-line interface powered by the `typer` library. The core logic is organized into several modules within the `src/jules_cli` directory. `cli.py` serves as the main entry point, aggregating sub-commands from the `commands/` directory. The application uses a global state (`_state`) to manage session data across commands and secure storage (`keyring`) for credentials.

---

## 🗺️ Roadmap

### Upcoming
- **Spec-First Mode**: Generate specs, then code, then tests.
- **AI-powered merge conflict resolver**: Intelligent conflict resolution strategies.
- **Enhanced Workspace Support**: Deeper integration for monorepos and multi-repo setups.

### Completed
- **Automated test fixer**: `jules auto`
- **Proactive Suggestions**: `jules suggest`
- **Intelligent Test Generation**: `jules testgen`
- **Interactive REPL**: `jules interact`
- **Multi-Platform PR/MRs**: `jules pr create`
- **Workspace Automation**: `jules workspace run`
- **Secure Auth**: Keyring integration.
- **Self-Updates**: `jules upgrade`

---

## 🤝 Contributing & License

Contributions, bug reports, and feature requests are welcome. Please refer to the `FEATURE_PROPOSAL_TEMPLATE` for more information.

This project is licensed under the MIT License. See `LICENSE` for details.
