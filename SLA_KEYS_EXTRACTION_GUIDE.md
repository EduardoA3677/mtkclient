# Extracción de Claves SLA para MT6768 Lamu

## Situación Actual

El dispositivo MT6768 (lamu) tiene **SLA (Secure Link Authentication)** habilitado, como se confirmó en el análisis del PCAPNG:

```
Frame 93469: Challenge enviado
  Comando: 0x0820201f
  Challenge: 22defb438025b98431868a1a0b9df3706584719167971c15

Frame 93527: Response recibido
  Comando: 0x052006d1  
  Response: 3f76e5ee37
```

## ¿Qué son las Claves SLA?

Las claves SLA son pares de claves RSA-2048 utilizadas para:

1. **Autenticar el DA agent** antes de ejecutarlo
2. **Challenge-response** entre bootrom y host
3. **Verificar firma digital** del DA

### Componentes de la Clave

```python
SlaKey(
    vendor="Motorola_Lamu",
    da_codes=[0x6768],      # MT6768
    name="Lamu_AuthKey",
    d=<private_key_d>,      # Exponente privado (secreto)
    n=<modulus_n>,          # Módulo (público)
    e="010001"              # Exponente público (65537)
)
```

## ¿Por Qué No Están en el PCAPNG?

El PCAPNG solo captura la **comunicación USB**, no las claves:

- **Challenge**: Enviado por el dispositivo
- **Response**: Calculado por el host usando la clave privada
- **Las claves en sí**: Nunca se transmiten por USB

## ¿Por Qué No Están en el DA Agent?

El DA agent contiene:

- **Código ejecutable** del DA
- **Firma RSA** (resultado de firmar el código)
- **NO contiene** la clave privada que generó la firma

```
signature = RSA_sign(hash(DA_code), private_key)
```

La firma puede verificarse con la clave pública, pero no se puede extraer la clave de ella.

## ¿De Dónde Vienen las Claves?

Las claves SLA se obtienen mediante:

### 1. Bootrom Reverse Engineering

El bootrom del chip contiene la clave pública hardcodeada:

```bash
# Extraer bootrom (requiere exploit)
python mtk.py dumpbrom brom.bin

# Analizar con binwalk/strings
strings brom.bin | grep -i "key"
binwalk -E brom.bin
```

### 2. Firmware Oficial

Algunos vendors incluyen las claves en:
- Herramientas de flash oficiales (SP Flash Tool)
- Archivos de autenticación (.auth)
- Certificados (.cert)

```bash
# Buscar en firmware
find firmware/ -name "*.auth"
find firmware/ -name "*.cert"
strings SP_Flash_Tool.exe | grep "BEGIN"
```

### 3. Análisis de Preloader

El preloader puede contener referencias:

```bash
# Strings en preloader
strings preloader_lamu.bin | grep -E "[0-9a-f]{64}"

# Buscar patrones de clave
hexdump -C preloader_lamu.bin | grep "01 00 01"  # Exponente 0x10001
```

### 4. Community Leaks

Algunas claves han sido compartidas por:
- Desarrolladores de custom ROMs
- Investigadores de seguridad
- Leaks de vendors

Ejemplo: Las claves de Tecno/Infinix en `sla_keys.py` provienen de leaks conocidos.

## Cómo Agregar Claves Si Las Tienes

### Paso 1: Verificar el Formato

Las claves deben ser números enteros grandes:

```python
# Ejemplo de clave (valores ficticios)
d = 123456789...  # ~617 dígitos
n = 987654321...  # ~617 dígitos  
e = "010001"      # 65537 en hex
```

### Paso 2: Agregar a sla_keys.py

Editar `/mtkclient/Library/Auth/sla_keys.py`:

```python
da_sla_keys = [
    # ... otras claves ...
    
    SlaKey(vendor="Motorola_Lamu",
           da_codes=[0x6768],
           name="Lamu_AuthKey",
           d=<tu_valor_d>,
           n=<tu_valor_n>,
           e="010001"),
]
```

### Paso 3: Verificar

```bash
# Test con el dispositivo
python mtk.py gettargetconfig --loader DA_A15_lamu_FORBID_SIGNED.bin

# Debe pasar SLA sin error
```

## Alternativas Si No Tienes las Claves

### 1. Usar DA Firmado Correcto

El `DA_A15_lamu_FORBID_SIGNED.bin` ya está firmado:

```bash
# Debería funcionar sin necesitar claves SLA manualmente
python mtk.py <comando> --loader DA_A15_lamu_FORBID_SIGNED.bin
```

### 2. Exploit Kamakiri2

Si el dispositivo es vulnerable, Kamakiri2 puede bypass SLA:

```bash
python mtk.py payload --loader DA_A15_lamu_FORBID_SIGNED.bin
```

### 3. Modo META

Algunos dispositivos permiten modo META sin SLA:

```bash
python mtk.py meta --loader DA_A15_lamu_FORBID_SIGNED.bin
```

## Estructura de la Firma RSA-2048

En el DA agent (`DA_A15_lamu_FORBID_SIGNED.bin`):

```
Región 2 (DA Stage 1):
  Offset: 0x0003F348
  Código: 259,144 bytes
  Firma:  256 bytes (RSA-2048)

Región 3 (DA Stage 2):
  Offset: 0x0005913C
  Código: 365,116 bytes  
  Firma:  256 bytes (RSA-2048)
```

### Formato de la Firma

```
Firma = RSA_PKCS1_v1_5_Sign(SHA256(código), private_key)
```

### Verificación

```python
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA256

# Si tuvieras la clave pública
public_key = RSA.construct((n, e))
h = SHA256.new(da_code)

try:
    pkcs1_15.new(public_key).verify(h, signature)
    print("Firma válida")
except:
    print("Firma inválida")
```

## Herramientas Útiles

### 1. Binwalk

```bash
# Analizar entropy del DA (detectar crypto)
binwalk -E DA_A15_lamu_FORBID_SIGNED.bin

# Extraer estructuras
binwalk -e DA_A15_lamu_FORBID_SIGNED.bin
```

### 2. OpenSSL

```bash
# Si tienes un archivo .pem con la clave
openssl rsa -in key.pem -text -noout

# Convertir a formato Python
openssl rsa -in key.pem -modulus -noout
```

### 3. Python Script

```python
# Extraer n, e, d de archivo .pem
from Cryptodome.PublicKey import RSA

with open('key.pem', 'r') as f:
    key = RSA.import_key(f.read())

print(f"n = {key.n}")
print(f"e = {hex(key.e)}")
if key.has_private():
    print(f"d = {key.d}")
```

## Análisis del Challenge-Response

Del PCAPNG podemos ver el protocolo pero no las claves:

```python
# Frame 93469: El host recibe challenge del dispositivo
challenge = bytes.fromhex("22defb438025b98431868a1a0b9df3706584719167971c15")

# Frame 93527: El host envía response
# Este response se calcula como:
# response = RSA_decrypt(challenge, private_key) o
# response = RSA_sign(challenge, private_key)
response = bytes.fromhex("3f76e5ee37")

# Pero sin la private_key, no podemos calcular el response
```

## FAQ

### ¿Puedo usar mtkclient sin las claves SLA?

**Sí**, si:
- El DA ya está firmado correctamente (como `DA_A15_lamu_FORBID_SIGNED.bin`)
- El dispositivo es vulnerable a exploits (Kamakiri2)
- Usas modo preloader sin protección

### ¿Las claves son únicas por dispositivo?

**No necesariamente**:
- Claves por vendor (ej: todas las Motorola)
- Claves por modelo (ej: solo lamu)
- Claves por lote de producción

### ¿Puedo generar mis propias claves?

**No**, el bootrom solo acepta claves que conoce:
- Las claves públicas están hardcoded en el bootrom
- No puedes cambiarlas sin modificar el hardware

### ¿Es legal tener estas claves?

**Depende de tu jurisdicción**:
- Para investigación: generalmente permitido
- Para unlock de tu propio dispositivo: usualmente legal
- Para redistribución: puede violar DMCA/términos de servicio

## Conclusión

Las claves SLA para MT6768 lamu:

1. ❌ No están en el PCAPNG
2. ❌ No pueden extraerse del DA firmado
3. ✅ Pueden estar en el bootrom
4. ✅ Pueden estar en herramientas oficiales
5. ✅ Pueden obtenerse de leaks

**Estado actual**: El dispositivo funciona con el DA firmado proporcionado, pero las claves RSA para generar nuevos DA no están disponibles públicamente.

Si alguien tiene acceso a estas claves, puede agregarlas siguiendo el formato en `sla_keys.py`.

---

**Referencias**:
- PCAPNG Analysis: frames 93446-93550
- DA Agent: `DA_A15_lamu_FORBID_SIGNED.bin`
- Preloader: `preloader_lamu.bin`
- SLA Keys: `mtkclient/Library/Auth/sla_keys.py`
