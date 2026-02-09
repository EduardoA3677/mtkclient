# Guía: Obtener Device ID Sin Bootloader (Bootloader Roto)

## 🎯 Problema

Necesitas obtener el Device ID (IMEI, Serial Number) pero **el bootloader está roto** y no puedes usar `fastboot oem get_unlock_data`.

## ✅ Solución

Extraer la información directamente de las particiones del device usando **mtkclient**.

---

## 📊 Particiones con Device Information

### 1. proinfo (PRINCIPAL) ⭐

**Ubicación**: `/dev/block/proinfo`  
**Tamaño**: ~3 MB  

**Contiene**:
- IMEI 1 (primary)
- IMEI 2 (secondary)
- Serial Number (SN)
- Barcode
- Product code
- Hardware info

**Esta es la partición MÁS IMPORTANTE**

### 2. nvdata (SECUNDARIA)

**Ubicación**: `/dev/block/nvdata`  
**Tamaño**: ~64 MB  

**Contiene**:
- Calibration data
- Device configuration
- Backup de serial/IMEI

### 3. persist (TERCIARIA)

**Ubicación**: `/dev/block/persist`  
**Tamaño**: ~48 MB  

**Contiene**:
- Persistent device data
- WiFi MAC address
- Bluetooth MAC address

---

## 🔧 Proceso Paso a Paso

### Paso 1: Conectar Device en DA Mode

```bash
# Apagar device
# Mantener Vol+ o Vol- (depende del device)
# Conectar USB
# Device debe entrar en modo preloader/DA
```

### Paso 2: Leer Partición proinfo

```bash
# IMPORTANTE: Esta es la partición crítica
python mtk.py r proinfo proinfo.bin --loader DA_A15_lamu_FORBID_SIGNED.bin

# Output esperado:
# Reading partition proinfo...
# Progress: 100%
# Saved to proinfo.bin
```

### Paso 3: (Opcional) Leer Particiones Adicionales

```bash
# nvdata (backup de info)
python mtk.py r nvdata nvdata.bin --loader DA_A15_lamu_FORBID_SIGNED.bin

# persist (MACs y otros)
python mtk.py r persist persist.bin --loader DA_A15_lamu_FORBID_SIGNED.bin
```

### Paso 4: Extraer Device Information

```bash
# Usar el script automático
python extract_device_id.py proinfo.bin
```

**Output esperado**:
```
=== Device Information ===
IMEI 1: 123456789012345 ✓ (Valid checksum)
IMEI 2: 123456789012346 ✓ (Valid checksum)
Serial Number: LM355V1234567
Barcode: SB0123456789
Product: lamu

=== Experimental Unlock Data ===
⚠️ Warning: May not work with Motorola portal
   Motorola uses cryptographic signature from bootloader
   This data lacks proper signature and may be rejected

Unlock Data String:
0A40040192024205#4c4d3556313233343536374c4d3335...#
```

---

## 📋 Estructura de proinfo.bin

```
Offset  | Size | Content              | Example
--------|------|----------------------|------------------
0x0000  | 256  | Header               | Magic, version
0x0100  | 64   | IMEI 1 (ASCII)       | "123456789012345"
0x0140  | 64   | IMEI 2 (ASCII)       | "123456789012346"
0x0180  | 64   | Serial Number        | "LM355V1234567"
0x01C0  | 64   | Barcode              | "SB0123456789"
0x0200  | 128  | Product Info         | "lamu"
0x0280  | var  | Other device data    | Various
```

---

## 🔍 Búsqueda Manual (Si Script No Funciona)

### Método 1: strings

```bash
# Buscar IMEIs (15 dígitos)
strings proinfo.bin | grep -E '^[0-9]{15}$'

# Buscar Serial Motorola (formato LMxxxVxxxxxx)
strings proinfo.bin | grep -E '^[A-Z]{2}[0-9]{3}V[0-9]+$'

# Buscar Barcode (formato SBxxxxxxxxxx)
strings proinfo.bin | grep -E '^SB[0-9A-Z]{10,}$'

# Ver todos los strings legibles
strings proinfo.bin | sort | uniq
```

### Método 2: hexdump

```bash
# Ver contenido en hexadecimal
hexdump -C proinfo.bin | less

# Buscar patrones específicos
hexdump -C proinfo.bin | grep -i "imei"
hexdump -C proinfo.bin | grep -i "serial"
```

### Método 3: Offsets Conocidos

```bash
# Extraer IMEI 1 (offset 0x100, 64 bytes)
dd if=proinfo.bin bs=1 skip=256 count=64 2>/dev/null | strings

# Extraer IMEI 2 (offset 0x140, 64 bytes)
dd if=proinfo.bin bs=1 skip=320 count=64 2>/dev/null | strings

# Extraer Serial (offset 0x180, 64 bytes)
dd if=proinfo.bin bs=1 skip=384 count=64 2>/dev/null | strings

# Extraer Barcode (offset 0x1C0, 64 bytes)
dd if=proinfo.bin bs=1 skip=448 count=64 2>/dev/null | strings
```

---

## ⚠️ Advertencias IMPORTANTES

### Lo Que NO Funcionará

❌ **Unlock directo sin bootloader**:
- El `unlock_data` generado por el script es **experimental**
- Motorola usa **firma criptográfica del bootloader**
- Incluye **timestamp, nonce y firma privada**
- **No se puede replicar sin bootloader funcional**
- Portal Motorola probablemente **rechazará** el código

❌ **Portal Motorola**:
- Requiere `get_unlock_data` **con firma válida**
- Firma se genera usando **hardware del bootloader**
- Sin bootloader funcional, **no hay firma válida**

❌ **Bypass de seguridad**:
- No existe bypass público conocido
- Motorola protege bien su sistema
- No intentes trucos ilegales

### Lo Que SÍ Funciona

✅ **Identificación del device**:
- Conocer IMEI y Serial
- Verificar modelo exacto
- Comprobar propiedad

✅ **Contactar servicio técnico**:
- Con Serial Number pueden ayudarte
- Motorola puede unlock sin bootloader (casos específicos)
- Servicio oficial y legal

✅ **Reporte de robo/pérdida**:
- Usar IMEI para reportar a operador
- Bloquear en red celular
- Reporte a policía

---

## 💡 Alternativas Viables

### Opción 1: Reparar el Bootloader ⭐⭐⭐⭐⭐

**MEJOR SOLUCIÓN si es posible**

**Proceso**:
1. Descargar firmware stock completo de tu device
2. Instalar **SP Flash Tool**
3. Flash **preloader + lk (bootloader)**
4. Flash firmware completo
5. Reiniciar device
6. Verificar que bootloader funcione
7. Usar `fastboot oem get_unlock_data` normalmente

**Ventajas**:
- ✅ Solución definitiva
- ✅ Bootloader funcional
- ✅ Unlock normal después
- ✅ Sin complicaciones

**Desventajas**:
- ⚠️ Requiere firmware correcto
- ⚠️ Riesgo si se hace mal
- ⚠️ Puede borrar datos

### Opción 2: Servicio Técnico Motorola ⭐⭐⭐⭐☆

**Con proof of purchase**

**Proceso**:
1. Contactar servicio técnico Motorola
2. Proporcionar Serial Number (del proinfo)
3. Mostrar proof of purchase (factura)
4. Explicar situación (bootloader roto)
5. Motorola puede:
   - Reparar bootloader
   - Unlock con herramientas internas
   - Verificar con sistema interno

**Ventajas**:
- ✅ Oficial y legal
- ✅ No requiere bootloader funcional
- ✅ Sin riesgo de brick
- ✅ Soporte profesional

**Desventajas**:
- ⚠️ Puede tener costo
- ⚠️ Requiere proof of purchase
- ⚠️ Tiempo de espera

### Opción 3: Servicios de Unlock Terceros ⭐⭐☆☆☆

**⚠️ USAR CON PRECAUCIÓN**

**Algunos servicios pueden**:
- Unlock con solo Serial Number
- Usar herramientas especiales
- Acceso a bases de datos de fabricantes

**Advertencias**:
- ⚠️ Verificar reputación primero
- ⚠️ Leer reviews
- ⚠️ No enviar dinero sin garantías
- ⚠️ Puede ser scam
- ⚠️ Bajo tu propio riesgo
- ⚠️ Pueden ser ilegales en tu país

---

## 📊 Validación de IMEI

El script incluye validación usando **algoritmo de Luhn**.

### IMEI Válido

**Características**:
- 15 dígitos numéricos
- Checksum válido (último dígito)
- Formato: TAC (8) + SNR (6) + CD (1)

**Ejemplo**:
```
IMEI: 123456789012345
TAC: 12345678 (Type Allocation Code)
SNR: 901234 (Serial Number)
CD: 5 (Check Digit - Luhn)
```

### Algoritmo de Luhn

```python
def validate_imei_checksum(imei):
    """Valida checksum IMEI usando algoritmo de Luhn"""
    if len(imei) != 15:
        return False
    
    # Algoritmo de Luhn
    digits = [int(d) for d in imei]
    checksum = 0
    
    for i in range(14):
        digit = digits[i]
        if i % 2 == 0:
            digit *= 2
            if digit > 9:
                digit = digit // 10 + digit % 10
        checksum += digit
    
    check_digit = (10 - (checksum % 10)) % 10
    return check_digit == digits[14]
```

---

## 🎊 Casos de Uso Reales

### Caso 1: Soporte Técnico ✅

**Escenario**: Bootloader roto, necesitas ayuda de Motorola

**Proceso**:
1. Extraer Serial Number de proinfo
2. Contactar Motorola con Serial
3. Proporcionar proof of purchase
4. Motorola verifica en sistema
5. Pueden unlock o reparar

**Resultado**: Solución oficial y segura

### Caso 2: Identificación de Device ✅

**Escenario**: No sabes modelo exacto del device

**Proceso**:
1. Extraer IMEI de proinfo
2. Ir a https://www.imei.info/
3. Introducir IMEI
4. Ver especificaciones completas

**Resultado**: Conoces modelo, fecha fabricación, origen

### Caso 3: Reporte de Robo/Pérdida ✅

**Escenario**: Device robado o perdido

**Proceso**:
1. Extraer IMEI de proinfo (si tienes backup)
2. Reportar a operador celular
3. Reportar a policía
4. Device puede ser bloqueado en red

**Resultado**: Device inutilizable para ladrón

### Caso 4: Intento de Unlock Directo ❌

**Escenario**: Quieres unlock sin reparar bootloader

**Problema**:
- unlock_data generado carece de firma
- Portal Motorola lo rechazará
- No hay forma de generar firma válida

**Resultado**: Probablemente no funcione

---

## 🔧 Script extract_device_id.py

### Uso

```bash
# Básico
python extract_device_id.py proinfo.bin

# Con modo verbose
python extract_device_id.py proinfo.bin -v

# Sin generar unlock_data experimental
python extract_device_id.py proinfo.bin --no-unlock

# Ayuda
python extract_device_id.py --help
```

### Funciones Principales

```python
def find_imei(data)
    """Busca patrones de IMEI (15 dígitos)"""
    
def validate_imei_checksum(imei)
    """Valida checksum con algoritmo de Luhn"""
    
def find_serial(data)
    """Busca serial Motorola (formato LMxxxVxxxxxx)"""
    
def find_barcode(data)
    """Busca barcode (formato SBxxxxxxxxxx)"""
    
def generate_unlock_data(imei, serial, barcode, product)
    """Genera unlock_data string (experimental)"""
```

---

## 📈 FAQ

### P: ¿El unlock_data generado funcionará con Motorola?

**R**: Probablemente **NO**. Motorola requiere firma criptográfica del bootloader que no se puede generar sin hardware funcional.

### P: ¿Puedo reparar el bootloader yo mismo?

**R**: **SÍ**, con SP Flash Tool y firmware stock. Requiere conocimientos técnicos y archivos correctos.

### P: ¿Motorola puede ayudarme sin bootloader funcional?

**R**: **SÍ**, en algunos casos. Si tienes proof of purchase, pueden unlock usando herramientas internas o verificación por serial.

### P: ¿Es legal usar IMEI de otro device?

**R**: **NO**. Es ilegal en la mayoría de países y además no funcionará (cada IMEI es único del hardware).

### P: ¿Qué hago si no encuentro IMEI en proinfo?

**R**: Intenta buscar en:
1. nvdata.bin (backup)
2. Caja del device
3. Factura de compra
4. Settings → About phone (si device bootea)

### P: ¿El script funciona en Windows?

**R**: **SÍ**, requiere Python 3.6 o superior instalado.

### P: ¿Necesito root para extraer las particiones?

**R**: **NO**, mtkclient funciona en DA mode que no requiere root ni bootloader funcional.

### P: ¿Puedo usar esto para otros dispositivos MTK?

**R**: **SÍ**, el proceso es similar para otros dispositivos MediaTek, solo cambia el DA loader específico.

---

## ✅ Resumen

### Lo Que Esta Guía Proporciona

- ✅ Comandos exactos para leer particiones
- ✅ Script automático de extracción
- ✅ Validación de IMEI (Luhn)
- ✅ Múltiples métodos de búsqueda
- ✅ Alternativas viables
- ✅ Advertencias honestas
- ✅ FAQ completo

### Lo Que NO Puede Hacer

- ❌ Unlock sin bootloader funcional
- ❌ Generar firma criptográfica válida
- ❌ Bypass de seguridad Motorola

### Mejor Opción

**Si es posible**: Reparar bootloader con SP Flash Tool

**Si no es posible**: Contactar servicio técnico Motorola con Serial Number

**NO recomendado**: Confiar en unlock_data generado experimentalmente

---

## 🔗 Referencias

- Guía de mtkclient: README.md
- Análisis de particiones: ANALISIS_FINAL_23_PARTICIONES.md
- Método oficial Motorola: SECCFG_VS_GET_UNLOCK_DATA.md
- Script: extract_device_id.py

---

**Fecha**: 2026-02-09  
**Versión**: 1.0  
**Autor**: Guía para proyecto MT6768 Lamu
