# MT6768 Lamu Device Files

## DA_A15_lamu_FORBID_SIGNED.bin

**Device**: Motorola Moto E32/E32s (codename: lamu)
**Chipset**: MediaTek MT6768 (Helio P65/G85)
**Type**: Download Agent (DA) - Signed
**Version**: MTK_AllInOne_DA_v3.3001.2025/11/07
**Size**: 625 KB (639,072 bytes)

This is a signed MediaTek Download Agent compatible with:
- MT6765
- MT6768
- MT6785
- MT6873
- MT6885
- MT6853

### Usage
This DA can be used with mtkclient for flashing operations on MT6768 devices that require signed DA authentication.

## Preloader/preloader_lamu.bin

**Device**: Motorola lamu (Moto E32/E32s)
**Chipset**: MediaTek MT6768
**Type**: Bootloader Preloader
**Size**: 322 KB (328,868 bytes)
**Build**: VVTA35.51-28_lamu-g_user_mv-stable1.2_r-mtk_release-keys

### Purpose
The preloader is the first-stage bootloader that initializes hardware and loads the main bootloader. This file can be used for:
- Firmware analysis
- Boot recovery operations
- Device initialization understanding

## Related Documentation
See `docs/MT6768_ANALYSIS.md` for detailed USB capture analysis and protocol information.

## Hardware Code Information
- **MT6768 Hardware Code**: 0x0707
- **USB VID:PID**: 0x0e8d:0x2000
- **BROM Mode**: Supported
- **DA Mode**: XFLASH (v5)
- **Exploit**: Kamakiri compatible (var1=0x25)
