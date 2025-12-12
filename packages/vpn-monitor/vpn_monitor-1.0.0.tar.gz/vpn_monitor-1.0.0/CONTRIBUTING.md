# Contributing to VPN Monitor

Thank you for your interest in contributing to VPN Monitor! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Branching Strategy](#branching-strategy)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)
- [Code Style](#code-style)
- [Testing](#testing)
- [Building](#building)

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code:

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive feedback
- Accept responsibility for mistakes and learn from them

## Getting Started

1. **Fork the repository** on GitHub: https://github.com/henrykp/vpn_status_monitor
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/vpn_status_monitor.git
   cd vpn_status_monitor
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/henrykp/vpn_status_monitor.git
   ```

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- Windows OS (for full functionality testing - the application is Windows-specific)

### Codebase Overview

The project structure:

- `vpn_monitor/main.py` - Entry point, CLI argument parsing, startup integration, and main application logic
- `vpn_monitor/monitor.py` - Process detection (`msrdc.exe`, `Windows365.exe`) and network/IP checking via ip-api.com
- `vpn_monitor/gui.py` - Warning window (PowerShell-based) and input dialogs
- `vpn_monitor/tray.py` - System tray icon and menu functionality
- `tests/` - Test suite (currently placeholder tests)
- `run.py` - Convenience script to run the application from source

### Setting Up Your Environment

1. **Create a virtual environment**:

   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment**:

   ```bash
   # Windows (PowerShell)
   .\venv\Scripts\Activate.ps1

   # Windows (Command Prompt)
   .\venv\Scripts\activate.bat
   ```

3. **Install dependencies**:

   ```bash
   pip install -e .
   pip install -r requirements-dev.txt
   ```

4. **Install pre-commit hooks**:

   ```bash
   pre-commit install
   pre-commit install --hook-type commit-msg
   ```

5. **Verify setup**:
   ```bash
   python run.py --help
   ```

## Branching Strategy

We use a **trunk-based development** model with `main` as the release branch.

### Branch Types

| Branch Pattern   | Purpose               | Base Branch | Merges Into |
| ---------------- | --------------------- | ----------- | ----------- |
| `main`           | Production releases   | -           | -           |
| `feature/<name>` | New features          | `main`      | `main`      |
| `fix/<name>`     | Bug fixes             | `main`      | `main`      |
| `docs/<name>`    | Documentation updates | `main`      | `main`      |
| `chore/<name>`   | Maintenance tasks     | `main`      | `main`      |

### Workflow

1. **Create a feature branch** from `main`:

   ```bash
   git checkout main
   git pull upstream main
   git checkout -b feature/my-new-feature
   ```

2. **Make your changes** with atomic commits

3. **Keep your branch updated**:

   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

4. **Push and create a Pull Request**:
   ```bash
   git push origin feature/my-new-feature
   ```

## Commit Messages

We use **[Conventional Commits](https://www.conventionalcommits.org/)** specification for commit messages. This enables automatic changelog generation and semantic versioning.

### Format

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Types

| Type       | Description                                         |
| ---------- | --------------------------------------------------- |
| `feat`     | A new feature                                       |
| `fix`      | A bug fix                                           |
| `docs`     | Documentation only changes                          |
| `style`    | Code style changes (formatting, whitespace)         |
| `refactor` | Code changes that neither fix bugs nor add features |
| `perf`     | Performance improvements                            |
| `test`     | Adding or updating tests                            |
| `build`    | Build system or dependency changes                  |
| `ci`       | CI/CD configuration changes                         |
| `chore`    | Other changes that don't modify src or test files   |
| `revert`   | Reverts a previous commit                           |

### Scopes (Optional)

- `monitor` - Core monitoring functionality (process detection, network checks)
- `gui` - GUI/warning window and dialogs
- `tray` - System tray functionality
- `main` - Entry point, CLI, startup integration
- `deps` - Dependencies
- `ci` - CI/CD configuration
- `build` - Build configuration and tooling

### Examples

```bash
# Feature
git commit -m "feat(tray): add custom snooze duration option"

# Bug fix
git commit -m "fix(monitor): resolve memory leak in process detection"

# Breaking change (use ! or BREAKING CHANGE footer)
git commit -m "feat(api)!: change configuration file format"

# With body
git commit -m "fix(gui): prevent warning window from appearing behind other windows

The warning window now uses HWND_TOPMOST flag consistently
to ensure visibility across all Windows versions.

Fixes #123"
```

## Pull Request Process

1. **Ensure your code passes all checks**:

   ```bash
   # Run linting
   flake8 vpn_monitor tests

   # Run tests
   pytest
   ```

2. **Update documentation** if needed (README.md, CONTRIBUTING.md, CHANGELOG.md, code comments)

3. **Check for placeholder URLs** - Ensure all links point to the correct repository (henrykp/vpn_status_monitor)

4. **Create the Pull Request** on GitHub

5. **Address feedback** promptly

### PR Requirements

- [ ] All CI checks pass
- [ ] Code follows project style guidelines
- [ ] Commits follow conventional commit format
- [ ] Documentation updated (if applicable)
- [ ] Tests added/updated (if applicable)

### Merge Strategy

We use **squash merging** for PRs to keep the main branch history clean. Your PR title should follow conventional commit format as it becomes the squash commit message.

## Code Style

We follow **PEP 8** with some project-specific guidelines.

### Linting

We use `flake8` for linting:

```bash
flake8 vpn_monitor tests
```

### Guidelines

- **Line length**: 100 characters maximum
- **Imports**: Use absolute imports, group in order (stdlib, third-party, local)
- **Docstrings**: Use Google-style docstrings for public functions/classes
- **Type hints**: Encouraged but not required

### Pre-commit Hooks

Pre-commit hooks automatically check your code before each commit:

```bash
# Install hooks (one-time)
pre-commit install
pre-commit install --hook-type commit-msg

# Run manually on all files
pre-commit run --all-files
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=vpn_monitor

# Run specific test file
pytest tests/test_monitor.py
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files `test_<module>.py`
- Name test functions `test_<description>`
- Use pytest fixtures for common setup (see `tests/conftest.py`)

**Note**: The current test suite contains placeholder tests. When adding new functionality, please add appropriate unit tests. Consider:

- Mocking external API calls (ip-api.com)
- Mocking Windows API calls for cross-platform testing
- Testing edge cases (network failures, missing files, etc.)

### Test Coverage

We encourage maintaining good test coverage. Run tests with coverage:

```bash
pytest --cov=vpn_monitor --cov-report=html
```

Then open `htmlcov/index.html` to view the coverage report.

## Building

### Building the Executable

```bash
# Install PyInstaller
pip install pyinstaller

# Build
pyinstaller --noconsole --onefile --name vpn-monitor run.py
```

The executable will be created in the `dist/` folder.

### Verifying the Build

```bash
# Run the built executable
.\dist\vpn-monitor.exe --help
```

## Codebase Architecture

### Key Components

1. **VPNMonitorApp** (`main.py`): Main application class that orchestrates all components

   - Manages monitoring loop (runs every 5 seconds)
   - Handles snooze functionality
   - Coordinates between tray icon, warning window, and monitor

2. **Process Detection** (`monitor.py`):

   - Uses `psutil` to find target processes
   - Uses Windows API (`ctypes.windll.user32`) to check for visible windows
   - Only triggers when processes have visible windows

3. **Network Checking** (`monitor.py`):

   - Queries `ip-api.com` for public IP and country code
   - Supports `allowed_ips.txt` for IP-based bypass
   - Falls back to "safe" if network check fails

4. **Warning Window** (`gui.py`):

   - Uses PowerShell scripts to create topmost windows
   - Custom styling with EPAM brand colors (#39c2d7, #464547)

5. **System Tray** (`tray.py`):
   - Uses `pystray` for cross-platform tray support (though app is Windows-only)
   - Custom shield icon generated with PIL/Pillow

### Dependencies

- `psutil` - Process and system utilities
- `requests` - HTTP requests to ip-api.com
- `pystray` - System tray icon
- `Pillow` - Image generation for tray icon

See `pyproject.toml` for complete dependency list.

## Common Development Tasks

### Adding a New Target Process

Edit `TARGET_PROCESSES` in `vpn_monitor/monitor.py`:

```python
TARGET_PROCESSES = ["msrdc.exe", "Windows365.exe", "newprocess.exe"]
```

### Changing Monitoring Interval

Edit the wait time in `monitor_loop()` in `vpn_monitor/main.py`:

```python
threading.Event().wait(5)  # Change 5 to desired seconds
```

### Modifying Warning Window Appearance

Edit the PowerShell script in `POWERSHELL_WARNING_SCRIPT` in `vpn_monitor/gui.py`.

## Questions?

If you have questions about contributing, feel free to:

1. Search existing [Issues](https://github.com/henrykp/vpn_status_monitor/issues)
2. Create a new [Issue](https://github.com/henrykp/vpn_status_monitor/issues/new)
3. Check the [README.md](README.md) for user-facing documentation

Thank you for contributing! 🎉
