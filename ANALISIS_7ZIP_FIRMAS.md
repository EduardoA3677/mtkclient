# Análisis Completo con 7zip - Firmas y Extracción

## Resumen Ejecutivo

**Método**: Extracción con 7zip + análisis de firmas  
**Archivos extraídos**: 8 particiones exitosas  
**Device ID completo**: ✅ ENCONTRADO  
**Private Keys**: ❌ No encontradas  

---

## 🔍 Firmas Encontradas

### Particiones con Datos Comprimidos

#### blackbox.bin ✅
```
Firmas: GZIP (1f 8b)
Extraído: Logs del sistema
  - fatal_log/
  - poweron_log/
  - rescue_log/
```

#### elabel.bin ✅
```
Firmas: Sistema de archivos ext2/ext4
Extraído: regulatory_info.png
```

#### expdb.bin ✅
```
Firmas: ZIP (50 4b), GZIP (1f 8b), BZIP2 (42 5a)
Extraído: expdb (519 KB - Exception database)
```

#### nvcfg.bin ✅
```
Firmas: ZIP (50 4b)
Extraído: Configuración del modem
  - fg/ (fuel gauge)
  - sensor/
  - simlock/
```

#### nvdata.bin ✅ ⭐
```
Firmas: BZIP2 (42 5a) - ULBZ format
Extraído: **DATOS CRÍTICOS DEL DEVICE**
  - APCFG/ (WiFi, BT, calibración)
  - md/NVRAM/NVD_IMEI/ ← **IMEI AQUÍ**
  - AllFile, AllMap
```

#### persist.bin ✅ ⭐
```
Firmas: GZIP (1f 8b)
Extraído: **Device attestation**
  - keybox/attestation_ids.so
  - keybox/attest_keybox.so
  - mcRegistry/
```

#### protect1.bin ✅
```
Extraído: Datos de calibración del modem
  - md/ (archivos calibración)
```

#### protect2.bin ✅
```
Firmas: ZIP (50 4b)
Extraído: Backup de calibración del modem
```

---

## 📊 DEVICE ID COMPLETO ENCONTRADO

### IMEI (DE NVDATA)
```
Archivo: nvdata/md/NVRAM/NVD_IMEI/CSKA_000
Offset: 0x50

IMEI: 359488357396203
Checksum Luhn: 0 (válido)
Formato: 15 dígitos estándar
Estado: ✅ VÁLIDO
```

### Serial Number (DE PROINFO)
```
Serial: ZY32LNRW97
Ubicación: proinfo.bin @ 0x0000
Hex: 5A5933324C4E52573937
```

### Barcode
```
Barcode: VEKRL52ZJD
Ubicación: proinfo.bin @ 0x0200
```

### Product Code
```
Product: amxmx
Ubicación: proinfo.bin @ 0x0210
También en: nvdata CSKA_000 @ 0x40
```

### Chip ID
```
Chip ID: 53498853376902f3
Ubicación: proinfo.bin @ 0x0040
Tipo: MediaTek MT6768
```

### WiFi MAC
```
MAC: 00:62:01:8a:ed:b2
Archivo: nvdata/APCFG/APRDEB/WIFI
Offset: 0x05
```

### Bluetooth MAC
```
MAC: 00:62:01:8a:ed:b1:60
Archivo: nvdata/APCFG/APRDEB/BT_Addr
Offset: 0x00
```

---

## 🔐 Análisis de Private Keys

### Archivos de Attestation (Keybox)

#### persist/keybox/attestation_ids.so (792 bytes)
```
Tipo: Android Device Attestation data
Contenido: Encriptado/Binario
Propósito: Hardware-backed key attestation
Acceso: Solo TrustZone/TEE
```

#### persist/keybox/attest_keybox.so (8.6 KB)
```
Tipo: Hardware keybox data
Contenido: Certificados device attestation
Propósito: Google SafetyNet/Play Integrity
Acceso: Solo secure element
```

**Conclusión**: Estos archivos contienen certificados de attestation, NO claves privadas para unlock.

### Archivos IMEI Encriptados

#### NVD_IMEI/NV0S_000, NV01_000, LD0B_001
```
Contenido: IMEI encriptado (binario)
Formato: Encriptación propietaria MTK
Clave: Solo conocida por modem firmware
```

#### NVD_IMEI/CSTS_000 ⭐
```
Contenido: SIM Test data + IMEI en CLARO
IMEI ASCII: "359488357396203"
También contiene: Test strings hex-encoded
```

---

## 💡 Reconstrucción de get_unlock_data

### Datos Completos Disponibles

```
✅ Header base: 0A40040192024205 (estándar Motorola)
✅ IMEI: 359488357396203
✅ Serial: ZY32LNRW97
✅ Product: amxmx
✅ Chip ID: 53498853376902f3
❌ Signature: Requiere bootloader
❌ Timestamp/Nonce: Requiere bootloader
```

### Formato Reconstruido (EXPERIMENTAL)

```
Parte 1 (Header): 0A40040192024205
Parte 2 (IMEI + Serial hex):
  IMEI: 333539343838333537333936323033 (hex)
  Serial: 5A5933324C4E52573937 (hex)
Parte 3 (Signature): [FALTA - 40 hex chars]
Parte 4 (Nonce): [FALTA - 31 hex chars]
```

### Unlock Data Reconstruido
```
(bootloader) 0A40040192024205#33353934383833
(bootloader) 35373339363230335A5933324C4E5257
(bootloader) 3937#00000000000000000000000000
(bootloader) 000000000000000#0000000000000000
(bootloader) 000000000000000
```

### ⚠️ ADVERTENCIA CRÍTICA

**Este unlock_data NO FUNCIONARÁ** porque:

1. Signature es ceros (inválida)
2. Nonce/Timestamp son ceros (inválido)
3. Motorola valida la firma criptográfica en backend
4. **La firma solo puede generarse con clave privada del bootloader**

**Probabilidad de éxito: 0%**

---

## 🔬 Análisis de Firmas Crypto

### Firmas de Archivos Comprimidos Encontradas

| Firma | Hex | Archivos |
|-------|-----|----------|
| GZIP | 1F 8B | blackbox, persist, nvdata (parcial) |
| ZIP | 50 4B | expdb, nvcfg, protect2, lk_a/b (falsos positivos) |
| BZIP2 | 42 5A | expdb, nvdata |
| ANDROID! | 41 4E 44 52 4F 49 44 21 | lk_a, lk_b (boot images) |
| ELF | 7F 45 4C 46 | lk_a, lk_b (ejecutables) |

### Firmas NO Encontradas
```
❌ LZ4 (04 22 4D 18)
❌ XZ (FD 37 7A 58 5A)
❌ RSA Private Key (-----BEGIN)
❌ PEM Certificate
```

---

## 📋 Archivos NO Extraíbles

**Razón**: No son archivos comprimidos, son datos binarios raw

| Archivo | Propósito | Formato |
|---------|-----------|---------|
| boot_para.bin | Parámetros de boot | Binario MTK |
| efuse.bin | Hardware fuses | Binario (0xAA) |
| frp.bin | Factory Reset Protection | Encriptado |
| lk_a.bin / lk_b.bin | Little Kernel bootloader | ELF + boot.img |
| proinfo.bin | Product info | Binario estructurado |
| seccfg.bin | Security config | Encriptado AES |
| sec1.bin | Security data | Binario |

---

## ✅ Información Completa del Device

### Para Motorola Support
```
IMEI: 359488357396203 ⭐
Serial: ZY32LNRW97
Barcode: VEKRL52ZJD
Product: amxmx
Chip: MT6768 (53498853376902f3)
WiFi MAC: 00:62:01:8a:ed:b2
BT MAC: 00:62:01:8a:ed:b1:60
```

### Firmado Firmware
```
Modem FW: MOLY.LR12A.R3.MP.V340.4.P15
Build Date: 2025/01/07 17:50
Target: LAMU
```

---

## 🎯 Conclusiones Finales

### Lo que SÍ se encontró ✅
- ✅ IMEI completo y válido
- ✅ Serial Number
- ✅ Barcode
- ✅ Product code
- ✅ WiFi/BT MACs
- ✅ Chip ID
- ✅ Firmware version
- ✅ Attestation keybox data

### Lo que NO se encontró ❌
- ❌ Private key del bootloader
- ❌ Clave AES de seccfg
- ❌ Signature key para get_unlock_data
- ❌ IMEI no encriptado en proinfo (solo en nvdata)

### Por Qué NO se puede generar unlock_data válido

**Razones técnicas**:

1. **Signature missing**: La firma requiere:
   - Clave privada RSA del bootloader (en secure element)
   - Solo accesible por bootloader en runtime
   - NO está en ninguna partición flash

2. **Timestamp/Nonce missing**: 
   - Generado dinámicamente por bootloader
   - Incluye time seed + random nonce
   - Previene replay attacks

3. **Backend validation**:
   - Motorola valida firma en servidor
   - Rechaza firmas inválidas o falsas
   - No hay bypass posible

---

## 📊 Scripts Creados

### reconstruct_unlock_data.py
```python
# Script para reconstruir unlock_data experimental
# Ubicación: /home/runner/work/mtkclient/mtkclient/
# Uso: python3 reconstruct_unlock_data.py
```

**Funciones**:
- Analiza proinfo.bin
- Busca IMEI en nvdata
- Genera unlock_data formato bootloader
- Advertencias sobre validez

---

## 🎊 Recomendación Final

### Para Obtener Unlock Real

**Opción 1: Reparar Bootloader** ⭐⭐⭐⭐⭐
```bash
1. Flash firmware stock con SP Flash Tool
2. Incluir: preloader, lk_a, lk_b, boot, etc.
3. Boot device normalmente
4. fastboot oem get_unlock_data
5. Usar código REAL en portal Motorola
```

**Opción 2: Contactar Motorola** ⭐⭐⭐⭐☆
```
IMEI: 359488357396203
Serial: ZY32LNRW97
Link: https://motorola-global-portal.custhelp.com/

Con proof of purchase:
- Motorola puede verificar con IMEI/Serial
- Unlock sin bootloader funcional
- Servicio oficial gratuito
```

**Opción 3: Servicios Terceros** ⭐⭐☆☆☆
```
⚠️ Algunos servicios pueden unlock con IMEI
Verificar reputación
Costo variable ($10-50 USD típicamente)
Bajo tu propio riesgo
```

---

## 🔬 Herramientas Utilizadas

```bash
# Extracción
7z x archivo.bin -ooutput/

# Análisis hex
hexdump -C archivo.bin

# Búsqueda de strings
strings archivo.bin

# Búsqueda de patrones
grep -E 'pattern' archivo.bin

# Scripts custom
- analyze_extracted.sh
- decode_imei.py
- reconstruct_unlock_data.py
```

---

## ✅ Conclusión

**Device ID COMPLETO encontrado**, incluyendo IMEI que estaba encriptado en proinfo pero en claro en nvdata.

**Unlock_data NO puede generarse sin bootloader** porque requiere firma criptográfica que solo el bootloader puede crear.

**Mejor solución**: Reparar bootloader → obtener unlock_data real → unlock oficial Motorola

---

**Documento generado**: 2026-02-09  
**Herramientas**: 7zip, hexdump, strings, Python  
**Estado**: Análisis completo con IMEI encontrado ✅  
**Commits**: 60 total en el PR
