# Sistema de overrides

Esta carpeta guarda archivos HTML personalizados que sobrescriben el resultado generado en `out/`.

## Regla base

- No edites `out/` directamente.
- Genera primero, luego crea un override del HTML que quieres ajustar.
- La estructura dentro de `overrides/` debe coincidir con la de `out/`.

## Flujo recomendado

1. Genera el output normal:

```bash
rm -rf out && python3 html_modifier_v2_navigation.py
```

2. Crea el override desde el HTML generado o desde la ruta original:

```bash
python3 html_modifier_v2_navigation.py --init-override antropologia-1/u1/t1/3.html

# tambien funciona con la ruta fuente original
python3 html_modifier_v2_navigation.py --init-override asignaturas-produccion/biologia-1/u1/u1/t1/3.html

# helper corto
./override asignaturas-produccion/biologia-1/u1/u1/t1/3.html
```

3. Edita el archivo en `overrides/`:

```bash
nano overrides/antropologia-1/u1/t1/3.html
```

4. Regenera para reaplicar todo y volver a copiar el override:

```bash
rm -rf out && python3 html_modifier_v2_navigation.py
```

## Comandos utiles

```bash
# Crear override y abrirlo en el editor
./override --edit asignaturas-produccion/biologia-1/u1/u1/t1/3.html

# Regenerar output y luego crear override
./override --generate asignaturas-produccion/biologia-1/u1/u1/t1/3.html

# Listar overrides activos
./override --list
python3 html_modifier_v2_navigation.py --list-overrides

# Validar estructura de overrides
./override --validate
python3 html_modifier_v2_navigation.py --validate-overrides

# Generar sin aplicar overrides
python3 html_modifier_v2_navigation.py --no-overrides
```

El comando `--init-override` crea automaticamente las carpetas necesarias dentro de `overrides/`.

## Ejemplo de estructura

```text
overrides/
└── antropologia-1/
    └── u1/
        └── t1/
            └── 3.html
```

Ese archivo reemplaza a:

```text
out/antropologia-1/u1/t1/3.html
```

## Alcance actual

El sistema aplica overrides de archivos `.html`.
