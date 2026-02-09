#!/usr/bin/env python3
"""
Reconstrucción de get_unlock_data desde particiones
Formato Motorola:
(bootloader) 0A40040192024205#4C4D3556313230
(bootloader) 30373731363031303332323239#BD00
(bootloader) 8A672BA4746C2CE02328A2AC0C39F95
(bootloader) 1A3E5#1F53280002000000000000000
(bootloader) 0000000
"""

import struct
import hashlib
import binascii

def hex_encode(data):
    """Convierte string ASCII a hex"""
    if isinstance(data, str):
        return binascii.hexlify(data.encode()).decode().upper()
    return binascii.hexlify(data).decode().upper()

def analyze_proinfo(filename):
    """Analiza proinfo.bin"""
    with open(filename, 'rb') as f:
        data = f.read()
    
    print("="*60)
    print("ANÁLISIS DE PROINFO.BIN")
    print("="*60)
    
    # Serial @ 0x0000
    serial = data[0x0000:0x0040].split(b'\x00')[0].decode('ascii', errors='ignore')
    print(f"Serial @ 0x0000: {serial}")
    print(f"  Hex: {hex_encode(serial)}")
    
    # Chip ID @ 0x0040
    chip_id = data[0x0040:0x0050]
    print(f"\nChip ID @ 0x0040: {chip_id.hex()}")
    
    # Code @ 0x0160
    code = data[0x0160:0x0170].split(b'\x00')[0].decode('ascii', errors='ignore')
    print(f"\nCode @ 0x0160: {code}")
    print(f"  Hex: {hex_encode(code)}")
    
    # Barcode @ 0x0200
    barcode = data[0x0200:0x0210].split(b'\x00')[0].decode('ascii', errors='ignore')
    print(f"\nBarcode @ 0x0200: {barcode}")
    print(f"  Hex: {hex_encode(barcode)}")
    
    # Product @ 0x0210
    product = data[0x0210:0x0220].split(b'\x00')[0].decode('ascii', errors='ignore')
    print(f"\nProduct @ 0x0210: {product}")
    print(f"  Hex: {hex_encode(product)}")
    
    # Date @ 0x0244
    date = data[0x0244:0x0254].split(b'\x00')[0].decode('ascii', errors='ignore')
    print(f"\nDate @ 0x0244: {date}")
    
    return {
        'serial': serial,
        'chip_id': chip_id,
        'code': code,
        'barcode': barcode,
        'product': product,
        'date': date
    }

def search_imei(filename):
    """Busca IMEI en archivo"""
    with open(filename, 'rb') as f:
        data = f.read()
    
    # Buscar secuencias de 15 dígitos
    import re
    text = data.decode('latin-1', errors='ignore')
    
    # Patrón IMEI: 15 dígitos
    pattern = r'\b\d{15}\b'
    matches = re.findall(pattern, text)
    
    return matches

def reconstruct_unlock_data(proinfo_data):
    """Intenta reconstruir unlock_data"""
    print("\n" + "="*60)
    print("RECONSTRUCCIÓN DE get_unlock_data")
    print("="*60)
    
    # Ejemplo del formato:
    # 0A40040192024205#4C4D355631323030373731363031303332323239#...
    
    # Parte 1: Header (desconocido, parece ser fijo o basado en chip)
    # 0A40040192024205
    header = "0A40040192024205"
    
    print(f"\n[1] Header (chip ID hash?):")
    print(f"    {header}")
    
    # Parte 2: Serial Number en HEX
    # 4C4D355631323030373731363031303332323239
    # = "LM355V120077160103222"  (ejemplo del formato Motorola)
    
    serial = proinfo_data['serial']
    serial_hex = hex_encode(serial)
    
    print(f"\n[2] Serial Number:")
    print(f"    ASCII: {serial}")
    print(f"    HEX: {serial_hex}")
    
    # Parte 3: Hash/Signature (requiere clave privada del bootloader)
    # BD008A672BA4746C2CE02328A2AC0C39F951A3E5
    # Este es un hash firmado que no podemos generar sin la clave privada
    
    print(f"\n[3] Signature (NO PODEMOS GENERAR):")
    print(f"    Requiere clave privada del bootloader")
    print(f"    Formato: ~40 caracteres hex")
    print(f"    Ejemplo: BD008A672BA4746C2CE02328A2AC0C39F951A3E5")
    
    # Parte 4: Timestamp/Nonce
    # 1F53280002000000000000000000000
    print(f"\n[4] Timestamp/Nonce:")
    print(f"    Formato: ~31 caracteres hex")
    print(f"    Ejemplo: 1F53280002000000000000000000000")
    
    # Intento de reconstrucción (sin firma)
    print("\n" + "="*60)
    print("UNLOCK DATA RECONSTRUIDO (SIN FIRMA VÁLIDA)")
    print("="*60)
    
    # Sin firma válida, solo podemos mostrar el formato
    fake_signature = "00000000000000000000000000000000000000000"
    fake_nonce = "0000000000000000000000000000000"
    
    unlock_data = f"{header}#{serial_hex}#{fake_signature}#{fake_nonce}"
    
    print(f"\n{unlock_data}")
    
    # Dividir en líneas como bootloader
    print("\n\nFormato bootloader:")
    print("(bootloader) " + unlock_data[0:32])
    print("(bootloader) " + unlock_data[32:64])
    print("(bootloader) " + unlock_data[64:96])
    print("(bootloader) " + unlock_data[96:128])
    if len(unlock_data) > 128:
        print("(bootloader) " + unlock_data[128:])
    
    print("\n" + "="*60)
    print("⚠️  ADVERTENCIA CRÍTICA")
    print("="*60)
    print("""
Este unlock_data NO ES VÁLIDO porque:

1. El header puede ser incorrecto (calculado desde chip ID)
2. La firma es falsa (requiere clave privada del bootloader)
3. El timestamp/nonce es falso
4. Motorola validará la firma y RECHAZARÁ este código

Para obtener unlock_data REAL:
1. Reparar el bootloader (flash firmware stock)
2. Ejecutar: fastboot oem get_unlock_data
3. O contactar Motorola con serial: {}
""".format(serial))
    
    return unlock_data

def main():
    import sys
    
    print("="*60)
    print("EXTRACTOR DE DEVICE ID - RECONSTRUCCIÓN UNLOCK DATA")
    print("="*60)
    
    # Analizar proinfo
    proinfo_data = analyze_proinfo('/tmp/proinfo.bin')
    
    # Buscar IMEI en nvdata
    print("\n" + "="*60)
    print("BÚSQUEDA DE IMEI")
    print("="*60)
    
    print("\nBuscando en nvdata.bin...")
    imeis = search_imei('/tmp/nvdata.bin')
    if imeis:
        print(f"  Encontrados: {imeis[:5]}")
    else:
        print("  ❌ No encontrado en formato ASCII")
    
    print("\nBuscando en persist.bin...")
    imeis = search_imei('/tmp/persist.bin')
    if imeis:
        print(f"  Encontrados: {imeis[:5]}")
    else:
        print("  ❌ No encontrado en formato ASCII")
    
    # Reconstruir unlock_data
    unlock_data = reconstruct_unlock_data(proinfo_data)
    
    # Información adicional
    print("\n" + "="*60)
    print("INFORMACIÓN DEL DEVICE")
    print("="*60)
    print(f"""
Serial Number: {proinfo_data['serial']}
Barcode: {proinfo_data['barcode']}
Product Code: {proinfo_data['product']}
Manufacturing Date: {proinfo_data['date']}

Esta información es válida para:
✅ Contactar Motorola Support
✅ Verificar garantía
✅ Proof of ownership
❌ NO válida para unlock directo

Link Motorola: https://motorola-global-portal.custhelp.com/
""")

if __name__ == '__main__':
    main()
