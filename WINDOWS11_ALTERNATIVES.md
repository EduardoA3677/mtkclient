# Windows 11 - Alternativas a UsbDk / Windows 11 - UsbDk Alternatives

**[Español](#español) | [English](#english)**

---

## Español

### ¿Es UsbDk compatible con Windows 11?

**SÍ**, UsbDk es compatible con Windows 11. El README oficial indica: "Works fine under Windows 10 and 11 :D"

Sin embargo, si experimentas problemas con UsbDk en Windows 11, existen alternativas:

---

## Alternativa 1: Modo Puerto Serial/COM (Recomendado para Windows 11)

### ✅ **Usar Puerto COM Directamente - Sin necesidad de UsbDk**

mtkclient soporta el modo puerto serial que **NO requiere UsbDk**. Esta es la forma más simple para Windows 11.

### Pasos:

#### 1. Instalar Driver MTK Serial Port
- Instalar el driver de puerto serial MTK estándar
- O usar el driver COM port predeterminado de Windows
- Verificar en "Administrador de dispositivos" que no haya signos de exclamación

#### 2. Detectar Puerto COM
Cuando conectes tu dispositivo MTK, Windows asignará un puerto COM (ej: COM3, COM4, etc.)

Para detectar automáticamente:
```bash
python mtk.py --serialport DETECT gettargetconfig
```

O especificar manualmente:
```bash
python mtk.py --serialport COM3 gettargetconfig
```

#### 3. Usar Comandos con Puerto Serial

**Leer particiones:**
```bash
python mtk.py --serialport COM3 r boot boot.bin
```

**Escribir particiones:**
```bash
python mtk.py --serialport COM3 w boot boot.bin
```

**Desbloquear bootloader:**
```bash
python mtk.py --serialport COM3 da seccfg unlock
```

**Mostrar GPT:**
```bash
python mtk.py --serialport COM3 printgpt
```

### ⚠️ Limitaciones del Modo Serial:
- **No soporta exploits de bootrom** (kamakiri, kamakiri2, amonet, hashimoto)
- Solo funciona en **modo preloader o META**
- Velocidad **más lenta** que USB directo
- Para usar exploits, necesitas UsbDk u otra alternativa USB

### ✅ Ventajas del Modo Serial:
- ✅ No requiere UsbDk
- ✅ No requiere drivers USB especiales
- ✅ Compatible con Windows 11 nativo
- ✅ Más estable en algunas configuraciones
- ✅ Funciona con driver COM port de Windows

---

## Alternativa 2: libusbK Driver (Zadig)

Si necesitas usar exploits y no quieres UsbDk, puedes usar **libusbK**:

### Pasos:

1. **Descargar Zadig:**
   - https://zadig.akeo.ie/
   - Ejecutar como administrador

2. **Instalar libusbK:**
   - Conectar dispositivo en modo BROM
   - En Zadig: Options → List All Devices
   - Seleccionar dispositivo MTK (VID: 0x0E8D)
   - Seleccionar "libusbK (v3.x.x)" en el dropdown
   - Click "Replace Driver" o "Install Driver"

3. **Verificar:**
   - mtkclient debería detectar el dispositivo automáticamente
   - El backend libusb1 en mtkclient soporta libusbK

### Nota:
- libusbK funciona bien en Windows 11
- Soporta exploits de bootrom
- Velocidad completa USB

---

## Alternativa 3: WinUSB Driver

WinUSB es el driver nativo de Windows y también funciona:

### Pasos:

1. **Usar Zadig** (igual que libusbK)
2. Seleccionar "WinUSB" en lugar de "libusbK"
3. Click "Replace Driver" o "Install Driver"

### Compatibilidad:
- ✅ Windows 11 nativo
- ✅ No requiere software adicional
- ⚠️ Puede requerir configuración adicional para algunos dispositivos

---

## Comparación de Métodos

| Método | UsbDk | Serial/COM | libusbK | WinUSB |
|--------|-------|------------|---------|---------|
| **Windows 11** | ✅ Sí | ✅ Sí | ✅ Sí | ✅ Sí |
| **Exploits BROM** | ✅ Sí | ❌ No | ✅ Sí | ✅ Sí |
| **Velocidad** | 🟢 Rápido | 🟡 Normal | 🟢 Rápido | 🟢 Rápido |
| **Instalación** | UsbDk MSI | Driver COM | Zadig | Zadig |
| **Estabilidad W11** | ✅ Alta | ✅ Alta | ✅ Alta | ✅ Media |

---

## Recomendaciones por Caso de Uso

### 📱 Solo leer/escribir particiones → Usar **Modo Serial/COM**
```bash
python mtk.py --serialport DETECT r boot boot.bin
```

### 🔓 Desbloquear bootloader → Usar **Modo Serial/COM**
```bash
python mtk.py --serialport COM3 da seccfg unlock
```

### 💥 Necesitas exploits (kamakiri, amonet) → Usar **UsbDk** o **libusbK**
```bash
python mtk.py --ptype kamakiri2 dumpbrom
```

### 🆕 Nuevo en Windows 11 → Empezar con **Modo Serial/COM**
- Más fácil de configurar
- Sin conflictos de drivers
- Suficiente para la mayoría de tareas

---

## Solución de Problemas Windows 11

### Problema: "Device not found" con UsbDk

**Solución 1:** Probar modo serial
```bash
python mtk.py --serialport DETECT gettargetconfig
```

**Solución 2:** Reinstalar UsbDk
1. Desinstalar UsbDk actual
2. Descargar versión más reciente: https://github.com/daynix/UsbDk/releases/
3. Instalar como administrador
4. Reiniciar PC

**Solución 3:** Usar libusbK con Zadig

### Problema: Puerto COM no detectado

1. Abrir "Administrador de dispositivos"
2. Buscar "Puertos (COM y LPT)"
3. Verificar que aparece "MediaTek USB Port" o similar
4. Si hay signo de exclamación: Click derecho → Actualizar driver
5. Seleccionar "Buscar automáticamente drivers"

---

## GUI: Uso de Puerto Serial

El GUI de mtkclient también soporta puerto serial:

1. Ejecutar: `python mtk_gui.py`
2. En el dropdown superior, seleccionar tu puerto COM (ej: COM3)
3. Conectar dispositivo
4. Usar funciones normalmente

**Nota:** Algunas funciones de exploit no estarán disponibles en modo serial.

---

## Conclusión

**Para Windows 11:**
- ✅ **Más fácil:** Modo Serial/COM (`--serialport`)
- ✅ **Más rápido:** UsbDk (funciona en W11)
- ✅ **Alternativa:** libusbK vía Zadig

**El modo serial es suficiente para el 90% de las tareas** y no requiere UsbDk.

---

# English

### Is UsbDk compatible with Windows 11?

**YES**, UsbDk is compatible with Windows 11. The official README states: "Works fine under Windows 10 and 11 :D"

However, if you experience issues with UsbDk on Windows 11, alternatives exist:

---

## Alternative 1: Serial/COM Port Mode (Recommended for Windows 11)

### ✅ **Use COM Port Directly - No UsbDk needed**

mtkclient supports serial port mode which **does NOT require UsbDk**. This is the simplest way for Windows 11.

### Steps:

#### 1. Install MTK Serial Port Driver
- Install standard MTK serial port driver
- Or use default Windows COM port driver
- Verify in "Device Manager" that there are no exclamation marks

#### 2. Detect COM Port
When you connect your MTK device, Windows will assign a COM port (e.g., COM3, COM4, etc.)

To auto-detect:
```bash
python mtk.py --serialport DETECT gettargetconfig
```

Or specify manually:
```bash
python mtk.py --serialport COM3 gettargetconfig
```

#### 3. Use Commands with Serial Port

**Read partitions:**
```bash
python mtk.py --serialport COM3 r boot boot.bin
```

**Write partitions:**
```bash
python mtk.py --serialport COM3 w boot boot.bin
```

**Unlock bootloader:**
```bash
python mtk.py --serialport COM3 da seccfg unlock
```

**Show GPT:**
```bash
python mtk.py --serialport COM3 printgpt
```

### ⚠️ Serial Mode Limitations:
- **Does not support bootrom exploits** (kamakiri, kamakiri2, amonet, hashimoto)
- Only works in **preloader or META mode**
- **Slower** speed than direct USB
- To use exploits, you need UsbDk or another USB alternative

### ✅ Serial Mode Advantages:
- ✅ No UsbDk required
- ✅ No special USB drivers required
- ✅ Native Windows 11 compatible
- ✅ More stable in some configurations
- ✅ Works with Windows COM port driver

---

## Alternative 2: libusbK Driver (Zadig)

If you need to use exploits and don't want UsbDk, you can use **libusbK**:

### Steps:

1. **Download Zadig:**
   - https://zadig.akeo.ie/
   - Run as administrator

2. **Install libusbK:**
   - Connect device in BROM mode
   - In Zadig: Options → List All Devices
   - Select MTK device (VID: 0x0E8D)
   - Select "libusbK (v3.x.x)" in dropdown
   - Click "Replace Driver" or "Install Driver"

3. **Verify:**
   - mtkclient should auto-detect the device
   - libusb1 backend in mtkclient supports libusbK

### Note:
- libusbK works well on Windows 11
- Supports bootrom exploits
- Full USB speed

---

## Alternative 3: WinUSB Driver

WinUSB is Windows' native driver and also works:

### Steps:

1. **Use Zadig** (same as libusbK)
2. Select "WinUSB" instead of "libusbK"
3. Click "Replace Driver" or "Install Driver"

### Compatibility:
- ✅ Native Windows 11
- ✅ No additional software required
- ⚠️ May require additional configuration for some devices

---

## Method Comparison

| Method | UsbDk | Serial/COM | libusbK | WinUSB |
|--------|-------|------------|---------|---------|
| **Windows 11** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **BROM Exploits** | ✅ Yes | ❌ No | ✅ Yes | ✅ Yes |
| **Speed** | 🟢 Fast | 🟡 Normal | 🟢 Fast | 🟢 Fast |
| **Installation** | UsbDk MSI | COM Driver | Zadig | Zadig |
| **W11 Stability** | ✅ High | ✅ High | ✅ High | ✅ Medium |

---

## Recommendations by Use Case

### 📱 Only read/write partitions → Use **Serial/COM Mode**
```bash
python mtk.py --serialport DETECT r boot boot.bin
```

### 🔓 Unlock bootloader → Use **Serial/COM Mode**
```bash
python mtk.py --serialport COM3 da seccfg unlock
```

### 💥 Need exploits (kamakiri, amonet) → Use **UsbDk** or **libusbK**
```bash
python mtk.py --ptype kamakiri2 dumpbrom
```

### 🆕 New to Windows 11 → Start with **Serial/COM Mode**
- Easier to configure
- No driver conflicts
- Sufficient for most tasks

---

## Windows 11 Troubleshooting

### Problem: "Device not found" with UsbDk

**Solution 1:** Try serial mode
```bash
python mtk.py --serialport DETECT gettargetconfig
```

**Solution 2:** Reinstall UsbDk
1. Uninstall current UsbDk
2. Download latest version: https://github.com/daynix/UsbDk/releases/
3. Install as administrator
4. Restart PC

**Solution 3:** Use libusbK with Zadig

### Problem: COM port not detected

1. Open "Device Manager"
2. Look for "Ports (COM & LPT)"
3. Verify "MediaTek USB Port" or similar appears
4. If exclamation mark: Right-click → Update driver
5. Select "Search automatically for drivers"

---

## GUI: Using Serial Port

The mtkclient GUI also supports serial port:

1. Run: `python mtk_gui.py`
2. In the top dropdown, select your COM port (e.g., COM3)
3. Connect device
4. Use functions normally

**Note:** Some exploit functions won't be available in serial mode.

---

## Conclusion

**For Windows 11:**
- ✅ **Easiest:** Serial/COM Mode (`--serialport`)
- ✅ **Fastest:** UsbDk (works on W11)
- ✅ **Alternative:** libusbK via Zadig

**Serial mode is sufficient for 90% of tasks** and doesn't require UsbDk.

---

## Additional Resources

- [Windows Installation Guide](README-WINDOWS.md)
- [Usage Instructions](README-USAGE.md)
- [UsbDk Releases](https://github.com/daynix/UsbDk/releases/)
- [Zadig Tool](https://zadig.akeo.ie/)

---

## Technical Details

### How Serial Mode Works

mtkclient detects the connection type in `Port.py`:
```python
if serialportname is not None and serialportname != "":
    self.cdc = SerialClass(portconfig=portconfig, loglevel=loglevel, devclass=10)
    self.cdc.setportname(serialportname)
else:
    self.cdc = UsbClass(portconfig=portconfig, loglevel=loglevel, devclass=10)
```

### USB Backend (libusb1)

mtkclient uses libusb1 backend which supports:
- ✅ UsbDk on Windows
- ✅ libusbK on Windows
- ✅ WinUSB on Windows
- ✅ libusb-1.0 on Linux/macOS

The backend is selected automatically in `usblib.py`:
```python
elif sys.platform.startswith('win32'):
    if calcsize("P") * 8 == 64:
        self.backend = usb.backend.libusb1.get_backend(find_library=lambda x: "libusb-1.0.dll")
    else:
        self.backend = usb.backend.libusb1.get_backend(find_library=lambda x: "libusb32-1.0.dll")
```

---

**Last Updated:** 2026-02-08  
**mtkclient version:** Latest from main branch
