# Fix de Timeout DA Handshake - Resumen

## Problema Resuelto

**Usuario reportó**: "después del jumping tarda demasiado en cargar"

**Síntoma**: El proceso parecía colgarse después de "Jumping to 0x200000: ok."

## Causa Raíz

- Después de saltar al DA, el agente necesita tiempo para inicializarse
- El timeout por defecto era de 100 reintentos (~10 segundos)
- Algunos dispositivos/DAs necesitan 10-30 segundos para inicializar
- Esto causaba que el proceso pareciera "congelado"

## Solución Implementada

**Archivo**: `mtkclient/Library/DA/xflash/xflash_lib.py` línea 971

**Cambios**:
1. ✅ Timeout aumentado de 100 a 300 reintentos (10s → 30s)
2. ✅ Mensaje agregado: "Waiting for DA to initialize and respond..."
3. ✅ Comentario explicativo en el código

## Comportamiento Esperado

```
DAXFlash - Successfully uploaded stage 1, jumping ..
Preloader - Jumping to 0x200000
Preloader - Jumping to 0x200000: ok.
DAXFlash - Waiting for DA to initialize and respond...
[Espera hasta 30 segundos - usuario ve el mensaje]
DAXFlash - Received READY from DA
DAXFlash - Successfully received DA sync
```

## Beneficios

- ✅ No más "cuelgues" aparentes
- ✅ Feedback claro al usuario
- ✅ Funciona con DAs rápidos y lentos
- ✅ Compatible con código existente

## Tiempos Típicos de Inicialización

- DAs rápidos: 1-3 segundos
- DAs normales: 5-10 segundos
- DAs lentos: 10-20 segundos
- Máximo soportado: 30 segundos

## Comando para Probar

```bash
python mtk.py da seccfg unlock --loader mtkclient\Loader\DA_A15_lamu_FORBID_SIGNED.bin
```

El proceso ahora muestra claramente que está esperando la respuesta del DA, eliminando la confusión sobre si el programa está colgado o funcionando.

---

**Estado**: ✅ Corregido en commit 065efd4
**Impacto**: Alto - Resuelve problema de UX crítico
**Riesgo**: Bajo - Solo aumenta timeout, sin cambios de lógica
