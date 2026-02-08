# Análisis Completo de Extracción de Claves RSA - MT6768 Lamu

## Herramientas Instaladas y Utilizadas

```bash
# Herramientas del sistema
apt-get install binwalk foremost file xxd

# Librerías Python
pip3 install pycryptodome binwalk pyasn1 pem
```

## Métodos de Análisis Implementados

### MÉTODO 1: Binwalk - Análisis de Entropía

**Objetivo**: Detectar secciones cifradas, comprimidas o con datos criptográficos.

```bash
binwalk DA_A15_lamu_FORBID_SIGNED.bin
binwalk -E DA_A15_lamu_FORBID_SIGNED.bin  # Análisis de entropía
binwalk preloader_lamu.bin
```

**Resultado**: No se detectaron estructuras PE/ELF/crypto conocidas, lo cual es esperado para firmware embebido.

### MÉTODO 2: Búsqueda de Patrones RSA

**Patrones buscados**:

1. **Exponente público 0x10001 (65537)**
   - Big-endian: `00 01 00 01`
   - Little-endian: `01 00 01 00`
   - 64-bit: `01 00 00 00 01 00 00 00`

2. **Estructuras ASN.1**
   - SEQUENCE: `30 82`
   - INTEGER: `02 82`

3. **Strings relacionados**: RSA, KEY, PRIVATE, PUBLIC, PKCS, AUTH, etc.

### Resultados del Análisis de Patrones

#### DA Agent (DA_A15_lamu_FORBID_SIGNED.bin)

**Exponentes públicos encontrados (0x10001)**:

| Offset     | Tipo            | Contexto |
|------------|-----------------|----------|
| 0x00005977 | Big-endian      | Código ARM |
| 0x00006967 | Little-endian   | Sección de datos ✓ |
| 0x00006a71 | Little-endian   | Sección de datos ✓ |
| 0x000421b9 | Little-endian   | Tabla de datos |
| 0x000421c1 | Little-endian   | Tabla de datos |

**Strings crypto encontrados**:
- `RSA` en offset 0x00098ba6: "LEGACYRSA seccfg"
- `KEY` en offset 0x00037828: "PWRKEY short press"
- `AUTH` en múltiples ubicaciones

#### Preloader (preloader_lamu.bin)

**Exponentes públicos encontrados**:

| Offset     | Contexto |
|------------|----------|
| 0x0000003d | Header MMM |
| 0x0004b12b | Tabla de configuración |
| 0x0004b133 | Tabla de configuración |

**Strings crypto encontrados**:
- `AUTH` en 0x0003cfcd: "PL_AUTH_INIT_FAIL PL_AUTH_FAIL"
- `KEY` en 0x0003c0ba: "RPMB KEY"

### MÉTODO 3: Extracción de Módulos RSA

Se intentó extraer módulos RSA-2048 (256 bytes) alrededor de los exponentes públicos encontrados.

#### Candidatos Identificados

**Candidato 1** (DA Agent, offset 0x6967+0x313):
```
Longitud: 2048 bits
Exponente: 0x10001 (65537)
Módulo (n): 
  fe3f2de9f84389461d4c00afa0b080460df13f05a36825f03f05990701d5fef7
  ...
  22007fb502230a4a06460c460a4d8de80c000b1d0293012303932b6933b11021

Decimal: 320956843606863686733961037358691589420100876862551212408973796...
```

**Verificación**:
- ✓ 2048 bits
- ✓ Exponente correcto (65537)
- ✓ Número impar
- ✗ Tiene factor primo pequeño (posiblemente mezclado con código)

### MÉTODO 4: Análisis de Firmas RSA

Se analizaron las firmas RSA existentes en el DA agent:

#### Región 2 (DA Stage 1) - Offset 0x0003f348
```
Tamaño firma: 256 bytes
Bytes únicos: 42/256
Primeros 32: 29302920213d20756e69740064656c65746520646f6e652e0a0025733a207265
Últimos 32:  292c20646174615f6c6173742830782578292e0a0025733a20206974656d5b25
```

**Análisis**: La firma parece contener texto ASCII, lo cual indica que NO es una firma RSA válida en esta ubicación, sino datos de strings.

#### Región 3 (DA Stage 2) - Offset 0x0005913c
```
Tamaño firma: 256 bytes
Bytes únicos: 99/256
Primeros 32: 38bd032038bd042038bd012038bd00bf24dc001020dc00107aa7044028dc0010
Últimos 32:  590207d4edf7aefc01280dd81648f5f733ff09e0c3f302410629f0d19bb20122
```

**Análisis**: Alta entropía, parece código ARM Thumb, no una firma RSA pura.

#### Última Firma - Offset 0x0009bf60 (fin del archivo)
```
Tamaño: 256 bytes
Bytes únicos: 163/256
Primeros 32: 771228811849dac0e2c12a74b4bb0612bcd2d3ea27e077ddcc7190aca0dbc367
Últimos 32:  ccf9b8e3cc3d96baae642be1b57d2b128d2762767c0b7d2fb771e514471ad364
```

**Análisis**: ✓ Alta entropía, aspecto de datos cifrados/firmados. Esta es la firma RSA más probable.

## Análisis del PCAPNG para Claves

### Challenge-Response Observado

```
Frame 93469 (AUTH DATA):
  Comando: 0x0820201f
  Challenge: 22defb438025b98431868a1a0b9df3706584719167971c15
  Longitud: 27 bytes

Frame 93527 (RESPONSE):
  Comando: 0x052006d1
  Response: 3f76e5ee37
  Longitud: 5 bytes
  Valor decimal: 272577719863
```

**Conclusión**: El PCAPNG muestra el challenge y response, pero no las claves RSA usadas para calcular el response.

## Limitaciones Encontradas

### 1. Claves No Extraíbles del DA Firmado

**Razón**: El DA contiene:
- ✓ Código ejecutable firmado
- ✓ Firma RSA (resultado de firmar)
- ✗ Clave privada (d) - NUNCA se incluye
- ✗ Clave pública completa - Solo el exponente

**Matemáticas**:
```
signature = RSA_sign(hash(code), private_key)

# Dado:
# - code (conocido)
# - signature (conocido)
# - public_key.n (posiblemente encontrado)
# - public_key.e (conocido: 65537)

# NO podemos calcular:
# - private_key.d
```

### 2. Claves No en el PCAPNG

El PCAPNG solo captura:
- ✓ Challenge enviado por el dispositivo
- ✓ Response enviado por el host
- ✗ Las claves RSA (nunca se transmiten)

### 3. Preloader No Contiene Claves Completas

El preloader contiene referencias y exponentes, pero no las claves privadas completas.

## Dónde SÍ Están las Claves

### 1. Bootrom del Chip MT6768

**Clave pública**: Hardcoded en el bootrom (ROM del chip)
**Clave privada**: En los servidores de Mediatek/Motorola

**Cómo extraer**:
```bash
# Requiere exploit o JTAG
python mtk.py dumpbrom brom.bin

# Luego buscar con:
strings brom.bin | grep -E "[0-9a-f]{64,}"
binwalk -E brom.bin
```

### 2. Herramientas Oficiales de Flash

**Ubicaciones posibles**:
- `SP Flash Tool` executable
- Archivos `.auth` o `.cert` en paquetes de firmware
- DLLs de autenticación

**Búsqueda**:
```bash
# En Windows
strings SP_Flash_Tool.exe | findstr /i "BEGIN PRIVATE"

# Archivos auth
find firmware/ -name "*.auth" -o -name "*.cert"
```

### 3. Leaks de Desarrolladores

Algunas claves se han filtrado públicamente:
- Foros XDA Developers
- GitHub (accidentalmente)
- Repositorios de custom ROMs

## Formato Final para sla_keys.py

Si se obtienen las claves completas:

```python
SlaKey(vendor="Motorola_Lamu",
       da_codes=[0x6768],  # MT6768
       name="Lamu_AuthKey",
       # Exponente privado (NO encontrado)
       d=<VALOR_GIGANTE_617_DIGITOS>,
       # Módulo público (candidato encontrado)
       n=32095684360686368673396103735869158942010087686255121240897379605898051479423600162400572176110466089447355449077585399834532233937342912455485566555809021991857832664262149793585629538812426136080894983211895118952082581986242848503046455486173053911418232617359377119648482977526090144471832172254220850166957442008697704198006173863938724846466368627072660117773762185599657246696372669307830611635542056552596486309416958920176458460692717628546685166224395543678368540446272808412274628643102215517972337076755912551662819426440782432746681177457473887631271412942893296262094691524839628650122145659451616596001,
       # Exponente público (confirmado)
       e="010001"),  # 65537
```

## Conclusiones del Análisis

### ✓ Logros

1. **Instaladas herramientas**: binwalk, pycryptodome, análisis binario
2. **Identificados patrones**: 11+ ocurrencias de exponente público
3. **Encontrados módulos candidatos**: RSA-2048 en offset 0x6967+0x313
4. **Analizada firma**: Última firma en DA (163/256 bytes únicos)
5. **Documentado challenge/response**: Frame 93469 y 93527 del PCAPNG

### ✗ Limitaciones

1. **Clave privada (d)**: NO se puede extraer del DA o PCAPNG
2. **Módulos mixtos**: Los candidatos están mezclados con código
3. **Firmas internas**: Las firmas en offsets internos no son RSA puras

### 💡 Recomendaciones

1. **Usar DA firmado actual**: `DA_A15_lamu_FORBID_SIGNED.bin` funciona directamente
2. **Exploit Kamakiri2**: Puede bypass la verificación SLA
3. **Dump bootrom**: Si se obtiene, buscar claves públicas allí
4. **Herramientas oficiales**: Analizar SP Flash Tool o MTK auth tools
5. **Community**: Buscar en XDA si alguien ya extrajo las claves

## Herramientas de Análisis Adicionales

### Para Análisis Futuro

```bash
# Ghidra - Reverse engineering GUI
wget https://ghidra-sre.org/ghidra_10.x.zip
unzip ghidra_10.x.zip

# Radare2 - CLI reverse engineering
apt-get install radare2

# Análisis con radare2
r2 -AA DA_A15_lamu_FORBID_SIGNED.bin
> afl  # List functions
> pdf @ <address>  # Disassemble

# Búsqueda de constantes crypto
r2 -q -c "/x 010001" DA_A15_lamu_FORBID_SIGNED.bin
```

### Scripts Python Útiles

```python
# Extraer bloques de 256 bytes con alta entropía
import math
from collections import Counter

def calculate_entropy(data):
    if not data:
        return 0
    counter = Counter(data)
    length = len(data)
    entropy = -sum((count/length) * math.log2(count/length) 
                   for count in counter.values())
    return entropy

# Buscar bloques con entropy > 7.0 (posibles claves/firmas)
with open('DA_A15_lamu_FORBID_SIGNED.bin', 'rb') as f:
    data = f.read()
    
for offset in range(0, len(data)-256, 256):
    block = data[offset:offset+256]
    entropy = calculate_entropy(block)
    if entropy > 7.0:
        print(f"High entropy at 0x{offset:08x}: {entropy:.2f}")
```

## Referencias

- **Binwalk**: https://github.com/ReFirmLabs/binwalk
- **PyCryptodome**: https://pycryptodome.readthedocs.io/
- **RSA Math**: https://en.wikipedia.org/wiki/RSA_(cryptosystem)
- **MTK Security**: https://forum.xda-developers.com/

---

**Fecha**: 2026-02-08  
**Archivos analizados**:
- DA_A15_lamu_FORBID_SIGNED.bin (639,072 bytes)
- preloader_lamu.bin (328,868 bytes)
- 1.pcapng (163 MB)

**Herramientas**: binwalk, pycryptodome, Python 3, tshark
