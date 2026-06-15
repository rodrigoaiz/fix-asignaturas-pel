# Scripts de modificacion masiva de HTML

Este repositorio genera una version reparada de las asignaturas en `out/`.
Los archivos fuente no se editan durante la generacion.

## Comando recomendado

Usa el script v2 para el flujo normal:

```bash
python3 html_modifier_v2_navigation.py
```

Ese comando procesa automaticamente las asignaturas que encuentre en:

```text
asignaturas-muestra/
asignaturas-produccion/
```

El resultado queda en:

```text
out/<asignatura>/
```

No necesitas borrar `out/` antes: el script v2 limpia el output completo cuando se ejecuta sin `--subject`.

## Procesar una sola asignatura

Puedes pasar solo el nombre de la asignatura:

```bash
python3 html_modifier_v2_navigation.py --subject mate3
python3 html_modifier_v2_navigation.py --subject matematicas-4
```

Tambien puedes pasar la ruta relativa completa:

```bash
python3 html_modifier_v2_navigation.py --subject asignaturas-muestra/mate3
python3 html_modifier_v2_navigation.py --subject asignaturas-produccion/matematicas-4
```

Cuando usas `--subject`, el script solo recrea esa asignatura dentro de `out/`.

## Previsualizar sin escribir cambios

```bash
python3 html_modifier_v2_navigation.py --dry-run
python3 html_modifier_v2_navigation.py --dry-run --subject mate3
```

## Que hace el script v2

1. Copia la asignatura fuente a `out/`.
2. Reorganiza estructuras Moodle duplicadas, por ejemplo `u1/u1/t1/` a `u1/t1/`.
3. Corrige rutas de assets despues de reorganizar.
4. Copia `assets/pel-navigation.css`, `assets/pel-navigation.js` y `assets/logo-pel.svg` a cada unidad.
5. Quita ligas del breadcrumb.
6. Corrige flechas anterior/siguiente.
7. Reemplaza la navegacion vieja por el sistema PEL v2.
8. Convierte actividades Moodle en iframes con `?theme=photo`.
9. Aplica `config-overrides/` antes de procesar HTML.
10. Aplica `overrides/` al final.

## Que script debo usar

### `html_modifier_v2_navigation.py`

Es el script principal. Usalo casi siempre.

```bash
python3 html_modifier_v2_navigation.py
python3 html_modifier_v2_navigation.py --subject mate3
```

Incluye el nuevo diseno PEL, overrides, config-overrides, assets compartidos y reorganizacion de carpetas.

### `html_modifier_simple.py`

Es una version anterior sin el nuevo diseno PEL. Solo usala si necesitas las reparaciones basicas sin insertar la navegacion v2.

```bash
python3 html_modifier_simple.py
python3 html_modifier_simple.py --subject mate3
python3 html_modifier_simple.py --dry-run --subject mate3
```

Tambien busca asignaturas dentro de `asignaturas-muestra/` y `asignaturas-produccion/`.

## Estructura esperada

```text
fix-asignaturas-pel/
├── asignaturas-muestra/
│   ├── antropologia-1/
│   ├── derecho-1/
│   └── mate3/
├── asignaturas-produccion/
│   └── matematicas-4/
├── assets/
│   ├── logo-pel.svg
│   ├── pel-navigation.css
│   └── pel-navigation.js
├── config-overrides/
├── overrides/
├── html_modifier_v2_navigation.py
├── html_modifier_simple.py
└── out/
```

Las asignaturas pueden venir en formato ya plano:

```text
asignatura/u1/t1/1.html
```

o en formato Moodle duplicado:

```text
asignatura/u1/u1/t1/1.html
```

El script v2 reorganiza el output para que quede plano en `out/`.

## Overrides de HTML

No edites `out/` directamente. Si quieres cambiar un HTML final, crea un override:

```bash
./override --edit out/mate3/u2/t3/1.html
```

Tambien funciona desde la ruta fuente:

```bash
./override --edit asignaturas-muestra/mate3/u2/t3/1.html
```

Eso crea o abre:

```text
overrides/mate3/u2/t3/1.html
```

Despues regenera:

```bash
python3 html_modifier_v2_navigation.py --subject mate3
```

## Config-overrides

Si el archivo afecta la compilacion, no lo pongas en `overrides/`.
Usa `config-overrides/`.

Ejemplos de archivos de config:

- `activities_moodle.js`
- JSON de navegacion
- cualquier archivo que cambie menus, paginas o actividades

Crear config-override compartido para todas las unidades:

```bash
./override --config --edit asignaturas-produccion/matematicas-4/u1/assets/scripts/activities_moodle.js
```

Crear config-override solo para una unidad:

```bash
./override --config --unit-specific --edit asignaturas-produccion/matematicas-4/u2/assets/scripts/activities_moodle.js
```

## Validar overrides

```bash
python3 html_modifier_v2_navigation.py --list-overrides
python3 html_modifier_v2_navigation.py --list-config-overrides
python3 html_modifier_v2_navigation.py --validate-overrides
python3 html_modifier_v2_navigation.py --validate-config-overrides
```

El helper corto tambien lista y valida ambos:

```bash
./override --list
./override --validate
```

## Verificar salida

Abre un HTML generado:

```bash
firefox out/mate3/u2/t3/1.html
```

O revisa la estructura:

```bash
find out/mate3 -maxdepth 3 -type f -name '*.html' | sort
```

## Errores comunes

### `FileNotFoundError: .../mate3`

Estabas usando un script que buscaba `mate3` directo en la raiz. Ahora ambos scripts resuelven `mate3` a `asignaturas-muestra/mate3`, pero si ves este error revisa que estes usando la version actual del repo.

### Cambie `out/` y se perdio

Es esperado. `out/` se regenera. Guarda cambios finales en `overrides/`.

### Cambie `activities_moodle.js` y no afecto el menu

Pon ese archivo en `config-overrides/`, no en `overrides/`.

### El output copia carpetas raras como `out/out`

No uses carpetas contenedoras como asignatura. Estos comandos son invalidos:

```bash
python3 html_modifier_v2_navigation.py --subject asignaturas-produccion
python3 html_modifier_v2_navigation.py --subject out
```

Usa el nombre de la asignatura:

```bash
python3 html_modifier_v2_navigation.py --subject matematicas-4
```
