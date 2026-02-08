# Advanced Settings Dialog - Visual Guide

## Dialog Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│ Advanced Settings                                          [_][□][X] │
├─────────────────────────────────────────────────────────────────────┤
│ ┌───────────────────────────────────────────────────────────────┐   │
│ │ [Connection] [Authentication] [Exploit] [GPT/Partition] [Debug]│   │
│ └───────────────────────────────────────────────────────────────┘   │
│                                                                       │
│ ┌─ Connection Settings ─────────────────────────────────────────┐   │
│ │  VID:              [0x0e8d                    ]                │   │
│ │  PID:              [0x2000                    ]                │   │
│ │  Serial Port:      [Auto-detect               ]                │   │
│ │  [ ] No reconnect                                              │   │
│ │  [ ] Use stock DA                                              │   │
│ └────────────────────────────────────────────────────────────────┘   │
│                                                                       │
│ ┌─ Logging ─────────────────────────────────────────────────────┐   │
│ │  UART Log Level:   [2 - Normal          ▼]                     │   │
│ │  Log Level:        [2 - Normal          ▼]                     │   │
│ └────────────────────────────────────────────────────────────────┘   │
│                                                                       │
│ ┌─ Options ─────────────────────────────────────────────────────┐   │
│ │  [ ] Dump preloader to file                                    │   │
│ │  [ ] Derive hardware keys                                      │   │
│ │  [ ] IoT mode (MT6261/2301)                                    │   │
│ │  [ ] Read SoC ID                                               │   │
│ └────────────────────────────────────────────────────────────────┘   │
│                                                                       │
│                                           [Restore Defaults] [OK] [Cancel]│
└─────────────────────────────────────────────────────────────────────┘
```

## Tab 1: Connection
- **Purpose**: Configure USB/Serial connection and logging
- **Fields**: 
  - VID/PID: Hex input fields with placeholders
  - Serial Port: Text input for manual port entry
  - Checkboxes: No reconnect, Use stock DA
  - Dropdowns: UART Log Level (4 options), Log Level (4 options)
  - Additional checkboxes: Dump preloader, Derive keys, IoT mode, Read SoC ID

## Tab 2: Authentication

```
┌─ Authentication Files ────────────────────────────────────────────┐
│  Auth File:  [                              ] [Browse...]         │
│  Cert File:  [                              ] [Browse...]         │
└────────────────────────────────────────────────────────────────────┘

Note: Authentication files are required only for devices with
secure boot enabled. Leave empty for most devices.
```

- **Purpose**: Configure authentication for secure devices
- **Fields**:
  - Auth File: Text input + Browse button (filters: *.auth)
  - Cert File: Text input + Browse button (filters: *.pem, *.cert)
- **Info**: Helpful note about when these are needed

## Tab 3: Exploit

```
┌─ Exploit Type ────────────────────────────────────────────────────┐
│  Payload Type:  [kamakiri2            ▼]                          │
└────────────────────────────────────────────────────────────────────┘

┌─ Loader Files ────────────────────────────────────────────────────┐
│  DA Loader:   [Auto-detect             ] [Browse...]              │
│  Preloader:   [Auto-detect             ] [Browse...]              │
└────────────────────────────────────────────────────────────────────┘

┌─ Advanced Exploit Settings ───────────────────────────────────────┐
│  Var1:          [0xA (auto)            ]                          │
│  UART Address:  [Auto-detect           ]                          │
│  DA Address:    [Auto-detect           ]                          │
│  BROM Address:  [Auto-detect           ]                          │
│  Watchdog Addr: [Auto-detect           ]                          │
│  Crash Mode:    [Auto                  ▼]                         │
│  App ID:        [Optional              ]                          │
└────────────────────────────────────────────────────────────────────┘

[ ] Skip watchdog init
[ ] Enforce crash in preloader mode
```

- **Purpose**: Configure bootrom/preloader exploit settings
- **Dropdowns**: 
  - Payload Type: kamakiri, kamakiri2, amonet, carbonara
  - Crash Mode: Auto, 0-dasend1, 1-dasend2, 2-daread
- **File Browsers**: DA Loader, Preloader (*.bin files)
- **Hex Inputs**: var1, addresses (all with auto-detect option)
- **Checkboxes**: Skip WDT, Enforce crash

## Tab 4: GPT/Partition

```
┌─ GPT Settings ────────────────────────────────────────────────────┐
│  Sector Size:        [0x200                ]                      │
│  Partition Entries:  [0     ▲▼]                                   │
│  Entry Size:         [0     ▲▼]                                   │
│  Start LBA:          [0     ▲▼]                                   │
└────────────────────────────────────────────────────────────────────┘

┌─ Partition Options ───────────────────────────────────────────────┐
│  Partition Type:   [user                ▼]                        │
│  Skip Partitions:  [e.g., boot,recovery  ]                        │
└────────────────────────────────────────────────────────────────────┘
```

- **Purpose**: Configure GPT and partition access settings
- **Fields**:
  - Sector Size: Hex input (default 0x200)
  - Spinboxes: Partition Entries, Entry Size, Start LBA (0-256, 0-1000000)
  - Dropdown: Partition Type (user, boot1, boot2, rpmb, gp1-4)
  - Text input: Skip Partitions (comma-separated list)

## Tab 5: Debug

```
┌─ Debug Options ───────────────────────────────────────────────────┐
│  [✓] Enable debug mode                                            │
└────────────────────────────────────────────────────────────────────┘

Debug Mode: Enables detailed logging for troubleshooting.
This will generate more verbose output in the log window.

Tip: Enable this if you're experiencing connection issues or
need to report a bug.
```

- **Purpose**: Enable verbose debug output
- **Fields**: Single checkbox for debug mode
- **Info**: Helpful text explaining when to use debug mode

## Common UI Elements

### All Tabs Have:
1. **Tooltips**: Hover over any field to see helpful description
2. **Placeholders**: Gray text showing example values or "Auto-detect"
3. **Tab Icons**: Visual indicators for each tab category

### Bottom Buttons:
- **Restore Defaults**: Resets all settings to default values
- **OK**: Saves settings to config and closes dialog
- **Cancel**: Discards changes and closes dialog

### Keyboard Shortcuts:
- **Ctrl+,**: Open dialog (from main window)
- **Enter**: Accept/OK
- **Escape**: Cancel

## Visual Indicators

### Field States:
- **Empty fields**: Use auto-detection or defaults
- **Filled fields**: Override defaults with custom values
- **Hex values**: Support both `0x1234` and `1234` formats
- **Invalid input**: Silently ignored (existing config preserved)

### Validation:
- Hex fields: Accept 0-9, a-f, A-F
- Spinboxes: Enforce min/max ranges
- Dropdowns: Only allow valid selections
- File browsers: Filter by file extension

## Integration with Main Window

```
┌─ MTKClient GUI ───────────────────────────────────────────────────┐
│ File  Tools  Help                                                  │
│ ├─ Advanced Settings...  Ctrl+,  <──── Opens this dialog          │
│ ├─ ───────────────────                                            │
│ └─ Quit                                                            │
└────────────────────────────────────────────────────────────────────┘
```

## Workflow Example

### Scenario: Configure custom DA loader and debug mode

1. **Open Dialog**: File → Advanced Settings (Ctrl+,)
2. **Go to Exploit Tab**: Click "Exploit" tab
3. **Select DA Loader**: 
   - Click "Browse..." next to "DA Loader"
   - Navigate to custom DA file
   - Select file (e.g., `custom_da.bin`)
4. **Go to Debug Tab**: Click "Debug" tab
5. **Enable Debug**: Check "Enable debug mode"
6. **Apply**: Click "OK" button
7. **Verify**: See "Settings updated successfully" in main window log

### Scenario: Fix connection issues

1. **Open Dialog**: Ctrl+,
2. **Connection Tab**: Already selected
3. **Set VID/PID**: 
   - VID: `0x0e8d` (MediaTek)
   - PID: `0x2000` (Preloader mode)
4. **Set Log Level**: Change to "0 - Trace" for both
5. **Enable Debug**: Switch to Debug tab, check debug mode
6. **Apply**: Click OK
7. **Reconnect**: Device should now show detailed logs

## File Browser Filters

Each file browser has appropriate filters:

| Field | Extensions | Example |
|-------|-----------|---------|
| Auth File | `*.auth` | `auth_sv5.auth` |
| Cert File | `*.pem`, `*.cert` | `device.pem` |
| DA Loader | `*.bin` | `MTKAllInOneDA.bin` |
| Preloader | `*.bin` | `preloader_k62v1_64_bsp.bin` |

All browsers include "All Files (*)" as fallback option.
