#!/usr/bin/env python3
"""
extract_device_id.py - Extract Device ID from proinfo partition

Usage:
    python extract_device_id.py proinfo.bin
    python extract_device_id.py proinfo.bin -v
    python extract_device_id.py proinfo.bin --no-unlock

Extracts IMEI, Serial Number, and Barcode from proinfo partition dump.
Validates IMEI checksum using Luhn algorithm.
Optionally generates experimental unlock_data string (may not work).
"""

import sys
import re
import argparse

def find_imei(data):
    """Find IMEI patterns (15 digits) in binary data"""
    imeis = []
    
    # Convert binary to string
    try:
        text = data.decode('latin-1')
    except:
        text = str(data)
    
    # Pattern for IMEI: 15 consecutive digits
    pattern = r'\b\d{15}\b'
    matches = re.finditer(pattern, text)
    
    for match in matches:
        imei = match.group()
        if validate_imei_checksum(imei):
            if imei not in imeis:
                imeis.append(imei)
    
    return imeis

def validate_imei_checksum(imei):
    """Validate IMEI checksum using Luhn algorithm"""
    if len(imei) != 15:
        return False
    
    if not imei.isdigit():
        return False
    
    # Luhn algorithm
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

def find_serial(data):
    """Find Motorola serial number (format: LMxxxVxxxxxx)"""
    serials = []
    
    try:
        text = data.decode('latin-1')
    except:
        text = str(data)
    
    # Motorola serial pattern: 2 letters, 3 digits, V, then more digits
    pattern = r'\b[A-Z]{2}\d{3}V\d+\b'
    matches = re.finditer(pattern, text)
    
    for match in matches:
        serial = match.group()
        if len(serial) >= 10 and len(serial) <= 20:
            if serial not in serials:
                serials.append(serial)
    
    return serials

def find_barcode(data):
    """Find barcode (format: SBxxxxxxxxxx)"""
    barcodes = []
    
    try:
        text = data.decode('latin-1')
    except:
        text = str(data)
    
    # Barcode pattern: SB followed by alphanumeric
    pattern = r'\bSB[0-9A-Z]{10,}\b'
    matches = re.finditer(pattern, text)
    
    for match in matches:
        barcode = match.group()
        if barcode not in barcodes:
            barcodes.append(barcode)
    
    return barcodes

def find_product(data):
    """Find product name"""
    products = []
    
    try:
        text = data.decode('latin-1')
    except:
        text = str(data)
    
    # Common Motorola product names
    common_products = ['lamu', 'corfu', 'hawaii', 'ellis', 'kyoto']
    
    for product in common_products:
        if product in text.lower():
            if product not in products:
                products.append(product)
    
    return products

def generate_unlock_data(imei, serial, barcode, product):
    """Generate experimental unlock_data string
    
    WARNING: This is EXPERIMENTAL and likely won't work with Motorola portal.
    Motorola uses cryptographic signature from bootloader hardware.
    """
    # Convert to hex
    imei_hex = imei.encode().hex()
    serial_hex = serial.encode().hex()
    barcode_hex = barcode.encode().hex()
    product_hex = product.encode().hex()
    
    # Motorola format (approximated):
    # [Header]#[DeviceInfo][Footer]#
    header = "0A40040192024205"
    footer = ""
    
    device_info = imei_hex + serial_hex + barcode_hex + product_hex
    
    unlock_data = f"{header}#{device_info}{footer}#"
    
    return unlock_data

def main():
    parser = argparse.ArgumentParser(
        description='Extract Device ID from proinfo partition',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python extract_device_id.py proinfo.bin
  python extract_device_id.py proinfo.bin -v
  python extract_device_id.py proinfo.bin --no-unlock

Note:
  The generated unlock_data is EXPERIMENTAL and likely won't work.
  Motorola requires cryptographic signature from bootloader.
        '''
    )
    
    parser.add_argument('proinfo_file', help='Path to proinfo.bin file')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Verbose output')
    parser.add_argument('--no-unlock', action='store_true',
                        help='Do not generate experimental unlock_data')
    
    args = parser.parse_args()
    
    # Read proinfo file
    try:
        with open(args.proinfo_file, 'rb') as f:
            data = f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {args.proinfo_file}")
        return 1
    except Exception as e:
        print(f"Error reading file: {e}")
        return 1
    
    if args.verbose:
        print(f"File size: {len(data)} bytes")
        print()
    
    # Extract information
    print("=== Device Information ===")
    print()
    
    # Find IMEIs
    imeis = find_imei(data)
    if imeis:
        for i, imei in enumerate(imeis, 1):
            print(f"IMEI {i}: {imei} ✓ (Valid checksum)")
    else:
        print("IMEI: Not found ❌")
    
    # Find Serial
    serials = find_serial(data)
    if serials:
        for serial in serials:
            print(f"Serial Number: {serial}")
    else:
        print("Serial Number: Not found ❌")
    
    # Find Barcode
    barcodes = find_barcode(data)
    if barcodes:
        for barcode in barcodes:
            print(f"Barcode: {barcode}")
    else:
        print("Barcode: Not found ❌")
    
    # Find Product
    products = find_product(data)
    if products:
        for product in products:
            print(f"Product: {product}")
    else:
        print("Product: Not found ❌")
    
    print()
    
    # Generate experimental unlock_data
    if not args.no_unlock and imeis and serials:
        print("=== Experimental Unlock Data ===")
        print()
        print("⚠️  WARNING: This may NOT work with Motorola portal!")
        print("   Motorola uses cryptographic signature from bootloader.")
        print("   This data lacks proper signature and will likely be rejected.")
        print()
        
        unlock_data = generate_unlock_data(
            imeis[0],
            serials[0],
            barcodes[0] if barcodes else "UNKNOWN",
            products[0] if products else "lamu"
        )
        
        print("Unlock Data String:")
        print(unlock_data)
        print()
        print("Note: If bootloader is broken, this won't work.")
        print("      Better options:")
        print("      1. Repair bootloader with SP Flash Tool")
        print("      2. Contact Motorola service with Serial Number")
        print()
    
    # Summary
    if args.verbose:
        print("=== Search Summary ===")
        print(f"IMEIs found: {len(imeis)}")
        print(f"Serials found: {len(serials)}")
        print(f"Barcodes found: {len(barcodes)}")
        print(f"Products found: {len(products)}")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
