#!/bin/bash

# Script para realizar cambios masivos en archivos HTML de las asignaturas
# Versión simplificada usando herramientas de línea de comandos

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="${1:-$SCRIPT_DIR}"

echo "=== Script de modificación masiva de HTML ==="
echo "Directorio base: $BASE_DIR"

# Función para procesar breadcrumbs
remove_breadcrumb_links() {
    local file="$1"
    echo "  Removiendo enlaces del breadcrumb en: $(basename "$file")"
    
    # Usar sed para remover enlaces pero mantener el texto
    sed -i.backup 's/<a[^>]*>\([^<]*\)<\/a>/\1/g' "$file" 
}

# Función para quitar el nav__menu
remove_nav_menu() {
    local file="$1"
    echo "  Removiendo nav__menu en: $(basename "$file")"
    
    # Buscar y remover el div nav__menu completo
    sed -i '/class="nav__menu"/,/<\/div>/c\
        <div class="nav__menu">\
            <!-- Menu de navegación por unidades -->\
            <p>Navegación simplificada</p>\
        </div>' "$file"
}

# Función para procesar un archivo HTML
process_html_file() {
    local file="$1"
    echo "Procesando: $file"
    
    # Verificar que el archivo existe
    if [[ ! -f "$file" ]]; then
        echo "  ⚠️  Archivo no encontrado: $file"
        return 1
    fi
    
    # Hacer backup del archivo original
    cp "$file" "${file}.original"
    
    # Aplicar modificaciones
    remove_breadcrumb_links "$file"
    remove_nav_menu "$file"
    
    echo "  ✓ Completado: $file"
}

# Función para procesar una asignatura
process_subject() {
    local subject="$1"
    local subject_path="$BASE_DIR/$subject"
    
    echo
    echo "=== Procesando asignatura: $subject ==="
    
    if [[ ! -d "$subject_path" ]]; then
        echo "⚠️  Directorio no encontrado: $subject_path"
        return 1
    fi
    
    # Encontrar todos los archivos HTML
    local html_files
    mapfile -t html_files < <(find "$subject_path" -name "*.html" -type f)
    
    echo "Encontrados ${#html_files[@]} archivos HTML"
    
    # Procesar cada archivo
    for file in "${html_files[@]}"; do
        process_html_file "$file"
    done
}

# Función principal
main() {
    if [[ ! -d "$BASE_DIR" ]]; then
        echo "Error: El directorio $BASE_DIR no existe"
        exit 1
    fi
    
    cd "$BASE_DIR"
    
    # Si se especifica una asignatura específica
    if [[ -n "$2" ]]; then
        process_subject "$2"
        exit 0
    fi
    
    # Encontrar todas las asignaturas (directorios que no empiecen con .)
    local subjects
    mapfile -t subjects < <(find . -maxdepth 1 -type d -not -name ".*" -printf "%f\n" | grep -v "^\.$")
    
    echo "Asignaturas encontradas: ${subjects[*]}"
    
    # Procesar cada asignatura
    for subject in "${subjects[@]}"; do
        process_subject "$subject"
    done
    
    echo
    echo "=== Procesamiento completado ==="
    echo "Los archivos originales se guardaron con extensión .original"
}

# Mostrar ayuda si se solicita
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    echo "Uso: $0 [DIRECTORIO] [ASIGNATURA]"
    echo
    echo "Parámetros:"
    echo "  DIRECTORIO    Directorio base donde están las asignaturas (default: directorio actual)"
    echo "  ASIGNATURA    Nombre de la asignatura específica a procesar (opcional)"
    echo
    echo "Ejemplos:"
    echo "  $0                        # Procesar todas las asignaturas en el directorio actual"
    echo "  $0 /ruta/a/asignaturas    # Procesar todas las asignaturas en la ruta especificada"
    echo "  $0 . derecho-1            # Procesar solo la asignatura 'derecho-1'"
    exit 0
fi

# Ejecutar función principal
main "$@"
