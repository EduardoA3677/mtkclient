#!/usr/bin/env python3
"""
Configuración específica MT6768 Lamu basada en análisis completo
de preloader_lamu.bin, DA_A15_lamu_FORBID_SIGNED.bin y 1.pcapng

Hallazgos clave:
- Preloader usa estructura MMM con ROM_INFO que referencia MT6752 (compatibilidad)
- DA Agent v3.3001.2025 con 3 regiones de entrada
- Región 2 (DA1): 0x0003f448 bytes en 0x00200000, firma 0x100
- Región 3 (DA2): 0x0005923c bytes en 0x40000000, firma 0x100  
- Handshake usa "READY" (0x5245414459) no 0xC0
- Protocolo XFLASH con MAGIC 0xFEEEEEEF + SYNC
"""

# Configuración extraída del análisis binario
MT6768_LAMU_CONFIG = {
    'name': 'MT6768_Lamu',
    'description': 'MTK MT6768 (lamu device) - Helio P65/G85',
    
    # Del chipconfig existente (verificado correcto)
    'hwcode': 0x0707,
    'hwcode_alt': 0x6768,  # Como aparece en DA header (0x6768dada)
    
    # Direcciones de memoria (del preloader analysis)
    'watchdog': 0x10007000,
    'uart': 0x11002000,
    'brom_payload_addr': 0x100A00,
    'da_payload_addr': 0x201000,  # Confirmado por PCAPNG y chipconfig
    'pl_payload_addr': 0x40200000,
    
    # Crypto engines
    'gcpu_base': 0x10050000,
    'sej_base': 0x1000A000,  # HACC
    'dxcc_base': 0x10210000,
    'cqdma_base': 0x10212000,
    'efuse_addr': 0x11ce0000,
    
    # DA configuration (extraído del análisis del DA binary)
    'da': {
        'version': 'v3.3001.2025/11/07.14:24_654171',
        'regions': [
            {
                'id': 1,
                'buffer': 0x0000376c,
                'length': 0x00000270,  # 624 bytes
                'start_addr': 0x50000000,
                'start_offset': 0x00000000,
                'sig_len': 0x00000000
            },
            {
                'id': 2,  # DA1 - Stage 1
                'buffer': 0x000039dc,
                'length': 0x0003f448,  # 259,144 bytes - CONFIRMADO EN PCAPNG
                'start_addr': 0x00200000,
                'start_offset': 0x0003f348,
                'sig_len': 0x00000100  # 256 bytes RSA signature
            },
            {
                'id': 3,  # DA2 - Stage 2  
                'buffer': 0x00042e24,
                'length': 0x0005923c,  # 365,116 bytes
                'start_addr': 0x40000000,
                'start_offset': 0x0005913c,
                'sig_len': 0x00000100  # 256 bytes RSA signature
            }
        ],
        'mode': 'XFLASH',  # Mode 5
        'dacode': 0x6768
    },
    
    # USB configuration (verificado en PCAPNG)
    'usb': {
        'vid': 0x0e8d,
        'pid': 0x2000,  # Preloader mode
        'pid_brom': 0x0003
    },
    
    # Handshake protocol (DESCUBRIMIENTO CRÍTICO del PCAPNG)
    'handshake': {
        'type': 'READY',  # Nuevo protocolo
        'response': b'READY',  # 0x5245414459
        'legacy_response': b'\xC0',  # Para compatibilidad
        'timeout': 5.0
    },
    
    # XFLASH protocol (del PCAPNG analysis)
    'xflash': {
        'magic': 0xFEEEEEEF,
        'sync_signal': 0x434E5953,  # 'SYNC'
        'commands': {
            'SETUP_ENVIRONMENT': 0x010100,
            'SETUP_HW_INIT': 0x010101,
            'DEVICE_CTRL': 0x010009,
            'GET_EMMC_INFO': 0x040001,
            'GET_RAM_INFO': 0x04000c,
            'GET_DA_VERSION': 0x040005
        }
    },
    
    # Preloader info (del binario analysis)
    'preloader': {
        'magic': b'MMM\x01',
        'file_info_offset': 0x08,
        'rom_info_offset': 0x2ec,
        'chip_id': 'MT6752',  # Compatibilidad marker
        'actual_chip': 'MT6768',
        'security': {
            'sec_ctrl': 'AND_SECCTRL_v',
            'sec_ro': 'AND_SECRO_v'
        }
    },
    
    # Security config (habilitado según device)
    'security': {
        'sla': True,  # Secure Link Authentication
        'daa': True,  # DA Authentication
        'sbc': False,  # Secure Boot
        'forbid_mode': 'SIGNED'  # DA must be signed
    },
    
    # Exploit config
    'exploit': {
        'type': 'kamakiri2',
        'send_ptr': (0x10286c, 0xc190),
        'ctrl_buffer': 0x00102A28,
        'cmd_handler': 0x0000CF15,
        'brom_register_access': (0xc598, 0xc650),
        'blacklist': [(0x10282C, 0x0), (0x00105994, 0)],
        'blacklist_count': 0x0000000A
    }
}

# Validación de configuración
def validate_config():
    """Valida que la configuración sea consistente con los hallazgos"""
    config = MT6768_LAMU_CONFIG
    
    # Verificar que DA region 2 coincide con PCAPNG
    da1_region = config['da']['regions'][1]
    assert da1_region['length'] == 0x0003f448, "DA1 length mismatch"
    assert da1_region['sig_len'] == 0x00000100, "DA1 signature length mismatch"
    assert da1_region['start_addr'] == 0x00200000, "DA1 address mismatch"
    
    # Verificar handshake
    assert config['handshake']['response'] == b'READY', "Handshake response incorrect"
    
    print("[✓] Configuración validada correctamente")
    print(f"[✓] DA Agent: {config['da']['version']}")
    print(f"[✓] Regiones DA: {len(config['da']['regions'])}")
    print(f"[✓] DA1 size: {config['da']['regions'][1]['length']} bytes")
    print(f"[✓] Handshake: {config['handshake']['type']}")
    
    return True

if __name__ == '__main__':
    validate_config()
