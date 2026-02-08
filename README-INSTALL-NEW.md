# MTKClient Installation and Setup Guide

This document provides comprehensive installation instructions for MTKClient with the new installer features.

## Table of Contents
- [System Requirements](#system-requirements)
- [Installation Methods](#installation-methods)
- [GUI Features](#gui-features)
- [Advanced Settings](#advanced-settings)
- [Workflows](#workflows)

## System Requirements

### Windows
- Windows 7/8/10/11 (64-bit only)
- Python 3.8 or higher (64-bit)
- Administrator privileges

### Linux
- Ubuntu 18.04+, Debian 10+, Fedora 30+, Arch Linux, or compatible distribution
- Python 3.8 or higher
- libusb-1.0, libfuse2, and udev

### macOS
- macOS 10.14 or higher
- Python 3.8 or higher

## Installation Methods

### Windows x64 - Automated Installer

1. Download the `mtkclient-windows-x64-installer.zip` from releases
2. Extract the archive
3. Right-click `install.bat` and select "Run as administrator"
4. Follow the on-screen instructions

The installer will:
- Verify your system is 64-bit Windows
- Install Python dependencies
- Create desktop and Start Menu shortcuts
- Configure the GUI to run with administrator privileges

#### Running the GUI on Windows

**Option 1:** Double-click the "MTKClient" shortcut on your desktop or Start Menu

**Option 2:** Run `mtk_gui_admin.bat` from the installation directory

**Option 3:** From Command Prompt:
```batch
cd path\to\mtkclient
pythonw mtk_gui.py
```

### Linux - Automated Installer

1. Download and extract the `mtkclient-linux-installer.tar.gz`
2. Open a terminal in the extracted directory
3. Run the installer:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

The installer will:
- Install system dependencies (libusb, libfuse, udev)
- Install Python dependencies
- Install udev rules for USB device access
- Create desktop entry with icon
- Add command-line utilities to PATH

#### Running the GUI on Linux

**Option 1:** Find "MTKClient" in your application menu

**Option 2:** From terminal:
```bash
mtk-gui
```

**Option 3:** From the installation directory:
```bash
./mtk_gui.py
```

The GUI will automatically request administrator privileges when launched.

### Manual Installation (All Platforms)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the GUI
python3 mtk_gui.py

# Run the CLI
python3 mtk.py --help
```

## GUI Features

### Main Features
- **Read Flash**: Read partitions, full flash, or specific sectors
- **Write Flash**: Write partitions, full flash, or specific sectors
- **Erase Flash**: Erase partitions or specific sectors
- **Unlock/Lock Device**: Device security configuration
- **Generate Keys**: Hardware key derivation
- **RPMB Operations**: Read/Write RPMB partitions

### Connection Settings
- Serial port selection with auto-detect
- Custom VID/PID for USB devices
- DA loader configuration
- Preloader configuration
- IoT mode for MT6261/2301

### New Advanced Settings Dialog

Access via **File → Advanced Settings...** in the menu bar.

The Advanced Settings dialog provides access to all CLI arguments through a user-friendly interface:

#### Connection Tab
- **USB Settings**: Custom VID/PID, auto-reconnect control
- **Serial Port**: Manual or auto-detect serial port selection
- **DA Settings**: Stock DA usage option
- **Other Options**: 
  - Generate hardware keys on connect
  - Read SoC ID on connect
  - Write preloader to file

#### Authentication Tab
- **Auth File**: Specify authentication file (auth_sv5.auth)
- **Cert File**: Specify certificate file

#### Exploit Options Tab
- **Payload Type**: Select exploit type (amonet, kamakiri, kamakiri2, carbonara)
- **Kamakiri Settings**:
  - var1 value
  - UART address
  - DA address
  - BROM address
  - Watchdog address
  - Crash mode selection
  - Skip WDT initialization
  - Enforce crash in preloader mode
- **Application ID**: Set app ID for specific operations

#### GPT/Partition Tab
- **GPT Settings**:
  - Sector size configuration
  - GPT partition entries count
  - GPT entry size
  - GPT entry start LBA
- **Partition Settings**:
  - Partition type selection (user, boot1, boot2, rpmb, gp1-4)
  - Skip specific partitions

#### Debug Tab
- **Debug Mode**: Enable verbose logging
- **Log Level**: Set application log level (Trace, Debug, Normal, Warning, Error)
- **UART Log Level**: Set UART communication log level

All settings are applied in real-time and persist for the current session.

## Workflows

### Automated Build Workflow

The project includes GitHub Actions workflows for automated building:

#### Build Release Packages (`build-release.yml`)
- Triggers on: Push to tags (v*), workflow dispatch, pull requests
- Builds executables for:
  - Windows x64 (Console + GUI)
  - Linux (Console + GUI)
  - macOS (Console + GUI)
- Uses PyInstaller to create standalone executables
- Uploads artifacts for download

#### Build Installer Packages (`build-installer.yml`)
- Triggers on: Push to tags (v*), workflow dispatch
- Creates complete installer packages:
  - **Windows x64**: ZIP archive with installer script and executables
  - **Linux**: TAR.GZ archive with installer/uninstaller scripts
- Includes all necessary documentation and setup files

### Running Workflows

Workflows can be triggered manually:

1. Go to Actions tab in GitHub
2. Select the desired workflow
3. Click "Run workflow"
4. Choose the branch and click "Run workflow"

## Uninstallation

### Windows
Currently, manual uninstallation:
1. Delete desktop and Start Menu shortcuts
2. Delete the installation folder
3. (Optional) Uninstall Python packages:
   ```batch
   pip uninstall pyusb pycryptodome pycryptodomex colorama shiboken6 pyside6 pyserial fusepy
   ```

### Linux
Run the uninstaller:
```bash
./uninstall.sh
```

This will:
- Remove desktop entry and icon
- Remove command-line utilities
- Remove udev rules
- Optionally remove Python packages

## Troubleshooting

### Windows: "This installer is for Windows x64 only"
**Solution**: Your system is 32-bit. This installer requires 64-bit Windows.

### Linux: Device not detected
**Solution**: 
1. Ensure udev rules are installed: `sudo ./install.sh`
2. Reload udev: `sudo udevadm control --reload-rules && sudo udevadm trigger`
3. Replug the device

### Permission denied errors
**Solution**: Run the GUI with administrator/root privileges (the installers configure this automatically)

### Python module errors
**Solution**: Reinstall dependencies: `pip install -r requirements.txt`

## Additional Resources

- **Usage Guide**: See [README-USAGE.md](README-USAGE.md)
- **Windows Installation**: See [README-WINDOWS.md](README-WINDOWS.md)
- **Windows x64 Installer**: See [README-INSTALLER-WINDOWS.md](README-INSTALLER-WINDOWS.md)
- **Main Documentation**: See [README.md](README.md)
- **GitHub Issues**: https://github.com/EduardoA3677/mtkclient/issues

## License

GPLv3 License - See [LICENSE](LICENSE) file

## Credits

MTK Flash Client (c) B.Kerler 2018-2026
