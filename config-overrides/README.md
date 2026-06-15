# Sistema de config-overrides

`config-overrides/` guarda archivos que deben copiarse antes de procesar los HTML.

Usa esta carpeta cuando el archivo afecta la compilacion:

- `activities_moodle.js`
- JSON de navegacion
- archivos que cambian menus
- archivos que cambian paginas
- archivos que cambian actividades Moodle

## Diferencia con `overrides/`

`config-overrides/` se aplica antes de transformar HTML.

`overrides/` se aplica al final y reemplaza archivos ya generados.

Por eso `activities_moodle.js` debe ir aqui: el script lo lee para construir menus, flechas y actividades.

## Crear config-override para todas las unidades

Este es el default:

```bash
./override --config --edit asignaturas-produccion/matematicas-4/u1/assets/scripts/activities_moodle.js
```

Ruta resultante:

```text
config-overrides/matematicas-4/_all-units/assets/scripts/activities_moodle.js
```

Ese archivo se copia a todas las unidades de la asignatura antes de procesar HTML.

## Crear config-override para una sola unidad

```bash
./override --config --unit-specific --edit asignaturas-produccion/matematicas-4/u2/assets/scripts/activities_moodle.js
```

Ruta resultante:

```text
config-overrides/matematicas-4/u2/assets/scripts/activities_moodle.js
```

Ese archivo se copia solo a `out/matematicas-4/u2/...` antes de procesar HTML.

## Regenerar despues de editar

```bash
python3 html_modifier_v2_navigation.py --subject matematicas-4
```

O para todo:

```bash
python3 html_modifier_v2_navigation.py
```

## Listar y validar

```bash
python3 html_modifier_v2_navigation.py --list-config-overrides
python3 html_modifier_v2_navigation.py --validate-config-overrides
```

O con el helper:

```bash
./override --list
./override --validate
```

## Generar sin config-overrides

Util para diagnosticar si un problema viene de un archivo de configuracion:

```bash
python3 html_modifier_v2_navigation.py --subject matematicas-4 --no-config-overrides
```
