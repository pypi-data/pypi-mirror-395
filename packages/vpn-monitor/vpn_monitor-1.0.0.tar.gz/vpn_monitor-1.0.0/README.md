# VPN Monitor

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/vpn-monitor.svg)](https://badge.fury.io/py/vpn-monitor)

A Windows background application that monitors specific "Windows App" processes (e.g., `msrdc.exe`, `Windows365.exe`) and enforces VPN usage by checking the current region.

## Features

- **Process Monitoring**: Detects if `msrdc.exe` or `Windows365.exe` has a visible window
- **Region Check**: Verifies if the current public IP is in the allowed country (default: HU) via [ip-api.com](http://ip-api.com)
- **Allowed IPs**: Supports an optional list of allowed external IPs that bypass the country check
- **Warning System**: Displays a custom, topmost warning window if the region is incorrect while the target app is running
- **System Tray Integration**:
  - Snooze functionality (5m, 15m, 1h, 8h)
  - Set Allowed Country (hidden when `allowed_ips.txt` exists)
  - Exit
- **Startup Integration**: Can register itself to run at Windows startup
- **Continuous Monitoring**: Checks VPN status every 5 seconds

## Installation

### Option 1: Install from PyPI (Recommended)

```bash
pip install vpn-monitor
```

Then run:

```bash
vpn-monitor
```

### Option 2: Install from Source

**Prerequisites**: Python 3.8 or higher

1. **Clone the repository**:

   ```bash
   git clone https://github.com/henrykp/vpn_status_monitor.git
   cd vpn_status_monitor
   ```

2. **Install the package**:

   ```bash
   pip install -e .
   ```

3. **Run the application**:
   ```bash
   python run.py
   ```
   Or use the installed script:
   ```bash
   vpn-monitor
   ```

### Option 3: Download Pre-built Executable

Download the latest `.exe` file from the [Releases](https://github.com/henrykp/vpn_status_monitor/releases) page. No Python installation required.

## Usage

### Running the Application

Run from source:

```bash
python run.py
```

Or if installed via pip:

```bash
vpn-monitor
```

The application runs in the background and appears as a shield icon in the system tray.

### Command Line Arguments

- `--install-startup`: Registers the app to run on Windows startup
- `--remove-startup`: Removes the app from Windows startup
- `--help`: Show help message

**Example**:

```bash
python run.py --install-startup
```

### Configuration

#### Allowed Country

The default allowed country is **HU** (Hungary). You can change this via:

1. **System Tray Menu**: Right-click the tray icon → "Set Country..." → Enter 2-letter country code (e.g., US, DE, FR)
2. **Environment Variable**: Set `ALLOWED_COUNTRY` before running:
   ```bash
   set ALLOWED_COUNTRY=US
   python run.py
   ```

#### Allowed IPs (Bypass)

You can create a file named `allowed_ips.txt` in the same directory as the executable (or `run.py`). Add one IP address per line. If your current external IP matches any IP in this list, the warning will be suppressed regardless of your country.

**Note**: When `allowed_ips.txt` exists, the "Set Country..." option is hidden from the tray menu.

**Example `allowed_ips.txt`**:

```
203.0.113.1
198.51.100.2
192.0.2.10
```

## How It Works

1. **Process Detection**: Every 5 seconds, the application checks if `msrdc.exe` or `Windows365.exe` has a visible window
2. **Network Check**: If a target process is running, it queries [ip-api.com](http://ip-api.com) to determine your current public IP and country
3. **Safety Validation**:
   - First checks if your IP is in `allowed_ips.txt` (if the file exists)
   - Then verifies your country code matches the allowed country
4. **Warning Display**: If the region doesn't match (and IP is not in the allowed list), a topmost warning window appears

## Building Executable

To build a standalone `.exe` file:

1. **Install PyInstaller**:

   ```bash
   pip install pyinstaller
   ```

2. **Build the executable**:

   ```bash
   pyinstaller --noconsole --onefile --name vpn-monitor run.py
   ```

3. **Find the executable**:
   The output will be in the `dist/` folder as `vpn-monitor.exe`

## Project Structure

```
vpn_status_monitor/
├── vpn_monitor/          # Main package
│   ├── __init__.py
│   ├── main.py          # Entry point and CLI
│   ├── monitor.py       # Process and network monitoring
│   ├── gui.py           # Warning window and dialogs
│   └── tray.py          # System tray icon
├── tests/               # Test suite
├── run.py               # Convenience script to run from source
├── pyproject.toml       # Package configuration and dependencies
├── requirements-dev.txt # Development dependencies
└── README.md            # This file
```

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed development guidelines.

### Quick Start for Developers

1. **Clone and set up**:

   ```bash
   git clone https://github.com/henrykp/vpn_status_monitor.git
   cd vpn_status_monitor
   python -m venv venv
   .\venv\Scripts\Activate.ps1  # Windows PowerShell
   pip install -e .
   pip install -r requirements-dev.txt
   ```

2. **Install pre-commit hooks**:

   ```bash
   pre-commit install
   pre-commit install --hook-type commit-msg
   ```

3. **Run tests**:
   ```bash
   pytest
   ```

### Releasing a New Version

This project uses [setuptools-scm](https://github.com/pypa/setuptools_scm) — the version is automatically derived from git tags.

To release a new version:

```bash
git tag v1.0.0
git push --tags
```

Pushing the tag triggers the release workflow, which:

- Builds the Windows executable
- Builds and publishes the Python package to PyPI
- Creates a GitHub release with the executable and changelog

The package version is automatically set based on the tag (e.g., tag `v1.0.0` → version `1.0.0`).

## Troubleshooting

### Warning Window Doesn't Appear

- Ensure the target process (`msrdc.exe` or `Windows365.exe`) has a visible window
- Check that you're connected to the internet (the app needs to query ip-api.com)
- Verify your current IP country doesn't match the allowed country

### "Set Country" Option Not Visible

This option is hidden when `allowed_ips.txt` exists in the application directory. Delete or rename the file to restore the option.

### Application Doesn't Start at Boot

- Manually run with `--install-startup` flag:
  ```bash
  python run.py --install-startup
  ```
- Check Windows Startup folder or Registry (HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run)

### Network Check Fails

- Ensure you have an active internet connection
- The app uses [ip-api.com](http://ip-api.com) which has rate limits (45 requests/minute for free tier)
- If network check fails, the app assumes "safe" to avoid blocking legitimate use

## Security Considerations

- The application queries external services (ip-api.com) to determine your location
- No data is transmitted except your public IP address
- The `allowed_ips.txt` file is stored locally and not encrypted
- The application requires network access to function

## Known Limitations

- **Windows Only**: This application only works on Windows due to its use of Windows-specific APIs
- **Process-Specific**: Currently monitors only `msrdc.exe` and `Windows365.exe`
- **Internet Dependency**: Requires internet connection to check IP/region
- **Rate Limits**: ip-api.com has rate limits that may affect frequent checks

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Links

- **Homepage**: https://github.com/henrykp/vpn_status_monitor
- **Repository**: https://github.com/henrykp/vpn_status_monitor
- **Issues**: https://github.com/henrykp/vpn_status_monitor/issues
- **PyPI Package**: https://pypi.org/project/vpn-monitor/

## Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#troubleshooting) section
2. Search existing [Issues](https://github.com/henrykp/vpn_status_monitor/issues)
3. Create a new [Issue](https://github.com/henrykp/vpn_status_monitor/issues/new) if your problem isn't already reported
