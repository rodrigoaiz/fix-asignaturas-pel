# Workflow: sistema de navegacion PEL v2

Esta es la guia operativa para generar `out/` y trabajar sin perder cambios.

## Comandos principales

Generar todo:

```bash
python3 html_modifier_v2_navigation.py
```

Generar una sola asignatura:

```bash
python3 html_modifier_v2_navigation.py --subject mate3
python3 html_modifier_v2_navigation.py --subject matematicas-4
```

Ver que haria sin escribir:

```bash
python3 html_modifier_v2_navigation.py --dry-run
python3 html_modifier_v2_navigation.py --dry-run --subject mate3
```

Ver ayuda:

```bash
python3 html_modifier_v2_navigation.py --help
```

## Regla de oro

- Edita `assets/` para cambios globales de navegacion, CSS, JS o logo.
- Edita `overrides/` para cambios finales en HTML generado.
- Edita `config-overrides/` para archivos que alimentan la generacion.
- No edites `out/` como fuente de verdad. Se puede borrar o recrear.
- No necesitas crear carpetas de overrides a mano; usa `./override`.

## Que procesa el script

El script busca asignaturas en:

```text
asignaturas-muestra/
asignaturas-produccion/
```

El output queda plano en:

```text
out/<asignatura>/<unidad>/<tema>/<pagina>.html
```

Ejemplo:

```text
out/matematicas-4/u3/t1/3.html
```

Si la fuente viene como `u3/u3/t1/3.html`, el script la reorganiza en el output.

## Flujo para cambios globales

### Cambiar CSS

```bash
nano assets/pel-navigation.css
python3 html_modifier_v2_navigation.py
```

### Cambiar JavaScript de navegacion

```bash
nano assets/pel-navigation.js
python3 html_modifier_v2_navigation.py
```

### Cambiar logo

```bash
nano assets/logo-pel.svg
python3 html_modifier_v2_navigation.py
```

## Flujo para cambiar un HTML puntual

1. Genera la asignatura:

```bash
python3 html_modifier_v2_navigation.py --subject mate3
```

2. Crea o abre el override:

```bash
./override --edit out/mate3/u2/t3/1.html
```

Tambien puedes usar la ruta fuente:

```bash
./override --edit asignaturas-muestra/mate3/u2/t3/1.html
```

3. Edita el archivo en `overrides/`.

4. Regenera la asignatura:

```bash
python3 html_modifier_v2_navigation.py --subject mate3
```

El override se aplica al final y reemplaza el archivo generado.

## Flujo para `activities_moodle.js`

`activities_moodle.js` afecta menus, paginas y actividades durante la compilacion.
Por eso va en `config-overrides/`, no en `overrides/`.

Crear o abrir config-override para todas las unidades:

```bash
./override --config --edit asignaturas-produccion/matematicas-4/u1/assets/scripts/activities_moodle.js
```

Eso crea algo como:

```text
config-overrides/matematicas-4/_all-units/assets/scripts/activities_moodle.js
```

Crear o abrir config-override solo para una unidad:

```bash
./override --config --unit-specific --edit asignaturas-produccion/matematicas-4/u2/assets/scripts/activities_moodle.js
```

Eso crea algo como:

```text
config-overrides/matematicas-4/u2/assets/scripts/activities_moodle.js
```

Despues regenera:

```bash
python3 html_modifier_v2_navigation.py --subject matematicas-4
```

## Validar antes de generar

```bash
python3 html_modifier_v2_navigation.py --validate-overrides
python3 html_modifier_v2_navigation.py --validate-config-overrides
```

O con el helper:

```bash
./override --validate
```

## Listar overrides activos

```bash
python3 html_modifier_v2_navigation.py --list-overrides
python3 html_modifier_v2_navigation.py --list-config-overrides
```

O con el helper:

```bash
./override --list
```

## Generar sin aplicar overrides

Para diagnosticar si un problema viene de un override:

```bash
python3 html_modifier_v2_navigation.py --no-overrides
python3 html_modifier_v2_navigation.py --no-config-overrides
```

Tambien puedes combinarlo con una asignatura:

```bash
python3 html_modifier_v2_navigation.py --subject mate3 --no-overrides
```

## Script simple

`html_modifier_simple.py` existe para reparaciones basicas sin insertar la navegacion PEL v2.
No es el flujo principal.

```bash
python3 html_modifier_simple.py --subject mate3
python3 html_modifier_simple.py --dry-run --subject mate3
```

## Verificar el resultado

Abrir en navegador:

```bash
firefox out/mate3/u2/t3/1.html
```

Ver HTMLs generados:

```bash
find out/mate3 -maxdepth 3 -type f -name '*.html' | sort
```

Buscar rutas duplicadas que no deberian quedar:

```bash
find out -path '*/u[0-9]/u[0-9]/*.html' -print
```

Si ese ultimo comando imprime HTMLs, hay una estructura duplicada que revisar.

## Troubleshooting

### `FileNotFoundError: .../mate3`

El script estaba intentando buscar `mate3` en la raiz del repo.
Usa el script actualizado o pasa la ruta completa:

```bash
python3 html_modifier_v2_navigation.py --subject asignaturas-muestra/mate3
```

### Mi cambio se perdio

Probablemente editaste `out/`. Mueve el cambio a `overrides/` y regenera.

### El menu no refleja cambios de actividades

El cambio debe estar en `config-overrides/`, no en `overrides/`.

### El CSS no cambia

Edita `assets/pel-navigation.css`, regenera y fuerza recarga del navegador.

### El output tiene carpetas raras

No pases carpetas contenedoras como `--subject`.
Estos comandos no son correctos:

```bash
python3 html_modifier_v2_navigation.py --subject asignaturas-produccion
python3 html_modifier_v2_navigation.py --subject out
```

Usa la asignatura:

```bash
python3 html_modifier_v2_navigation.py --subject matematicas-4
```

## Checklist final

- CSS nuevo visible.
- Logo visible en header y footer.
- Botones de unidades funcionan.
- Navegacion de temas funciona.
- Navegacion de paginas funciona.
- Flechas anterior/siguiente funcionan.
- Actividades Moodle cargan como iframe.
- Validaciones de overrides pasan.
