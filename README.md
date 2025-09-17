# Scripts de Modificación Masiva de HTML

Este repositorio contiene scripts para realizar cambios masivos en archivos HTML de cursos académicos.

## Cambios que realizan los scripts

Los scripts automatizan las siguientes modificaciones:

1. **Eliminación de enlaces en breadcrumbs**: Quita las ligas del breadcrumb `course__header--breadcrumb` manteniendo solo el texto
2. **Navegación corregida**: Arregla las flechas de navegación `course__content__nav` para continuar correctamente al siguiente tema/unidad
3. **Nuevo menú de navegación**: Reemplaza `nav__menu` con un menú que navegue por unidades basado en `activities_moodle.js`
4. **Conversión de actividades**: Cambia enlaces de actividades a iframes con `?theme=photo`

## Scripts disponibles

### 1. Script de Python (Recomendado)

**Archivo**: `html_modifier_simple.py`

**Características**:
- ✅ Funcionalidad completa
- ✅ Manejo inteligente de la navegación basado en `activities_moodle.js`
- ✅ Conversión automática de actividades a iframes
- ✅ Solo usa librerías estándar de Python
- ✅ Manejo robusto de errores

**Uso**:
```bash
# Procesar todas las asignaturas
python3 html_modifier_simple.py

# Procesar una asignatura específica
python3 html_modifier_simple.py --subject derecho-1

# Especificar directorio
python3 html_modifier_simple.py /ruta/a/asignaturas

# Ver ayuda
python3 html_modifier_simple.py --help
```

### 2. Script de Bash (Versión simplificada)

**Archivo**: `html_modifier.sh`

**Características**:
- ✅ Muy rápido
- ✅ Solo herramientas estándar de Linux
- ⚠️ Funcionalidad limitada (solo breadcrumbs y eliminación de nav__menu)
- ✅ Crea backups automáticos

**Uso**:
```bash
# Procesar todas las asignaturas
./html_modifier.sh

# Procesar una asignatura específica
./html_modifier.sh . derecho-1

# Especificar directorio
./html_modifier.sh /ruta/a/asignaturas

# Ver ayuda
./html_modifier.sh --help
```

## Estructura esperada del proyecto

```
base_directory/
├── asignatura1/
│   ├── u1/
│   │   ├── assets/scripts/activities_moodle.js
│   │   └── u1/t1/*.html
│   ├── u2/
│   │   ├── assets/scripts/activities_moodle.js
│   │   └── u2/t1/*.html
│   └── ...
├── asignatura2/
│   └── ...
└── ...
```

## Formato de `activities_moodle.js`

El archivo debe contener:

```javascript
export const unit_themes = [
    {
        unit: "u1",
        themes: [
            { themeName: "Nombre del tema", themeURL: "t1", pages: "17" }
        ]
    },
    // ...
];

export const moodleActivities = [
    { idHTML: "u1a1", url: "mod/quiz/view.php?id=", id: "2537" },
    // ...
];
```

## Ejemplos de uso

### Caso de uso típico

Si tienes un directorio con asignaturas como `derecho-1` y `mate3`:

```bash
# Ir al directorio de trabajo
cd /ruta/a/tus/asignaturas

# Procesar todas las asignaturas (RECOMENDADO)
python3 html_modifier_simple.py

# O procesar solo una para probar
python3 html_modifier_simple.py --subject derecho-1
```

### Backup y recuperación

**El script de Python no crea backups automáticos**, por lo que es recomendable hacer backup manual:

```bash
# Hacer backup de todo el directorio
cp -r asignaturas asignaturas_backup

# O usar git si ya está en un repositorio
git add -A && git commit -m "Backup antes de modificar HTML"
```

**El script de Bash sí crea backups automáticos** con extensión `.original`.

### Verificar cambios

Después de ejecutar el script, puedes verificar los cambios:

```bash
# Ver diferencias en un archivo específico
diff archivo.html.original archivo.html

# Ver todos los archivos modificados (solo bash script)
find . -name "*.original"
```

## Solución de problemas

### Error: "No module named 'bs4'"

El script de Python simple no requiere BeautifulSoup. Si usas el script `html_modifier.py` (versión completa), instala las dependencias:

```bash
pip install beautifulsoup4
```

### Error: "command not found: python3"

Intenta con:
```bash
python html_modifier_simple.py
```

### Error de permisos

```bash
chmod +x html_modifier_simple.py
chmod +x html_modifier.sh
```

### Archivos no encontrados

Verifica que estés en el directorio correcto y que la estructura de carpetas sea la esperada.

## Contribuir

Para agregar nuevas funcionalidades o corregir errores:

1. Haz un fork del repositorio
2. Crea una rama para tu feature
3. Implementa los cambios
4. Prueba con datos de ejemplo
5. Envía un pull request

## Licencia

Este script es de uso interno para modificación de contenidos académicos.
