# MT6768 Lamu Device Files

## Required Files for MT6768 Lamu Support

### DA Agent (Download Agent)
**File**: `DA_A15_lamu_FORBID_SIGNED.bin`  
**Size**: 625 KB  
**Download**: https://github.com/EduardoA3677/mtkclient/releases/download/v1/DA_A15_lamu_FORBID_SIGNED.bin  
**Location**: Place in `mtkclient/Loader/` directory  
**Note**: This file is excluded from git (large binary)

**How to download**:
```bash
cd mtkclient/Loader
wget https://github.com/EduardoA3677/mtkclient/releases/download/v1/DA_A15_lamu_FORBID_SIGNED.bin
```

Or on Windows (PowerShell):
```powershell
cd mtkclient\Loader
Invoke-WebRequest -Uri "https://github.com/EduardoA3677/mtkclient/releases/download/v1/DA_A15_lamu_FORBID_SIGNED.bin" -OutFile "DA_A15_lamu_FORBID_SIGNED.bin"
```

### Preloader
**File**: `preloader_lamu.bin`  
**Size**: 322 KB  
**Download**: https://github.com/EduardoA3677/mtkclient/releases/download/v1/preloader_lamu.bin  
**Location**: Place in `mtkclient/Loader/Preloader/` directory  
**Status**: ✅ Included in repository

## Usage

### Option 1: Use with Default Settings (Recommended)
```bash
python mtk.py da seccfg unlock
```
mtkclient will use the default DA agent (MTK_DA_V5.bin or MTK_DA_V6.bin).

### Option 2: Use Lamu-Specific DA Agent
```bash
python mtk.py da seccfg unlock --loader mtkclient/Loader/DA_A15_lamu_FORBID_SIGNED.bin
```

### Option 3: Use Both Custom DA and Preloader (Advanced)
```bash
python mtk.py da seccfg unlock \
    --loader mtkclient/Loader/DA_A15_lamu_FORBID_SIGNED.bin \
    --preloader mtkclient/Loader/Preloader/preloader_lamu.bin
```

### Option 4: With Kamakiri2 Exploit
```bash
python mtk.py da seccfg unlock \
    --ptype kamakiri2 \
    --loader mtkclient/Loader/DA_A15_lamu_FORBID_SIGNED.bin
```

## Understanding the Files

### What is a DA Agent?
- **DA** = Download Agent
- Large binary file (typically 500KB-10MB)
- Runs on the device to perform flash operations
- Version: MTK_AllInOne_DA_v3.3001.2025/11/07
- This specific DA is **signed and authorized** for Lamu devices

### What is a Preloader?
- Small bootloader (typically 200-500KB)
- First code that runs after BROM
- Contains device-specific initialization
- Can be used with exploits (kamakiri, kamakiri2)

### What is a Payload?
- **Different from DA agent!**
- Small exploit code (typically <1KB)
- Located in `mtkclient/payloads/mt6768_payload.bin`
- Used by Kamakiri exploit to gain code execution
- **Do NOT confuse with DA agent**

## Common Mistakes

### ❌ WRONG: Using DA as payload
```bash
# This is WRONG - DA agent is not a payload!
cp DA_A15_lamu_FORBID_SIGNED.bin ../payloads/mt6768_payload.bin
```

### ❌ WRONG: Using preloader flag with DA file
```bash
# This is WRONG - --preloader expects preloader, not DA
python mtk.py da seccfg unlock --preloader DA_A15_lamu_FORBID_SIGNED.bin
```

### ✅ CORRECT: Proper usage
```bash
# Use --loader for DA agent
python mtk.py da seccfg unlock --loader DA_A15_lamu_FORBID_SIGNED.bin

# Use --preloader for preloader (rare, usually not needed)
python mtk.py da seccfg unlock --preloader preloader_lamu.bin
```

## File Relationships

```
BROM (in chip)
  ↓
Preloader (preloader_lamu.bin - 322KB)
  ↓
[Exploit Payload if needed] (mt6768_payload.bin - 612 bytes)
  ↓
DA Agent (DA_A15_lamu_FORBID_SIGNED.bin - 625KB)
  ↓
Flash Operations
```

## Troubleshooting

### Kamakiri Exploit Hangs at "Kamakiri Run"
**Problem**: Exploit payload not responding

**Solutions**:
1. Try without exploit (device in preloader mode, no buttons):
   ```bash
   python mtk.py da seccfg unlock
   ```

2. Use crash exploit instead:
   ```bash
   python mtk.py da seccfg unlock --ptype kamakiri2
   ```

3. Try manual BROM entry:
   - Power off device
   - Hold Vol+ AND Vol- together
   - Connect USB while holding
   - Keep holding 3-5 seconds
   - Run command

### "Handshake failed after retries"
See `MT6768_LAMU_HANDSHAKE_FIX.md` for solutions.

### "DA handshake error"
See `TROUBLESHOOTING_MT6768_HANDSHAKE.md` for solutions.

### Crash exploit loops forever
See `MT6768_CRASH_TROUBLESHOOTING.md` for solutions.

## Configuration

The MT6768 configuration is already set up in `mtkclient/config/brom_config.py`:
- Hardware code: 0x707
- DA payload address: 0x201000
- Exploit: Kamakiri2 supported
- SLA authentication: Supported (keys in sla_keys.py)

## Additional Resources

- **Complete Analysis**: `HEXADECIMAL_ANALYSIS.md`
- **Crash Fix**: `MT6768_CRASH_EXPLOIT_FIX.md`
- **Windows 11**: `WINDOWS11_ALTERNATIVES.md`
- **Integration**: `MT6768_INTEGRATION_GUIDE.md`

---

**Last Updated**: 2026-02-08  
**Status**: ✅ Complete MT6768 Lamu support
