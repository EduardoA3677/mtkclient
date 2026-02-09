#!/usr/bin/env python3
"""
Analyze preloader_lamu.bin RE data for AES key
Tests crypto structures from offset 0x4FF60 onwards
"""

import sys
from Crypto.Cipher import AES
from hashlib import sha256

# Crypto structures from preloader (256 bytes each)
# Structure A @ 0x4FF60
STRUCT_A_HEX = """
2FC83DAF81F7DCAEh, 0A8A2C12508200AA7h, 25E10D46C972943Eh
0BF0DD94AF7368FA8h, 13FF19B88DBF1C94h, 0EF904C97626222C3h
7FA13005A91B9B0Ah, 0E2E18FD85B58778Ch, 58551BDB5AE12650h
0C2A899BF8258314Ah, 6E50EBAD04090F89h, 0D27ED19CE3BE1E80h
0CDE06E34213A59C7h, 354C6F7F15B24BD6h, 91DD3D459DB3C881h
0FB611040A9EC6B34h, 68458CEE4CA5E142h, 623B1EA27689ADA4h
185EA8DBD144342Dh, 13666BE076C9AEE1h, 0D5BD557C28B192F5h
780826D574E6F09h, 7DD981123F2856FFh, 60CFBA04CDBDD11Bh
863ABEC495A9F1EAh, 0EB0A64BD8C60597Dh, 0EEF1A402DB6FCECEh
62DB3A846C437C77h, 8DE1C2DB166A9410h, 736A18FB3088E902h
9BD7C60FF052CB82h
"""

# Structure B @ 0x50160
STRUCT_B_HEX = """
8C8DD3B600000000h, 0B91EF6FE735FA59h, 0D159FB00EAEF97CEh
0C97D583765BB84AFh, 0FF5EBE679A26478Bh, 745F08FEAC195E70h
93D69A6FCD7048A3h, 0E3E5953B13FFC637h, 0F6149095AE3A3846h
0C4AD154A1464A0Ah, 993A6903A56E6EC4h, 9400A7816B1E801Ah
8CABA4B71FB9896Ah, 4FF663EBEAAA3217h, 3039CFC08F7B19CAh
0F3C53D0D48CA640Dh, 0FB6EA0F9F62C70B0h, 0A0E4E0AE566A7E80h
7EB4AA1CD6AE74C8h, 3259357C05D32032h, 0E533B926823AE11Eh
0CB56B9939FB784E3h, 0CC0F72CD0F41530Eh, 6D5C40F5FA578B93h
0E828D13E6C045860h, 591CE53DBBE7A47Fh, 0BA08F116F56BE587h
0A43C8A8D8142A9C7h, 4C9B0604634AD856h, 0ADE002039F4B3F6h
"""

# Structure C @ 0x50380
STRUCT_C_HEX = """
7186A7C700000000h, 163D74F009DDEEF4h, 996FFA1A8D0CAA7Ch
33F087367D66F1B5h, 42574C2C70D5D30Bh, 1D1443C6D394C998h
3EF10625A6D7D713h, 9B5E0B5D9A765DDh, 30B1855E70AB141Fh
0C76C4A6A61B5DE58h, 0AFFDB60AA22C6F61h, 853D3BF7C4396C56h
2647F93F8B4EE55Fh, 0B60CA994D3F3F077h, 893F8DCC26ADF91Ch
474FB25C297B9A24h, 0A26EE790C01F06CEh, 0BB5C548AC16D4A96h
49EE0EE4B59674B0h, 207CD81C50BB586Ch, 0F91B4A8372D6DBF5h
0CCCB4984DEAAFBC1h, 0BED9B36C4104353Dh, 507B2302376EFE4Fh
0E2E604BC391C8516h, 0D7D84059C633ED5Ah, 628E7DA08CB68B9Ch
7660887EE6C8F1C1h, 0F950E03EA521251Bh, 0B677F708EAAF4607h
"""

def parse_hex_structure(hex_str):
    """Parse hex structure string to bytes"""
    # Remove 'h' suffix, '0x' prefix, and whitespace
    clean = hex_str.replace('h', '').replace('0x', '').replace('0', '')
    # Split by comma
    parts = [p.strip() for p in clean.split(',') if p.strip()]
    
    # Convert to bytes (little-endian qwords)
    data = b''
    for part in parts:
        try:
            # Pad to 16 chars (8 bytes)
            part = part.zfill(16)
            # Convert hex to bytes (little-endian)
            qword = int(part, 16)
            data += qword.to_bytes(8, byteorder='little')
        except:
            pass
    
    return data

def test_structure_as_key(struct_bytes, seccfg_file, struct_name):
    """Test if structure contains AES key"""
    print(f"\n{'='*60}")
    print(f"Testing {struct_name} ({len(struct_bytes)} bytes)")
    print(f"{'='*60}")
    
    if len(struct_bytes) < 32:
        print(f"❌ Structure too small: {len(struct_bytes)} bytes")
        return False
    
    # Load seccfg
    try:
        with open(seccfg_file, 'rb') as f:
            seccfg_data = f.read()
    except:
        print(f"❌ Cannot open {seccfg_file}")
        return False
    
    # Extract encrypted hash (offset 0x1C, 32 bytes)
    encrypted_hash = seccfg_data[0x1C:0x3C]
    
    # Calculate expected hash
    temp_data = seccfg_data[:0x1C] + b'\x00' * 32 + seccfg_data[0x3C:]
    expected_hash = sha256(temp_data).digest()
    
    print(f"Encrypted hash: {encrypted_hash[:16].hex()}...")
    print(f"Expected hash:  {expected_hash[:16].hex()}...")
    
    # Try multiple extraction methods
    methods = [
        ("First 16+16", struct_bytes[:16], struct_bytes[16:32]),
        ("Last 16+16", struct_bytes[-32:-16], struct_bytes[-16:]),
        ("Offset 0+16", struct_bytes[0:16], struct_bytes[16:32]),
        ("Offset 32+48", struct_bytes[32:48] if len(struct_bytes) >= 48 else None,
                        struct_bytes[48:64] if len(struct_bytes) >= 64 else None),
        ("XOR pattern", bytes([b ^ 0x5A for b in struct_bytes[:16]]),
                       bytes([b ^ 0xA5 for b in struct_bytes[16:32]])),
    ]
    
    for method_name, key, iv in methods:
        if key is None or iv is None or len(key) != 16 or len(iv) != 16:
            continue
            
        try:
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted = cipher.decrypt(encrypted_hash)
            
            if decrypted == expected_hash:
                print(f"\n🎉 SUCCESS! Method: {method_name}")
                print(f"KEY: {key.hex()}")
                print(f"IV:  {iv.hex()}")
                return True
            else:
                print(f"  ❌ {method_name}: No match")
        except Exception as e:
            print(f"  ❌ {method_name}: Error - {e}")
    
    return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python analyze_preloader_data.py seccfg.bin")
        sys.exit(1)
    
    seccfg_file = sys.argv[1]
    
    print("="*60)
    print("PRELOADER CRYPTO STRUCTURE ANALYSIS")
    print("="*60)
    
    # Parse structures
    struct_a = parse_hex_structure(STRUCT_A_HEX)
    struct_b = parse_hex_structure(STRUCT_B_HEX)
    struct_c = parse_hex_structure(STRUCT_C_HEX)
    
    print(f"\nStructure A: {len(struct_a)} bytes")
    print(f"Structure B: {len(struct_b)} bytes")
    print(f"Structure C: {len(struct_c)} bytes")
    
    # Test each structure
    results = []
    results.append(test_structure_as_key(struct_a, seccfg_file, "Structure A"))
    results.append(test_structure_as_key(struct_b, seccfg_file, "Structure B"))
    results.append(test_structure_as_key(struct_c, seccfg_file, "Structure C"))
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    if any(results):
        print("✅ SUCCESS! Found working AES key!")
    else:
        print("❌ No key found in preloader structures")
        print("\nThese structures are likely:")
        print("  - Bootloader configuration tables")
        print("  - Memory layout definitions")
        print("  - NOT direct AES keys")
        print("\nRecommendation: Use official Motorola unlock method")
    
    return 0 if any(results) else 1

if __name__ == "__main__":
    sys.exit(main())
