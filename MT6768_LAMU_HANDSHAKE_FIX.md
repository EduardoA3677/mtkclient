# MT6768 Lamu Handshake Fix Guide

## Problem
Device fails to establish initial USB handshake with error:
```
Port - Handshake failed after retries
Preloader - [LIB]: Status: Handshake failed, retrying...
```

## Root Cause Analysis

The handshake failure occurs **before** the DA agent is sent, meaning the issue is at the BROM/Preloader level, not with the DA handshake that was fixed in this PR.

## Solutions

### Solution 1: Correct Command Flags

The command you used has conflicting flags:
```bash
python mtk.py gettargetconfig --loader .\mtkclient\Loader\DA_A15_lamu_FORBID_SIGNED.bin --ptype kamakiri2 --preloader .\mtkclient\Loader\Preloader\preloader_lamu.bin --crash
```

**Issue**: Using both `--preloader` and `--crash` together is incorrect. The `--crash` flag is for Kamakiri2 exploit which crashes the bootrom, but you're also providing a preloader file.

**Fix**: Remove the `--crash` flag:
```bash
python mtk.py gettargetconfig --loader .\mtkclient\Loader\DA_A15_lamu_FORBID_SIGNED.bin --ptype kamakiri2 --preloader .\mtkclient\Loader\Preloader\preloader_lamu.bin
```

OR use Kamakiri2 exploit without preloader:
```bash
python mtk.py gettargetconfig --loader .\mtkclient\Loader\DA_A15_lamu_FORBID_SIGNED.bin --ptype kamakiri2
```

### Solution 2: Device Connection Mode

The device must be in the correct mode for handshake to work:

#### For BROM Mode (recommended for exploits):
1. **Power off** the device completely
2. **Hold** Volume Up + Volume Down buttons
3. **Connect** USB cable while holding buttons
4. **Keep holding** for 2-3 seconds
5. **Run** the command immediately

#### For Preloader Mode (if BROM doesn't work):
1. **Power off** the device completely
2. **Do NOT press** any buttons
3. **Connect** USB cable
4. **Run** the command immediately

### Solution 3: USB Driver Issues (Windows)

If the device is not detected:

1. **Check Device Manager**:
   - Look for "MediaTek USB Port" or "MTK VCOM" or "Android" device
   - If you see "Unknown Device" or "USB Device Not Recognized", drivers are missing

2. **Install MediaTek USB Drivers**:
   - Download from: https://mtk-drivers.com/
   - Or use the drivers included with SP Flash Tool
   - Install and reboot

3. **Disable Driver Signature Enforcement** (Windows 10/11):
   ```
   1. Hold Shift + Click "Restart"
   2. Troubleshoot → Advanced Options → Startup Settings → Restart
   3. Press F7 for "Disable driver signature enforcement"
   4. Boot Windows and try again
   ```

### Solution 4: USB Port and Cable

1. **Use USB 2.0 port** (not USB 3.0/3.1) - preferably rear ports on desktop
2. **Use short cable** (<1 meter) with data lines (not charge-only cable)
3. **Try different USB ports** - some ports have better power/signal
4. **Avoid USB hubs** - connect directly to PC

### Solution 5: Device-Specific Boot Sequence

For Motorola Lamu devices:

1. **Complete power off**:
   - Hold power button for 10+ seconds
   - Wait 5 seconds after screen goes black

2. **Enter EDL/BROM mode**:
   ```
   Method 1 (Bootloader):
   - Hold Vol Down
   - Press Power
   - When bootloader menu appears, select "Brom mode" or "Emergency Download"
   
   Method 2 (Direct):
   - Hold Vol Up + Vol Down simultaneously
   - Connect USB
   - Keep holding for 5 seconds
   
   Method 3 (Test Point):
   - If software methods fail, use test point method
   - Short test point to ground while connecting USB
   ```

3. **Verify in Device Manager**:
   - Should show "MediaTek USB Port (COM5)" or similar
   - VID: 0x0E8D, PID: 0x2000 or 0x0003

### Solution 6: Timing Issues

The handshake timing might be too aggressive for some devices. Try:

1. **Add delay before running command**:
   ```bash
   # Connect device first, wait 2 seconds, then run:
   timeout /t 2 /nobreak >nul && python mtk.py gettargetconfig --loader .\mtkclient\Loader\DA_A15_lamu_FORBID_SIGNED.bin --ptype kamakiri2
   ```

2. **Increase retries in code** (temporary debug):
   - Edit `mtkclient/Library/mtk_preloader.py` line 158
   - Change `maxtries = 100` to `maxtries = 500`

### Solution 7: Check USB VID/PID

Verify the device is detected with correct VID/PID:

**Windows**:
```batch
# In PowerShell:
Get-PnpDevice | Where-Object {$_.FriendlyName -like "*MediaTek*" -or $_.FriendlyName -like "*MTK*"}
```

**Linux**:
```bash
lsusb | grep -i mediatek
# Should show: Bus 001 Device 005: ID 0e8d:2000 MediaTek Inc.
```

Expected values:
- VID: `0x0E8D` (MediaTek)
- PID: `0x2000` (Preloader) or `0x0003` (BROM)

### Solution 8: Battery Level

Low battery can cause handshake failures:
1. **Charge device** to at least 50%
2. **Keep USB connected** during charging
3. Try again after 30 minutes of charging

## Verification Commands

After fixing, test with:

```bash
# 1. List connected devices
python mtk.py --list

# 2. Simple config read (no exploit needed)
python mtk.py gettargetconfig

# 3. With DA agent
python mtk.py gettargetconfig --loader .\mtkclient\Loader\DA_A15_lamu_FORBID_SIGNED.bin

# 4. With Kamakiri2 exploit
python mtk.py gettargetconfig --ptype kamakiri2
```

## Expected Output

Successful handshake:
```
Preloader - Status: Waiting for PreLoader VCOM, please reconnect mobile/iot device to brom mode
Port - Device detected :)
Preloader - CPU:               MT6768/MT6769 (Helio P65/G85 k68v1)
Preloader - HW version:        0xca00
Preloader - WDT:               0x10007000
Preloader - HW code:           0x707
```

## Still Not Working?

If none of the above works:

1. **Enable debug logging**:
   ```bash
   python mtk.py gettargetconfig --debugmode
   ```
   Check `logs/log.txt` for detailed errors

2. **Test with different device**:
   - If you have another MTK device, test if handshake works
   - This isolates whether it's device-specific or system-wide issue

3. **Try Linux Live USB**:
   - Boot Ubuntu Live USB
   - Install mtkclient: `pip3 install mtkclient`
   - Test without Windows USB driver issues

4. **Hardware issue**:
   - USB port on device might be damaged
   - Try professional repair service

## Technical Details

The handshake sequence is:
```
1. PC sends: 0xA0 0x0A 0x50 0x05
2. Device echoes back (inverted): 0x5F 0xF5 0xAF 0xFA
3. PC verifies echo
4. If match: handshake successful
5. If no response: "Handshake failed after retries"
```

The issue in your case is step 2 - the device is not responding at all, which means:
- Device is not in BROM/Preloader mode, OR
- USB connection is not working, OR
- Device needs specific timing/button combination

## Summary

**Most likely fix**: Remove `--crash` flag from your command. Use either:
```bash
python mtk.py gettargetconfig --loader .\mtkclient\Loader\DA_A15_lamu_FORBID_SIGNED.bin --ptype kamakiri2 --preloader .\mtkclient\Loader\Preloader\preloader_lamu.bin
```

or

```bash
python mtk.py gettargetconfig --loader .\mtkclient\Loader\DA_A15_lamu_FORBID_SIGNED.bin --ptype kamakiri2
```

The handshake must succeed **before** any DA agent or exploit code is sent.
