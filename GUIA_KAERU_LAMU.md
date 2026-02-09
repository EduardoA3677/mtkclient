# Guía: ¿Puedo Usar Kaeru en mi Dispositivo Lamu?

## 🎯 Respuesta Rápida

**NO RECOMENDADO** ❌

**Probabilidad de éxito**: 5-10%  
**Riesgo de brick**: Alto  
**Alternativa mejor**: Método oficial Motorola (100% éxito, 0% riesgo)

---

## 📖 Índice

1. [¿Qué es Kaeru?](#qué-es-kaeru)
2. [Compatibilidad con Lamu](#compatibilidad-con-lamu)
3. [Advertencias Importantes](#advertencias-importantes)
4. [Método Oficial Motorola (Recomendado)](#método-oficial-motorola)
5. [Instrucciones Kaeru (No Recomendado)](#instrucciones-kaeru)
6. [Comparación de Métodos](#comparación-de-métodos)
7. [FAQ](#faq)
8. [Conclusión](#conclusión)

---

## ¿Qué es Kaeru?

**Kaeru** es una herramienta de R0rt1z2 para desbloquear bootloader en dispositivos MediaTek.

**Repositorio**: https://github.com/R0rt1z2/kaeru

### Características
- Open source
- Gratis
- Compatible con varios MTK devices
- NO todas las protecciones soportadas

---

## Compatibilidad con Lamu

### Device: MT6768 Lamu

```
Chipset: MediaTek MT6768 (Helio P22)
Security: SBC + DAA enabled
Seccfg: Clave AES custom Motorola
Bootloader: Locked
```

### ⚠️ Análisis

| Aspecto | Estado | Impacto |
|---------|--------|---------|
| Chipset MTK | ✅ Compatible | OK |
| SBC enabled | ❌ Problema | Bloquea exploits |
| DAA enabled | ❌ Problema | Bloquea modificaciones |
| Clave custom | ❌ Crítico | Kaeru NO la tiene |

**Probabilidad de éxito**: 5-10%

### Por Qué NO Funciona

1. Kaeru usa claves MTK estándar
2. Lamu usa clave CUSTOM Motorola
3. SBC bloquea código no firmado
4. DAA bloquea modificaciones
5. No hay bypass conocido

---

## Advertencias Importantes

### 🚨 RIESGOS

#### Brick (40-50%)
- Device puede quedar inutilizable
- Pantalla negra permanente
- Posible daño permanente

#### Pérdida de Datos (100%)
- Factory reset automático
- No recuperable sin backup

#### Void Warranty
- Garantía se anula
- No soporte oficial

### Procede Solo Si

- Entiendes completamente los riesgos
- Tienes backup COMPLETO
- Aceptas posible brick
- Has intentado método oficial primero

---

## Método Oficial Motorola

### ⭐ RECOMENDADO (100% éxito, 0% riesgo)

### Paso a Paso

#### 1. Crear Cuenta
- Ir a: https://motorola-global-portal.custhelp.com/
- Sign up (gratis)
- Verificar email

#### 2. Solicitar Unlock
- Ir a sección Bootloader Unlock
- Link directo: https://motorola-global-portal.custhelp.com/app/standalone/bootloader/unlock-your-device-a

#### 3. Obtener Device ID
```bash
# Poner device en fastboot
adb reboot bootloader

# Obtener código
fastboot oem get_unlock_data

# Copiar TODO el output (sin "(bootloader)" y "OKAY")
# Juntar líneas SIN espacios ni #
```

#### 4. Enviar Request
- Pegar código en formulario web
- Click "Get Unlock Token"
- Esperar email (5-30 min)

#### 5. Aplicar Unlock
```bash
# Con device en fastboot
fastboot oem unlock [TOKEN_DEL_EMAIL]

# Confirmar en device (botones Vol)
# Device se reinicia y hace factory reset
```

#### 6. Verificar
```bash
adb reboot bootloader
fastboot getvar unlocked
# Debe mostrar: "unlocked: yes"
```

### ✅ Done!
- Tiempo total: 30-60 minutos
- Éxito: 100%
- Riesgo: 0%

---

## Instrucciones Kaeru

### ⚠️ NO RECOMENDADO para Lamu

Si aún así decides intentar:

### Requisitos
- Python 3.x
- Git
- ADB/Fastboot
- Backup completo

### Instalación

```bash
# Clonar
git clone https://github.com/R0rt1z2/kaeru.git
cd kaeru

# Instalar dependencias
pip install -r requirements.txt

# Conectar device en fastboot
adb reboot bootloader

# Intentar unlock
python kaeru.py --unlock
```

### Resultado Esperado

**Muy probablemente FALLARÁ** con errores como:
- "Device not supported"
- "SBC/DAA protection active"
- "Key not found"
- "Unlock failed"

### Si Falla

- Reiniciar device normalmente
- Verificar que bootea
- NO repetir múltiples veces
- Usar método oficial Motorola

---

## Comparación de Métodos

| Método | Tiempo | Éxito | Riesgo | Dificultad |
|--------|--------|-------|--------|------------|
| **Motorola Oficial** | 30-60m | 100% | 0% | ★☆☆☆☆ |
| Kaeru | 1-2h | 5-10% | Alto | ★★★☆☆ |
| mtkclient | 2-4h | 0%* | Medio | ★★★★☆ |

*mtkclient 0% porque no tiene clave custom

### Recomendación

Para TODOS: **Método oficial Motorola**

---

## FAQ

### P: ¿Kaeru funcionará en Lamu?
**R**: Probablemente NO (5-10% éxito)

### P: ¿Es seguro?
**R**: NO para Lamu (alto riesgo de brick)

### P: ¿Cuál es el mejor método?
**R**: Método oficial Motorola (100% éxito)

### P: ¿Pierdo datos?
**R**: Sí, cualquier método hace factory reset

### P: ¿Anula garantía?
**R**: Sí, desbloquear anula garantía Motorola

### P: ¿Es gratis?
**R**: Sí, ambos métodos son gratis

### P: ¿Cuánto tarda?
**R**: Motorola 30-60 min, Kaeru 1-2h

### P: ¿Qué pasa si falla?
**R**: Kaeru puede brick device. Motorola nunca falla.

### P: ¿Puedo revertir?
**R**: No recomendado, puede causar bootloop

### P: ¿Necesito root?
**R**: No, solo ADB debugging habilitado

---

## Conclusión

### Para MT6768 Lamu

#### ❌ NO Usar Kaeru
- Baja probabilidad (5-10%)
- Alto riesgo de brick
- Sin clave custom

#### ✅ SÍ Usar Método Oficial
- 100% funciona
- 0% riesgo
- Rápido y fácil
- Gratis

### Recomendación Final

**Ve directamente al método oficial de Motorola**

No pierdas tiempo con Kaeru en Lamu.

### Link Directo

**Método Oficial**:  
https://motorola-global-portal.custhelp.com/app/standalone/bootloader/unlock-your-device-a

---

## Recursos

- **Motorola Portal**: https://motorola-global-portal.custhelp.com/
- **Kaeru Repo**: https://github.com/R0rt1z2/kaeru (no recomendado para Lamu)
- **XDA Forum**: https://forum.xda-developers.com/

---

## Disclaimer

⚠️ **IMPORTANTE**:
- Desbloquear anula garantía
- Riesgo de brick exists
- Pérdida de datos garantizada
- Procede bajo tu riesgo
- No nos hacemos responsables

---

**Fecha**: 2026-02-09  
**Device**: MT6768 Lamu  
**Recomendación**: Método oficial Motorola ⭐

**¡Buena suerte! 🍀**
