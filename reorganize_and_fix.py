#!/usr/bin/env python3
"""
Script para reorganizar las carpetas y arreglar los HTML
Mueve de estructura u1/u1/t1/ a u1/t1/ y ajusta todas las rutas

Mejoras:
- Regex compilados como constantes (eficiencia)
- Una sola pasada de lectura/escritura por archivo HTML
- Mejor manejo de errores y logging
- Output independiente: las asignaturas base NO se modifican
"""

import os
import shutil
import re
from pathlib import Path


class FolderReorganizer:
    # Compiled regex for path fixing
    RE_CSS_DOUBLE_DOT = re.compile(r'href="../../assets/')
    RE_SRC_DOUBLE_DOT = re.compile(r'src="../../assets/')
    RE_NAV_DOUBLE_UNIT = re.compile(r'href="../(u\d+)/\1/')

    def __init__(self, output_dir=None):
        self.output_dir = Path(output_dir) if output_dir else None

    def reorganize_subject_folders(self, subject_path):
        """Reorganiza las carpetas de una asignatura - maneja diferentes estructuras"""
        subject_path = Path(subject_path)

        print(f"  📁 Reorganizando {subject_path.name}...")

        # Buscar todas las carpetas de unidades (u1, u2, u3, etc.)
        unit_folders = sorted([
            f for f in subject_path.iterdir()
            if f.is_dir() and f.name.startswith('u') and f.name[1:].isdigit()
        ])

        if not unit_folders:
            print(f"    ⚠ No se encontraron carpetas de unidad en {subject_path.name}")
            return

        for unit_folder in unit_folders:
            print(f"    Procesando {unit_folder.name}...")

            # Caso 1: Estructura u1/u1/t1/ (mate3, derecho-1)
            inner_unit_folder = unit_folder / unit_folder.name

            # Caso 2: Estructura u1/build/u1/t1/ (antropologia-1)
            build_unit_folder = unit_folder / "build" / unit_folder.name

            target_structure = None
            source_path = None

            if inner_unit_folder.exists() and inner_unit_folder.is_dir():
                print(f"      → Estructura tipo 1: {inner_unit_folder}")
                target_structure = "type1"
                source_path = inner_unit_folder

            elif build_unit_folder.exists() and build_unit_folder.is_dir():
                print(f"      → Estructura tipo 2: {build_unit_folder}")
                target_structure = "type2"
                source_path = build_unit_folder

            if target_structure and source_path:
                self._move_contents(source_path, unit_folder, target_structure)
            else:
                print(f"      ✓ No hay estructura duplicada en {unit_folder.name}")

    def _move_contents(self, source_path, unit_folder, target_structure):
        """Mueve el contenido de la carpeta fuente a la carpeta de unidad"""
        for item in sorted(source_path.iterdir()):
            destination = unit_folder / item.name

            if destination.exists():
                if destination.is_dir():
                    self.merge_directories(item, destination)
                else:
                    print(f"        ⚠ {destination.name} ya existe, saltando...")
            else:
                print(f"        → Moviendo {item.name}")
                shutil.move(str(item), str(destination))

        # Tipo 2: mover assets si existe
        if target_structure == "type2":
            build_folder = unit_folder / "build"
            assets_folder = build_folder / "assets"

            if assets_folder.exists():
                destination_assets = unit_folder / "assets"
                if destination_assets.exists():
                    self.merge_directories(assets_folder, destination_assets)
                else:
                    print(f"        → Moviendo assets")
                    shutil.move(str(assets_folder), str(destination_assets))

            # Limpiar build si está vacío
            self._safe_rmdir(build_folder)

        # Limpiar carpeta fuente vacía
        self._safe_rmdir(source_path)

        # Limpiar build padre si quedó vacío (tipo 1)
        if target_structure == "type1":
            build_folder = unit_folder / "build"
            self._safe_rmdir(build_folder)

    @staticmethod
    def _safe_rmdir(path):
        """Intenta eliminar un directorio vacío de forma segura"""
        try:
            if path.exists() and not any(path.iterdir()):
                path.rmdir()
        except Exception:
            pass  # Silenciar errores de directorio no vacío

    def merge_directories(self, source, destination):
        """Fusiona directorios recursivamente"""
        for item in source.iterdir():
            dest_item = destination / item.name

            if item.is_dir():
                if dest_item.exists():
                    self.merge_directories(item, dest_item)
                else:
                    shutil.move(str(item), str(dest_item))
            else:
                if dest_item.exists():
                    print(f"          ⚠ {dest_item.name} ya existe, saltando...")
                else:
                    shutil.move(str(item), str(dest_item))

    def fix_html_paths_after_reorganization(self, subject_path):
        """Arregla las rutas en los HTML después de la reorganización — una sola pasada"""
        subject_path = Path(subject_path)

        print(f"  🔧 Arreglando rutas HTML en {subject_path.name}...")

        html_files = list(subject_path.rglob("*.html"))
        updated_count = 0

        for html_file in html_files:
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Apply all path fixes in one pass
                content = self.RE_CSS_DOUBLE_DOT.sub('href="../assets/', content)
                content = self.RE_SRC_DOUBLE_DOT.sub('src="../assets/', content)
                content = self.RE_NAV_DOUBLE_UNIT.sub(r'href="../\1/', content)

                if content != open(html_file, 'r', encoding='utf-8').read():
                    with open(html_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    updated_count += 1

            except Exception as e:
                print(f"    ✗ Error en {html_file}: {e}")

        print(f"    ✓ {updated_count} archivos actualizados de {len(html_files)}")


def prepare_output(base_dir, output_dir, subject_name):
    """Copia la asignatura base al directorio de output"""
    source = base_dir / subject_name
    
    # Extraer solo el nombre de la asignatura (sin la carpeta padre)
    # Ej: "asignaturas-muestra/mate3" -> "mate3"
    subject_base_name = Path(subject_name).name
    dest = output_dir / subject_base_name

    if dest.exists():
        print(f"  ♻  {subject_base_name} ya existe en output, recreando...")
        shutil.rmtree(dest)

    shutil.copytree(source, dest)
    print(f"  📋 {subject_name} copiada a {dest}")
    return dest


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Reorganiza carpetas de asignaturas y arregla rutas HTML. '
                    'Las asignaturas base NO se modifican — se copia todo al directorio de output.'
    )
    parser.add_argument(
        'directory', nargs='?', default='.',
        help='Directorio base donde están las asignaturas (default: directorio actual)'
    )
    parser.add_argument(
        '--output', '-o', default='out',
        help='Directorio de output para las asignaturas reorganizadas (default: out/)'
    )
    parser.add_argument(
        '--subject', '-s',
        help='Procesar solo una asignatura específica'
    )

    args = parser.parse_args()

    base_path = Path(args.directory).resolve()
    output_path = Path(args.output).resolve()
    output_path.mkdir(parents=True, exist_ok=True)

    # Buscar todas las asignaturas en asignaturas-muestra/ y asignaturas-produccion/
    subjects = []
    
    # Buscar en asignaturas-muestra/
    muestra_folder = base_path / "asignaturas-muestra"
    if muestra_folder.exists() and muestra_folder.is_dir():
        for subject_dir in sorted(muestra_folder.iterdir()):
            if subject_dir.is_dir() and not subject_dir.name.startswith('.'):
                # Verificar que tenga carpetas de unidades (u1, u2, etc.)
                has_units = any(
                    d.is_dir() and d.name.startswith('u') and d.name[1:].isdigit()
                    for d in subject_dir.iterdir()
                )
                if has_units:
                    # Guardar ruta relativa desde base_path
                    subjects.append(muestra_folder.name + '/' + subject_dir.name)
    
    # Buscar en asignaturas-produccion/
    produccion_folder = base_path / "asignaturas-produccion"
    if produccion_folder.exists() and produccion_folder.is_dir():
        for subject_dir in sorted(produccion_folder.iterdir()):
            if subject_dir.is_dir() and not subject_dir.name.startswith('.'):
                # Verificar que tenga carpetas de unidades (u1, u2, etc.)
                has_units = any(
                    d.is_dir() and d.name.startswith('u') and d.name[1:].isdigit()
                    for d in subject_dir.iterdir()
                )
                if has_units:
                    # Guardar ruta relativa desde base_path
                    subjects.append(produccion_folder.name + '/' + subject_dir.name)

    if not subjects:
        print("No se encontraron asignaturas en asignaturas-muestra/ ni asignaturas-produccion/")
        return

    print("Asignaturas encontradas:")
    for i, subject in enumerate(subjects, 1):
        print(f"  {i}. {subject}")

    print(f"\nDirectorio base: {base_path}")
    print(f"Directorio output: {output_path}")
    print("\nOpciones:")
    print("  0. Procesar TODAS las asignaturas")
    print("  1-N. Procesar solo la asignatura seleccionada")
    print("  q. Salir")

    choice = input("\nSelecciona una opción: ").strip().lower()

    if choice == 'q':
        print("Cancelado por el usuario.")
        return

    subjects_to_process = []

    if choice == '0':
        subjects_to_process = subjects
        print(f"\n🔄 Procesando TODAS las asignaturas ({len(subjects)} encontradas)")
    else:
        try:
            index = int(choice) - 1
            if 0 <= index < len(subjects):
                subjects_to_process = [subjects[index]]
                print(f"\n🔄 Procesando solo: {subjects[index]}")
            else:
                print("❌ Índice inválido.")
                return
        except ValueError:
            print("❌ Entrada inválida.")
            return

    reorganizer = FolderReorganizer()

    for subject in subjects_to_process:
        print(f"\n{'='*50}")
        print(f"PROCESANDO: {subject}")
        print(f"{'='*50}")

        # Copy to output directory
        output_subject = prepare_output(base_path, output_path, subject)

        # Reorganize in output
        reorganizer.reorganize_subject_folders(output_subject)

        # Fix paths in output
        reorganizer.fix_html_paths_after_reorganization(output_subject)

        print(f"  ✅ Output en: {output_subject}")

    print(f"\n{'='*50}")
    print(f"🎉 Proceso completado para {len(subjects_to_process)} asignatura(s).")
    print(f"📁 Archivos en: {output_path}")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
