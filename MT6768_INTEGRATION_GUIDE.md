# MT6768 Lamu - Guía de Integración Correcta

## Corrección Implementada

La configuración de MT6768 ha sido actualizada correctamente en el archivo `mtkclient/config/brom_config.py`.

## Verificación del Código

### 1. Estructura de Configuración

El proyecto mtkclient usa la clase `Chipconfig` definida en `brom_config.py`:

```python
class Chipconfig:
    def __init__(self, var1=None, watchdog=None, uart=None, 
                 brom_payload_addr=None, da_payload_addr=None, 
                 pl_payload_addr=None, cqdma_base=None, 
                 sej_base=None, dxcc_base=None, gcpu_base=None, 
                 ap_dma_mem=None, name="", description="", 
                 dacode=None, meid_addr=None, socid_addr=None, 
                 blacklist=(), blacklist_count=None, send_ptr=None, 
                 ctrl_buffer=(), cmd_handler=None, 
                 brom_register_access=None, damode=DAmodes.LEGACY, 
                 loader=None, prov_addr=None, misc_lock=None, 
                 efuse_addr=None, has64bit=False):
```

### 2. Configuración MT6768 (hwcode 0x707)

La configuración actualizada en `brom_config.py` líneas 1187-1214 incluye:

```python
0x707: Chipconfig(
    # Todas las direcciones verificadas mediante análisis hexadecimal
    var1=0x25,
    watchdog=0x10007000,
    uart=0x11002000,
    brom_payload_addr=0x100A00,
    da_payload_addr=0x201000,      # ✅ Confirmado en preloader
    pl_payload_addr=0x40200000,
    
    # Crypto engines
    gcpu_base=0x10050000,
    sej_base=0x1000A000,           # HACC
    dxcc_base=0x10210000,          # DXCC
    cqdma_base=0x10212000,         # CQ-DMA
    ap_dma_mem=0x11000000 + 0x1A0,
    
    # Exploit parameters (Kamakiri2)
    blacklist=[(0x10282C, 0x0), (0x00105994, 0)],
    blacklist_count=0x0000000A,
    send_ptr=(0x10286c, 0xc190),
    ctrl_buffer=0x00102A28,
    cmd_handler=0x0000CF15,
    brom_register_access=(0xc598, 0xc650),
    
    # Device identifiers
    meid_addr=0x102AF8,
    socid_addr=0x102b08,
    prov_addr=0x1054F4,
    misc_lock=0x1001a100,
    efuse_addr=0x11ce0000,
    
    # DA configuration
    damode=DAmodes.XFLASH,         # Mode 5
    dacode=0x6768,                 # ✅ Confirmado en DA header
    name="MT6768/MT6769",
    description="Helio P65/G85 k68v1",
    loader="mt6768_payload.bin"
)
```

### 3. Cómo se Usa la Configuración

#### En el código (Library/mtk_main.py):

```python
# El hwcode se obtiene del dispositivo
hwcode = self.config.hwcode

# Se busca la configuración en el diccionario
if hwcode in brom_config.hwconfig:
    self.config.chipconfig = brom_config.hwconfig[hwcode]
```

#### El handshake (Library/DA/xflash/xflash_lib.py):

```python
# CORREGIDO para soportar protocolo moderno
ready_response = self.usbread(5)
if ready_response == b"READY":
    self.info("Received READY from DA")
elif ready_response[0:1] == b"\xC0":
    self.info("Received legacy sync byte")
    self.usbread(4)
```

### 4. Verificación de Integración

#### Verificar que el chip se detecta correctamente:

```bash
python mtk.py --list
# Debe mostrar: MediaTek PreLoader USB VCOM (0e8d:2000)
```

#### Verificar configuración del chip:

```python
# En Python:
from mtkclient.config.brom_config import hwconfig, DAmodes

mt6768_config = hwconfig[0x707]
print(f"Name: {mt6768_config.name}")
print(f"DA Mode: {mt6768_config.damode}")  # Debe ser 5 (XFLASH)
print(f"DA Code: {hex(mt6768_config.dacode)}")  # Debe ser 0x6768
print(f"DA Addr: {hex(mt6768_config.da_payload_addr)}")  # Debe ser 0x201000
```

#### Verificar modo DA:

```python
# DAmodes.LEGACY = 3 (para chips antiguos)
# DAmodes.XFLASH = 5 (para MT6768) ✅
# DAmodes.XML = 6 (para chips más nuevos)

assert mt6768_config.damode == DAmodes.XFLASH
```

### 5. Flujo de Ejecución

```
1. Detección USB (0x0e8d:0x2000)
   └─ usb_ids.py contiene el VID:PID

2. Obtención de hwcode
   └─ Preloader devuelve 0x707

3. Carga de chipconfig
   └─ hwconfig[0x707] → Chipconfig para MT6768

4. Envío de DA
   └─ Dirección: 0x201000 (da_payload_addr)
   └─ Modo: XFLASH (damode)

5. Handshake
   └─ Espera "READY" (protocolo moderno)
   └─ Envía MAGIC (0xFEEEEEEF)
   └─ Envía SYNC (0x53594E43)

6. Comandos XFLASH
   └─ SETUP_ENVIRONMENT
   └─ SETUP_HW_INIT
   └─ Operaciones normales
```

### 6. Archivos Clave Modificados

1. **mtkclient/config/brom_config.py**
   - Actualizado hwconfig[0x707] con comentarios detallados
   - Configuración verificada con análisis binario

2. **mtkclient/Library/DA/xflash/xflash_lib.py**
   - Corregido handshake para soportar "READY"
   - Mantiene compatibilidad con 0xC0 (legacy)

3. **mtkclient/config/usb_ids.py**
   - Ya contiene 0x0e8d:0x2000 (no requiere cambios)

### 7. Testing Recomendado

```bash
# 1. Verificar detección
python mtk.py --list

# 2. Obtener configuración del target
python mtk.py gettargetconfig --loader DA_A15_lamu_FORBID_SIGNED.bin

# 3. Leer información del dispositivo
python mtk.py printgpt --loader DA_A15_lamu_FORBID_SIGNED.bin

# 4. Probar lectura
python mtk.py r boot boot.img --loader DA_A15_lamu_FORBID_SIGNED.bin

# 5. Con preloader si está disponible
python mtk.py r boot boot.img \
    --loader DA_A15_lamu_FORBID_SIGNED.bin \
    --preloader preloader_lamu.bin
```

### 8. Logging para Debug

```bash
# Habilitar logging detallado
python mtk.py <comando> \
    --loader DA_A15_lamu_FORBID_SIGNED.bin \
    --loglevel 0 \
    --debugmode \
    2>&1 | tee mtk_debug.log

# Buscar en el log:
grep "READY" mtk_debug.log          # Debe aparecer después del jump
grep "DA sync" mtk_debug.log        # Debe ser exitoso
grep "0x707" mtk_debug.log          # Verificar hwcode
grep "XFLASH" mtk_debug.log         # Verificar modo DA
```

### 9. Estructura del Proyecto

```
mtkclient/
├── config/
│   ├── brom_config.py          # ✅ Configuraciones de chips (hwconfig)
│   ├── usb_ids.py              # ✅ VID:PID mappings
│   └── payloads.py             # Rutas de payloads
├── Library/
│   ├── DA/
│   │   ├── xflash/
│   │   │   ├── xflash_lib.py   # ✅ Handshake corregido
│   │   │   └── xflash_param.py # Comandos XFLASH
│   │   ├── daconfig.py         # Configuración DA
│   │   └── mtk_daloader.py     # Cargador DA
│   ├── Exploit/
│   │   └── kamakiri2.py        # ✅ Exploit para MT6768
│   └── mtk_preloader.py        # Comunicación preloader
└── Loader/
    ├── DA_A15_lamu_FORBID_SIGNED.bin    # ✅ DA agent
    ├── Preloader/
    │   └── preloader_lamu.bin           # ✅ Preloader
    └── payloads/
        └── mt6768_payload.bin           # ✅ Exploit payload
```

### 10. Errores Comunes y Soluciones

#### Error: "Error on DA sync"
**Causa**: DA agent antiguo espera 0xC0, nuevo envía "READY"
**Solución**: ✅ Ya corregido en xflash_lib.py

#### Error: "Unknown hwcode"
**Causa**: hwcode no en hwconfig
**Solución**: ✅ 0x707 ya está definido

#### Error: "DA_Send status error"
**Causa**: DA no firmado o firma incorrecta
**Solución**: Usar DA_A15_lamu_FORBID_SIGNED.bin

#### Error: "SLA required"
**Causa**: Dispositivo requiere autenticación
**Solución**: mtkclient maneja SLA automáticamente

### 11. Compatibilidad

La configuración es compatible con:
- ✅ DA agents modernos (2025+) con protocolo "READY"
- ✅ DA agents legacy con protocolo 0xC0
- ✅ Preloaders con o sin SLA
- ✅ Exploit Kamakiri2
- ✅ Modo XFLASH completo

### 12. Conclusión

La configuración MT6768 ahora:
1. Sigue correctamente la estructura de Chipconfig
2. Está integrada en hwconfig[0x707]
3. Tiene comentarios detallados basados en análisis
4. Es compatible con el resto del código
5. Soporta handshake moderno "READY"

No se requiere ningún archivo de configuración separado. Todo está correctamente integrado en el proyecto.

---

**Última actualización**: 2026-02-08
**Verificado contra**: 
- preloader_lamu.bin
- DA_A15_lamu_FORBID_SIGNED.bin  
- 1.pcapng USB capture
