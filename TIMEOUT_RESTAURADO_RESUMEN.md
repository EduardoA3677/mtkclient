# Timeout Restaurado y Jump Mejorado ✅

## Cambios Realizados

### 1. ✅ Timeout Restaurado al Original

**Ubicación**: `mtkclient/Library/DA/xflash/xflash_lib.py` línea 970

**ANTES** (modificado):
```python
self.info("Waiting for DA to initialize and respond...")
ready_response = self.usbread(5, maxtimeout=30)  # 3 segundos
```

**AHORA** (original):
```python
ready_response = self.usbread(5)  # Usa timeout por defecto
```

**Timeout Original**: 100 reintentos = ~10 segundos (como estaba antes de TODAS las modificaciones)

### 2. ✅ Logging Mejorado en Jump

**Ubicación**: `mtkclient/Library/mtk_preloader.py` líneas 682-714

**Agregado**:
- Debug después de recibir dirección
- Debug antes de leer status
- Debug después de recibir status
- Mensajes de error mejorados

**Salida Esperada** (jump exitoso):
```
Preloader - Jumping to 0x200000
Preloader - Jump_DA: Received address response: 0x200000
Preloader - Jump_DA: Address confirmed, reading status...
Preloader - Jump_DA: Received status: 0x0
Preloader - Jumping to 0x200000: ok.
```

**Salida de Error** (mostrará dónde falla):
```
Preloader - Jumping to 0x200000
Preloader - Jump_DA: echo command failed
```
O
```
Preloader - Jumping to 0x200000
Preloader - Jump_DA: Received address response: 0x200000
Preloader - Jump_DA: Address confirmed, reading status...
[timeout o error]
Preloader - Jump_DA No data available [error details]
```

## Problema Original

El usuario reportó:
1. "Restaura el timeout como el original" ✅ HECHO
2. "Corrije el jumping" ✅ Agregado debug logging para identificar el problema

El log mostraba:
```
Preloader - Jumping to 0x200000
[SE DETIENE AQUÍ]
```

No mostraba "ok", lo que indica que algo falla en el proceso de jump.

## Diagnóstico

Con los nuevos mensajes de debug, ahora veremos exactamente dónde falla:

1. **Si falla en echo**: "Jump_DA: echo command failed"
2. **Si falla dirección**: "Jump_DA address mismatch: expected X, got Y"
3. **Si falla status**: Mostrará el error de timeout o el status incorrecto

## Prueba el Comando

```bash
python mtk.py da seccfg unlock --loader mtkclient\Loader\DA_A15_lamu_FORBID_SIGNED.bin
```

Con `--debugmode` para ver los mensajes debug:
```bash
python mtk.py da seccfg unlock --loader mtkclient\Loader\DA_A15_lamu_FORBID_SIGNED.bin --debugmode
```

## Posibles Causas del Problema de Jump

Si sigue fallando después de estos cambios, las causas pueden ser:

1. **Timeout en rdword()**: El dispositivo no responde con la dirección
2. **Timeout en rword()**: El dispositivo no responde con el status
3. **Status != 0**: El DA retorna un error (no 0)
4. **USB desconectado**: El dispositivo se desconecta durante el jump

Los nuevos mensajes de debug mostrarán exactamente cuál es el problema.

## Estado

- ✅ Timeout restaurado a valor original (100 reintentos = ~10 segundos)
- ✅ Mensajes de "Waiting for DA..." removidos
- ✅ Comentarios sobre timeout removidos
- ✅ Debug logging agregado a jump_da()
- ✅ Mensajes de error mejorados

**Commit**: ff948f1
**Archivos modificados**: 2 (xflash_lib.py, mtk_preloader.py)
**Listo para probar**: ✅ SÍ
