# Portabilidad del Proyecto

## ✅ El script ES portable

El script `html_modifier_v2_navigation.py` **NO tiene rutas hardcodeadas**. Funciona en cualquier equipo y directorio.

### Cómo funciona:

```bash
# Funciona desde cualquier directorio
cd /ruta/cualquiera/mi-proyecto
python3 html_modifier_v2_navigation.py

# También puedes especificar el directorio
python3 html_modifier_v2_navigation.py /otra/ruta

# O cambiar el directorio de output
python3 html_modifier_v2_navigation.py --output mi-output
```

### Rutas relativas automáticas:

El script usa `Path().resolve()` y calcula rutas relativas automáticamente:
- ✅ Detecta carpetas fuente (antropologia-1/, mate3/, etc.)
- ✅ Lee `assets/` del directorio actual
- ✅ Genera output en `out/` (configurable con `--output`)
- ✅ Calcula rutas relativas entre páginas automáticamente

---

## ⚠️ URLs hardcodeadas (intencionales)

Hay **2 URLs** hardcodeadas en el script que son **específicas del sistema PEL de la UNAM**:

### Ubicación: `html_modifier_v2_navigation.py` líneas 415-418

```python
<a href="https://pel.cch.unam.mx/?theme=moove" class="pel-header-nav__link">
    <i class="ri-arrow-left-line"></i> Volver a mis cursos
</a>
<a href="https://pel.cch.unam.mx/login/logout.php?sesskey=acdpwASwF9&alt=logout" class="pel-header-nav__link">
    <i class="ri-logout-box-line"></i> Cerrar sesión
</a>
```

### ¿Por qué están hardcodeadas?

Estas URLs son **enlaces funcionales** en las páginas generadas:
- **"Volver a mis cursos"**: Regresa al dashboard de Moodle
- **"Cerrar sesión"**: Logout del sistema PEL

Son específicas del entorno de producción de la UNAM y **deben estar hardcodeadas** porque:
1. Son las mismas para todas las asignaturas
2. Apuntan al servidor de producción de PEL
3. Los usuarios finales necesitan estos enlaces funcionales

---

## 🔧 Cómo cambiar las URLs (si es necesario)

Si necesitas cambiar estas URLs (por ejemplo, para un entorno de desarrollo o testing):

### Opción 1: Editar el script directamente

```bash
nano html_modifier_v2_navigation.py
# Buscar líneas 415-418 y cambiar las URLs
```

### Opción 2: Usar variables de entorno (modificación futura)

Podrías modificar el script para leer URLs de variables de entorno:

```python
import os

MOODLE_URL = os.getenv('MOODLE_URL', 'https://pel.cch.unam.mx')
LOGOUT_URL = os.getenv('LOGOUT_URL', f'{MOODLE_URL}/login/logout.php?sesskey=acdpwASwF9&alt=logout')
```

### Opción 3: Crear archivo de configuración

Crear un archivo `config.json`:

```json
{
  "moodle_url": "https://pel.cch.unam.mx",
  "theme": "moove",
  "logout_sesskey": "acdpwASwF9"
}
```

---

## 📋 Resumen

| Elemento | ¿Hardcodeado? | ¿Portable? | Notas |
|----------|---------------|------------|-------|
| Rutas de archivos | ❌ No | ✅ Sí | Usa rutas relativas automáticas |
| Directorio base | ❌ No | ✅ Sí | Configurable con argumentos |
| Directorio output | ❌ No | ✅ Sí | Default: `out/`, configurable con `--output` |
| URLs de navegación | ✅ Sí | ⚠️ Parcial | URLs del sistema PEL UNAM |
| Assets (CSS/JS/Logo) | ❌ No | ✅ Sí | Lee desde `assets/` relativo |

---

## 🚀 Para usar en otro equipo

1. **Clona o copia el proyecto**:
   ```bash
   git clone <repo>
   # o
   cp -r fix-asignaturas-pel /nuevo/lugar
   ```

2. **Entra al directorio**:
   ```bash
   cd fix-asignaturas-pel
   ```

3. **Ejecuta el script**:
   ```bash
   rm -rf out && python3 html_modifier_v2_navigation.py
   ```

4. **¡Listo!** Funciona sin configuración adicional.

---

## 🔍 Verificar portabilidad

```bash
# Prueba en diferentes directorios
cd /tmp
python3 /ruta/completa/html_modifier_v2_navigation.py /ruta/a/asignaturas

# Prueba con output personalizado
python3 html_modifier_v2_navigation.py --output /tmp/test-output

# Prueba dry-run (no modifica nada)
python3 html_modifier_v2_navigation.py --dry-run
```

---

## 📝 Conclusión

El proyecto es **completamente portable** excepto por las URLs de navegación del sistema PEL, que son intencionales y específicas del entorno de producción de la UNAM.

Para desarrollo local o testing, puedes modificar esas URLs según necesites.
