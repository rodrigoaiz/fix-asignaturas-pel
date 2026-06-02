# Workflow: Sistema de Navegación PEL v2

Documentación del flujo de trabajo para el sistema de navegación de asignaturas PEL con nuevo diseño.

## 🚀 Comando principal (hace TODO)

```bash
# Desde el directorio del proyecto
cd /ruta/a/tu/proyecto
rm -rf out && python3 html_modifier_v2_navigation.py
```

### ¿Qué hace este comando?

1. ✅ **Borra el output anterior** (`rm -rf out`)
2. ✅ **Copia asignaturas** desde carpetas fuente → `/out/`
3. ✅ **Copia assets** a cada unidad:
   - `pel-navigation.css` → cada unidad
   - `pel-navigation.js` → cada unidad  
   - `logo-pel.svg` → cada unidad
4. ✅ **Repara HTMLs**:
   - Quita links del breadcrumb
   - Arregla navegación de flechas
   - Reemplaza menú con botones de unidades
   - Convierte actividades a iframes
   - Limpia URLs de Moodle rotas
5. ✅ **Aplica nuevo diseño**:
   - 3 barras de navegación (institucional, usuario, curso)
   - Navegación de temas
   - Navegación de páginas
   - Logo PEL en header y footer
   - Footer reubicado

### Resultado:
Todo listo en `/out/` con diseño nuevo y bugs reparados.

---

## 📝 Cómo hacer cambios

### 1. Editar estilos CSS

```bash
# EDITA el archivo fuente
nano assets/pel-navigation.css

# REGENERA todo
rm -rf out && python3 html_modifier_v2_navigation.py
```

El CSS se copia automáticamente a:
```
/out/antropologia-1/u1/assets/css/pel-navigation.css
/out/antropologia-1/u2/assets/css/pel-navigation.css
/out/mate3/u1/assets/css/pel-navigation.css
...
```

### 2. Editar el logo

```bash
# EDITA el logo fuente
nano assets/logo-pel.svg

# REGENERA todo
rm -rf out && python3 html_modifier_v2_navigation.py
```

El logo se copia automáticamente a cada unidad en `assets/logo-pel.svg`

### 3. Editar JavaScript de navegación

```bash
# EDITA el JS fuente
nano assets/pel-navigation.js

# REGENERA todo
rm -rf out && python3 html_modifier_v2_navigation.py
```

### 4. Editar lógica del script Python

```bash
# EDITA el script
nano html_modifier_v2_navigation.py

# REGENERA todo
rm -rf out && python3 html_modifier_v2_navigation.py
```

### 5. Editar contenido HTML sin perder cambios

```bash
# GENERA primero
rm -rf out && python3 html_modifier_v2_navigation.py

# CREA override desde un HTML generado
python3 html_modifier_v2_navigation.py --init-override antropologia-1/u1/t1/3.html

# o desde la ruta original de la asignatura
python3 html_modifier_v2_navigation.py --init-override asignaturas-produccion/biologia-1/u1/u1/t1/3.html

# helper corto
./override asignaturas-produccion/biologia-1/u1/u1/t1/3.html

# helper que crea y abre el archivo
./override --edit asignaturas-produccion/biologia-1/u1/u1/t1/3.html

# EDITA el override
nano overrides/antropologia-1/u1/t1/3.html

# REGENERA todo
rm -rf out && python3 html_modifier_v2_navigation.py
```

El override reemplaza el HTML generado correspondiente al final del proceso.
No necesitas crear carpetas a mano: `--init-override` normaliza la ruta y crea toda la estructura en `overrides/`.
Si quieres, `./override --generate ...` regenera `out/` antes de crear el override.

---

## ⚠️ REGLAS IMPORTANTES

### ❌ NUNCA hagas esto:
- **NO edites archivos en `/out/`** → se borran en cada regeneración
- **NO modifiques las carpetas fuente** (antropologia-1/, mate3/, derecho-1/)

### ✅ SIEMPRE haz esto:
- **Edita solo archivos en `/assets/`** o el script Python
- **Para contenido HTML puntual, edita en `/overrides/`**
- **Regenera con el comando completo** después de editar
- **Verifica cambios en `/out/`** abriendo un HTML en el navegador

---

## 📂 Estructura del proyecto

```
fix-asignaturas-pel/              ← Tu directorio del proyecto
│
├── 📁 asignaturas-muestra/      ← Asignaturas de prueba (EN GIT)
│   ├── antropologia-1/
│   ├── mate3/
│   └── derecho-1/
│
├── 📁 asignaturas-produccion/   ← Todas las demás (NO EN GIT)
│   ├── historia-1/
│   ├── fisica-1/
│   └── ... (agrega aquí tus asignaturas)
│
├── 📁 assets/                   ← EDITA AQUÍ
│   ├── pel-navigation.css      ← Estilos de navegación
│   ├── pel-navigation.js       ← JavaScript de navegación
│   └── logo-pel.svg            ← Logo PEL
│
├── 📁 overrides/                ← EDITA HTMLS PERSONALIZADOS AQUÍ
│   ├── README.md
│   └── antropologia-1/u1/t1/3.html
│
├── 📁 logo/
│   └── logo-pel.svg            ← Logo original
│
├── 📄 html_modifier_v2_navigation.py  ← Script principal
│
└── 📁 out/                     ← Output (se regenera)
    ├── antropologia-1/
    │   ├── u1/
    │   │   ├── assets/
    │   │   │   ├── css/pel-navigation.css
    │   │   │   ├── scripts/pel-navigation.js
    │   │   │   └── logo-pel.svg
    │   │   └── t1/
    │   │       ├── 1.html
    │   │       └── 2.html
    │   ├── u2/
    │   └── u3/
    └── mate3/
```

### 📝 Explicación de carpetas:

#### `asignaturas-muestra/` 
- **Propósito**: Asignaturas de prueba para desarrollo
- **En git**: ✅ SÍ (se suben al repositorio)
- **Uso**: Testing, ejemplos, documentación

#### `asignaturas-produccion/`
- **Propósito**: Todas las demás asignaturas reales
- **En git**: ❌ NO (está en `.gitignore`)
- **Uso**: Procesamiento de asignaturas completas para producción
- **Nota**: Coloca aquí tus asignaturas sin preocuparte por el tamaño

El script procesa **AMBAS** carpetas automáticamente.

---

## 🎨 Sistema de navegación (diseño)

### Barra 1: Institucional (Negra - `#1E1E1E`)
- Logo PEL (32px altura) + texto "Programas de Estudio en Línea"
- Botones de unidades (U1, U2, U3...)

### Barra 2: Usuario (Naranja - `#F26C4F`)
- "Volver a mis cursos"
- "Cerrar sesión"

### Barra 3: Curso (Teal - `#2F8F8B`)
- Título de la asignatura centrado
- Gradiente teal

### Navegación de Temas
- Fondo gris claro (`#F5F5F5`)
- Tabs horizontales
- Tema activo resaltado
- Full width

### Navegación de Páginas
- Botones numerados (32px × 32px)
- Página activa con fondo teal
- Alineados a la izquierda

---

## 🔍 Verificar cambios

### Abrir en navegador:
```bash
# Ejemplo: ver antropologia-1, unidad 2, tema 1, página 1
firefox out/antropologia-1/u2/t1/1.html

# O con el navegador que uses
google-chrome out/mate3/u1/t1/1.html
```

### Ver logs del script:
```bash
python3 html_modifier_v2_navigation.py 2>&1 | less
```

### Ver overrides activos:
```bash
python3 html_modifier_v2_navigation.py --list-overrides
python3 html_modifier_v2_navigation.py --validate-overrides
```

### Ver qué se copió:
```bash
find out/antropologia-1/u1/assets -type f
```

---

## 🐛 Troubleshooting

### El CSS no se actualiza
1. Verifica que editaste `/assets/pel-navigation.css` (NO el de `/out/`)
2. Borra todo y regenera: `rm -rf out && python3 html_modifier_v2_navigation.py`
3. Refresca el navegador con Ctrl+Shift+R (forzar recarga)

### Mi cambio de contenido se perdio
1. Verifica que el cambio esta en `overrides/` y no en `out/`
2. Lista overrides: `python3 html_modifier_v2_navigation.py --list-overrides`
3. Valida estructura: `python3 html_modifier_v2_navigation.py --validate-overrides`
4. Regenera sin `--no-overrides`

### El logo no aparece
1. Verifica que existe: `ls -lh assets/logo-pel.svg`
2. Regenera: `rm -rf out && python3 html_modifier_v2_navigation.py`
3. Revisa la consola del navegador (F12) por errores 404
4. Verifica la ruta en el HTML: `grep logo-pel.svg out/*/u1/t1/1.html`

### Las rutas están rotas
- El script calcula rutas relativas automáticamente
- Verifica estructura: debe ser `asignatura/uX/tY/N.html`
- Revisa que `config.js` existe en cada unidad

### Script falla con error
```bash
# Ver error completo
python3 html_modifier_v2_navigation.py 2>&1 | tee error.log

# Modo dry-run para ver qué haría sin modificar
python3 html_modifier_v2_navigation.py --dry-run
```

---

## 📋 Checklist después de cambios

Después de modificar assets y regenerar, verifica:

- [ ] CSS se ve correcto en el navegador
- [ ] Logo aparece en header (barra negra)
- [ ] Logo aparece en footer
- [ ] Botones de unidades funcionan
- [ ] Navegación de temas funciona
- [ ] Navegación de páginas funciona
- [ ] Flechas anterior/siguiente funcionan
- [ ] Sin errores en consola del navegador (F12)

---

## 🎓 Asignaturas procesadas

El script procesa automáticamente:
- **antropologia-1**: Antropología I (3 unidades)
- **mate3**: Matemáticas III (5 unidades)  
- **derecho-1**: Derecho I (unidades variables)

Para agregar más, solo copia la carpeta al directorio base y ejecuta el script.

---

## 📝 Resumen ejecutivo

**Para cambiar algo:**
1. Edita archivo en `/assets/`
2. Si es HTML puntual, crea/edita override en `/overrides/`
3. Ejecuta: `rm -rf out && python3 html_modifier_v2_navigation.py`
4. Abre HTML en navegador para verificar

**Eso es todo.** 🚀
