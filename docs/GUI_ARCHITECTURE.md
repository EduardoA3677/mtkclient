# MTKClient GUI Architecture

## Complete System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         MTKClient GUI                            │
│                         (mtk_gui.py)                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────┐         ┌──────────────────────────┐   │
│  │   Main Window      │         │  Advanced Settings       │   │
│  │                    │         │  Dialog (NEW!)           │   │
│  │  ┌──────────────┐  │         │                          │   │
│  │  │ Menu Bar     │  │         │  ┌────────────────────┐  │   │
│  │  ├──────────────┤  │         │  │ Tab 1: Connection  │  │   │
│  │  │ File         │◄─┼─────────┼──┤ - VID/PID         │  │   │
│  │  │ ├─ Settings...│ │         │  │ - Serial Port     │  │   │
│  │  │ └─ Quit      │  │         │  │ - Logging         │  │   │
│  │  └──────────────┘  │         │  │ - Options         │  │   │
│  │                    │         │  └────────────────────┘  │   │
│  │  ┌──────────────┐  │         │                          │   │
│  │  │ Device Info  │  │         │  ┌────────────────────┐  │   │
│  │  │ - Chipset    │  │         │  │ Tab 2: Auth        │  │   │
│  │  │ - Boot Mode  │  │         │  │ - Auth File       │  │   │
│  │  └──────────────┘  │         │  │ - Cert File       │  │   │
│  │                    │         │  └────────────────────┘  │   │
│  │  ┌──────────────┐  │         │                          │   │
│  │  │ Quick Config │  │         │  ┌────────────────────┐  │   │
│  │  │ - IoT ☐      │  │         │  │ Tab 3: Exploit     │  │   │
│  │  │ - DA Loader  │  │         │  │ - Payload Type    │  │   │
│  │  │ - Preloader  │  │         │  │ - Loader Files    │  │   │
│  │  │ - Serial Port│  │         │  │ - Advanced Addrs  │  │   │
│  │  └──────────────┘  │         │  └────────────────────┘  │   │
│  │                    │         │                          │   │
│  │  ┌──────────────┐  │         │  ┌────────────────────┐  │   │
│  │  │ Operations   │  │         │  │ Tab 4: GPT         │  │   │
│  │  │ - Read       │  │         │  │ - Sector Size     │  │   │
│  │  │ - Write      │  │         │  │ - Partition Type  │  │   │
│  │  │ - Erase      │  │         │  └────────────────────┘  │   │
│  │  └──────────────┘  │         │                          │   │
│  │                    │         │  ┌────────────────────┐  │   │
│  └────────────────────┘         │  │ Tab 5: Debug       │  │   │
│                                  │  │ - Debug Mode ☐    │  │   │
│                                  │  └────────────────────┘  │   │
│                                  │                          │   │
│                                  │  [OK] [Cancel] [Defaults]│   │
│                                  └──────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Configuration Layer                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    MtkConfig Object                       │  │
│  │                                                            │  │
│  │  Connection:  vid, pid, serialport, reconnect, stock...  │  │
│  │  Auth:        auth, cert                                 │  │
│  │  Exploit:     ptype, loader, preloader, var1, addrs...   │  │
│  │  GPT:         sectorsize, parttype, entries...           │  │
│  │  Debug:       debugmode                                  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Device Layer                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────┐      ┌──────────────────┐                 │
│  │ USB Connection  │      │  Serial Port     │                 │
│  │                 │      │                  │                 │
│  │ - Auto-detect ⭐│◄────►│ - Auto-detect ⭐ │                 │
│  │ - VID:PID scan  │      │ - Natural sort   │                 │
│  │ - Interface cfg │      │ - MTK filter     │                 │
│  └─────────────────┘      └──────────────────┘                 │
│           │                         │                           │
│           └─────────────┬───────────┘                           │
│                         ▼                                       │
│           ┌──────────────────────────┐                          │
│           │   Device Handler         │                          │
│           │                          │                          │
│           │  - BROM Mode             │                          │
│           │  - Preloader Mode        │                          │
│           │  - DA Mode               │                          │
│           │  - Exploit Selection     │                          │
│           └──────────────────────────┘                          │
│                         │                                       │
│                         ▼                                       │
│           ┌──────────────────────────┐                          │
│           │   MediaTek Device        │                          │
│           │                          │                          │
│           │  Read/Write/Erase        │                          │
│           └──────────────────────────┘                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

### Settings Configuration Flow
```
User opens Advanced Settings
         │
         ▼
Settings Dialog loads from MtkConfig
         │
         ├─► Tab 1: Connection settings
         ├─► Tab 2: Auth files  
         ├─► Tab 3: Exploit parameters
         ├─► Tab 4: GPT settings
         └─► Tab 5: Debug options
         │
User makes changes
         │
         ▼
Click [OK] → save_settings()
         │
         ▼
Update MtkConfig object
         │
         ▼
Settings applied to device operations
```

### Device Connection Flow
```
App Start
    │
    ▼
Auto-detect COM ports
    │
    ├─► MediaTek VIDs: 0x0E8D, 0x1004, 0x22d9, 0x0FCE
    │   └─► Mark with ⭐
    │
    ├─► Single MTK device? → Auto-select
    └─► Multiple devices? → Show dialog with first selected
    │
    ▼
Apply MtkConfig settings
    │
    ├─► VID/PID if specified
    ├─► Exploit type (ptype)
    ├─► Loader files
    └─► Connection options
    │
    ▼
Connect to device
    │
    ├─► BROM mode detection
    ├─► Preloader mode detection  
    └─► DA mode initialization
    │
    ▼
Ready for operations
```

## Component Interaction

### Settings Dialog → Config → Device
```
SettingsDialog
    ├─ Connection Tab
    │   └─► config.vid, config.pid, config.serialport
    │       config.reconnect, config.stock, config.uartloglevel
    │
    ├─ Auth Tab
    │   └─► config.auth, config.cert
    │
    ├─ Exploit Tab
    │   └─► config.ptype, config.loader, config.preloader
    │       config.var1, config.skipwdt, config.enforcecrash
    │       config.chipconfig.uart, config.chipconfig.watchdog
    │
    ├─ GPT Tab
    │   └─► config.gpt_settings.gpt_num_part_entries
    │       config.gpt_settings.gpt_part_entry_size
    │
    └─ Debug Tab
        └─► config.debugmode
```

## File Organization

```
mtkclient/
├── mtk_gui.py                           Main GUI application
│   ├── MainWindow class
│   ├── SerialPortDialog class          Auto-detection dialog
│   ├── DeviceHandler class             Device operations
│   └── getDevInfo()                    Device initialization
│
├── mtkclient/gui/
│   ├── settings_dialog.py (NEW!)       Advanced Settings Dialog
│   │   ├── SettingsDialog class
│   │   ├── create_connection_tab()
│   │   ├── create_auth_tab()
│   │   ├── create_exploit_tab()
│   │   ├── create_gpt_tab()
│   │   ├── create_debug_tab()
│   │   ├── load_settings()
│   │   └── save_settings()
│   │
│   ├── main_gui.py                     Generated UI file
│   ├── readFlashPartitions.py          Read operations
│   ├── writeFlashPartitions.py         Write operations
│   └── eraseFlashPartitions.py         Erase operations
│
├── mtkclient/config/
│   ├── mtk_config.py                   MtkConfig class
│   ├── brom_config.py                  Chipconfig definitions
│   └── usb_ids.py                      VID/PID mappings
│
└── mtkclient/Library/
    ├── Connection/                      USB/Serial handlers
    ├── DA/                              DA mode handlers
    └── Exploit/                         Exploit implementations
```

## Key Classes

### SettingsDialog
```python
class SettingsDialog(QDialog):
    """
    Comprehensive settings interface
    
    Attributes:
        config: MtkConfig object reference
        tabs: QTabWidget with 5 tabs
        
    Methods:
        create_*_tab(): Create individual tabs
        load_settings(): Load from config
        save_settings(): Save to config  
        restore_defaults(): Reset all
        browse_file(): File selection helper
    """
```

### SerialPortDialog
```python
class SerialPortDialog(QDialog):
    """
    Auto-detecting COM port selector
    
    Methods:
        detect_mtk_port(): Auto-detect single MTK device
        get_serial_port(): Show dialog or auto-select
        refresh_ports(): Scan and display ports
        
    Features:
        - MediaTek VID filtering
        - Natural sorting
        - Visual indicators (⭐)
        - Auto-selection
    """
```

### MainWindow
```python
class MainWindow(QMainWindow):
    """
    Main application window
    
    Methods:
        openAdvancedSettings(): Open settings dialog
        add_settings_menu(): Add menu item
        openserialportdialog(): Open port selector
        selectDaLoader(): Browse DA file
        selectPreloader(): Browse preloader file
        
    Integration:
        - Settings dialog
        - Port auto-detection
        - Device operations
    """
```

## Configuration Hierarchy

```
MtkConfig (Root)
├── Connection
│   ├── vid, pid              (int)
│   ├── serialportname        (str)
│   ├── reconnect             (bool)
│   ├── stock                 (bool)
│   ├── uartloglevel          (int 0-3)
│   ├── loglevel              (int)
│   ├── write_preloader_to_file (bool)
│   ├── generatekeys          (bool)
│   ├── iot                   (bool)
│   └── readsocid             (bool)
│
├── Authentication
│   ├── auth                  (str - file path)
│   └── cert                  (str - file path)
│
├── Exploit
│   ├── ptype                 (str - payload type)
│   ├── loader                (str - file path)
│   ├── preloader             (bytes)
│   ├── preloader_filename    (str)
│   ├── var1                  (int - hex)
│   ├── skipwdt               (bool)
│   ├── enforcecrash          (bool)
│   └── chipconfig
│       ├── uart              (int - hex addr)
│       ├── watchdog          (int - hex addr)
│       ├── da_payload_addr   (int - hex addr)
│       └── brom_payload_addr (int - hex addr)
│
├── GPT Settings
│   ├── gpt_settings
│   │   ├── gpt_num_part_entries (str)
│   │   ├── gpt_part_entry_size  (str)
│   │   └── gpt_part_entry_start_lba (str)
│   └── SECTOR_SIZE_IN_BYTES  (int)
│
└── Debug
    └── debugmode             (bool)
```

## Feature Matrix

| Feature | Status | Location | Notes |
|---------|--------|----------|-------|
| Auto COM Port Detection | ✅ | mtk_gui.py | VID-based, natural sort |
| Advanced Settings Dialog | ✅ | gui/settings_dialog.py | All CLI args |
| Connection Settings | ✅ | Settings Tab 1 | VID/PID/port/logging |
| Authentication Files | ✅ | Settings Tab 2 | Auth/cert browsers |
| Exploit Configuration | ✅ | Settings Tab 3 | ptype/loader/addrs |
| GPT Configuration | ✅ | Settings Tab 4 | Sector/partition |
| Debug Mode | ✅ | Settings Tab 5 | Verbose logging |
| File Browsers | ✅ | All tabs | Filtered dialogs |
| Input Validation | ✅ | All inputs | Hex/dropdown/spin |
| Tooltips | ✅ | All fields | Inline help |
| Restore Defaults | ✅ | Dialog button | Reset all |
| Keyboard Shortcut | ✅ | Ctrl+, | Quick access |
| Config Persistence | ✅ | Load/Save | MtkConfig sync |

## Integration Points

### 1. Menu System
```
File Menu (ui.menuFile)
    │
    ├─ actionAdvancedSettings ← NEW!
    │   └─ Triggered → openAdvancedSettings()
    │
    └─ action_Quit
```

### 2. Config Object
```
MainWindow
    └─ devhandler (DeviceHandler)
        └─ da_handler (DaHandler)
            └─ mtk (Mtk)
                └─ config (MtkConfig) ← Settings modify this
```

### 3. Auto-Detection
```
openserialportdialog()
    └─ SerialPortDialog.get_serial_port()
        ├─ detect_mtk_port() → Auto if 1 device
        └─ Dialog if multiple or manual
```

## Future Architecture Extensions

### Planned Enhancements
```
┌─────────────────────────────┐
│  Configuration Profiles     │
│  (Save/Load Presets)        │
└─────────────────────────────┘
              │
              ▼
┌─────────────────────────────┐
│  Per-Device Memory          │
│  (Remember device settings) │
└─────────────────────────────┘
              │
              ▼
┌─────────────────────────────┐
│  CLI Import/Export          │
│  (Convert CLI ↔ GUI)        │
└─────────────────────────────┘
```

## Benefits of Architecture

### Modularity
- ✅ Settings isolated in separate dialog
- ✅ Config object centralized
- ✅ Clear separation of concerns

### Maintainability
- ✅ Easy to add new settings
- ✅ Tab structure organizes complexity
- ✅ Type-safe validation

### Extensibility
- ✅ New tabs can be added
- ✅ Additional validation easy
- ✅ Profiles system ready

### User Experience
- ✅ Consistent interface
- ✅ Logical grouping
- ✅ Progressive disclosure
- ✅ Inline help everywhere
