# Sistema de config-overrides

Esta carpeta guarda archivos de configuracion que deben aplicarse antes de procesar los HTML.

Usala para archivos como:

- `activities_moodle.js`
- JSON de navegacion
- cualquier archivo que cambie menus, paginas o actividades durante la compilacion

## Ejemplos

```bash
# por default va a _all-units
./override --config asignaturas-produccion/biologia-1/u1/assets/scripts/activities_moodle.js

# equivalente explicito
./override --config --all-units asignaturas-produccion/biologia-1/u1/assets/scripts/activities_moodle.js

# solo para una unidad
./override --config --unit-specific asignaturas-produccion/biologia-1/u1/assets/scripts/activities_moodle.js
```

Estructuras resultantes:

```text
config-overrides/biologia-1/u1/assets/scripts/activities_moodle.js
config-overrides/biologia-1/_all-units/assets/scripts/activities_moodle.js
```
