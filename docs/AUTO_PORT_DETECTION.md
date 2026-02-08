# Automatic COM Port Detection Feature

## Overview
The GUI now includes automatic MediaTek device detection and intelligent port selection to improve user experience, especially on Windows.

## Features

### 1. Automatic Port Detection
When opening the serial port dialog, the application will:
- **Auto-detect MediaTek devices** by VID (Vendor ID)
- **Automatically select** the first detected MediaTek device
- **Mark MediaTek devices** with a ⭐ symbol for easy identification
- **Skip the dialog** entirely if only one MediaTek device is connected

### 2. Supported Device VIDs
The following vendor IDs are automatically detected:
- `0x0E8D` - MediaTek Inc.
- `0x1004` - LG Electronics
- `0x22d9` - OPPO Electronics
- `0x0FCE` - Sony Ericsson

### 3. Improved Windows Support
- **Natural sorting** of COM ports (COM1, COM2, COM10 instead of COM1, COM10, COM2)
- Better handling of Windows-specific COM port names
- Improved port descriptions and manufacturer information

### 4. Enhanced Port Dialog
- Visual indication of MediaTek devices with ⭐ prefix
- Automatic selection of detected devices
- Refresh button to rescan ports
- Device information display (description, manufacturer)

## Usage

### Automatic Mode (Default)
When you click the "Select Port" button:
1. If exactly one MediaTek device is found → automatically selected (dialog skipped)
2. If multiple MediaTek devices are found → dialog opens with first one pre-selected
3. If no MediaTek devices are found → dialog opens with first available port selected

### Manual Selection
Users can still:
- Click "Refresh" to rescan ports
- Manually select any available serial port
- Cancel the selection

## Technical Details

### Auto-Detection Logic
```python
# MediaTek VID list
mtk_vids = [0x0E8D, 0x1004, 0x22d9, 0x0FCE]

# Automatic port detection
def detect_mtk_port():
    ports = serial.tools.list_ports.comports()
    mtk_ports = [p for p in ports if p.vid in mtk_vids]
    if len(mtk_ports) == 1:
        return mtk_ports[0].device
    return ""
```

### Natural Sorting
COM ports are now sorted naturally:
- Before: COM1, COM10, COM11, COM2, COM20, COM3
- After: COM1, COM2, COM3, COM10, COM11, COM20

## Benefits

### For Users
- **Faster workflow**: No need to manually select port when only one device is connected
- **Fewer errors**: Automatic selection reduces chance of selecting wrong port
- **Better UX**: Clear indication of MediaTek devices
- **Windows-friendly**: Proper COM port sorting

### For Developers
- Extensible VID list for supporting more devices
- Maintains backward compatibility
- Clean, maintainable code

## Future Enhancements
- Option to disable auto-detection in settings
- Remember last used port
- Port availability monitoring
- Multi-device connection support
