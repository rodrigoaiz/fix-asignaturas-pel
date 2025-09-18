#!/usr/bin/env python3
"""
Script para realizar cambios masivos en archivos HTML de las asignaturas
Realiza las siguientes modificaciones:
1. Quita las ligas del breadcrumb course__header--breadcrumb
2. Arregla la navegación course__content__nav para continuar correctamente  
3. Reemplaza nav__menu con un menú que navegue por unidades
4. Convierte actividades de ligas a iframes con ?theme=photo

Versión que usa solo librerías estándar de Python
"""

import os
import re
import json
import sys
from pathlib import Path

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
        
        # Extraer unit_themes usando regex más robusto
        unit_themes_match = re.search(r'export const unit_themes\s*=\s*(\[[\s\S]*?\n\];)', js_content)
        if unit_themes_match:
            try:
                # Extraer cada unidad manualmente
                themes_text = unit_themes_match.group(1)
                unit_themes = self.parse_unit_themes(themes_text)
            except Exception as e:
                print(f"Error parseando unit_themes: {e}")
                
        # Extraer moodleActivities usando regex
        activities_match = re.search(r'export const moodleActivities\s*=\s*(\[[\s\S]*?\n\];)', js_content)
        if activities_match:
            try:
                activities_text = activities_match.group(1)
                moodle_activities = self.parse_moodle_activities(activities_text)
            except Exception as e:
                print(f"Error parseando moodleActivities: {e}")
                
        # Extraer moodleURL
        url_match = re.search(r'moodleURL:\s*["\']([^"\']*)["\']', js_content)
        if url_match:
            moodle_url = url_match.group(1)
            
        return unit_themes, moodle_activities, moodle_url
    
    def parse_unit_themes(self, themes_text):
        """Parsea manualmente la estructura de unit_themes"""
        units = []
        
        # Buscar cada unidad
        unit_pattern = r'\{\s*unit:\s*["\']([^"\']*)["\'],\s*themes:\s*\[([\s\S]*?)\]\s*\}'
        unit_matches = re.findall(unit_pattern, themes_text)
        
        for unit_name, themes_block in unit_matches:
            themes = []
            
            # Buscar cada tema dentro de la unidad
            theme_pattern = r'\{\s*themeName:\s*["\']([^"\']*)["\'],\s*themeURL:\s*["\']([^"\']*)["\'],\s*pages:\s*["\']([^"\']*)["\']'
            theme_matches = re.findall(theme_pattern, themes_block)
            
            for theme_name, theme_url, pages in theme_matches:
                themes.append({
                    'themeName': theme_name,
                    'themeURL': theme_url,
                    'pages': pages
                })
            
            units.append({
                'unit': unit_name,
                'themes': themes
            })
        
        return units
    
    def parse_moodle_activities(self, activities_text):
        """Parsea manualmente la estructura de moodleActivities"""
        activities = []
        
        # Buscar cada actividad
        activity_pattern = r'\{\s*idHTML:\s*["\']([^"\']*)["\'],\s*url:\s*["\']([^"\']*)["\'],\s*id:\s*["\']([^"\']*)["\']'
        activity_matches = re.findall(activity_pattern, activities_text)
        
        for id_html, url, activity_id in activity_matches:
            activities.append({
                'idHTML': id_html,
                'url': url,
                'id': activity_id
            })
        
        return activities
    
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
    
    def remove_breadcrumb_links(self, html_content):
        """Quita las ligas del breadcrumb manteniendo solo el texto"""
        # Buscar el breadcrumb
        breadcrumb_pattern = r'(<p class="course__header--breadcrumb">)(.*?)(</p>)'
        breadcrumb_match = re.search(breadcrumb_pattern, html_content, re.DOTALL)
        
        if breadcrumb_match:
            opening_tag, content, closing_tag = breadcrumb_match.groups()
            
            # Remover todos los enlaces pero mantener el texto
            content_without_links = re.sub(r'<a[^>]*>([^<]*)</a>', r'\1', content)
            
            new_breadcrumb = opening_tag + content_without_links + closing_tag
            html_content = html_content.replace(breadcrumb_match.group(0), new_breadcrumb)
        
        return html_content
    
    def generate_units_menu(self, subject, current_unit, current_theme, unit_themes):
        """Genera el nuevo menú de navegación por unidades simplificado (solo botones U1, U2, etc.)"""
        menu_items = []
        
        for unit in unit_themes:
            unit_name = unit['unit']
            active_class = 'nav__menu--item--active' if unit_name == current_unit else ''
            
            # Solo crear botón simple para cada unidad sin lista desplegable de temas
            unit_item = f'''                <li class="nav__menu--item {active_class}">
                    <a class="nav__menu__item--link" href="/{subject}/{unit_name}/t1/1.html">
                        <span>{unit_name.upper()}</span>
                    </a>
                </li>'''
            menu_items.append(unit_item)
        
        return f'''            <ul class="nav__menu--units">
{chr(10).join(menu_items)}
            </ul>'''
    
    def replace_nav_menu(self, html_content, subject, current_unit, current_theme, unit_themes):
        """Reemplaza el nav__menu existente con el nuevo menú de unidades"""
        if not unit_themes:
            return html_content
            
        # Buscar el div nav__menu y reemplazar su contenido
        nav_menu_pattern = r'(<div class="nav__menu">)(.*?)(</div>)'
        nav_menu_match = re.search(nav_menu_pattern, html_content, re.DOTALL)
        
        if nav_menu_match:
            opening_tag, old_content, closing_tag = nav_menu_match.groups()
            new_menu_html = self.generate_units_menu(subject, current_unit, current_theme, unit_themes)
            new_nav_menu = opening_tag + new_menu_html + closing_tag
            html_content = html_content.replace(nav_menu_match.group(0), new_nav_menu)
        
        return html_content
    
    def get_subject_from_path(self, current_path):
        """Extrae el nombre del subject desde la ruta del archivo"""
        path_parts = current_path.parts
        # Buscar cualquier carpeta que contenga subcarpetas con patrón u1, u2, etc.
        for i, part in enumerate(path_parts):
            # Si encontramos una carpeta que parece ser una unidad (u1, u2, etc.)
            if part.startswith('u') and len(part) >= 2 and part[1:].isdigit():
                # El subject sería la carpeta anterior a esta
                if i > 0:
                    return path_parts[i-1]
        return None
    
    def calculate_next_navigation(self, current_path, unit_themes):
        """Calcula la navegación siguiente basada en la estructura de temas"""
        path_parts = current_path.parts
        
        # Extraer información del path actual
        file_name = path_parts[-1]
        current_theme = path_parts[-2]
        current_unit = path_parts[-3]
        subject = self.get_subject_from_path(current_path)
        
        if not subject:
            return None
        
        try:
            current_page = int(file_name.replace('.html', ''))
        except ValueError:
            return None
        
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
        current_theme_index = -1
        for i, theme in enumerate(current_unit_data['themes']):
            if theme['themeURL'] == current_theme:
                current_theme_data = theme
                current_theme_index = i
                break
                
        if not current_theme_data:
            return None
            
        try:
            max_pages = int(current_theme_data['pages'])
        except ValueError:
            return None
        
        # Si no es la última página del tema, ir a la siguiente página (ruta absoluta)
        if current_page < max_pages:
            return f"{current_unit}/{current_theme}/{current_page + 1}.html"
            
        # Si es la última página del tema, ir al siguiente tema (ruta absoluta)
        if current_theme_index < len(current_unit_data['themes']) - 1:
            next_theme = current_unit_data['themes'][current_theme_index + 1]
            return f"{current_unit}/{next_theme['themeURL']}/1.html"
            
        # Si es el último tema de la unidad, ir a la siguiente unidad (ruta absoluta)
        current_unit_index = -1
        for i, unit in enumerate(unit_themes):
            if unit['unit'] == current_unit:
                current_unit_index = i
                break
                
        if current_unit_index >= 0 and current_unit_index < len(unit_themes) - 1:
            next_unit = unit_themes[current_unit_index + 1]
            return f"/{subject}/{next_unit['unit']}/{next_unit['themes'][0]['themeURL']}/1.html"
            
        # Si es la última página de la última unidad, no hay siguiente
        return None

    def calculate_previous_navigation(self, current_path, unit_themes):
        """Calcula la navegación anterior basada en la estructura de temas"""
        path_parts = current_path.parts
        
        # Extraer información del path actual
        file_name = path_parts[-1]
        current_theme = path_parts[-2]
        current_unit = path_parts[-3]
        subject = self.get_subject_from_path(current_path)
        
        if not subject:
            return None
        
        try:
            current_page = int(file_name.replace('.html', ''))
        except ValueError:
            return None
        
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
        current_theme_index = -1
        for i, theme in enumerate(current_unit_data['themes']):
            if theme['themeURL'] == current_theme:
                current_theme_data = theme
                current_theme_index = i
                break
                
        if not current_theme_data:
            return None
        
        # Si no es la primera página del tema, ir a la página anterior (ruta absoluta)
        if current_page > 1:
            return f"{current_unit}/{current_theme}/{current_page - 1}.html"
            
        # Si es la primera página del tema, ir al tema anterior (ruta absoluta)
        if current_theme_index > 0:
            prev_theme = current_unit_data['themes'][current_theme_index - 1]
            try:
                prev_theme_max_pages = int(prev_theme['pages'])
                return f"{current_unit}/{prev_theme['themeURL']}/{prev_theme_max_pages}.html"
            except ValueError:
                return f"{current_unit}/{prev_theme['themeURL']}/1.html"
            
        # Si es el primer tema de la unidad, ir a la unidad anterior (ruta absoluta)
        current_unit_index = -1
        for i, unit in enumerate(unit_themes):
            if unit['unit'] == current_unit:
                current_unit_index = i
                break
                
        if current_unit_index > 0:
            prev_unit = unit_themes[current_unit_index - 1]
            last_theme = prev_unit['themes'][-1]
            try:
                last_theme_max_pages = int(last_theme['pages'])
                return f"/{subject}/{prev_unit['unit']}/{last_theme['themeURL']}/{last_theme_max_pages}.html"
            except ValueError:
                return f"/{subject}/{prev_unit['unit']}/{last_theme['themeURL']}/1.html"
            
        # Si es la primera página de la primera unidad, no hay anterior
        return None
    
    def fix_content_navigation(self, html_content, current_path, unit_themes):
        """Arregla la navegación de las flechas"""
        if not unit_themes:
            return html_content
            
        # Calcular navegación siguiente y anterior
        next_path = self.calculate_next_navigation(current_path, unit_themes)
        prev_path = self.calculate_previous_navigation(current_path, unit_themes)
        
        # Actualizar flecha derecha (siguiente)
        if next_path:
            right_arrow_pattern = r'(<a class="course__content__nav--right"[^>]*data-link=")[^"]*(")'
            replacement = f'\\g<1>{next_path}\\g<2>'
            html_content = re.sub(right_arrow_pattern, replacement, html_content)
            
            # También actualizar href si existe
            href_pattern = r'(<a class="course__content__nav--right"[^>]*href=")[^"]*(")'
            href_replacement = f'\\g<1>{next_path}\\g<2>'
            html_content = re.sub(href_pattern, href_replacement, html_content)
        
        # Actualizar flecha izquierda (anterior)
        if prev_path:
            left_arrow_pattern = r'(<a class="course__content__nav--left"[^>]*data-link=")[^"]*(")'
            left_replacement = f'\\g<1>{prev_path}\\g<2>'
            html_content = re.sub(left_arrow_pattern, left_replacement, html_content)
            
            # También actualizar href si existe
            left_href_pattern = r'(<a class="course__content__nav--left"[^>]*href=")[^"]*(")'
            left_href_replacement = f'\\g<1>{prev_path}\\g<2>'
            html_content = re.sub(left_href_pattern, left_href_replacement, html_content)
            
            # Remover clase hidden si existe
            html_content = re.sub(r'class="course__content__nav--left hidden"', 'class="course__content__nav--left"', html_content)
        else:
            # Si no hay navegación anterior, agregar clase hidden
            html_content = re.sub(r'class="course__content__nav--left"', 'class="course__content__nav--left hidden"', html_content)
        
        return html_content
    
    def convert_activities_to_iframes(self, html_content, moodle_activities, moodle_url):
        """Convierte actividades de enlaces a iframes"""
        if not moodle_activities or not moodle_url:
            return html_content
            
        for activity in moodle_activities:
            id_html = activity['idHTML']
            
            # Buscar el enlace con este ID
            link_pattern = rf'<a[^>]*id="{id_html}"[^>]*>.*?</a>'
            link_match = re.search(link_pattern, html_content, re.DOTALL)
            
            if link_match:
                # Crear iframe con URL correcta
                full_url = f"{moodle_url}{activity['url']}{activity['id']}&theme=photo"
                iframe = f'''<iframe src="{full_url}" width="100%" height="600" style="border: none;" title="{id_html}"></iframe>'''
                
                # Reemplazar el enlace con el iframe
                html_content = html_content.replace(link_match.group(0), iframe)
        
        return html_content
    
    def process_html_file(self, file_path, subject):
        """Procesa un archivo HTML individual"""
        print(f"Procesando: {file_path}")
        
        try:
            # Leer el archivo HTML
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
                
            # Extraer información del path
            path_parts = file_path.parts
            unit_indices = [i for i, part in enumerate(path_parts) if part.startswith('u') and re.match(r'^u\d+$', part)]
            
            if not unit_indices:
                print(f"No se pudo determinar la unidad para {file_path}")
                return
                
            unit_index = unit_indices[0]
            current_unit = path_parts[unit_index]
            current_theme = path_parts[unit_index + 1] if unit_index + 1 < len(path_parts) else 't1'
            subject_path = Path(*path_parts[:unit_index])
            
            # Obtener el nombre del subject desde el path
            subject = self.get_subject_from_path(file_path)
            
            # Cargar configuración para esta unidad
            unit_themes, moodle_activities, moodle_url = self.load_activity_config(subject_path, current_unit)
            
            # Aplicar modificaciones
            html_content = self.remove_breadcrumb_links(html_content)
            
            if unit_themes:
                html_content = self.replace_nav_menu(html_content, subject, current_unit, current_theme, unit_themes)
                html_content = self.fix_content_navigation(html_content, file_path, unit_themes)
                
            if moodle_activities and moodle_url:
                html_content = self.convert_activities_to_iframes(html_content, moodle_activities, moodle_url)
            
            # Guardar el archivo modificado
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
                
            print(f"✓ Procesado: {file_path}")
            
        except Exception as e:
            print(f"Error procesando {file_path}: {e}")
            import traceback
            traceback.print_exc()
    
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
