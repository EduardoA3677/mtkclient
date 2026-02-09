#!/usr/bin/env python3
"""
Seccfg Partition Analyzer for MT6768 Lamu
Analyzes seccfg partition dump to determine crypto method
"""
import sys
import os
from hashlib import sha256
try:
    from Crypto.Cipher import AES
except ImportError:
    print("Please install pycryptodome: pip install pycryptodome")
    sys.exit(1)

def analyze_seccfg(filename):
    """Analyze seccfg partition dump"""
    if not os.path.exists(filename):
        print(f"Error: File {filename} not found")
        return
    
    with open(filename, 'rb') as f:
        data = f.read()
    
    print("=" * 60)
    print("SECCFG PARTITION ANALYSIS")
    print("=" * 60)
    print(f"File: {filename}")
    print(f"Size: {len(data)} bytes ({len(data) // 1024} KB)")
    print()
    
    # Show first 256 bytes as hex
    print("First 256 bytes (hex):")
    for i in range(0, min(256, len(data)), 16):
        hex_str = data[i:i+16].hex()
        ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[i:i+16])
        print(f"{i:04x}:  {hex_str:32s}  {ascii_str}")
    print()
    
    # Try to detect structure
    print("Structure Detection:")
    magic = data[:4]
    print(f"  Magic: {magic.hex()} ({magic})")
    
    # Common offsets to check
    if len(data) >= 16:
        version = int.from_bytes(data[4:8], 'little')
        size = int.from_bytes(data[8:12], 'little')
        print(f"  Version: 0x{version:08x}")
        print(f"  Size field: 0x{size:08x}")
    
    print()
    
    # Try to extract encrypted hash (typically last 32 bytes or at specific offset)
    print("Crypto Analysis:")
    print("  Testing decryption with known keys...")
    print()
    
    # Keys to try (from seccfg.py)
    keys_to_try = [
        ("SW Default", b"MediaTek Inc.   ", b"0000000000000000"),
        ("SW ALT1", b"1A52A367CB12C458965D32CD874B36B2"[:16], bytes.fromhex("57325A5A125497661254976657325A5A")[:16]),
        ("SW ALT2", b"2B6B478B2CD365954C21BC3A7612A521"[:16], bytes.fromhex("5A5A32576696475212544766975A5A32")[:16]),
        ("SW ALT3", b"48657368656E7365486973656E736548"[:16], bytes.fromhex("48697365486973654869736548697365")[:16]),
        ("SW ALT4", b"0102030405060708090A0B0C0D0E0F10"[:16], bytes.fromhex("11121314151617181920212223242526")[:16]),
    ]
    
    # Try different offsets for encrypted hash
    possible_hash_offsets = []
    
    # Common patterns: last 32 bytes, or at offsets like 0x180, 0x1C0, etc.
    if len(data) >= 32:
        possible_hash_offsets.append(len(data) - 32)  # Last 32 bytes
    
    for offset in [0x180, 0x1C0, 0x200, 0x240]:
        if offset + 32 <= len(data):
            possible_hash_offsets.append(offset)
    
    for offset in possible_hash_offsets:
        encrypted_hash = data[offset:offset+32]
        print(f"  Trying offset 0x{offset:04x}:")
        print(f"    Encrypted: {encrypted_hash.hex()}")
        
        for name, key, iv in keys_to_try:
            try:
                cipher = AES.new(key, AES.MODE_CBC, iv)
                decrypted = cipher.decrypt(encrypted_hash)
                print(f"    {name}: {decrypted.hex()}")
                
                # Check if it looks like a valid hash (all printable or specific pattern)
                if all(b == 0 for b in decrypted):
                    print(f"      -> All zeros (might be unlocked state)")
                elif all(32 <= b < 127 or b in [0, 9, 10, 13] for b in decrypted):
                    print(f"      -> Contains printable characters")
                    
            except Exception as e:
                print(f"    {name}: Failed - {e}")
        print()
    
    # Show last 256 bytes as hex
    print("\nLast 256 bytes (hex):")
    start = max(0, len(data) - 256)
    for i in range(start, len(data), 16):
        hex_str = data[i:i+16].hex()
        ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data[i:i+16])
        print(f"{i:04x}:  {hex_str:32s}  {ascii_str}")
    
    print()
    print("=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Check if any decryption produced recognizable pattern")
    print("2. Compare with expected hash of seccfg content")
    print("3. If no match, may need to extract key from preloader/DA")
    print()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python analyze_seccfg.py seccfg.bin")
        print()
        print("This script analyzes a seccfg partition dump to determine")
        print("the correct crypto method for unlocking.")
        print()
        print("Example:")
        print("  python analyze_seccfg.py seccfg.bin")
        sys.exit(1)
    
    analyze_seccfg(sys.argv[1])
