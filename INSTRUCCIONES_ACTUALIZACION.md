# 📥 Instrucciones de Actualización - Fix GUI Pagesize

## ⚠️ Problema

Error en GUI al leer particiones:
```
TypeError: unsupported operand type(s) for //: 'Mock' and 'int'
File "mtkclient\Library\DA\mtk_da_handler.py", line 474
```

## ✅ Solución

El fix ya está implementado en el branch `copilot/update-mt6768-support` (commit 59c9ce5).

**Necesitas actualizar tu código local.**

---

## 📋 Opción 1: Git Pull (RECOMENDADO)

### Paso 1: Abrir terminal en el directorio

```bash
cd C:\Users\Eduardo\mtkclient
```

### Paso 2: Hacer fetch

```bash
git fetch origin
```

### Paso 3: Cambiar a branch correcto

```bash
git checkout copilot/update-mt6768-support
```

### Paso 4: Actualizar

```bash
git pull origin copilot/update-mt6768-support
```

### Paso 5: Verificar

```bash
git log --oneline -5
```

Deberías ver:
```
2e12d76 Add update instructions for GUI pagesize fix
cec0509 Final partition analysis: flashinfo, mrdump, otp
bf9ce12 Add comprehensive documentation for GUI pagesize Mock fix
59c9ce5 Fix GUI crash: Handle Mock pagesize in flash operations
```

---

## 📋 Opción 2: Descargar ZIP

### Paso 1: Hacer backup de tu código actual

```bash
# Copiar todo el directorio
xcopy C:\Users\Eduardo\mtkclient C:\Users\Eduardo\mtkclient_backup\ /E /I /H /Y
```

### Paso 2: Descargar el ZIP

1. Abrir: https://github.com/EduardoA3677/mtkclient/tree/copilot/update-mt6768-support
2. Click en botón verde "Code"
3. Click en "Download ZIP"
4. Guardar como `mtkclient-copilot-update-mt6768-support.zip`

### Paso 3: Extraer y reemplazar

```bash
# Extraer el ZIP
# Copiar contenido a C:\Users\Eduardo\mtkclient\
# Reemplazar cuando pregunte
```

---

## 📋 Opción 3: Fix Manual (Si git no funciona)

### Archivo a editar

`C:\Users\Eduardo\mtkclient\mtkclient\Library\DA\mtk_da_handler.py`

### Paso 1: Agregar método helper

**Buscar línea ~67** (después de `def __init__`):

```python
def get_pagesize(self):
    """Safely get pagesize, handling Mock objects or invalid values"""
    pagesize = self.config.pagesize
    if not isinstance(pagesize, int) or pagesize <= 0:
        return 512  # default fallback
    return pagesize
```

### Paso 2: Actualizar método da_rf()

**Buscar línea ~470** (dentro de `def da_rf`):

**CAMBIAR:**
```python
if display:
    print(
        f"Dumping sector {addr // self.config.pagesize}/addr {hex(addr)} with flash size {hex(length)} as {filename}.")
```

**POR:**
```python
pagesize = self.get_pagesize()

if display:
    print(
        f"Dumping sector {addr // pagesize}/addr {hex(addr)} with flash size {hex(length)} as {filename}.")
```

**Y también en línea ~478:**
```python
if display:
    print(
        f"Dumped sector {addr // pagesize}/addr {hex(addr)} with flash size {hex(length)} as {filename}.")
```

### Paso 3: Actualizar método da_rs()

**Buscar línea ~486** (dentro de `def da_rs`):

**CAMBIAR:**
```python
for sector in range(offset // self.config.pagesize, ...
```

**POR:**
```python
pagesize = self.get_pagesize()
for sector in range(offset // pagesize, ...
```

### Paso 4: Actualizar loops de write/format

**Buscar líneas ~680-693 y ~716-739**:

Agregar al inicio de cada loop:
```python
pagesize = self.get_pagesize()
```

Y cambiar todas las ocurrencias de `self.config.pagesize` por `pagesize`

---

## 🔍 Verificación

### Verificar que el fix está aplicado

```python
# Abrir Python
import os
os.chdir(r'C:\Users\Eduardo\mtkclient')

# Buscar el método
with open('mtkclient/Library/DA/mtk_da_handler.py', 'r') as f:
    content = f.read()
    if 'def get_pagesize(self):' in content:
        print("✅ Método get_pagesize() encontrado")
    else:
        print("❌ Método get_pagesize() NO encontrado - aplicar fix")
    
    if 'pagesize = self.get_pagesize()' in content:
        print("✅ Uso de get_pagesize() encontrado")
    else:
        print("❌ Uso de get_pagesize() NO encontrado - aplicar fix")
```

---

## ✅ Después de Actualizar

### Paso 1: Cerrar GUI

Si `mtk_gui` está abierto, cerrarlo completamente.

### Paso 2: Ejecutar de nuevo

```bash
cd C:\Users\Eduardo\mtkclient
.\mtk_gui.bat
```

### Paso 3: Probar lectura de partición

1. Abrir GUI
2. Click en "Read flash partitions"
3. Seleccionar partición (ej: boot)
4. Click "Read"
5. ✅ Debe funcionar sin errores

---

## 🎯 Si el Error Persiste

### Diagnóstico

1. **Verificar versión del código**
   ```bash
   git log --oneline -1
   # Debe mostrar: 2e12d76 Add update instructions...
   ```

2. **Verificar archivo modificado**
   ```bash
   git diff HEAD~4 mtkclient/Library/DA/mtk_da_handler.py
   # Debe mostrar los cambios del fix
   ```

3. **Verificar que Python usa el código correcto**
   ```python
   import mtkclient.Library.DA.mtk_da_handler as handler
   print(handler.__file__)
   # Debe apuntar a tu directorio
   ```

### Si nada funciona

1. Desinstalar completamente Python
2. Reinstalar Python 3.9+
3. Reinstalar dependencias: `pip install -r requirements.txt`
4. Aplicar fix manual completo
5. O usar versión anterior sin GUI (CLI funciona)

---

## 📞 Soporte

Si después de seguir todos los pasos el error persiste:

1. Compartir output de:
   ```bash
   git log --oneline -5
   git status
   ```

2. Compartir líneas 460-490 de `mtk_da_handler.py`

3. Compartir traceback completo del error

---

**Actualizado**: 2026-02-08  
**Commit con fix**: 59c9ce5  
**Branch**: copilot/update-mt6768-support  
**Status**: Fix disponible, usuario debe actualizar
