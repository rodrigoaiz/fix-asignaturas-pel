# Sistema de overrides

`overrides/` guarda archivos finales que reemplazan el resultado generado en `out/`.

Usa esta carpeta para cambios puntuales de HTML ya procesado.

## Regla base

- No edites `out/` como fuente de verdad.
- Crea un override del archivo que quieres ajustar.
- Edita el archivo dentro de `overrides/`.
- Regenera con `html_modifier_v2_navigation.py`.

## Crear o abrir un override

Desde un archivo generado:

```bash
./override --edit out/mate3/u2/t3/1.html
```

Desde un archivo fuente:

```bash
./override --edit asignaturas-muestra/mate3/u2/t3/1.html
./override --edit asignaturas-produccion/matematicas-4/u3/u3/t1/3.html
```

El helper normaliza la ruta y crea algo como:

```text
overrides/mate3/u2/t3/1.html
overrides/matematicas-4/u3/t1/3.html
```

## Regenerar despues de editar

Para una asignatura:

```bash
python3 html_modifier_v2_navigation.py --subject mate3
```

Para todo:

```bash
python3 html_modifier_v2_navigation.py
```

## Listar y validar

```bash
./override --list
./override --validate
```

Equivalentes directos:

```bash
python3 html_modifier_v2_navigation.py --list-overrides
python3 html_modifier_v2_navigation.py --validate-overrides
```

## Cuando no usar overrides

No uses `overrides/` para archivos que alimentan la compilacion.

Estos van en `config-overrides/`:

- `activities_moodle.js`
- JSON de navegacion
- archivos que cambian menus
- archivos que cambian paginas
- archivos que cambian actividades

Ejemplo correcto para `activities_moodle.js`:

```bash
./override --config --edit asignaturas-produccion/matematicas-4/u1/assets/scripts/activities_moodle.js
```

## Generar sin overrides

Util para diagnosticar si un problema viene de un override:

```bash
python3 html_modifier_v2_navigation.py --subject mate3 --no-overrides
```

## Ejemplo

Este archivo:

```text
overrides/mate3/u2/t3/1.html
```

reemplaza a:

```text
out/mate3/u2/t3/1.html
```

al final de la generacion.
