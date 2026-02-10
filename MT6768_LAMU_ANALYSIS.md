# MT6768 (lamu) Device Analysis

## Overview
This document summarizes the USB capture analysis for the MT6768 (lamu) device variant and confirms the existing mtkclient support.

## Device Information
- **Chipset**: MediaTek MT6768 (Helio P65/G85)
- **Variant**: lamu (A15)
- **Hardware Code**: 0x707
- **USB VID:PID**: 0x0e8d:0x2000 (MediaTek Preloader)

## Files Added
- `mtkclient/Loader/Preloader/preloader_lamu.bin` - Device-specific preloader binary

## USB Communication Analysis

### Device Descriptor
```
bcdUSB: 0x0200 (USB 2.0)
bDeviceClass: 0x02 (Communications and CDC Control)
bMaxPacketSize0: 64
idVendor: 0x0e8d (MediaTek Inc.)
idProduct: 0x2000 (MT65xx Preloader)
```

### Communication Protocol
The device follows the standard MediaTek preloader protocol:
1. Device responds with "READY" (0x5245414459)
2. Standard handshake and authentication sequence
3. Bulk transfers for data exchange
4. Compatible with existing mtkclient implementation

## Current mtkclient Support

### Configuration Status
✅ **VID/PID Detection**: Already configured in `mtkclient/config/usb_ids.py`
- Entry: `0x0E8D: {0x2000: -1}  # MTK Preloader`

✅ **BROM Configuration**: Complete configuration exists in `mtkclient/config/brom_config.py`
- Hardware code: 0x707
- Configuration includes all necessary addresses and parameters
- DA mode: XFLASH
- DA code: 0x6768

✅ **Exploit Support**: Kamakiri exploit compatible
- var1: 0x25
- Watchdog: 0x10007000
- UART: 0x11002000

✅ **Payload**: `mtkclient/payloads/mt6768_payload.bin` exists

## Conclusion
The MT6768 chipset is already fully supported in mtkclient. The lamu device variant uses the same hardware code (0x707) and is compatible with the existing configuration. The analysis of the USB capture (1.pcapng) confirms that no changes to the core configuration are needed.

### Usage
The lamu device can be used with mtkclient's existing MT6768 support:
```bash
# Standard mtkclient commands work as expected
python mtk.py [command] [options]
```

The lamu-specific preloader binary has been added for device-specific operations that may require it.

## Source Files Analyzed
- DA_A15_lamu_FORBID_SIGNED.bin (625 KB) - DA agent binary
- preloader_lamu.bin (322 KB) - Preloader binary  
- 1.pcapng (163 MB) - USB communication capture from official flash tool

## References
- MediaTek BootROM protocol documentation
- mtkclient configuration in `mtkclient/config/brom_config.py`
- USB device IDs in `mtkclient/config/usb_ids.py`
