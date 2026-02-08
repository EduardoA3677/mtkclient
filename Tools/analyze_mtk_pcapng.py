#!/usr/bin/env python3
"""
Analizador de PCAPNG para protocolo MTK
Extrae y analiza la secuencia de handshake y comandos DA

Uso: python3 analyze_mtk_pcapng.py <archivo.pcapng>
"""

import subprocess
import sys
from binascii import unhexlify, hexlify

def analyze_pcapng(filename):
    """Analiza archivo pcapng para extraer protocolo MTK"""
    
    print("="*80)
    print(f"Analizando: {filename}")
    print("="*80)
    
    # Extraer todos los frames USB con datos
    result = subprocess.run([
        'tshark', '-r', filename,
        '-Y', 'usb',
        '-T', 'fields',
        '-e', 'frame.number',
        '-e', 'frame.time_relative', 
        '-e', 'usb.endpoint_address.direction',
        '-e', 'usb.data_fragment',
        '-E', 'separator=|'
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error ejecutando tshark: {result.stderr}")
        return
    
    lines = result.stdout.strip().split('\n')
    print(f"\nTotal de frames USB: {len(lines)}")
    
    # Buscar frames con datos
    frames_with_data = []
    for line in lines:
        parts = line.split('|')
        if len(parts) >= 4 and parts[3]:
            frame_num = parts[0]
            time = parts[1]
            direction = 'OUT' if parts[2] == '0' else 'IN '
            data = parts[3]
            
            if len(data) > 4:
                frames_with_data.append({
                    'frame': frame_num,
                    'time': float(time) if time else 0,
                    'dir': direction,
                    'data': data
                })
    
    print(f"Frames con datos: {len(frames_with_data)}\n")
    
    # Buscar patrones de handshake
    print("\n" + "="*80)
    print("ANÁLISIS DE HANDSHAKE")
    print("="*80)
    
    handshake_start = None
    for i, frame in enumerate(frames_with_data):
        data = frame['data']
        
        # Buscar "READY" response
        if data == '5245414459':
            if not handshake_start:
                handshake_start = i
                print(f"\n[HANDSHAKE START] Frame {frame['frame']} @ {frame['time']:.3f}s")
            print(f"  Frame {frame['frame']:>6} [{frame['dir']}]: READY")
        
        # Buscar comandos MAGIC (0xFEEEEEEF)
        elif data.startswith('efeeeefe'):
            print(f"  Frame {frame['frame']:>6} [{frame['dir']}]: MAGIC + cmd")
            
            # Siguiente frame debería ser el comando
            if i+1 < len(frames_with_data):
                next_frame = frames_with_data[i+1]
                cmd_data = next_frame['data']
                
                # Intentar decodificar
                try:
                    cmd_bytes = unhexlify(cmd_data)
                    cmd_text = cmd_bytes.decode('ascii', errors='ignore')
                    if cmd_text.isprintable():
                        print(f"  Frame {next_frame['frame']:>6} [{next_frame['dir']}]: '{cmd_text}'")
                    else:
                        print(f"  Frame {next_frame['frame']:>6} [{next_frame['dir']}]: {cmd_data[:40]}")
                except:
                    print(f"  Frame {next_frame['frame']:>6} [{next_frame['dir']}]: {cmd_data[:40]}")
        
        # Buscar "SYNC"
        elif data == '53594e43':
            print(f"  Frame {frame['frame']:>6} [{frame['dir']}]: SYNC")
        
        # Buscar patrones de dirección
        elif data in ['00200000', '0003f448', '00000100']:
            print(f"  Frame {frame['frame']:>6} [{frame['dir']}]: {data}")
        
        # Limitar output
        if handshake_start and i > handshake_start + 50:
            break
    
    # Buscar comandos XFLASH
    print("\n" + "="*80)
    print("COMANDOS XFLASH DETECTADOS")
    print("="*80)
    
    xflash_cmds = {
        '00010100': 'SETUP_ENVIRONMENT (0x010100)',
        '01010100': 'SETUP_HW_INIT (0x010101)',
        '09000100': 'DEVICE_CTRL (0x010009)',
        '01000400': 'GET_EMMC_INFO (0x040001)',
        '02000400': 'GET_NAND_INFO (0x040002)',
        '03000400': 'GET_NOR_INFO (0x040003)',
        '04000400': 'GET_UFS_INFO (0x040004)',
        '05000400': 'GET_DA_VERSION (0x040005)',
        '0c000400': 'GET_RAM_INFO (0x04000c)',
    }
    
    for frame in frames_with_data[handshake_start:handshake_start+100] if handshake_start else frames_with_data[:100]:
        data = frame['data']
        if data in xflash_cmds:
            print(f"Frame {frame['frame']:>6} [{frame['dir']}]: {xflash_cmds[data]}")
    
    # Estadísticas
    print("\n" + "="*80)
    print("ESTADÍSTICAS")
    print("="*80)
    
    out_count = sum(1 for f in frames_with_data if f['dir'] == 'OUT')
    in_count = sum(1 for f in frames_with_data if f['dir'] == 'IN ')
    
    print(f"Frames OUT: {out_count}")
    print(f"Frames IN:  {in_count}")
    print(f"Total:      {len(frames_with_data)}")
    
    # Buscar protocolo de autenticación
    print("\n" + "="*80)
    print("AUTENTICACIÓN DETECTADA")
    print("="*80)
    
    for frame in frames_with_data[:200]:
        data = frame['data']
        # Buscar comandos que empiecen con 0a20, 0820, 0520, 0620
        if data.startswith(('0a20', '0820', '0520', '0620')):
            print(f"Frame {frame['frame']:>6} [{frame['dir']}]: {data[:60]}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python3 analyze_mtk_pcapng.py <archivo.pcapng>")
        sys.exit(1)
    
    pcapng_file = sys.argv[1]
    analyze_pcapng(pcapng_file)
