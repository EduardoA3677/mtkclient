# GitHub Actions Workflows Documentation

This document describes the automated workflows configured for MTKClient.

## Overview

MTKClient uses GitHub Actions for continuous integration and automated builds. The workflows handle:
- Code linting and testing
- Building standalone executables for multiple platforms
- Creating installer packages
- Artifact management and release preparation

## Workflows

### 1. Python Application Test (`python-app.yml`)

**Purpose**: Run tests and code quality checks on every push and pull request.

**Triggers**:
- Push to `main` branch
- Pull requests
- Manual workflow dispatch

**Jobs**:
- **Test**: Runs on Ubuntu 24.04
  - Checks out code
  - Sets up Python 3.x with pip caching
  - Installs dependencies from requirements.txt
  - Runs flake8 linting:
    - Critical errors (E9, F63, F7, F82) fail the build
    - Style warnings don't fail but are reported

**Usage**: Automatically runs on every push/PR. View results in the Actions tab.

---

### 2. Build Release Packages (`build-release.yml`)

**Purpose**: Build standalone executables for Windows x64, Linux, and macOS.

**Triggers**:
- Push to tags matching `v*` (e.g., v1.0.0, v2.1.2)
- Pull requests (for testing)
- Manual workflow dispatch

**Jobs**:

#### build-windows
- **Platform**: windows-latest
- **Python**: 3.11 x64
- **Steps**:
  1. Install Python dependencies
  2. Install PyInstaller
  3. Build console version (`mtk_console.spec`)
  4. Build GUI version (`mtk_standalone.spec`)
  5. Upload artifacts:
     - `mtk-console-windows-x64`
     - `mtk-gui-windows-x64`

#### build-linux
- **Platform**: ubuntu-24.04
- **Python**: 3.11
- **System Dependencies**: libusb-1.0-0-dev, libfuse2, fuse
- **Steps**:
  1. Install system and Python dependencies
  2. Build console and GUI versions
  3. Upload artifacts:
     - `mtk-console-linux`
     - `mtk-gui-linux`

#### build-macos
- **Platform**: macos-latest
- **Python**: 3.11
- **Steps**:
  1. Install dependencies
  2. Build console and GUI versions
  3. Upload artifacts:
     - `mtk-console-macos`
     - `mtk-gui-macos`

**Usage**: 
```bash
# Create and push a version tag
git tag v2.1.3
git push origin v2.1.3
```

Or manually trigger from Actions tab → Build Release Packages → Run workflow.

**Artifacts**: Download from the workflow run in the Actions tab.

---

### 3. Build Installer Packages (`build-installer.yml`)

**Purpose**: Create complete installer packages with all necessary files.

**Triggers**:
- Push to tags matching `v*`
- Manual workflow dispatch

**Jobs**:

#### build-windows-installer
- **Platform**: windows-latest
- **Python**: 3.11 x64
- **Creates**: `mtkclient-windows-x64-installer.zip`
- **Includes**:
  - Built executables (`mtk_standalone_*`)
  - Installation scripts (`install.bat`, `mtk_gui_admin.bat`)
  - Documentation (README.md, README-INSTALLER-WINDOWS.md, LICENSE)
  - Setup files (udev rules, etc.)
  - Requirements file

#### build-linux-installer
- **Platform**: ubuntu-24.04
- **Python**: 3.11
- **Creates**: `mtkclient-linux-installer.tar.gz`
- **Includes**:
  - Built executables (if applicable)
  - Installation/uninstallation scripts (`install.sh`, `uninstall.sh`)
  - Documentation
  - Setup files
  - Requirements file

**Usage**:
```bash
# Create and push a version tag
git tag v2.1.3
git push origin v2.1.3
```

Or manually trigger from Actions tab → Build Installer Packages → Run workflow.

**Artifacts**: Download installer packages from the workflow run.

---

## PyInstaller Specifications

### One-File Executables

Both console and GUI versions are built as **single-file executables** that contain all dependencies, libraries, and resources embedded within the .exe file. This makes distribution easier as users only need to download and run a single file.

### Console Specification (`mtk_console.spec`)

- **Entry Point**: `mtk.py`
- **Build Mode**: One-file (all content in single .exe)
- **Target Architecture**: x86_64 (64-bit)
- **Console**: True (shows terminal window)
- **Icon**: `mtkclient/icon.ico`
- **Includes**:
  - Windows DLLs from `mtkclient/Windows/*`
  - Payload files from `mtkclient/payloads`
  - Loader binaries from `mtkclient/Loader`
  - Filesystem binaries from `mtkclient/Library/Filesystem/bin`
- **Output**: Single file `dist/mtk_console_YYYYMMDD.exe`
- **Features**: 
  - UPX compression enabled
  - All resources embedded in the executable
  - No external dependencies required

### GUI Specification (`mtk_standalone.spec`)

- **Entry Point**: `mtk_gui.py`
- **Build Mode**: One-file (all content in single .exe)
- **Target Architecture**: x86_64 (64-bit)
- **Console**: True (for debugging, can be set to False for release)
- **Icon**: `mtkclient/icon.ico`
- **Includes**:
  - GUI images from `mtkclient/gui/images`
  - All console spec includes
- **Output**: Single file `dist/mtk_standalone_YYYYMMDD.exe`
- **Features**: 
  - UPX compression enabled
  - All resources embedded in the executable
  - No external dependencies required
  - Ready to distribute as a single file

**Note**: When the executable runs, PyInstaller temporarily extracts files to a temp directory, but from the user's perspective, they only need to download and run a single .exe file.

---

## Manual Workflow Execution

### Via GitHub Web Interface

1. Go to the repository on GitHub
2. Click the "Actions" tab
3. Select the workflow you want to run
4. Click "Run workflow" button
5. Select the branch
6. Click "Run workflow"

### Via GitHub CLI

```bash
# Install GitHub CLI
# https://cli.github.com/

# Trigger build-release workflow
gh workflow run build-release.yml

# Trigger build-installer workflow
gh workflow run build-installer.yml

# Check workflow status
gh run list

# View workflow run details
gh run view <run-id>
```

---

## Artifact Download

### Via GitHub Web Interface

1. Go to Actions tab
2. Click on the workflow run
3. Scroll to "Artifacts" section
4. Click on the artifact name to download

### Via GitHub CLI

```bash
# List artifacts from a run
gh run view <run-id>

# Download all artifacts
gh run download <run-id>

# Download specific artifact
gh run download <run-id> -n artifact-name
```

---

## Troubleshooting

### Build Failures

**Python dependency issues**:
- Check `requirements.txt` is up to date
- Verify all dependencies are compatible with Python 3.11

**PyInstaller errors**:
- Ensure all data files are correctly specified in `.spec` files
- Check hidden imports are declared if needed
- Verify icon file paths are correct

**Platform-specific issues**:
- Linux: Ensure system dependencies (libusb, libfuse) are available
- Windows: Verify architecture is x64
- macOS: Check compatibility with macOS version

### Workflow Trigger Issues

**Tag not triggering workflow**:
- Ensure tag matches pattern `v*`
- Check tag was pushed: `git push origin v1.0.0`
- Verify workflows are enabled in repository settings

**Permission errors**:
- Check repository has GitHub Actions enabled
- Verify workflow files have correct permissions
- Ensure GITHUB_TOKEN has sufficient permissions

---

## Best Practices

### Version Tagging

Use semantic versioning for releases:
```bash
git tag -a v2.1.3 -m "Release version 2.1.3"
git push origin v2.1.3
```

### Release Process

1. Update version in `pyproject.toml`
2. Update CHANGELOG (if exists)
3. Commit changes
4. Create and push tag
5. Wait for workflows to complete
6. Download and test artifacts
7. Create GitHub release with artifacts

### Testing Before Release

Use workflow_dispatch to test builds:
```bash
gh workflow run build-release.yml --ref feature-branch
```

Or trigger from pull requests to test changes.

---

## Maintenance

### Updating Workflows

When modifying workflow files:
1. Test changes in a fork or feature branch first
2. Use pull requests to review changes
3. Verify all jobs complete successfully
4. Check artifacts are created correctly

### Dependency Updates

Regular maintenance tasks:
- Update Python version in workflows
- Update action versions (`@v4` → `@v5`)
- Update system dependencies
- Test PyInstaller spec files after updates

---

## Security Considerations

- Workflows use pinned action versions for security
- Artifacts are temporary and auto-expire
- No secrets or credentials are stored in workflow files
- Built executables should be scanned before distribution

---

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [PyInstaller Documentation](https://pyinstaller.org/)
- [Python Packaging Guide](https://packaging.python.org/)

---

## Support

For issues with workflows:
1. Check workflow logs in Actions tab
2. Review this documentation
3. Open an issue on GitHub with:
   - Workflow name
   - Run ID
   - Error messages
   - Steps to reproduce
