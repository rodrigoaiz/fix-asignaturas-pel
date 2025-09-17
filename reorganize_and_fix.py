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
        """Reorganiza las carpetas de una asignatura"""
        subject_path = Path(subject_path)
        
        print(f"Reorganizando {subject_path.name}...")
        
        # Buscar todas las carpetas de unidades (u1, u2, u3, etc.)
        unit_folders = [f for f in subject_path.iterdir() if f.is_dir() and f.name.startswith('u') and f.name[1:].isdigit()]
        
        for unit_folder in sorted(unit_folders):
            print(f"  Procesando {unit_folder.name}...")
            
            # Verificar si existe la estructura duplicada (u1/u1/, u2/u2/, etc.)
            inner_unit_folder = unit_folder / unit_folder.name
            
            if inner_unit_folder.exists() and inner_unit_folder.is_dir():
                print(f"    Encontrada estructura duplicada: {inner_unit_folder}")
                
                # Mover todo el contenido de la carpeta interna hacia arriba
                for item in inner_unit_folder.iterdir():
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
                
                # Eliminar la carpeta interna vacía
                if not any(inner_unit_folder.iterdir()):
                    inner_unit_folder.rmdir()
                    print(f"    Eliminada carpeta vacía: {inner_unit_folder}")
    
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
    
    # Buscar todas las asignaturas
    subjects = [d for d in base_path.iterdir() if d.is_dir() and not d.name.startswith('.')]
    
    for subject in subjects:
        if subject.name in ['mate3', 'derecho-1']:  # Solo procesar estas por ahora
            print(f"\n{'='*50}")
            print(f"PROCESANDO: {subject.name}")
            print(f"{'='*50}")
            
            # Hacer backup de la estructura original
            backup_path = base_path / f"{subject.name}_backup"
            if not backup_path.exists():
                print(f"Creando backup en {backup_path}")
                shutil.copytree(subject, backup_path)
            
            # Reorganizar carpetas
            reorganizer.reorganize_subject_folders(subject)
            
            # Arreglar rutas HTML
            reorganizer.fix_html_paths_after_reorganization(subject)
            
            print(f"✅ Completado: {subject.name}")

if __name__ == "__main__":
    main()
