# MT6768 (Lamu Device) Support Files

This document describes the MT6768 support files analyzed and integrated for the "lamu" device.

## Device Information

- **Chipset**: MediaTek MT6768 (Helio P65/G85)
- **Device**: Lamu (likely Motorola device based on naming)
- **Hardware Code**: 0x707 (mapped to 0x6768)
- **USB VID:PID**: 0x0e8d:0x2000

## Files Analyzed

### 1. DA Agent: DA_A15_lamu_FORBID_SIGNED.bin

**Source**: https://github.com/EduardoA3677/mtkclient/releases/download/v1/DA_A15_lamu_FORBID_SIGNED.bin

**Details**:
- Size: 625 KB (639,072 bytes)
- Version: MTK_AllInOne_DA_v3.3001.2025/11/07.14:24_654171
- Type: XFLASH mode DA agent (mode 5)
- Header: "MTK_DOWNLOAD_AGENT"

**Note**: This file is **NOT** included in the repository due to `.gitignore` rules (`DA_*.bin`).
Users need to download it manually from the release link above and place it in:
- `mtkclient/Loader/DA_A15_lamu_FORBID_SIGNED.bin`

### 2. Preloader: preloader_lamu.bin

**Source**: https://github.com/EduardoA3677/mtkclient/releases/download/v1/preloader_lamu.bin

**Details**:
- Size: 322 KB (328,942 bytes)
- Header identifier: "MMM" header with FILE_INFO structure
- Contains ROM info referencing MT6752 (compatibility marker)
- Actual chipset: MT6768

**Location**: `mtkclient/Loader/Preloader/preloader_lamu.bin`

### 3. USB Capture Analysis: 1.pcapng

**Source**: https://github.com/EduardoA3677/mtkclient/releases/download/v1/1.pcapng

**Details**:
- Size: 163 MB
- Content: USB traffic capture of flash operation using official tool
- Devices captured: Multiple USB devices including MTK device (0x0e8d:0x2000)

**Key Protocol Commands Identified**:
- `0a200100` - Command type 0x0100 (likely SETUP_ENVIRONMENT/INIT)
- `08202000...` - Command type 0x2000 (likely SET commands)
- `06200fa0...` - Command type 0x0fa0 (configuration)
- `0c200200` - Command type 0x0200 (likely GET commands)
- `05200...` - Command type 0x05 (unknown)

These match the XFLASH DA protocol defined in `mtkclient/Library/DA/xflash/xflash_param.py`.

## Current MT6768 Configuration

The MT6768 chipset is already configured in `mtkclient/config/brom_config.py` (hwcode 0x707):

```python
0x707: Chipconfig(
    var1=0x25,
    watchdog=0x10007000,
    uart=0x11002000,
    brom_payload_addr=0x100A00,
    da_payload_addr=0x201000,
    pl_payload_addr=0x40200000,
    gcpu_base=0x10050000,
    sej_base=0x1000A000,  # hacc
    dxcc_base=0x10210000,
    cqdma_base=0x10212000,
    ap_dma_mem=0x11000000 + 0x1A0,
    blacklist=[(0x10282C, 0x0), (0x00105994, 0)],
    blacklist_count=0x0000000A,
    send_ptr=(0x10286c, 0xc190),
    ctrl_buffer=0x00102A28,
    cmd_handler=0x0000CF15,
    brom_register_access=(0xc598, 0xc650),
    meid_addr=0x102AF8,
    socid_addr=0x102b08,
    prov_addr=0x1054F4,
    misc_lock=0x1001a100,
    efuse_addr=0x11ce0000,
    damode=DAmodes.XFLASH,
    dacode=0x6768,
    name="MT6768/MT6769",
    description="Helio P65/G85 k68v1",
    loader="mt6768_payload.bin"
)
```

## USB VID/PID Support

USB detection is configured in `mtkclient/config/usb_ids.py`:

```python
0x0E8D: {
    0x0003: -1,  # MTK Brom
    0x6000: 2,   # MTK Preloader
    0x2000: -1,  # MTK Preloader (used by lamu)
    0x2001: -1,  # MTK Preloader
    0x20FF: -1,  # MTK Preloader
    0x3000: -1   # MTK Preloader
}
```

The PID **0x2000** is already supported.

## Exploit Support

MT6768 uses the **Kamakiri2** exploit defined in:
- `mtkclient/Library/Exploit/kamakiri2.py`

This exploit:
- Uses USB control transfers to bypass security
- Works with BROM register access configuration
- Supports payload injection at configured addresses
- Compatible with SLA/DAA/SBC secured devices

## Authentication Analysis

From the USB capture analysis:
- Device uses XFLASH DA protocol (command-based)
- Commands follow little-endian format
- Authentication sequences visible in frames 93446-93535
- Protocol appears standard for MT6768 devices

## Existing DA Agent Comparison

**Existing**: Archivo eliminado (xiaomi_9_DA_6765_6785_6768_6873_6885_6853.bin)
- Versión antigua, incompatible con handshake moderno

**New**: `DA_A15_lamu_FORBID_SIGNED.bin`
- Version: MTK_AllInOne_DA_v3.3001.2025/11/07.14:24_654171  
- Date: November 2025
- **Protocolo actualizado**: Usa "READY" en lugar de 0xC0 para handshake

## IMPORTANTE: Corrección del Handshake

### Descubrimiento Mediante Análisis del PCAPNG

El análisis del archivo `1.pcapng` reveló que los DA agents modernos (2025) utilizan un protocolo de handshake diferente:

**Secuencia de Handshake Real:**
1. Jump a DA en 0x201000
2. DA responde con string **"READY"** (0x5245414459) - NO con byte 0xC0
3. Multiple intercambios de READY mientras DA inicializa
4. Handshake de dirección (0x00200000)
5. Envío de payload/código ARM
6. Confirmación de dirección
7. Comando MAGIC (0xFEEEEEEF) + "SYNC" (0x53594E43)
8. Comandos XFLASH normales (SETUP_ENVIRONMENT, etc.)

### Cambio en el Código

El archivo `mtkclient/Library/DA/xflash/xflash_lib.py` fue modificado para soportar ambos protocolos:
- **Nuevo**: Espera "READY" (5 bytes)
- **Legacy**: Soporta 0xC0 (1 byte) para compatibilidad

Este cambio corrige el error "Error on DA sync" que ocurría con DA agents modernos.

## Usage

To use the lamu-specific DA agent:

1. Download `DA_A15_lamu_FORBID_SIGNED.bin` from the release
2. Place it in `mtkclient/Loader/`
3. Reference it when using mtkclient tools:
   ```bash
   python mtk.py --loader=DA_A15_lamu_FORBID_SIGNED.bin [other options]
   ```

The preloader `preloader_lamu.bin` is already included in the repository for reference.

## References

- Release: https://github.com/EduardoA3677/mtkclient/releases/tag/v1
- DA Agent: [DA_A15_lamu_FORBID_SIGNED.bin](https://github.com/EduardoA3677/mtkclient/releases/download/v1/DA_A15_lamu_FORBID_SIGNED.bin)
- Preloader: [preloader_lamu.bin](https://github.com/EduardoA3677/mtkclient/releases/download/v1/preloader_lamu.bin)
- USB Capture: [1.pcapng](https://github.com/EduardoA3677/mtkclient/releases/download/v1/1.pcapng)

## Conclusion

The MT6768 chipset is already well-supported in mtkclient. The analyzed files confirm:
- ✅ Correct USB VID/PID detection (0x0e8d:0x2000)
- ✅ Proper chipconfig settings for hwcode 0x707
- ✅ XFLASH DA mode configuration
- ✅ Kamakiri2 exploit compatibility
- ✅ Authentication protocol support

The new DA agent provides an updated version that may offer better compatibility with newer security implementations.
