# MT6768 Crash Exploit Troubleshooting Guide

## Issue: Crash Loop After First Crash

### Symptoms

```
Port - Device detected :)
Preloader - CPU: MT6768/MT6769(Helio P65/G85 k68v1)
...
Mtk - We're not in bootrom, trying to crash da...
Exploitation - Crashing da...
[Device disconnects]
Port - Device detected :)
Preloader - CPU: MT6768/MT6769(Helio P65/G85 k68v1)
...
Exploitation - Crashing da...
DeviceClass - USBError(5, 'Input/Output Error')
[Loop continues indefinitely]
```

### Root Cause

After the first crash (mode 0), the device reconnects in **preloader mode** instead of **BROM mode**. The crasher logic then tries additional crash modes (1, 2) to force BROM entry, but MT6768 may not respond properly to these subsequent crashes, causing USB errors and preventing successful reconnection.

### Common Mistakes

#### ❌ WRONG: Using --preloader with DA file
```bash
python mtk.py da seccfg unlock --preloader .\mtkclient\Loader\DA_A15_lamu_FORBID_SIGNED.bin
```

#### ✅ CORRECT: Proper command syntax

**Without specifying files** (uses defaults):
```bash
python mtk.py da seccfg unlock
```

**With custom DA agent**:
```bash
python mtk.py da seccfg unlock --loader .\mtkclient\Loader\DA_A15_lamu_FORBID_SIGNED.bin
```

**With preloader AND DA** (rare, only if needed):
```bash
python mtk.py da seccfg unlock \
    --loader .\mtkclient\Loader\DA_A15_lamu_FORBID_SIGNED.bin \
    --preloader .\mtkclient\Loader\Preloader\preloader_lamu.bin
```

**With exploit type**:
```bash
python mtk.py da seccfg unlock --ptype kamakiri2
```

### Fixes Implemented (v2026-02-08)

#### 1. Longer Crash Delays
- **Changed**: Delay increased from 0.5s to 1.5s between crashes
- **Reason**: Gives device more time to fully reset and potentially enter BROM mode
- **File**: `mtkclient/Library/mtk_class.py`

#### 2. Maximum Retry Limit
- **Changed**: Crash attempts limited to 3 modes (0, 1, 2)
- **Reason**: Prevents infinite loop if device won't enter BROM mode
- **File**: `mtkclient/Library/mtk_class.py`

#### 3. Improved Error Handling for Crash Mode 1
- **Changed**: Crash mode 1 (`read32(0, 0x100)`) now catches USB errors gracefully
- **Reason**: Reading from invalid address causes device crash (expected behavior)
- **File**: `mtkclient/Library/exploit_handler.py`

#### 4. Better Logging
- **Changed**: Added debug messages showing crash mode progress
- **Reason**: Helps diagnose which crash mode works/fails
- **File**: `mtkclient/Library/mtk_class.py`

### Testing Steps

1. **Connect device in preloader mode** (no buttons pressed)

2. **Run basic command**:
```bash
python mtk.py da seccfg unlock
```

3. **Expected behavior**:
```
Port - Device detected :)
Preloader - CPU: MT6768/MT6769
...
Mtk - We're not in bootrom, trying to crash da...
Exploitation - Crashing da (mode 0)...
[Wait 1.5s]
Port - Device detected :)
Preloader - CPU: MT6768/MT6769
...
```

4. **If crash mode 0 fails**:
   - System tries mode 1 (after 1.5s delay)
   - Then mode 2 (after another 1.5s delay)
   - If all fail, shows warning message

5. **Alternative: Use exploit mode**:
```bash
python mtk.py da seccfg unlock --ptype kamakiri2
```

### Understanding Crash Modes

| Mode | Method | Purpose | Notes |
|------|--------|---------|-------|
| 0 | Invalid DA send | Send bad DA data | Usually works for most devices |
| 1 | Invalid memory read | Read address 0x0 | May cause USB error (expected) |
| 2 | Invalid payload+jump | Jump to bad code | Forces hard crash |
| 3 | Reset to BROM | Use watchdog reset | Most reliable but slowest |

### If Still Not Working

#### Option 1: Specify crash mode explicitly
```bash
python mtk.py da seccfg unlock --crash 3
```
Try mode 3 (reset_to_brom) which uses watchdog timer.

#### Option 2: Use exploit-specific crash
```bash
python mtk.py da seccfg unlock --ptype kamakiri2
```
Kamakiri2 exploit has its own crash mechanism.

#### Option 3: Manual BROM entry
1. Power off device
2. Hold **Vol+ AND Vol-** together
3. Connect USB while holding buttons
4. Keep holding for 3-5 seconds
5. Device should enter BROM mode
6. Release buttons
7. Run command without crash:
```bash
python mtk.py da seccfg unlock
```

### Technical Details

#### Crash Mode 0 (Most Common)
```python
# Sends 256 bytes of zeros to address 0x0
self.mtk.preloader.send_da(0, 0x100, 0x100, b'\x00' * 0x100)
# Device crashes trying to execute invalid code
# Our fix: Skip response wait, allow device to crash gracefully
```

#### Crash Mode 1 (Invalid Read)
```python
# Try to read 256 DWORDs from address 0x0
self.mtk.preloader.read32(0, 0x100)
# Device crashes accessing invalid memory
# Our fix: Catch USB errors (expected when device crashes)
```

#### Why Device Stays in Preloader Mode

Some MT6768 devices have security features that prevent BROM entry via crash:
- **Secure Boot Check (SBC)**: Enabled (shown in logs)
- **Device Authentication (DAA)**: Enabled (shown in logs)
- These may prevent crash-to-BROM on some firmware versions

**Workaround**: Try manual BROM entry (Option 3 above) or use serial/COM port mode:
```bash
python mtk.py --serialport COM3 da seccfg unlock
```

### Additional Notes

- **USB Driver**: Ensure proper USB drivers installed (UsbDk, libusbK, or WinUSB)
- **USB Cable**: Use good quality USB 2.0 cable (avoid USB 3.0 hubs)
- **USB Port**: Try different USB ports, preferably USB 2.0 directly on motherboard
- **Windows 11**: See `WINDOWS11_ALTERNATIVES.md` for driver options

### Success Indicators

✅ **Working**:
```
Exploitation - Crashing da (mode 0)...
[Wait]
Port - Device detected :)
Mtk - Successfully entered BROM mode with crash mode 0
```

✅ **Also Working** (even if not in BROM):
```
Exploitation - Crashing da (mode 0)...
[Wait]
Port - Device detected :)
[DA loads successfully and command executes]
```

❌ **Not Working**:
```
Exploitation - Crashing da (mode 1)...
DeviceClass - USBError(5, 'Input/Output Error')
[No reconnection or infinite loop]
```

### Getting Help

If issues persist:
1. Check USB drivers (see `WINDOWS11_ALTERNATIVES.md`)
2. Try serial/COM port mode
3. Try manual BROM entry
4. Check device firmware version
5. Report issue with full logs

---

**Version**: 2026-02-08  
**Related Docs**: 
- `MT6768_CRASH_EXPLOIT_FIX.md`  
- `WINDOWS11_ALTERNATIVES.md`  
- `MT6768_LAMU_HANDSHAKE_FIX.md`
