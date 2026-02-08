# Advanced Settings Dialog - Implementation Documentation

## Overview
Comprehensive settings dialog that exposes all mtk.py CLI arguments in a user-friendly GUI interface with proper validation and organization.

## Features

### 1. Organized Tab Structure
Settings are organized into 5 logical tabs matching the CLI argument groups:

#### Connection Tab
- **VID/PID**: USB Vendor/Product ID (auto-detect when empty)
- **Serial Port**: Manual port selection (auto-detected by default)
- **Reconnect**: Control automatic reconnection
- **Stock DA**: Use stock Download Agent
- **Logging Levels**: UART and general log levels (0=Trace, 2=Normal)
- **Options**: Dump preloader, derive keys, IoT mode, read SoC ID

#### Authentication Tab
- **Auth File**: Authentication file for secure devices (*.auth)
- **Cert File**: Certificate file for secure boot (*.pem, *.cert)
- **File Browsers**: Easy file selection with filters

#### Exploit Tab
- **Payload Type**: Dropdown with kamakiri, kamakiri2, amonet, carbonara
- **DA Loader**: Custom DA loader file selection
- **Preloader**: Preloader file for DRAM config
- **Advanced Settings**:
  - var1: Kamakiri variable (hex)
  - UART/DA/BROM addresses (hex)
  - Watchdog address (hex)
  - Crash mode (0-2)
  - App ID (hex string)
- **Options**: Skip WDT, enforce crash

#### GPT/Partition Tab
- **Sector Size**: Default 0x200 (512 bytes)
- **GPT Entries**: Number of partition entries
- **Entry Size**: GPT entry size
- **Start LBA**: Starting LBA sector
- **Partition Type**: Dropdown with user/boot1/boot2/rpmb/gp1-4
- **Skip Partitions**: Comma-separated list to skip

#### Debug Tab
- **Debug Mode**: Enable verbose logging
- **Informational Text**: Usage tips

### 2. Smart Input Validation
- Hex values auto-detected (0x prefix)
- Dropdown menus for known values
- Spinboxes with range limits for numeric values
- File browsers with appropriate filters
- Tooltips on all fields explaining their purpose

### 3. Configuration Management
- **Load Settings**: Automatically loads current config on dialog open
- **Save Settings**: Applies changes to MtkConfig object
- **Restore Defaults**: Reset all settings to defaults
- **OK/Cancel**: Standard dialog buttons

### 4. Integration
- Accessible via File → Advanced Settings... (Ctrl+,)
- Seamlessly integrates with existing GUI
- Updates config object in real-time
- Maintains backward compatibility

## Technical Details

### File Structure
```
mtkclient/gui/settings_dialog.py    - Settings dialog implementation
mtk_gui.py                           - Main GUI integration
```

### Key Classes
- `SettingsDialog`: Main dialog class
  - `create_connection_tab()`: Connection settings
  - `create_auth_tab()`: Authentication files
  - `create_exploit_tab()`: Exploit configuration
  - `create_gpt_tab()`: GPT/Partition settings
  - `create_debug_tab()`: Debug options
  - `load_settings()`: Load from MtkConfig
  - `save_settings()`: Save to MtkConfig
  - `restore_defaults()`: Reset all values

### Integration Points
```python
# In MainWindow.__init__():
self.add_settings_menu()  # Adds menu item

# New method:
def openAdvancedSettings(self):
    dialog = SettingsDialog(self.devhandler.da_handler.mtk.config, self)
    if dialog.exec() == QDialog.DialogCode.Accepted:
        self.sendToLog("Settings updated successfully")
```

## Usage

### For Users
1. Open MTKClient GUI
2. Click File → Advanced Settings... (or press Ctrl+,)
3. Configure desired options across tabs
4. Click OK to apply or Cancel to discard
5. Use "Restore Defaults" to reset all settings

### For Developers
```python
from mtkclient.gui.settings_dialog import SettingsDialog
from mtkclient.config.mtk_config import MtkConfig

# Create config
config = MtkConfig()

# Show dialog
dialog = SettingsDialog(config, parent_widget)
if dialog.exec() == QDialog.DialogCode.Accepted:
    # Settings were saved to config object
    print(f"Payload type: {config.ptype}")
    print(f"Debug mode: {config.debugmode}")
```

## CLI Argument Mapping

All CLI arguments from mtk.py are now accessible in GUI:

| CLI Argument | GUI Location | Widget Type |
|--------------|--------------|-------------|
| --vid | Connection → VID | Line Edit (hex) |
| --pid | Connection → PID | Line Edit (hex) |
| --serialport | Connection → Serial Port | Line Edit |
| --noreconnect | Connection → No reconnect | Checkbox |
| --stock | Connection → Use stock DA | Checkbox |
| --uartloglevel | Connection → UART Log Level | ComboBox |
| --loglevel | Connection → Log Level | ComboBox |
| --write_preloader_to_file | Connection → Dump preloader | Checkbox |
| --generatekeys | Connection → Derive keys | Checkbox |
| --iot | Connection → IoT mode | Checkbox |
| --socid | Connection → Read SoC ID | Checkbox |
| --auth | Authentication → Auth File | Line Edit + Browser |
| --cert | Authentication → Cert File | Line Edit + Browser |
| --ptype | Exploit → Payload Type | ComboBox |
| --loader | Exploit → DA Loader | Line Edit + Browser |
| --preloader | Exploit → Preloader | Line Edit + Browser |
| --var1 | Exploit → Var1 | Line Edit (hex) |
| --uart_addr | Exploit → UART Address | Line Edit (hex) |
| --da_addr | Exploit → DA Address | Line Edit (hex) |
| --brom_addr | Exploit → BROM Address | Line Edit (hex) |
| --wdt | Exploit → Watchdog Addr | Line Edit (hex) |
| --mode | Exploit → Crash Mode | ComboBox |
| --appid | Exploit → App ID | Line Edit (hex) |
| --skipwdt | Exploit → Skip WDT | Checkbox |
| --crash | Exploit → Enforce crash | Checkbox |
| --sectorsize | GPT → Sector Size | Line Edit (hex) |
| --gpt-num-part-entries | GPT → Partition Entries | SpinBox |
| --gpt-part-entry-size | GPT → Entry Size | SpinBox |
| --gpt-part-entry-start-lba | GPT → Start LBA | SpinBox |
| --parttype | GPT → Partition Type | ComboBox |
| --skip | GPT → Skip Partitions | Line Edit |
| --debugmode | Debug → Enable debug mode | Checkbox |

## Benefits

### For Users
- **Easier Configuration**: No need to remember CLI arguments
- **Visual Validation**: Dropdowns show valid options
- **Better Organization**: Logical grouping of related settings
- **Tooltips**: Inline help for each setting
- **File Browsers**: Easy file selection

### For Developers
- **Centralized Settings**: All config in one place
- **Maintainable**: Easy to add new settings
- **Type Safe**: Proper validation and parsing
- **Extensible**: Tab structure allows easy expansion

## Future Enhancements
- Configuration profiles (save/load presets)
- Per-device settings memory
- Advanced validation (e.g., address range checking)
- Import settings from CLI command line
- Export current settings as CLI command

## Testing

### Manual Testing
1. Launch GUI: `python mtk_gui.py`
2. Open Advanced Settings
3. Test each tab:
   - Verify dropdowns show correct values
   - Test file browsers open with correct filters
   - Enter hex values and verify parsing
   - Click Restore Defaults and verify reset
4. Apply settings and verify in logs
5. Test keyboard shortcut (Ctrl+,)

### Automated Testing
```bash
# Syntax check
python3 -m py_compile mtkclient/gui/settings_dialog.py

# Import test
python3 -c "from mtkclient.gui.settings_dialog import SettingsDialog; print('OK')"
```

## Known Limitations
- Some advanced exploit parameters (uart_addr, da_addr, etc.) require chipconfig object
- App ID field accepts any hex string (no validation of format)
- Mode combo shows descriptive text, index is used for config
- Serial port input doesn't auto-refresh (use Serial Port button instead)

## Troubleshooting

### Settings Not Persisting

**Symptoms**: Changes made in the Advanced Settings dialog don't take effect.

**Root Causes & Solutions**:

1. **Config object not passed correctly**
   - **Check**: Dialog receives config via `SettingsDialog(config, parent)`
   - **Verify**: In `mtk_gui.py`, dialog is created with `self.devhandler.da_handler.mtk.config`
   - **Fix**: Ensure you pass the actual config instance, not a copy
   ```python
   # Correct:
   dialog = SettingsDialog(self.devhandler.da_handler.mtk.config, self)
   
   # Wrong:
   dialog = SettingsDialog(MtkConfig(), self)  # Creates new config!
   ```

2. **Dialog cancelled instead of accepted**
   - **Check**: User must click "OK" button (not "Cancel" or close X)
   - **Verify**: `dialog.exec() == QDialog.DialogCode.Accepted` returns True
   - **Implementation**: `accept()` method calls `save_settings()` before closing
   ```python
   def accept(self):
       self.save_settings()  # This updates config in-place
       super().accept()
   ```

3. **Config not the same instance**
   - **Check**: Dialog stores reference in `self.config = config`
   - **Verify**: All modifications update this reference in-place
   - **Note**: Config object is passed by reference, not copied

### File Browsers Not Working

**Symptoms**: File browser doesn't open, shows wrong files, or can't select files.

**Root Causes & Solutions**:

1. **QFileDialog not imported**
   - **Check**: Line 9 in settings_dialog.py imports QFileDialog
   ```python
   from PySide6.QtWidgets import (
       QDialog, ..., QFileDialog, ...
   )
   ```
   - **Verify**: No ImportError when loading module

2. **File filters incorrect format**
   - **Correct format**: `"Description (*.ext);;All Files (*)"`
   - **Examples in code**:
     - Auth files: `"Auth Files (*.auth);;All Files (*)"`
     - Cert files: `"Certificate Files (*.pem *.cert);;All Files (*)"`
     - DA/Preloader: `"DA Files (*.bin);;All Files (*)"`
   - **Note**: Double semicolon `;;` separates filter groups

3. **File permissions**
   - **Check**: User has read access to target directory
   - **Try**: Browse from a different directory
   - **Linux**: Verify no SELinux/AppArmor restrictions

4. **Dialog returns but doesn't set value**
   - **Implementation**: Only sets value if filename is not empty
   ```python
   filename, _ = QFileDialog.getOpenFileName(...)
   if filename:  # Only set if user selected a file
       line_edit.setText(filename)
   ```

### Hex Values Not Parsing

**Symptoms**: Hex values entered in fields don't save correctly or cause errors.

**Root Causes & Solutions**:

1. **Missing 0x prefix**
   - **Supports both formats**: `0x1234` (hex) or `1234` (decimal)
   - **Implementation**:
   ```python
   value = int(text, 16) if text.startswith('0x') else int(text)
   ```
   - **Examples**:
     - VID: `0x0e8d` or `3725` (both work)
     - var1: `0xA` or `10` (both work)

2. **Invalid hex characters**
   - **Valid hex**: 0-9, a-f, A-F (case-insensitive)
   - **Invalid**: g-z, special characters, spaces
   - **Error handling**: ValueError caught, invalid input silently ignored
   ```python
   try:
       self.config.vid = int(vid_text, 16) if vid_text.startswith('0x') else int(vid_text)
   except ValueError:
       pass  # Keep existing config value
   ```

3. **Fields affected by hex parsing**:
   - Connection tab: VID, PID
   - Exploit tab: var1, UART address, DA address, BROM address, Watchdog address
   - GPT tab: Sector size
   - All handle ValueError exceptions gracefully

4. **Best practices**:
   - Use `0x` prefix for clarity when entering hex values
   - Test with placeholder values before applying
   - Check logs for any parsing errors (if debug mode enabled)
   - Invalid entries are silently ignored (config unchanged)

### Advanced Exploit Settings Not Saving

**Symptoms**: UART/DA/BROM addresses or mode/appid don't persist.

**Root Cause**: These fields require chipconfig object to be initialized.

**Solution**:
```python
# Check implementation in save_settings():
if hasattr(self.config, 'chipconfig') and self.config.chipconfig:
    if uart_text:
        self.config.chipconfig.uart = parsed_value
    # ... etc
```

- **Verify**: `config.chipconfig` is not None
- **When initialized**: After device connection established
- **Workaround**: Connect device first, then modify advanced settings

### Log Level Not Saving

**Fixed in v2.1.2**: Previously only UART log level was saved.

**Current implementation**:
```python
# Both levels now properly saved:
self.config.uartloglevel = self.uartloglevel_combo.currentIndex()
self.config.loglevel = self.loglevel_combo.currentIndex()
```

### Serial Port Not Saving

**Fixed in v2.1.2**: Serial port input now properly handled.

**Current implementation**:
```python
serialport_text = self.serialport_input.text().strip()
if serialport_text:
    if hasattr(self.config, 'serialportname'):
        self.config.serialportname = serialport_text
```

**Note**: Use the "Serial Port" button in main GUI for auto-detection with device filtering.

## Related Files
- `mtk.py`: CLI argument definitions
- `mtkclient/config/mtk_config.py`: Configuration object
- `mtk_gui.py`: Main GUI integration
- `docs/AUTO_PORT_DETECTION.md`: COM port auto-detection
