# MTKClient - Windows x64 Installer

## Requisitos del Sistema

- **Sistema Operativo**: Windows 7/8/10/11 (64-bit) - **SOLO x64**
- **Python**: 3.8 o superior (64-bit)
- **Privilegios**: Derechos de administrador

## Instalación

### Método 1: Instalación Automática (Recomendado)

1. Descomprima el archivo `mtkclient-windows-x64-installer.zip`
2. Haga clic derecho en `install.bat`
3. Seleccione "Ejecutar como administrador"
4. Siga las instrucciones en pantalla

El instalador realizará:
- ✅ Verificación de arquitectura x64
- ✅ Instalación de dependencias de Python
- ✅ Creación de accesos directos en el escritorio y menú inicio
- ✅ Configuración de PATH del sistema

**Nota**: Los ejecutables incluidos son de **un solo archivo** (.exe) con todo el contenido embebido. No necesitan archivos adicionales para funcionar.

### Método 2: Ejecutable Independiente (Sin Instalación)

Si descargó solo el ejecutable compilado:

1. Descargue `mtk_standalone_YYYYMMDD.exe` desde los artifacts del workflow
2. Colóquelo en cualquier carpeta
3. Haga doble clic para ejecutar

**Ventajas**:
- ✅ No requiere instalación de Python
- ✅ No requiere instalación de dependencias
- ✅ Un solo archivo .exe con todo incluido
- ✅ Portátil: puede ejecutarse desde USB o cualquier ubicación
- ✅ Comprimido con UPX para menor tamaño

**Limitaciones**:
- Requiere privilegios de administrador para operaciones USB
- Puede necesitar drivers USB (Zadig) instalados por separado

### Método 2: Instalación Manual

```batch
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la GUI
python mtk_gui.py
```

## Uso

### Interfaz Gráfica (GUI)

**Opción 1:** Doble clic en el acceso directo "MTKClient" en el escritorio o menú inicio

**Opción 2:** Ejecutar `mtk_gui_admin.bat` (solicita privilegios de administrador)

**Opción 3:** Desde línea de comandos:
```batch
pythonw mtk_gui.py
```

### Interfaz de Línea de Comandos (CLI)

```batch
python mtk.py [comando] [opciones]

# Ejemplos:
python mtk.py printgpt
python mtk.py r boot boot.img
python mtk.py rl backups/
```

## Controladores USB

Para el acceso a dispositivos USB en modo bootrom/preloader, puede necesitar:

1. **Zadig USB Driver** - Para modo bootrom/preloader
   - Descargar de: https://zadig.akeo.ie/
   - Instalar el driver WinUSB para el dispositivo MTK

2. **MediaTek USB VCOM Drivers** - Para modo DA
   - Generalmente incluidos con las herramientas SP Flash Tool

## Características

- ✅ Flasheo de particiones
- ✅ Lectura/escritura de flash completo
- ✅ Backup de todas las particiones
- ✅ Desbloqueo de bootloader
- ✅ Soporte para múltiples chipsets MediaTek
- ✅ Interfaz gráfica intuitiva
- ✅ Ejecución con privilegios de administrador

## Solución de Problemas

### El instalador falla al verificar la arquitectura

**Causa**: Sistema de 32 bits detectado

**Solución**: Este instalador solo funciona en Windows x64. Necesita una versión de 64 bits de Windows.

### Python no está instalado

**Solución**: Descargue e instale Python 3.8+ (64-bit) desde https://www.python.org/

Asegúrese de marcar "Add Python to PATH" durante la instalación.

### Error de permisos al instalar

**Solución**: Ejecute `install.bat` con privilegios de administrador (clic derecho → "Ejecutar como administrador")

### El dispositivo no se detecta

**Soluciones**:
1. Instale los drivers USB con Zadig
2. Verifique que el dispositivo esté en modo bootrom/preloader
3. Pruebe otro cable USB
4. Pruebe otro puerto USB (preferiblemente USB 2.0)

## Desinstalación

Actualmente no hay un desinstalador automático. Para desinstalar manualmente:

1. Elimine el acceso directo del escritorio y menú inicio
2. Elimine la carpeta de instalación
3. (Opcional) Desinstale las dependencias de Python:
   ```batch
   pip uninstall pyusb pycryptodome pycryptodomex colorama shiboken6 pyside6 pyserial fusepy
   ```

## Soporte

- GitHub Issues: https://github.com/EduardoA3677/mtkclient/issues
- Documentación: Consulte los archivos README-*.md en la carpeta principal

## Licencia

GPLv3 License - Ver archivo LICENSE para más detalles

## Créditos

MTK Flash Client (c) B.Kerler 2018-2026
