# Windows Compatibility Guide

## Overview
MTKClient now includes comprehensive Windows compatibility fixes to ensure reliable operation on Windows 10/11 systems.

## Fixed Issues

### Critical Bugs (v2.1.2+)

#### 1. Path Separator Issues ✅ FIXED
**Problem**: Hardcoded forward slashes `/` in paths caused failures on Windows
```python
# ❌ Before (BROKEN on Windows)
open('out/nvram.img', 'wb').write(data)

# ✅ After (Works on all platforms)
nvram_path = safe_path('out', 'nvram.img')
with safe_open(nvram_path, 'wb') as f:
    f.write(data)
```

**Impact**: 
- Windows: Creates `out\nvram.img` with backslash
- Linux/Mac: Creates `out/nvram.img` with forward slash
- Both work correctly

#### 2. Directory Creation ✅ FIXED
**Problem**: Directories like `out/` and `logs/` assumed to exist
```python
# ❌ Before (CRASH if directory missing)
os.path.mkdir('out')  # Fails if exists, doesn't create parents
open('logs/log.txt', 'w')  # Crashes if logs/ doesn't exist

# ✅ After (Always works)
ensure_directory_exists('out')  # Creates if needed, no error if exists
ensure_directory_exists('logs')
```

**Impact**: Fresh installs no longer crash with `FileNotFoundError`

#### 3. File Handle Leaks ✅ FIXED
**Problem**: Files opened without context managers, causing lock issues on Windows
```python
# ❌ Before (File handle leak, lock issues on Windows)
open("config.json", "r").read()
open("config.json", "w").write(json.dumps(data))

# ✅ After (Proper cleanup)
with safe_open("config.json", "r") as f:
    data = json.load(f)

with safe_open("config.json", "w") as f:
    json.dump(data, f)
```

**Impact**: 
- No more file lock errors preventing deletion/modification
- Proper resource cleanup
- Can now read/write files multiple times

#### 4. JSON Encoding Issues ✅ FIXED
**Problem**: No UTF-8 encoding specified, causing mojibake on some Windows systems
```python
# ❌ Before (May use wrong encoding on Windows)
with open("config.json", "r") as f:  # Uses system default encoding
    data = json.load(f)

# ✅ After (Always UTF-8)
with safe_open("config.json", "r") as f:  # Forces UTF-8
    data = json.load(f)
```

**Impact**: Consistent encoding across all platforms

## New Utility Functions

### `ensure_directory_exists(path)`
Creates a directory and all parent directories if they don't exist.

```python
from mtkclient.Library.utils import ensure_directory_exists

# Safe on all platforms
ensure_directory_exists('logs')
ensure_directory_exists('out/firmware')
ensure_directory_exists('C:\\Users\\Me\\mtk\\backups')  # Windows absolute path
```

### `safe_path(*parts)`
Joins path components using the correct separator for the platform.

```python
from mtkclient.Library.utils import safe_path

# Returns 'out\\nvram.img' on Windows, 'out/nvram.img' on Linux
path = safe_path('out', 'nvram.img')

# Works with multiple components
path = safe_path('logs', 'device', 'boot.log')
```

### `safe_open(filepath, mode, encoding=None)`
Opens files with proper encoding and auto-creates parent directories.

```python
from mtkclient.Library.utils import safe_open

# Auto-detects UTF-8 for text files
with safe_open('config.json', 'r') as f:
    data = json.load(f)

# Creates parent directory if needed
with safe_open('out/firmware/boot.img', 'wb') as f:
    f.write(data)

# Binary mode (no encoding)
with safe_open('bootloader.bin', 'rb') as f:
    data = f.read()
```

### `read_json_file(filepath)` & `write_json_file(filepath, data)`
Convenience functions for JSON with proper UTF-8 handling.

```python
from mtkclient.Library.utils import read_json_file, write_json_file

# Read JSON
config = read_json_file('config.json')

# Write JSON with pretty formatting
write_json_file('config.json', config, indent=2)
```

## Testing on Windows

### Prerequisites
- Windows 10/11 (64-bit)
- Python 3.8+
- All requirements installed: `pip install -r requirements.txt`

### Quick Test
```cmd
# Test directory creation
python -c "from mtkclient.Library.utils import ensure_directory_exists; ensure_directory_exists('test_dir'); print('OK')"

# Test path handling
python -c "from mtkclient.Library.utils import safe_path; print(safe_path('out', 'test.img'))"

# Test file operations
python -c "from mtkclient.Library.utils import safe_open, ensure_directory_exists; ensure_directory_exists('test'); f = safe_open('test/file.txt', 'w'); f.write('test'); f.close(); print('OK')"
```

### Expected Output
```
OK
out\test.img
OK
```

## Common Windows Issues

### Issue: "FileNotFoundError: [Errno 2] No such file or directory: 'logs\\log.txt'"
**Cause**: Logs directory doesn't exist
**Solution**: ✅ FIXED in v2.1.2 - automatically creates `logs/` directory

### Issue: "PermissionError: [WinError 32] The process cannot access the file..."
**Cause**: File handle not closed, file still locked
**Solution**: ✅ FIXED in v2.1.2 - uses context managers (`with` statements)

### Issue: Unicode/encoding errors in JSON files
**Cause**: System default encoding (cp1252) used instead of UTF-8
**Solution**: ✅ FIXED in v2.1.2 - forces UTF-8 encoding for all text files

### Issue: Paths with spaces not working
**Cause**: Improper path quoting
**Solution**: Use `safe_path()` which handles spaces correctly

```python
# ✅ Correct
path = safe_path('C:', 'Users', 'My Name', 'Documents', 'mtk')

# ❌ Incorrect
path = 'C:/Users/My Name/Documents/mtk'  # May fail on Windows
```

## Compatibility Notes

### Line Endings
Python automatically handles `\r\n` (Windows) vs `\n` (Unix) line endings in text mode.

### Path Separators
- Windows: Backslash `\`
- Linux/Mac: Forward slash `/`
- Solution: Always use `os.path.join()` or `safe_path()`

### File Permissions
Windows file permissions differ from Unix. The code handles this automatically.

### Case Sensitivity
- Windows: Case-insensitive filesystem
- Linux: Case-sensitive filesystem
- Best practice: Always use consistent case in filenames

## Migration Guide

### If You're Using Old Code

**Replace hardcoded paths:**
```python
# Old
open('out/file.img', 'wb')

# New
from mtkclient.Library.utils import safe_path, safe_open
with safe_open(safe_path('out', 'file.img'), 'wb') as f:
    f.write(data)
```

**Replace manual directory creation:**
```python
# Old
if not os.path.exists('logs'):
    os.mkdir('logs')

# New
from mtkclient.Library.utils import ensure_directory_exists
ensure_directory_exists('logs')
```

**Replace JSON operations:**
```python
# Old
config = json.loads(open("config.json", "r").read())

# New
from mtkclient.Library.utils import read_json_file
config = read_json_file("config.json")
```

## Future Enhancements

### Planned Improvements
- [ ] Fix remaining file handle leaks in DA modules
- [ ] Add Windows-specific tests
- [ ] Improve error messages for Windows users
- [ ] Add Windows installer
- [ ] Better COM port detection on Windows

### Known Limitations
- Some advanced features may require administrator privileges on Windows
- USB drivers must be installed separately (see README-WINDOWS.md)
- Serial port detection requires proper driver installation

## Troubleshooting

### Enable Debug Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Platform
```python
import sys
print(f"Platform: {sys.platform}")
print(f"Is Windows: {sys.platform.startswith('win')}")
```

### Test File Operations
```python
from mtkclient.Library.utils import (
    ensure_directory_exists,
    safe_path,
    safe_open
)

# Test directory creation
ensure_directory_exists('test_output')
print("✓ Directory created")

# Test file writing
with safe_open(safe_path('test_output', 'test.txt'), 'w') as f:
    f.write("Test successful")
print("✓ File written")

# Test file reading
with safe_open(safe_path('test_output', 'test.txt'), 'r') as f:
    content = f.read()
print(f"✓ File read: {content}")
```

## Support

For Windows-specific issues:
1. Check this guide first
2. Verify Python 3.8+ is installed
3. Ensure all dependencies are installed
4. Check antivirus isn't blocking file operations
5. Run Python as administrator if needed
6. Report issues with full error trace

## Related Documentation
- `README-WINDOWS.md` - Windows installation guide
- `README-INSTALL.md` - General installation
- `docs/ADVANCED_SETTINGS.md` - GUI configuration
