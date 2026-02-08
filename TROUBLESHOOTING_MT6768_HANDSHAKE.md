# Troubleshooting MT6768 DA Handshake Errors

## Problem Description

When attempting to flash or interact with MT6768 (lamu) devices, you may encounter a **"DA handshake error"** which typically manifests as:

```
Error on DA sync
Error jumping to DA
```

This occurs at line 968-969 in `mtkclient/Library/DA/xflash/xflash_lib.py` when the DA agent doesn't respond with the expected `\xC0` synchronization byte after being loaded and jumped to.

## Root Causes

### 1. DA Signature Verification Failure
The MT6768 device (especially lamu variant) requires a **signed DA agent**. If the DA signature doesn't match or is invalid, the device will refuse to execute it.

**Symptoms:**
- DA upload appears successful
- Jump_DA reports success (status 0)
- But no `\xC0` sync byte received

**Solution:**
Use the device-specific signed DA agent: `DA_A15_lamu_FORBID_SIGNED.bin`

### 2. Wrong DA Agent Version
Using an older or incompatible DA agent can cause handshake failures due to:
- Protocol version mismatch
- Missing security features
- Incompatible command set

**Currently Available DA Agents:**
- `xiaomi_9_DA_6765_6785_6768_6873_6885_6853.bin` - Version v3.3001.2020/07/07 (OLD)
- `DA_A15_lamu_FORBID_SIGNED.bin` - Version v3.3001.2025/11/07 (NEW - 5 years newer)

**Solution:**
Use the newer DA agent specifically for the lamu device.

### 3. SLA (Secure Link Authentication) Issues
Some MT6768 variants have SLA enabled, requiring authentication before DA execution.

**Symptoms:**
- "SLA required" message appears
- "Bad sla challenge" error
- DA fails to load

**Solution:**
Ensure SLA authentication is properly handled (mtkclient should handle this automatically).

### 4. USB Communication Issues
Timing or USB transfer problems can prevent proper synchronization.

**Symptoms:**
- Intermittent failures
- Works sometimes, fails other times
- USB timeout errors

**Solution:**
- Use shorter, high-quality USB cable
- Try different USB ports (preferably USB 2.0)
- Avoid USB hubs

## Step-by-Step Resolution

### Step 1: Download the Correct DA Agent

Download the lamu-specific DA agent:

```bash
# Download from releases
curl -L -o DA_A15_lamu_FORBID_SIGNED.bin \
  "https://github.com/EduardoA3677/mtkclient/releases/download/v1/DA_A15_lamu_FORBID_SIGNED.bin"

# Move to Loader directory
mv DA_A15_lamu_FORBID_SIGNED.bin mtkclient/Loader/
```

### Step 2: Use the Specific DA Agent

When running mtkclient commands, explicitly specify the DA agent:

```bash
# For reading operations
python mtk.py r <partition> <output_file> --loader DA_A15_lamu_FORBID_SIGNED.bin

# For writing operations  
python mtk.py w <partition> <input_file> --loader DA_A15_lamu_FORBID_SIGNED.bin

# For GPT operations
python mtk.py printgpt --loader DA_A15_lamu_FORBID_SIGNED.bin

# For reading entire flash
python mtk.py rf <output_file> --loader DA_A15_lamu_FORBID_SIGNED.bin
```

### Step 3: Use the Preloader (if available)

If you have the device's preloader, use it for better compatibility:

```bash
python mtk.py <command> --loader DA_A15_lamu_FORBID_SIGNED.bin --preloader preloader_lamu.bin
```

### Step 4: Enable Verbose Logging

To diagnose the exact issue:

```bash
python mtk.py <command> --loader DA_A15_lamu_FORBID_SIGNED.bin --loglevel 0 --debugmode
```

This will show:
- Exact point of failure
- USB transfer details
- Authentication status
- Sync byte reception

## Advanced Troubleshooting

### Check Device Detection

First, verify the device is detected correctly:

```bash
python mtk.py --list
```

Expected output:
```
MediaTek PreLoader USB VCOM (0e8d:2000)
```

### Verify Chipset Detection

```bash
python mtk.py gettargetconfig --loader DA_A15_lamu_FORBID_SIGNED.bin
```

This should show:
- HW Code: 0x707 or 0x6768
- Chipset: MT6768/MT6769
- SLA/DAA/SBC status

### Test with Stock DA

If the signed DA still fails, try the stock DA flag:

```bash
python mtk.py <command> --stock --loader DA_A15_lamu_FORBID_SIGNED.bin
```

### Manual DA Loading Test

To isolate the issue, try just loading the DA:

```bash
python mtk.py plstage --filename DA_A15_lamu_FORBID_SIGNED.bin --preloader preloader_lamu.bin
```

## Common Error Messages and Solutions

### "Error on DA sync"
**Cause:** DA didn't respond with 0xC0 byte
**Solution:** 
- Use correct signed DA agent
- Check USB connection
- Verify device is in correct mode

### "Bad sla challenge"
**Cause:** SLA authentication failed
**Solution:**
- Device requires specific authentication
- May need vendor-specific auth file
- Contact device manufacturer for auth certificate

### "DA_Send status error"
**Cause:** Device rejected DA upload
**Solution:**
- DA signature invalid
- Use device-specific signed DA
- Check if device is locked

### "Error on jumping to DA"
**Cause:** Jump command failed or DA address wrong
**Solution:**
- Verify DA payload address in chipconfig (0x201000 for MT6768)
- Check if exploit is working correctly
- May need Kamakiri exploit

## Device-Specific Notes for MT6768 Lamu

### Hardware Specifications
- **Chipset:** MediaTek MT6768 (Helio P65/G85)
- **HW Code:** 0x707 (maps to 0x6768)
- **USB VID:PID:** 0x0e8d:0x2000
- **DA Mode:** XFLASH (mode 5)
- **Security:** SLA/DAA enabled (requires signed DA)

### Verified Configuration
```python
# From brom_config.py line 1187
watchdog=0x10007000
uart=0x11002000
brom_payload_addr=0x100A00
da_payload_addr=0x201000
pl_payload_addr=0x40200000
gcpu_base=0x10050000
sej_base=0x1000A000
dxcc_base=0x10210000
cqdma_base=0x10212000
efuse_addr=0x11ce0000
```

### Exploit Method
- **Primary:** Kamakiri2 (USB control transfer exploit)
- **Location:** `mtkclient/Library/Exploit/kamakiri2.py`
- **Compatibility:** Confirmed working with MT6768

## Testing Checklist

Before reporting issues, verify:

- [ ] Downloaded the correct DA agent (DA_A15_lamu_FORBID_SIGNED.bin)
- [ ] Placed DA in `mtkclient/Loader/` directory
- [ ] Using `--loader` parameter to specify DA
- [ ] Device is in BROM/Preloader mode (0x0e8d:0x2000)
- [ ] USB cable is good quality and directly connected
- [ ] Tried with verbose logging (`--loglevel 0 --debugmode`)
- [ ] Verified chipset detection shows MT6768
- [ ] Checked for SLA/DAA/SBC status
- [ ] Preloader file available if required

## Alternative Approaches

### If Signed DA Still Fails

1. **Check if device bootloader is locked:**
   - Some devices require bootloader unlock first
   - Check manufacturer documentation

2. **Try older DA versions:**
   ```bash
   # Use the xiaomi DA which also supports MT6768
   python mtk.py <command> --loader xiaomi_9_DA_6765_6785_6768_6873_6885_6853.bin
   ```

3. **Boot to META mode:**
   ```bash
   python mtk.py meta --loader DA_A15_lamu_FORBID_SIGNED.bin
   ```

4. **Use BROM exploit mode:**
   ```bash
   python mtk.py payload --loader DA_A15_lamu_FORBID_SIGNED.bin
   ```

## File Locations

All required files:
- **DA Agent:** `mtkclient/Loader/DA_A15_lamu_FORBID_SIGNED.bin` (download from release)
- **Preloader:** `mtkclient/Loader/Preloader/preloader_lamu.bin` (included in repo)
- **Chipconfig:** `mtkclient/config/brom_config.py` (hwcode 0x707)
- **USB IDs:** `mtkclient/config/usb_ids.py` (VID:PID 0x0e8d:0x2000)
- **Exploit:** `mtkclient/Library/Exploit/kamakiri2.py`

## Success Indicators

When DA handshake succeeds, you'll see:

```
Sending payload via kamakiri
Done sending payload...
Successfully uploaded stage 1, jumping ..
Jumping to 0x201000: ok.
Successfully received DA sync
Setup environment
Setup hw init
```

Then the DA operations will proceed normally.

## Getting Help

If you still experience handshake errors after following this guide:

1. **Collect logs:**
   ```bash
   python mtk.py <command> --loader DA_A15_lamu_FORBID_SIGNED.bin --loglevel 0 --debugmode > mtk_log.txt 2>&1
   ```

2. **Collect device info:**
   ```bash
   python mtk.py gettargetconfig --loader DA_A15_lamu_FORBID_SIGNED.bin > device_info.txt 2>&1
   ```

3. **Report issue with:**
   - Full command used
   - Complete error log
   - Device model and variant
   - mtkclient version
   - Operating system

## References

- DA Agent Download: https://github.com/EduardoA3677/mtkclient/releases/tag/v1
- MT6768 Configuration: `mtkclient/config/brom_config.py` (line 1187)
- XFlash Protocol: `mtkclient/Library/DA/xflash/xflash_lib.py` (line 960-985)
- Kamakiri2 Exploit: `mtkclient/Library/Exploit/kamakiri2.py`

---

**Last Updated:** 2026-02-08
**Tested On:** MT6768 (lamu device with HW code 0x707)
**mtkclient Version:** 2.1.2+
