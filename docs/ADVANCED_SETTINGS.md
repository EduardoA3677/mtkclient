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
- Check that config object is properly passed to dialog
- Verify accept() is called (OK button clicked)
- Ensure config object is the same instance used by device handler

### File Browsers Not Working
- Check file filters in browse_file() calls
- Verify QFileDialog is properly imported
- Check file permissions

### Hex Values Not Parsing
- Ensure 0x prefix for hex values
- Check int() conversion in save_settings()
- Add proper error handling for ValueError

## Related Files
- `mtk.py`: CLI argument definitions
- `mtkclient/config/mtk_config.py`: Configuration object
- `mtk_gui.py`: Main GUI integration
- `docs/AUTO_PORT_DETECTION.md`: COM port auto-detection
