# MT6768 (Helio P65/G85) USB Capture Analysis

## Overview
This document contains the analysis results from the USB capture (1.pcapng) of a flash operation using the official MediaTek SP Flash Tool on an MT6768 device (lamu/A15).

## Device Information

### Hardware Identification
- **Chipset**: MT6768 (Helio P65/G85 k68v1)
- **Hardware Code**: 0x0707
- **Device Name**: lamu (Motorola Moto E32/E32s)
- **VID:PID**: 0x0e8d:0x2000 (MediaTek Preloader)

### Communication Protocol

#### USB Enumeration
The device enumerates as:
```
VID: 0x0e8d (MediaTek Inc.)
PID: 0x2000 (MTK Preloader)
Device Class: CDC (Communication Device Class)
```

#### BROM Communication Sequence
1. **Device Detection** (Packet 483): Device descriptor with VID:PID 0x0e8d:0x2000
2. **Handshake** (Packets 494-564): 
   - Host sends 0xD1 command (BROM_CMD_START_CMD)
   - Device responds with "READY" string
   - Multiple auth handshake exchanges
3. **Hardware Code Request** (Packet 569):
   - Host sends 0xA0 command (BROM_CMD_GET_HW_CODE)
   - Device responds with HWCODE: 0x0707 (Packet 599)
4. **DA Upload** (Packet 1535):
   - Large bulk transfer of 65,535 bytes
   - Contains ARM executable code (identified by vector table)
   - This is the initial stage DA loader

### Authentication Flow
The analysis shows the following authentication sequence:
1. Device enters BROM mode (VID:PID 0x0e8d:0x2000)
2. Host queries device status with 0xD1 commands
3. Device responds with "READY" indicating it's ready for commands
4. Host requests HWCODE with 0xA0 command
5. Device responds with 0x0707
6. Host begins DA upload process
7. Multiple command/response exchanges for memory operations

### Files Analyzed

#### DA Agent: DA_A15_lamu_FORBID_SIGNED.bin
- **Size**: 625 KB
- **Type**: MTK Download Agent v3.3001.2025/11/07
- **Header**: "MTK_DOWNLOAD_AGENT"
- **Format**: Signed MTK AllInOne DA binary
- **Compatible with**: MT6765, MT6768, MT6785, MT6873, MT6885, MT6853

#### Preloader: preloader_lamu.bin
- **Size**: 322 KB  
- **Type**: MediaTek Bootloader Preloader
- **Platform**: MT6768
- **Build Path**: Contains references to mt6768 platform sources
- **Device**: lamu (Motorola device)

### Current mtkclient Support Status

#### Already Configured
- ✅ VID:PID 0x0e8d:0x2000 in `mtkclient/config/usb_ids.py`
- ✅ MT6768 chipconfig (hwcode 0x707) in `mtkclient/config/brom_config.py`
- ✅ Payload file `mtkclient/payloads/mt6768_payload.bin`
- ✅ Existing DA loader: `mtkclient/Loader/xiaomi_9_DA_6765_6785_6768_6873_6885_6853.bin`
- ✅ Existing preloaders in `mtkclient/Loader/Preloader/preloader_k68v1_64_Vivo_MT6768*.bin`

#### MT6768 Chipconfig Details (hwcode 0x707)
```python
var1=0x25
watchdog=0x10007000
uart=0x11002000
brom_payload_addr=0x100A00
da_payload_addr=0x201000
pl_payload_addr=0x40200000
gcpu_base=0x10050000
sej_base=0x1000A000  # HACC
dxcc_base=0x10210000  # DXCC Security
cqdma_base=0x10212000
ap_dma_mem=0x110001A0  # AP_DMA_I2C2_CH0_RX_MEM_ADDR
blacklist=[(0x10282C, 0x0), (0x00105994, 0)]
blacklist_count=0x0000000A
send_ptr=(0x10286c, 0xc190)
ctrl_buffer=0x00102A28
cmd_handler=0x0000CF15
brom_register_access=(0xc598, 0xc650)
meid_addr=0x102AF8
socid_addr=0x102b08
prov_addr=0x1054F4
misc_lock=0x1001a100
efuse_addr=0x11ce0000
damode=DAmodes.XFLASH  # Uses XFLASH mode (v5)
dacode=0x6768
loader="mt6768_payload.bin"
```

### Added Resources
New files added to support specific MT6768 variants:
1. `mtkclient/Loader/DA_A15_lamu_FORBID_SIGNED.bin` - Signed DA for lamu device
2. `mtkclient/Loader/Preloader/preloader_lamu.bin` - Preloader for lamu device

## Conclusion

The MT6768 support in mtkclient is already comprehensive with proper:
- USB device detection (VID:PID)
- Chipconfig with correct memory addresses
- Exploit support (kamakiri compatible with var1=0x25)
- DA mode configuration (XFLASH)
- Payload binary

The pcapng analysis confirms that the existing configuration is correct:
- Device properly enumerates with PID 0x2000
- HWCODE 0x0707 is correctly configured
- BROM commands follow expected protocol
- DA upload mechanism works as designed

Additional DA agent and preloader binaries have been added for the lamu device variant to provide more options for users working with this specific model.
