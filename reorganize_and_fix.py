#!/usr/bin/env python3
"""
Script para reorganizar las carpetas y arreglar los HTML
Mueve de estructura u1/u1/t1/ a u1/t1/ y ajusta todas las rutas
"""

import os
import shutil
from pathlib import Path
import re

class FolderReorganizer:
    def __init__(self):
        pass
    
    def reorganize_subject_folders(self, subject_path):
        """Reorganiza las carpetas de una asignatura - maneja diferentes estructuras"""
        subject_path = Path(subject_path)
        
        print(f"Reorganizando {subject_path.name}...")
        
        # Buscar todas las carpetas de unidades (u1, u2, u3, etc.)
        unit_folders = [f for f in subject_path.iterdir() if f.is_dir() and f.name.startswith('u') and f.name[1:].isdigit()]
        
        for unit_folder in sorted(unit_folders):
            print(f"  Procesando {unit_folder.name}...")
            
            # Caso 1: Estructura u1/u1/t1/ (mate3, derecho-1)
            inner_unit_folder = unit_folder / unit_folder.name
            
            # Caso 2: Estructura u1/build/u1/t1/ (antropologia-1)
            build_unit_folder = unit_folder / "build" / unit_folder.name
            
            target_structure = None
            source_path = None
            
            if inner_unit_folder.exists() and inner_unit_folder.is_dir():
                print(f"    Encontrada estructura tipo 1: {inner_unit_folder}")
                target_structure = "type1"
                source_path = inner_unit_folder
                
            elif build_unit_folder.exists() and build_unit_folder.is_dir():
                print(f"    Encontrada estructura tipo 2: {build_unit_folder}")
                target_structure = "type2"
                source_path = build_unit_folder
                
            if target_structure and source_path:
                # Mover todo el contenido hacia la carpeta de unidad principal
                for item in source_path.iterdir():
                    destination = unit_folder / item.name
                    
                    if destination.exists():
                        if destination.is_dir():
                            # Si ya existe una carpeta con el mismo nombre, mover el contenido
                            self.merge_directories(item, destination)
                        else:
                            print(f"      ADVERTENCIA: {destination} ya existe, saltando...")
                    else:
                        print(f"      Moviendo {item.name}")
                        shutil.move(str(item), str(destination))
                
                # Para tipo 2, también necesitamos mover assets si existe
                if target_structure == "type2":
                    build_folder = unit_folder / "build"
                    assets_folder = build_folder / "assets"
                    
                    if assets_folder.exists():
                        destination_assets = unit_folder / "assets"
                        if destination_assets.exists():
                            self.merge_directories(assets_folder, destination_assets)
                        else:
                            print(f"      Moviendo assets")
                            shutil.move(str(assets_folder), str(destination_assets))
                    
                    # Eliminar la carpeta build completa si está vacía
                    try:
                        if build_folder.exists() and not any(build_folder.iterdir()):
                            build_folder.rmdir()
                    except:
                        pass
                
                # Eliminar la carpeta fuente vacía
                try:
                    if source_path.exists() and not any(source_path.iterdir()):
                        source_path.rmdir()
                        
                        # Si era tipo 1, también intentar eliminar el directorio padre si está vacío
                        if target_structure == "type1" and source_path.parent == unit_folder:
                            pass  # Ya fue eliminado
                        elif target_structure == "type2":
                            # Intentar eliminar build si está vacío
                            build_folder = unit_folder / "build"
                            if build_folder.exists() and not any(build_folder.iterdir()):
                                build_folder.rmdir()
                except Exception as e:
                    print(f"      No se pudo eliminar carpeta vacía: {e}")
            else:
                print(f"    No se encontró estructura duplicada en {unit_folder.name}")
    
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
                    print(f"        ADVERTENCIA: {dest_item} ya existe, saltando archivo...")
                else:
                    shutil.move(str(item), str(dest_item))
    
    def fix_html_paths_after_reorganization(self, subject_path):
        """Arregla las rutas en los HTML después de la reorganización"""
        subject_path = Path(subject_path)
        
        print(f"Arreglando rutas HTML en {subject_path.name}...")
        
        # Buscar todos los archivos HTML
        html_files = list(subject_path.rglob("*.html"))
        
        for html_file in html_files:
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # Arreglar rutas de CSS (../../assets/ -> ../assets/)
                content = re.sub(
                    r'href="../../assets/',
                    'href="../assets/',
                    content
                )
                
                # Arreglar rutas de scripts (../../assets/ -> ../assets/)
                content = re.sub(
                    r'src="../../assets/',
                    'src="../assets/',
                    content
                )
                
                # Arreglar rutas de imágenes (../../assets/ -> ../assets/)
                content = re.sub(
                    r'src="../../assets/',
                    'src="../assets/',
                    content
                )
                
                # Arreglar rutas en el menú de navegación
                # De ../u1/u1/t1/1.html a ../u1/t1/1.html
                content = re.sub(
                    r'href="../(u\d+)/\1/',
                    r'href="../\1/',
                    content
                )
                
                if content != original_content:
                    with open(html_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"    Actualizado: {html_file.relative_to(subject_path)}")
                
            except Exception as e:
                print(f"    ERROR procesando {html_file}: {e}")

def main():
    # Directorio base
    base_path = Path("/home/rodrigo-aizpuru/Descargas/fixeo")
    
    reorganizer = FolderReorganizer()
    
    # Buscar todas las asignaturas (excluir carpetas que no son asignaturas)
    exclude_folders = {'__pycache__', '.git', '.vscode', 'node_modules'}
    subjects = [d for d in base_path.iterdir() 
               if d.is_dir() 
               and not d.name.startswith('.') 
               and d.name not in exclude_folders
               and not d.name.endswith('_backup')]
    
    print("Asignaturas encontradas:")
    for i, subject in enumerate(subjects, 1):
        print(f"  {i}. {subject.name}")
    
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
                print(f"\n🔄 Procesando solo: {subjects[index].name}")
            else:
                print("❌ Índice inválido.")
                return
        except ValueError:
            print("❌ Entrada inválida.")
            return
    
    for subject in subjects_to_process:
        print(f"\n{'='*50}")
        print(f"PROCESANDO: {subject.name}")
        print(f"{'='*50}")
        
        # Reorganizar carpetas
        reorganizer.reorganize_subject_folders(subject)
        
        # Arreglar rutas HTML
        reorganizer.fix_html_paths_after_reorganization(subject)
        
        print(f"✅ Completado: {subject.name}")
    
    print(f"\n🎉 Proceso completado para {len(subjects_to_process)} asignatura(s).")

if __name__ == "__main__":
    main()
