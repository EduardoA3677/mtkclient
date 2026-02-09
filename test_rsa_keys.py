#!/usr/bin/env python3
"""
Test RSA-derived AES keys from FlashToolLib.dll reverse engineering
for MT6768 Lamu seccfg decryption
"""

import sys
from Crypto.Cipher import AES
from hashlib import sha256, md5

# RSA Modulus Keys extracted from FlashToolLib.dll
RSA_KEYS = [
    # RSA Key 1 (.data:1002F010) - Clean version
    "C43469A95B143CDC63CE318FE32BAD35B9554A136244FA74D13947425A32949E" +
    "E6DC808CDEBF4121687A570B83C51E657303C925EC280B420C757E5A63AD3EC6" +
    "980AAD5B6CA6D1BBDC50DB793D2FDDC0D0361C06163CFF9757C07F96559A2186" +
    "3222F7ABF1FFC7765F396673A48A4E8E3296427BC5510D0F97F54E5CA1BD7A93" +
    "ADE3F6A625056426BDFE77B3B502C68A18F08B470DA23B0A2FAE13B8D4DB3746" +
    "255371F43306582C74794D1491E97FDE504F0B1ECAC9DDEF282D674B817B7FFA" +
    "8522672CF6281790910378FEBFA7DC6C2B0AF9DA03A58509D60AA1AD6F9BFDC8" +
    "4537CD0959B8735FE0BB9B471104B458A38DF846366926993097222F90628528",
    
    # RSA Key 2 (.data:1002F218) - Clean version  
    "8E02CDB389BBC52D5383EBB5949C895B0850E633CF7DD3B5F7B5B8911B0DDF2A" +
    "80387B46FAF67D22BC2748978A0183B5B420BA579B6D847082EA0BD14AB21B6C" +
    "CCA175C66586FCE93756C2F426C85D7DF07629A47236265D1963B8354CB229AF" +
    "A2E560B7B3641DDB8A0A839ED8F39BA8C7CDB94104650E8C7790305E2FF6D182" +
    "06F49B7290B1ADB7B4C523E10EBF53630D438EF49C877402EA3C1BD6DD903892" +
    "FD662FBDF1DFF5D7B095712E58E728BD7F6A8B5621175F4C08EBD6143CDACD65" +
    "D9284DFFECAB64F70FD63182E4981551522727A2EE9873D0DB78180C26553AD0" +
    "EE1CAAA21BCEBC5A8C0B331FE7FD8710F905A7456AF675A04AF1118CE71E36C9",
    
    # RSA Key 3 (.data:1002F428) - Clean version
    "00A89DF958CEC69E5E82F12CC64F21B577A99916043912CC47ED278F88CB79BA" +
    "847E7601ABD8C502BEEF0BC706038A9C5269486C191B65DA800DCD465028CCD5" +
    "E530BEB93E02053AC49D1FF4F17BE3245B0BBD0CA7EA51558C439783648502E9" +
    "FF92AC3696CADF09603D1F89C1D1D09095EE5EE68CACE1B3A401EF401DE86D39" +
    "11EA96021DC5B5AF36E6BABF3D48D6A58A9075D5DEEACADBFD09F93748929EF4" +
    "66A9D339D92370334E0E50AFC0C43CFB1B9F2BFF5E3B5A7012B93E92D8644F03" +
    "2993033245EEC56D899837D1080C5ABA7E09FE2E2EAC06921159775392D64E81" +
    "9DAA905A2931352AE02E3A21318B207E0FBFA113E8A32A37987243DA2BB57D7D",
    
    # RSA Key 4 (.data:1002F630) - Clean version
    "00DB8F46CF8DA80AF8CCA1AEC9FF7B358CFE4CC5659ADE5EF9C196905CAAF979" +
    "658349284723BEF9524532B21F460C0897468BE95D0AA92682144D1BFCB84AFC" +
    "7712FF3B5DC34153E5EFE64B465A6D8CF2BD8C2FB1BF27D9C77F26E90BAA3DDA" +
    "DA18525D3F689441EF7B6DC5C4B8C496B0A9C92F29D26DAC8FF8B137D6A93CF2" +
    "6AD391BF6124207FF9EB26E10B65269C6BAD38EFF0C50AAB604A0128B874F242" +
    "63037C605BC9F855252F78173141D166B632DBB549370AF71EFDC522532CB55C" +
    "48B9A39A21EE8E0CC8BB34C394AEC92155A16F95B646AA9E5F88C989EAF2D7F6" +
    "15BF5AFE619E27DFAB5ADBBD7999DB9590AB0F30C95C98DA39616CAD6494BE52",
]

# Lookup table from .rdata:10024401
LOOKUP_TABLE = bytes(range(1, 256))

def test_seccfg(seccfg_file):
    """Test RSA-derived AES keys against seccfg.bin"""
    
    print(f"\n{'='*60}")
    print(f"Testing RSA-derived AES keys on: {seccfg_file}")
    print(f"{'='*60}\n")
    
    # Read seccfg
    with open(seccfg_file, 'rb') as f:
        data = f.read()
    
    # Extract components (V4 structure)
    encrypted_hash = data[0x1C:0x3C]  # 32 bytes at offset 0x1C
    
    # Calculate expected hash
    temp_data = data[:0x1C] + b'\x00'*32 + data[0x3C:]
    expected_hash = sha256(temp_data).digest()
    
    print(f"Encrypted hash: {encrypted_hash.hex()}")
    print(f"Expected hash:  {expected_hash.hex()}\n")
    
    # Test each RSA key
    for key_idx, rsa_key_hex in enumerate(RSA_KEYS, 1):
        print(f"Testing RSA Key #{key_idx}...")
        
        rsa_bytes = bytes.fromhex(rsa_key_hex)
        
        # Method 1: Direct extraction (first 32 bytes)
        methods = [
            ("Direct 16+16", rsa_bytes[:16], rsa_bytes[16:32]),
            ("Direct 0+16", rsa_bytes[:16], rsa_bytes[:16]),  # Same key as IV
            ("SHA256 derived", sha256(rsa_bytes).digest()[:16], sha256(rsa_bytes).digest()[16:32]),
            ("MD5 derived", md5(rsa_bytes).digest(), md5(rsa_bytes).digest()),
            ("First 16 + zeros", rsa_bytes[:16], b'\x00'*16),
            ("Last 16+16", rsa_bytes[-32:-16], rsa_bytes[-16:]),
            ("With lookup XOR", bytes(a^b for a,b in zip(rsa_bytes[:16], LOOKUP_TABLE[:16])), 
                              bytes(a^b for a,b in zip(rsa_bytes[16:32], LOOKUP_TABLE[16:32]))),
        ]
        
        for method_name, key, iv in methods:
            try:
                cipher = AES.new(key, AES.MODE_CBC, iv)
                decrypted = cipher.decrypt(encrypted_hash)
                
                if decrypted == expected_hash:
                    print(f"\n{'='*60}")
                    print(f"✅ SUCCESS! FOUND THE KEY!")
                    print(f"{'='*60}")
                    print(f"RSA Key: #{key_idx}")
                    print(f"Method: {method_name}")
                    print(f"AES Key: {key.hex()}")
                    print(f"AES IV:  {iv.hex()}")
                    print(f"{'='*60}\n")
                    return True, key_idx, method_name, key, iv
                    
            except Exception as e:
                pass  # Try next method
        
        print(f"  ❌ RSA Key #{key_idx} - No match with any method\n")
    
    print("❌ None of the RSA keys matched\n")
    return False, None, None, None, None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_rsa_keys.py seccfg.bin")
        sys.exit(1)
    
    success, key_num, method, aes_key, aes_iv = test_seccfg(sys.argv[1])
    
    if success:
        print("\n🎉 SUCCESS! The key can be implemented in mtkclient!")
        print(f"\nAdd to seccfg.py alt_keys:")
        print(f"(b\"{aes_key.hex().upper()}\", b\"{aes_iv.hex().upper()}\")")
        sys.exit(0)
    else:
        print("\n⚠️ Keys didn't match. May need:")
        print("  - Different derivation method")
        print("  - Additional parameters")
        print("  - Combination of multiple keys")
        sys.exit(1)
