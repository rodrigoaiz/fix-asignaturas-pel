#!/usr/bin/env python3
"""
Script para realizar cambios masivos en archivos HTML de las asignaturas
Realiza las siguientes modificaciones:
1. Quita las ligas del breadcrumb course__header--breadcrumb
2. Arregla la navegación course__content__nav para continuar correctamente  
3. Reemplaza nav__menu con un menú que navegue por unidades
4. Convierte actividades de ligas a iframes con ?theme=photo
"""

import os
import re
import json
import sys
from pathlib import Path
import html.parser
from html.parser import HTMLParser

class HTMLModifier:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.subjects = []
        self.unit_themes = {}
        self.moodle_activities = {}
        
    def find_subjects(self):
        """Encuentra todas las asignaturas en el directorio base"""
        self.subjects = [d.name for d in self.base_dir.iterdir() 
                        if d.is_dir() and not d.name.startswith('.')]
        print(f"Encontradas asignaturas: {', '.join(self.subjects)}")
        return self.subjects
    
    def parse_js_config(self, js_content):
        """Extrae configuración de archivos JavaScript de activities_moodle.js"""
        unit_themes = None
        moodle_activities = None
        moodle_url = None
        
        # Extraer unit_themes
        unit_themes_match = re.search(r'export const unit_themes\s*=\s*(\[[\s\S]*?\]);', js_content)
        if unit_themes_match:
            try:
                # Convertir JavaScript array a Python
                js_array = unit_themes_match.group(1)
                # Reemplazar comillas simples por dobles y arreglar formato
                js_array = re.sub(r"'([^']*)'", r'"\1"', js_array)
                js_array = re.sub(r'(\w+):', r'"\1":', js_array)
                unit_themes = json.loads(js_array)
            except Exception as e:
                print(f"Error parseando unit_themes: {e}")
                
        # Extraer moodleActivities
        activities_match = re.search(r'export const moodleActivities\s*=\s*(\[[\s\S]*?\]);', js_content)
        if activities_match:
            try:
                js_array = activities_match.group(1)
                js_array = re.sub(r"'([^']*)'", r'"\1"', js_array)
                js_array = re.sub(r'(\w+):', r'"\1":', js_array)
                moodle_activities = json.loads(js_array)
            except Exception as e:
                print(f"Error parseando moodleActivities: {e}")
                
        # Extraer moodleURL
        url_match = re.search(r'moodleURL:\s*["\']([^"\']*)["\']', js_content)
        if url_match:
            moodle_url = url_match.group(1)
            
        return unit_themes, moodle_activities, moodle_url
    
    def load_activity_config(self, subject_path, unit):
        """Carga la configuración de activities_moodle.js para una unidad específica"""
        config_path = subject_path / unit / 'assets' / 'scripts' / 'activities_moodle.js'
        
        if not config_path.exists():
            print(f"No se encontró {config_path}")
            return None, None, None
            
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            unit_themes, moodle_activities, moodle_url = self.parse_js_config(content)
            
            key = f"{subject_path.name}-{unit}"
            if unit_themes:
                self.unit_themes[key] = unit_themes
            if moodle_activities:
                self.moodle_activities[key] = moodle_activities
                
            return unit_themes, moodle_activities, moodle_url
            
        except Exception as e:
            print(f"Error cargando configuración de {config_path}: {e}")
            return None, None, None
    
    def find_html_files(self, subject_path):
        """Encuentra todos los archivos HTML en una asignatura"""
        html_files = []
        for html_file in subject_path.rglob('*.html'):
            html_files.append(html_file)
        return html_files
    
    def remove_breadcrumb_links(self, soup):
        """Quita las ligas del breadcrumb manteniendo solo el texto"""
        breadcrumb = soup.find(class_='course__header--breadcrumb')
        if breadcrumb:
            links = breadcrumb.find_all('a')
            for link in links:
                link.replace_with(link.get_text())
    
    def generate_units_menu(self, subject, current_unit, unit_themes):
        """Genera el nuevo menú de navegación por unidades"""
        menu_items = []
        
        for unit in unit_themes:
            unit_name = unit['unit']
            active_class = 'nav__menu--item--active' if unit_name == current_unit else ''
            
            themes_list = []
            for theme in unit['themes']:
                theme_item = f'''
                    <li class="nav__menu--theme">
                        <a href="../{unit_name}/{unit_name}/{theme['themeURL']}/1.html">
                            {theme['themeName']}
                        </a>
                    </li>'''
                themes_list.append(theme_item)
            
            unit_item = f'''
                <li class="nav__menu--item {active_class}">
                    <a class="nav__menu__item--link" href="../{unit_name}/{unit_name}/t1/1.html">
                        <span>{unit_name.upper()}</span>
                    </a>
                    <ul class="nav__menu--themes">
                        {"".join(themes_list)}
                    </ul>
                </li>'''
            menu_items.append(unit_item)
        
        return f'<ul class="nav__menu--units">{"".join(menu_items)}</ul>'
    
    def replace_nav_menu(self, soup, subject, current_unit, unit_themes):
        """Reemplaza el nav__menu existente con el nuevo menú de unidades"""
        nav_menu = soup.find(class_='nav__menu')
        if nav_menu and unit_themes:
            new_menu_html = self.generate_units_menu(subject, current_unit, unit_themes)
            nav_menu.clear()
            nav_menu.append(BeautifulSoup(new_menu_html, 'html.parser'))
    
    def calculate_next_navigation(self, current_path, unit_themes):
        """Calcula la navegación siguiente basada en la estructura de temas"""
        path_parts = current_path.parts
        
        # Extraer información del path actual
        file_name = path_parts[-1]
        current_theme = path_parts[-2]
        current_unit = path_parts[-3]
        current_page = int(file_name.replace('.html', ''))
        
        # Encontrar la unidad actual en unit_themes
        current_unit_data = None
        for unit in unit_themes:
            if unit['unit'] == current_unit:
                current_unit_data = unit
                break
                
        if not current_unit_data:
            return None
            
        # Encontrar el tema actual
        current_theme_data = None
        for theme in current_unit_data['themes']:
            if theme['themeURL'] == current_theme:
                current_theme_data = theme
                break
                
        if not current_theme_data:
            return None
            
        max_pages = int(current_theme_data['pages'])
        
        # Si no es la última página del tema, ir a la siguiente página
        if current_page < max_pages:
            return f"{current_page + 1}.html"
            
        # Si es la última página del tema, ir al siguiente tema
        current_theme_index = current_unit_data['themes'].index(current_theme_data)
        if current_theme_index < len(current_unit_data['themes']) - 1:
            next_theme = current_unit_data['themes'][current_theme_index + 1]
            return f"../{next_theme['themeURL']}/1.html"
            
        # Si es el último tema de la unidad, ir a la siguiente unidad
        current_unit_index = unit_themes.index(current_unit_data)
        if current_unit_index < len(unit_themes) - 1:
            next_unit = unit_themes[current_unit_index + 1]
            return f"../../{next_unit['unit']}/{next_unit['unit']}/{next_unit['themes'][0]['themeURL']}/1.html"
            
        # Si es la última página de la última unidad, no hay siguiente
        return None
    
    def fix_content_navigation(self, soup, current_path, unit_themes):
        """Arregla la navegación de las flechas"""
        right_arrow = soup.find(class_='course__content__nav--right')
        if right_arrow and unit_themes:
            next_path = self.calculate_next_navigation(current_path, unit_themes)
            if next_path:
                right_arrow['data-link'] = next_path
                if right_arrow.get('href'):
                    right_arrow['href'] = next_path
    
    def convert_activities_to_iframes(self, soup, moodle_activities, moodle_url):
        """Convierte actividades de enlaces a iframes"""
        if not moodle_activities or not moodle_url:
            return
            
        for activity in moodle_activities:
            element = soup.find(id=activity['idHTML'])
            if element and element.name == 'a':
                # Crear iframe
                iframe = soup.new_tag('iframe')
                full_url = f"{moodle_url}{activity['url']}{activity['id']}?theme=photo"
                
                iframe['src'] = full_url
                iframe['width'] = '100%'
                iframe['height'] = '600'
                iframe['style'] = 'border: none;'
                iframe['title'] = activity['idHTML']
                
                # Reemplazar el enlace con el iframe
                element.replace_with(iframe)
    
    def process_html_file(self, file_path, subject):
        """Procesa un archivo HTML individual"""
        print(f"Procesando: {file_path}")
        
        try:
            # Leer el archivo HTML
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
                
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extraer información del path
            path_parts = file_path.parts
            unit_indices = [i for i, part in enumerate(path_parts) if part.startswith('u') and re.match(r'^u\d+$', part)]
            
            if not unit_indices:
                print(f"No se pudo determinar la unidad para {file_path}")
                return
                
            unit_index = unit_indices[0]
            current_unit = path_parts[unit_index]
            subject_path = Path(*path_parts[:unit_index])
            
            # Cargar configuración para esta unidad
            unit_themes, moodle_activities, moodle_url = self.load_activity_config(subject_path, current_unit)
            
            # Aplicar modificaciones
            self.remove_breadcrumb_links(soup)
            
            if unit_themes:
                self.replace_nav_menu(soup, subject, current_unit, unit_themes)
                self.fix_content_navigation(soup, file_path, unit_themes)
                
            if moodle_activities and moodle_url:
                self.convert_activities_to_iframes(soup, moodle_activities, moodle_url)
            
            # Guardar el archivo modificado
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
                
            print(f"✓ Procesado: {file_path}")
            
        except Exception as e:
            print(f"Error procesando {file_path}: {e}")
    
    def process_subject(self, subject):
        """Procesa todos los archivos de una asignatura"""
        print(f"\n=== Procesando asignatura: {subject} ===")
        
        subject_path = self.base_dir / subject
        html_files = self.find_html_files(subject_path)
        
        print(f"Encontrados {len(html_files)} archivos HTML")
        
        for file_path in html_files:
            self.process_html_file(file_path, subject)
    
    def run(self):
        """Ejecuta el procesamiento completo"""
        print("=== Iniciando procesamiento masivo de HTML ===\n")
        
        self.find_subjects()
        
        for subject in self.subjects:
            self.process_subject(subject)
            
        print("\n=== Procesamiento completado ===")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Modifica masivamente archivos HTML de cursos')
    parser.add_argument('directory', nargs='?', default='.', 
                       help='Directorio base donde están las asignaturas (default: directorio actual)')
    parser.add_argument('--subject', '-s', help='Procesar solo una asignatura específica')
    parser.add_argument('--dry-run', '-n', action='store_true', 
                       help='Solo mostrar qué archivos se procesarían sin modificarlos')
    
    args = parser.parse_args()
    
    base_dir = Path(args.directory).resolve()
    print(f"Directorio base: {base_dir}")
    
    if not base_dir.exists():
        print(f"Error: El directorio {base_dir} no existe")
        sys.exit(1)
    
    modifier = HTMLModifier(base_dir)
    
    if args.subject:
        modifier.subjects = [args.subject]
        modifier.process_subject(args.subject)
    else:
        modifier.run()

if __name__ == "__main__":
    main()
