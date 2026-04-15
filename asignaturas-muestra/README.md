# Asignaturas de Muestra

Esta carpeta contiene asignaturas de prueba que se usan para desarrollo y testing.

**Estas asignaturas SÍ se suben a git.**

## Asignaturas incluidas:

- `antropologia-1/` - Antropología I (3 unidades)
- `mate3/` - Matemáticas III (5 unidades)
- `derecho-1/` - Derecho I

## Propósito:

Estas asignaturas se usan para:
- Probar cambios en el script
- Verificar que el diseño funcione correctamente
- Documentar ejemplos de uso
- CI/CD y tests automatizados

## Procesamiento:

Estas asignaturas se procesan automáticamente cuando ejecutas:

```bash
python3 html_modifier_v2_navigation.py
```

El output se genera en `/out/` con solo el nombre de la asignatura (sin la carpeta `asignaturas-muestra/`).
