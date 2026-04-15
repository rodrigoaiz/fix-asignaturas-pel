#!/usr/bin/env python3
"""
Script para realizar cambios masivos en archivos HTML de las asignaturas
Realiza las siguientes modificaciones:
1. Detecta y reorganiza automáticamente asignaturas con estructura Moodle (u1/u1/t1/)
2. Quita las ligas del breadcrumb course__header--breadcrumb
3. Arregla la navegación course__content__nav para continuar correctamente
4. Reemplaza nav__menu con un menú que navegue por unidades
5. Convierte actividades de ligas a iframes con ?theme=photo
6. Limpia URLs estáticas de Moodle en flechas de navegación (bug fix)

Versión optimizada: regex compilados, caché de config, una sola pasada I/O
Output independiente: los archivos originales NO se modifican, se copia todo a out/

NOTA: Este script incluye la funcionalidad de reorganize_and_fix.py (ahora DEPRECADO)
"""

import os
import re
import json
import sys
import shutil
from pathlib import Path


class FolderReorganizer:
    """Reorganiza carpetas de estructura Moodle u1/u1/t1/ a u1/t1/"""
    # Compiled regex for path fixing
    RE_CSS_DOUBLE_DOT = re.compile(r'href="../../assets/')
    RE_SRC_DOUBLE_DOT = re.compile(r'src="../../assets/')
    RE_NAV_DOUBLE_UNIT = re.compile(r'href="../(u\d+)/\1/')

    def __init__(self):
        pass

    def needs_reorganization(self, subject_path):
        """Detecta si una asignatura necesita reorganización"""
        subject_path = Path(subject_path)
        
        # Buscar carpetas de unidades (u1, u2, u3, etc.)
        unit_folders = [
            f for f in subject_path.iterdir()
            if f.is_dir() and f.name.startswith('u') and f.name[1:].isdigit()
        ]
        
        if not unit_folders:
            return False
        
        # Verificar si alguna unidad tiene estructura duplicada
        for unit_folder in unit_folders:
            # Caso 1: Estructura u1/u1/t1/ (mate3, derecho-1)
            inner_unit_folder = unit_folder / unit_folder.name
            # Caso 2: Estructura u1/build/u1/t1/ (antropologia-1)
            build_unit_folder = unit_folder / "build" / unit_folder.name
            
            if inner_unit_folder.exists() and inner_unit_folder.is_dir():
                return True
            if build_unit_folder.exists() and build_unit_folder.is_dir():
                return True
        
        return False

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

                original_content = content
                
                # Apply all path fixes in one pass
                content = self.RE_CSS_DOUBLE_DOT.sub('href="../assets/', content)
                content = self.RE_SRC_DOUBLE_DOT.sub('src="../assets/', content)
                content = self.RE_NAV_DOUBLE_UNIT.sub(r'href="../\1/', content)

                if content != original_content:
                    with open(html_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    updated_count += 1

            except Exception as e:
                print(f"    ✗ Error en {html_file}: {e}")

        print(f"    ✓ {updated_count} archivos actualizados de {len(html_files)}")


class HTMLModifier:
    # ── Compiled regex patterns (efficiency) ──
    RE_BREADCRUMB = re.compile(
        r'(<p class="course__header--breadcrumb">)(.*?)(</p>)', re.DOTALL
    )
    RE_BREADCRUMB_LINK = re.compile(r'<a[^>]*>([^<]*)</a>')
    RE_NAV_MENU = re.compile(
        r'(<div class="nav__menu">)(.*?)(</div>)', re.DOTALL
    )
    RE_UNIT_PATTERN = re.compile(r'^u\d+$')

    # Navigation patterns (flexible class matching to handle "hidden" suffix)
    RE_RIGHT_DATA_LINK = re.compile(
        r'(<a\s+[^>]*class="[^"]*course__content__nav--right[^"]*"[^>]*data-link=")[^"]*(")'
    )
    RE_RIGHT_HREF = re.compile(
        r'(<a\s+[^>]*class="[^"]*course__content__nav--right[^"]*"[^>]*href=")[^"]*(")'
    )
    RE_LEFT_DATA_LINK = re.compile(
        r'(<a\s+[^>]*class="[^"]*course__content__nav--left[^"]*"[^>]*data-link=")[^"]*(")'
    )
    RE_LEFT_HREF = re.compile(
        r'(<a\s+[^>]*class="[^"]*course__content__nav--left[^"]*"[^>]*href=")[^"]*(")'
    )

    # Moodle static URL detection
    RE_MOODLE_URL = re.compile(r'https?://[\w.]+/papiit/cch/')

    # JS config extraction
    RE_UNIT_THEMES = re.compile(
        r'export const unit_themes\s*=\s*(\[[\s\S]*?\n\];)'
    )
    RE_MOODLE_ACTIVITIES = re.compile(
        r'export const moodleActivities\s*=\s*(\[[\s\S]*?\n\];)'
    )
    RE_MOODLE_URL = re.compile(r'moodleURL:\s*["\']([^"\']*)["\']')
    RE_UNIT_IN_JS = re.compile(
        r'\{\s*unit:\s*["\']([^"\']*)["\'],\s*themes:\s*\[([\s\S]*?)\]\s*\}'
    )
    RE_THEME_IN_JS = re.compile(
        r'\{\s*themeName:\s*["\']([^"\']*)["\'],\s*themeURL:\s*["\']([^"\']*)["\'],\s*pages:\s*["\']([^"\']*)["\']'
    )
    RE_ACTIVITY_IN_JS = re.compile(
        r'\{\s*idHTML:\s*["\']([^"\']*)["\'],\s*url:\s*["\']([^"\']*)["\'],\s*id:\s*["\']([^"\']*)["\']'
    )

    # CSS/JS path fix patterns
    RE_CSS_DOUBLE_DOT = re.compile(r'href="../../assets/')
    RE_SRC_DOUBLE_DOT = re.compile(r'src="../../assets/')
    RE_NAV_DOUBLE_UNIT = re.compile(r'href="../(u\d+)/\1/')

    def __init__(self, base_dir, output_dir, dry_run=False):
        self.base_dir = Path(base_dir)
        self.output_dir = Path(output_dir)
        self.subjects = []
        self.unit_themes = {}        # cache: "subject-unit" -> themes list
        self.moodle_activities = {}  # cache: "subject-unit" -> activities list
        self.moodle_urls = {}        # cache: "subject-unit" -> moodle URL
        self.dry_run = dry_run
        self.reorganizer = FolderReorganizer()  # Reorganizador integrado

    # ─────────────────────────────────────────────
    #  Copy & Setup
    # ─────────────────────────────────────────────
    def prepare_output(self, subject_name):
        """Copia la asignatura base al directorio de output y reorganiza si es necesario"""
        source = self.base_dir / subject_name
        
        # Extraer solo el nombre de la asignatura (sin la carpeta padre)
        # Ej: "asignaturas-muestra/mate3" -> "mate3"
        subject_base_name = Path(subject_name).name
        dest = self.output_dir / subject_base_name

        if dest.exists():
            print(f"  ♻  {subject_base_name} ya existe en output, recreando...")
            shutil.rmtree(dest)

        shutil.copytree(source, dest)
        print(f"  📋 {subject_name} copiada a {dest}")
        
        # Detectar y reorganizar automáticamente si tiene estructura Moodle
        if self.reorganizer.needs_reorganization(dest):
            print(f"  🔍 Detectada estructura Moodle, reorganizando...")
            self.reorganizer.reorganize_subject_folders(dest)
            self.reorganizer.fix_html_paths_after_reorganization(dest)
        else:
            print(f"  ✓ Estructura correcta, no necesita reorganización")
        
        return dest

    def find_subjects(self):
        """Encuentra todas las asignaturas en las carpetas de muestra y producción"""
        # Carpetas donde buscar asignaturas
        subject_folders = [
            self.base_dir / 'asignaturas-muestra',
            self.base_dir / 'asignaturas-produccion'
        ]
        
        self.subjects = []
        
        for folder in subject_folders:
            if not folder.exists():
                continue
            
            # Buscar asignaturas dentro de esta carpeta
            for d in folder.iterdir():
                if not d.is_dir() or d.name.startswith('.'):
                    continue
                
                # Verificar si tiene al menos una carpeta de unidad (u1, u2, etc.)
                has_units = any(
                    sub.is_dir() and self.RE_UNIT_PATTERN.match(sub.name)
                    for sub in d.iterdir()
                )
                
                if has_units:
                    # Guardar la ruta relativa desde base_dir
                    relative_path = d.relative_to(self.base_dir)
                    self.subjects.append(str(relative_path))
        
        if self.subjects:
            print(f"Encontradas asignaturas: {', '.join(self.subjects)}")
        else:
            print("⚠️  No se encontraron asignaturas en asignaturas-muestra/ ni asignaturas-produccion/")
        
        return self.subjects

    def find_html_files(self, subject_path):
        """Encuentra todos los archivos HTML en una asignatura"""
        return list(subject_path.rglob('*.html'))

    # ─────────────────────────────────────────────
    #  JS Config parsing (with caching)
    # ─────────────────────────────────────────────
    def parse_js_config(self, js_content):
        """Extrae configuración de activities_moodle.js"""
        unit_themes = moodle_activities = moodle_url = None

        m = self.RE_UNIT_THEMES.search(js_content)
        if m:
            try:
                unit_themes = self._parse_unit_themes(m.group(1))
            except Exception as e:
                print(f"  ⚠ Error parseando unit_themes: {e}")

        m = self.RE_MOODLE_ACTIVITIES.search(js_content)
        if m:
            try:
                moodle_activities = self._parse_moodle_activities(m.group(1))
            except Exception as e:
                print(f"  ⚠ Error parseando moodleActivities: {e}")

        m = self.RE_MOODLE_URL.search(js_content)
        if m:
            moodle_url = m.group(1)

        return unit_themes, moodle_activities, moodle_url

    def _parse_unit_themes(self, themes_text):
        units = []
        for unit_name, themes_block in self.RE_UNIT_IN_JS.findall(themes_text):
            themes = [
                {'themeName': tn, 'themeURL': tu, 'pages': p}
                for tn, tu, p in self.RE_THEME_IN_JS.findall(themes_block)
            ]
            units.append({'unit': unit_name, 'themes': themes})
        return units

    def _parse_moodle_activities(self, activities_text):
        return [
            {'idHTML': ih, 'url': u, 'id': ai}
            for ih, u, ai in self.RE_ACTIVITY_IN_JS.findall(activities_text)
        ]

    def load_activity_config(self, subject_path, unit):
        """Carga config de activities_moodle.js con caché por unidad"""
        key = f"{subject_path.name}-{unit}"

        # Return from cache if already loaded
        if key in self.unit_themes or key in self.moodle_activities:
            return (
                self.unit_themes.get(key),
                self.moodle_activities.get(key),
                self.moodle_urls.get(key),
            )

        config_path = subject_path / unit / 'assets' / 'scripts' / 'activities_moodle.js'
        if not config_path.exists():
            return None, None, None

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                content = f.read()

            unit_themes, moodle_activities, moodle_url = self.parse_js_config(content)

            if unit_themes:
                self.unit_themes[key] = unit_themes
            if moodle_activities:
                self.moodle_activities[key] = moodle_activities
            if moodle_url:
                self.moodle_urls[key] = moodle_url

            return unit_themes, moodle_activities, moodle_url
        except Exception as e:
            print(f"  ⚠ Error cargando config de {config_path}: {e}")
            return None, None, None

    # ─────────────────────────────────────────────
    #  Path helpers
    # ─────────────────────────────────────────────
    @staticmethod
    def get_subject_from_path(current_path):
        path_parts = current_path.parts
        for i, part in enumerate(path_parts):
            if part.startswith('u') and len(part) >= 2 and part[1:].isdigit():
                if i > 0:
                    return path_parts[i - 1]
        return None

    @staticmethod
    def _extract_path_info(current_path):
        """Extrae unit, theme, page_number desde la ruta del archivo HTML"""
        path_parts = current_path.parts
        file_name = path_parts[-1]
        current_theme = path_parts[-2]
        current_unit = path_parts[-3]

        try:
            current_page = int(file_name.replace('.html', ''))
        except ValueError:
            return None

        return {
            'path_parts': path_parts,
            'file_name': file_name,
            'current_theme': current_theme,
            'current_unit': current_unit,
            'current_page': current_page,
        }

    # ─────────────────────────────────────────────
    #  Navigation calculation
    # ─────────────────────────────────────────────
    def calculate_next_navigation(self, current_path, unit_themes):
        info = self._extract_path_info(current_path)
        if not info:
            return None

        current_unit_data = None
        current_unit_index = -1
        for i, unit in enumerate(unit_themes):
            if unit['unit'] == info['current_unit']:
                current_unit_data = unit
                current_unit_index = i
                break
        if not current_unit_data:
            return None

        current_theme_data = None
        current_theme_index = -1
        for i, theme in enumerate(current_unit_data['themes']):
            if theme['themeURL'] == info['current_theme']:
                current_theme_data = theme
                current_theme_index = i
                break
        if not current_theme_data:
            return None

        try:
            max_pages = int(current_theme_data['pages'])
        except ValueError:
            return None

        # Next page within theme
        if info['current_page'] < max_pages:
            return f"{info['current_unit']}/{info['current_theme']}/{info['current_page'] + 1}.html"

        # Next theme within unit
        if current_theme_index < len(current_unit_data['themes']) - 1:
            next_theme = current_unit_data['themes'][current_theme_index + 1]
            return f"{info['current_unit']}/{next_theme['themeURL']}/1.html"

        # Next unit
        if current_unit_index < len(unit_themes) - 1:
            next_unit = unit_themes[current_unit_index + 1]
            return f"{next_unit['unit']}/{next_unit['themes'][0]['themeURL']}/1.html"

        # Last page of last unit — no next
        return None

    def calculate_previous_navigation(self, current_path, unit_themes):
        info = self._extract_path_info(current_path)
        if not info:
            return None

        current_unit_data = None
        current_unit_index = -1
        for i, unit in enumerate(unit_themes):
            if unit['unit'] == info['current_unit']:
                current_unit_data = unit
                current_unit_index = i
                break
        if not current_unit_data:
            return None

        current_theme_data = None
        current_theme_index = -1
        for i, theme in enumerate(current_unit_data['themes']):
            if theme['themeURL'] == info['current_theme']:
                current_theme_data = theme
                current_theme_index = i
                break
        if not current_theme_data:
            return None

        # Previous page within theme
        if info['current_page'] > 1:
            return f"{info['current_unit']}/{info['current_theme']}/{info['current_page'] - 1}.html"

        # Previous theme within unit
        if current_theme_index > 0:
            prev_theme = current_unit_data['themes'][current_theme_index - 1]
            try:
                prev_max = int(prev_theme['pages'])
                return f"{info['current_unit']}/{prev_theme['themeURL']}/{prev_max}.html"
            except ValueError:
                return f"{info['current_unit']}/{prev_theme['themeURL']}/1.html"

        # Previous unit
        if current_unit_index > 0:
            prev_unit = unit_themes[current_unit_index - 1]
            last_theme = prev_unit['themes'][-1]
            try:
                last_max = int(last_theme['pages'])
                return f"{prev_unit['unit']}/{last_theme['themeURL']}/{last_max}.html"
            except ValueError:
                return f"{prev_unit['unit']}/{last_theme['themeURL']}/1.html"

        # First page of first unit — no previous
        return None

    # ─────────────────────────────────────────────
    #  HTML transformations
    # ─────────────────────────────────────────────
    def remove_breadcrumb_links(self, html_content):
        """Quita las ligas del breadcrumb manteniendo solo el texto"""
        m = self.RE_BREADCRUMB.search(html_content)
        if m:
            opening, content, closing = m.groups()
            content_clean = self.RE_BREADCRUMB_LINK.sub(r'\1', content)
            html_content = html_content.replace(m.group(0), opening + content_clean + closing)
        return html_content

    def generate_units_menu(self, current_unit, unit_themes, current_path):
        """Genera menú de navegación por unidades (botones U1, U2, etc.)"""
        path_parts = current_path.parts
        current_unit_index = None
        for i, part in enumerate(path_parts):
            if part == current_unit:
                current_unit_index = i
                break

        items = []
        for unit in unit_themes:
            unit_name = unit['unit']
            active = 'nav__menu--item--active' if unit_name == current_unit else ''

            if current_unit_index is not None:
                levels_up = len(path_parts) - current_unit_index - 1
                rel_path = '../' * levels_up + f'{unit_name}/t1/1.html'
            else:
                rel_path = f'../../{unit_name}/t1/1.html'

            items.append(
                f'                <li class="nav__menu--item {active}">\n'
                f'                    <a class="nav__menu__item--link" href="{rel_path}">\n'
                f'                        <span>{unit_name.upper()}</span>\n'
                f'                    </a>\n'
                f'                </li>'
            )

        return '            <ul class="nav__menu--units">\n' + '\n'.join(items) + '\n            </ul>'

    def generate_new_header_bars(self, current_unit, unit_themes, current_path, subject_name):
        """Genera las 3 barras de navegación nuevas (Header institucional, navegación, curso)"""
        
        # Mapa de nombres de asignaturas
        subject_names = {
            'mate3': 'Matemáticas III',
            'antropologia-1': 'Antropología I',
            'derecho-1': 'Derecho I'
        }
        display_name = subject_names.get(subject_name, subject_name.replace('-', ' ').title())
        
        # Generar botones de unidades
        unit_buttons = ""
        path_parts = current_path.parts
        current_unit_index = None
        for i, part in enumerate(path_parts):
            if part == current_unit:
                current_unit_index = i
                break
        
        for idx, unit_data in enumerate(unit_themes, 1):
            unit_name = unit_data['unit']
            active_class = "pel-header-institutional__unit-btn--active" if unit_name == current_unit else ""
            
            # Calcular ruta relativa
            if current_unit_index is not None:
                levels_up = len(path_parts) - current_unit_index - 1
                rel_path = '../' * levels_up + f'{unit_name}/t1/1.html'
            else:
                rel_path = f'../../{unit_name}/t1/1.html'
            
            unit_buttons += f'            <a href="{rel_path}" class="pel-header-institutional__unit-btn {active_class}">Unidad {idx}</a>\n'
        
        # Generar las 3 barras
        header_html = f'''
<!-- Barra 1: Header Institucional (Negro) -->
<header class="pel-header-institutional">
    <div class="pel-header-institutional__inner">
        <div class="pel-header-institutional__logo">
            <img src="../assets/logo-pel.svg" alt="PEL" class="pel-header-institutional__logo-img">
            <span>Programas de Estudio en Línea</span>
        </div>
        <nav class="pel-header-institutional__units">
{unit_buttons}        </nav>
    </div>
</header>

<!-- Barra 2: Header Navegación (Naranja/Coral) -->
<nav class="pel-header-nav">
    <div class="pel-header-nav__inner">
        <a href="https://pel.cch.unam.mx/?theme=moove" class="pel-header-nav__link">
            <i class="ri-arrow-left-line"></i> Volver a mis cursos
        </a>
        <a href="https://pel.cch.unam.mx/login/logout.php?sesskey=acdpwASwF9&alt=logout" class="pel-header-nav__link">
            <i class="ri-logout-box-line"></i> Cerrar sesión
        </a>
    </div>
</nav>

<!-- Barra 3: Header Curso (Verde/Teal) -->
<header class="pel-header-course">
    <div class="pel-header-course__inner">
        <h1 class="pel-header-course__title">{display_name}</h1>
    </div>
</header>
'''
        return header_html

    def generate_theme_navigation(self, current_unit, current_theme, unit_themes, current_path):
        """Genera navegación de temas dentro del contenedor .course"""
        
        # Encontrar los temas de la unidad actual
        current_unit_themes = None
        for unit_data in unit_themes:
            if unit_data['unit'] == current_unit:
                current_unit_themes = unit_data.get('themes', [])
                break
        
        if not current_unit_themes:
            return ""
        
        # Calcular rutas relativas
        path_parts = current_path.parts
        current_unit_index = None
        for i, part in enumerate(path_parts):
            if part == current_unit:
                current_unit_index = i
                break
        
        # Generar lista de temas
        theme_items = ""
        for idx, theme_data in enumerate(current_unit_themes, 1):
            theme_url = theme_data['themeURL']
            theme_name = theme_data['themeName']
            active_class = "pel-theme-nav__item--active" if theme_url == current_theme else ""
            
            # Calcular ruta relativa al tema
            if current_unit_index is not None:
                levels_up = len(path_parts) - current_unit_index - 1
                theme_link = '../' * (levels_up - 1) + f'{theme_url}/1.html'
            else:
                theme_link = f'../{theme_url}/1.html'
            
            theme_items += f'            <li class="pel-theme-nav__item {active_class}">\n'
            theme_items += f'                <a href="{theme_link}" class="pel-theme-nav__link">{theme_name}</a>\n'
            theme_items += f'            </li>\n'
        
        nav_html = f'''    <!-- Navegación de Temas -->
    <nav class="pel-theme-nav">
        <h3 class="pel-theme-nav__title">Temas de esta unidad</h3>
        <ol class="pel-theme-nav__list">
{theme_items}        </ol>
    </nav>
'''
        return nav_html

    def generate_page_navigation(self, current_unit, current_theme, current_page_num, unit_themes, current_path):
        """Genera navegación de números de página dentro del tema actual"""
        
        # Encontrar el tema actual y su número de páginas
        current_theme_data = None
        for unit_data in unit_themes:
            if unit_data['unit'] == current_unit:
                for theme_data in unit_data.get('themes', []):
                    if theme_data['themeURL'] == current_theme:
                        current_theme_data = theme_data
                        break
                break
        
        if not current_theme_data:
            return ""
        
        total_pages = int(current_theme_data.get('pages', 1))
        
        if total_pages <= 1:
            return ""  # No mostrar navegación si solo hay 1 página
        
        # Generar botones de página
        page_buttons = ""
        for page_num in range(1, total_pages + 1):
            active_class = "pel-page-nav__btn--active" if page_num == current_page_num else ""
            page_link = f"{page_num}.html"
            page_buttons += f'            <a href="{page_link}" class="pel-page-nav__btn {active_class}">{page_num}</a>\n'
        
        nav_html = f'''    <!-- Navegación de Páginas -->
    <nav class="pel-page-nav">
        <div class="pel-page-nav__inner">
{page_buttons}        </div>
    </nav>
'''
        return nav_html

    def generate_new_footer(self):
        """Genera el footer moderno con franja PAPIIT naranja + info PEL oscura"""
        footer_html = '''
<footer class="pel-footer">
    <!-- Franja PAPIIT (Naranja) -->
    <div class="pel-footer__papiit">
        <div class="pel-footer__papiit-inner">
            <p class="pel-footer__papiit-text">
                Este sitio web es resultado del proyecto PAPIIT IV300420 'Alianza B@UNAM, CCH & ENP ante la pandemia: un estudio de impacto en docentes y estudiantes'. 
                Agradecemos el apoyo brindado por el programa PAPIIT para la realización de este trabajo.
            </p>
        </div>
    </div>
    
    <!-- Sección principal (Oscura) -->
    <div class="pel-footer__main">
        <div class="pel-footer__main-inner">
            <!-- Logo -->
            <div class="pel-footer__logo">
                <a href="https://pel.cch.unam.mx/?theme=moove">
                    <img src="../assets/logo-pel.svg" alt="Programas de Estudio en Línea" class="pel-footer__logo-img">
                </a>
            </div>
            
            <!-- Links -->
            <div class="pel-footer__links">
                <ul class="pel-footer__links-list">
                    <li><a href="https://portalacademico.cch.unam.mx/aviso-legal">Aviso</a></li>
                    <li><a href="https://portalacademico.cch.unam.mx/creditos">Créditos</a></li>
                    <li><a href="https://www.cch.unam.mx/calendario-escolar">Calendario</a></li>
                    <li><a href="https://www.cch.unam.mx/directorio">Directorio</a></li>
                </ul>
            </div>
            
            <!-- Redes Sociales -->
            <div class="pel-footer__social">
                <ul class="pel-footer__social-list">
                    <li>
                        <a href="https://www.facebook.com/portalacademico" target="_blank" rel="noopener noreferrer" aria-label="Facebook">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M9 8h-3v4h3v12h5v-12h3.642l.358-4h-4v-1.667c0-.955.192-1.333 1.115-1.333h2.885v-5h-3.808c-3.596 0-5.192 1.583-5.192 4.615v3.385z"/>
                            </svg>
                        </a>
                    </li>
                    <li>
                        <a href="https://twitter.com/academico_cch" target="_blank" rel="noopener noreferrer" aria-label="Twitter/X">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
                            </svg>
                        </a>
                    </li>
                    <li>
                        <a href="https://www.instagram.com/portalacademicocch" target="_blank" rel="noopener noreferrer" aria-label="Instagram">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
                            </svg>
                        </a>
                    </li>
                    <li>
                        <a href="https://www.youtube.com/user/portalacademicocch" target="_blank" rel="noopener noreferrer" aria-label="YouTube">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M19.615 3.184c-3.604-.246-11.631-.245-15.23 0-3.897.266-4.356 2.62-4.385 8.816.029 6.185.484 8.549 4.385 8.816 3.6.245 11.626.246 15.23 0 3.897-.266 4.356-2.62 4.385-8.816-.029-6.185-.484-8.549-4.385-8.816zm-10.615 12.816v-8l8 3.993-8 4.007z"/>
                            </svg>
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </div>
    
    <!-- Disclaimer legal -->
    <div class="pel-footer__legal">
        <div class="pel-footer__legal-inner">
            <p>Coordinación de Universidad Abierta, Innovación Educativa y Educación a Distancia de la UNAM. ©Todos los derechos reservados 2024. Hecho en México.</p>
            <p>Este sitio puede ser reproducido con fines no lucrativos, siempre y cuando no se mutile, se cite la fuente completa y su dirección electrónica.</p>
        </div>
    </div>
</footer>
'''
        return footer_html

    def replace_nav_menu(self, html_content, current_unit, unit_themes, current_path, subject_name, current_theme):
        """
        NUEVA VERSIÓN:
        1. Elimina completamente <nav class="nav">...</nav> y <aside class="summary">
        2. Agrega referencia a pel-navigation.css en <head>
        3. Inserta las 3 barras nuevas después de <body>
        4. Inserta navegación de temas dentro de <div class="course">
        5. Inserta navegación de páginas después de navegación de temas
        """
        if not unit_themes:
            return html_content
        
        # Extraer número de página actual del path
        current_page_num = 1
        page_file = current_path.name  # ej: "1.html", "2.html"
        if page_file.endswith('.html'):
            try:
                current_page_num = int(page_file.replace('.html', ''))
            except:
                current_page_num = 1
        
        # PASO 1: Eliminar <nav class="nav">...</nav> completamente
        nav_pattern = re.compile(r'<nav\s+class=["\']nav["\'][^>]*>.*?</nav>', re.DOTALL | re.IGNORECASE)
        html_content = nav_pattern.sub('', html_content)
        
        # PASO 1b: Eliminar <aside class="summary">...</aside> completamente
        aside_pattern = re.compile(r'<aside\s+class=["\']summary["\'][^>]*>.*?</aside>', re.DOTALL | re.IGNORECASE)
        html_content = aside_pattern.sub('', html_content)
        
        # PASO 2: Agregar referencia a pel-navigation.css y pel-navigation.js después de papiit.css
        css_pattern = re.compile(r'(<link[^>]*href="[^"]*papiit\.css"[^>]*>)')
        if css_pattern.search(html_content):
            html_content = css_pattern.sub(
                r'\1\n    <link rel="stylesheet" href="../assets/css/pel-navigation.css">\n    <script src="../assets/scripts/pel-navigation.js"></script>',
                html_content,
                count=1
            )
        
        # PASO 3: Insertar las 3 barras nuevas después de <body>
        new_header = self.generate_new_header_bars(current_unit, unit_themes, current_path, subject_name)
        body_pattern = re.compile(r'(<body[^>]*>)', re.IGNORECASE)
        if body_pattern.search(html_content):
            html_content = body_pattern.sub(r'\1\n' + new_header, html_content, count=1)
        
        # PASO 4: Insertar navegación de temas ANTES de <div class="course"> (full-width)
        theme_nav = self.generate_theme_navigation(current_unit, current_theme, unit_themes, current_path)
        
        course_pattern = re.compile(r'(<div\s+class=["\']course["\'][^>]*>)', re.IGNORECASE)
        if course_pattern.search(html_content):
            # Navegación de temas va ANTES del contenedor .course
            html_content = course_pattern.sub(theme_nav + r'\1', html_content, count=1)
        
        # PASO 4b: Insertar navegación de páginas DENTRO de <div class="course">
        page_nav = self.generate_page_navigation(current_unit, current_theme, current_page_num, unit_themes, current_path)
        
        course_pattern2 = re.compile(r'(<div\s+class=["\']course["\'][^>]*>)', re.IGNORECASE)
        if course_pattern2.search(html_content):
            html_content = course_pattern2.sub(r'\1\n' + page_nav, html_content, count=1)
        
        # PASO 5: Reemplazar footer viejo con footer nuevo moderno
        footer_pattern = re.compile(r'(<footer\s+class=["\']course__footer["\'][^>]*>.*?</footer>)', re.DOTALL | re.IGNORECASE)
        footer_match = footer_pattern.search(html_content)
        if footer_match:
            # Generar el footer nuevo
            new_footer = self.generate_new_footer()
            # Eliminar el footer viejo
            html_content = footer_pattern.sub('', html_content)
            # Insertar el footer nuevo antes de </body>
            html_content = re.sub(r'(</body>)', new_footer + r'\n\1', html_content, flags=re.IGNORECASE)
        
        return html_content

    def fix_content_navigation(self, html_content, current_path, unit_themes):
        """
        Arregla la navegación de flechas.
        FIX: Limpia URLs estáticas de Moodle cuando no hay siguiente/anterior.
        """
        if not unit_themes:
            return html_content

        next_path = self.calculate_next_navigation(current_path, unit_themes)
        prev_path = self.calculate_previous_navigation(current_path, unit_themes)

        # ── Right arrow (next) ──
        if next_path:
            html_content = self.RE_RIGHT_DATA_LINK.sub(
                rf'\g<1>{next_path}\g<2>', html_content
            )
            html_content = self.RE_RIGHT_HREF.sub(
                rf'\g<1>{next_path}\g<2>', html_content
            )
            html_content = html_content.replace(
                'class="course__content__nav--right hidden"',
                'class="course__content__nav--right"',
            )
        else:
            # FIX: Add hidden class + clear any Moodle static URL
            html_content = re.sub(
                r'class="course__content__nav--right(?!\s+hidden)"',
                'class="course__content__nav--right hidden"',
                html_content,
            )
            html_content = self.RE_RIGHT_DATA_LINK.sub(r'\g<1>\g<2>', html_content)
            html_content = self.RE_RIGHT_HREF.sub(r'\g<1>\g<2>', html_content)

        # ── Left arrow (previous) ──
        if prev_path:
            html_content = self.RE_LEFT_DATA_LINK.sub(
                rf'\g<1>{prev_path}\g<2>', html_content
            )
            html_content = self.RE_LEFT_HREF.sub(
                rf'\g<1>{prev_path}\g<2>', html_content
            )
            html_content = html_content.replace(
                'class="course__content__nav--left hidden"',
                'class="course__content__nav--left"',
            )
        else:
            # FIX: Add hidden class + clear any Moodle static URL
            html_content = re.sub(
                r'class="course__content__nav--left(?!\s+hidden)"',
                'class="course__content__nav--left hidden"',
                html_content,
            )
            html_content = self.RE_LEFT_DATA_LINK.sub(r'\g<1>\g<2>', html_content)
            html_content = self.RE_LEFT_HREF.sub(r'\g<1>\g<2>', html_content)

        return html_content

    def convert_activities_to_iframes(self, html_content, moodle_activities, moodle_url):
        """Convierte actividades de enlaces a iframes"""
        if not moodle_activities or not moodle_url:
            return html_content

        for activity in moodle_activities:
            id_html = activity['idHTML']
            pattern = re.compile(
                rf'<a[^>]*id="{re.escape(id_html)}"[^>]*>.*?</a>', re.DOTALL
            )
            match = pattern.search(html_content)
            if match:
                full_url = f"{moodle_url}{activity['url']}{activity['id']}&theme=photo"
                iframe = (
                    f'<iframe src="{full_url}" width="100%" height="600" '
                    f'style="border: none;" title="{id_html}"></iframe>'
                )
                html_content = html_content.replace(match.group(0), iframe)

        return html_content

    def fix_css_js_paths(self, html_content):
        """Arregla rutas CSS/JS después de reorganización de carpetas"""
        html_content = self.RE_CSS_DOUBLE_DOT.sub('href="../assets/', html_content)
        html_content = self.RE_SRC_DOUBLE_DOT.sub('src="../assets/', html_content)
        html_content = self.RE_NAV_DOUBLE_UNIT.sub(r'href="../\1/', html_content)
        return html_content

    # ─────────────────────────────────────────────
    #  File processing (single pass I/O)
    # ─────────────────────────────────────────────
    def process_html_file(self, file_path, subject):
        """Procesa un archivo HTML individual — una sola pasada de lectura/escritura"""
        action = "PROCESARÍA" if self.dry_run else "Procesando"
        print(f"  {action}: {file_path.relative_to(self.output_dir)}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()

            path_parts = file_path.parts
            unit_indices = [
                i for i, part in enumerate(path_parts)
                if self.RE_UNIT_PATTERN.match(part)
            ]

            if not unit_indices:
                return  # Not a unit HTML file

            unit_index = unit_indices[0]
            current_unit = path_parts[unit_index]
            current_theme = path_parts[unit_index + 1] if unit_index + 1 < len(path_parts) else 't1'
            subject_path = Path(*path_parts[:unit_index])
            subject_name = self.get_subject_from_path(file_path)

            # Load config (cached)
            unit_themes, moodle_activities, moodle_url = self.load_activity_config(
                subject_path, current_unit
            )

            # Apply all transformations in memory
            html_content = self.fix_css_js_paths(html_content)
            html_content = self.remove_breadcrumb_links(html_content)

            if unit_themes:
                html_content = self.replace_nav_menu(
                    html_content, current_unit, unit_themes, file_path, subject_name, current_theme
                )
                html_content = self.fix_content_navigation(
                    html_content, file_path, unit_themes
                )

            if moodle_activities and moodle_url:
                html_content = self.convert_activities_to_iframes(
                    html_content, moodle_activities, moodle_url
                )

            # Write back only if not dry run
            if not self.dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)

        except Exception as e:
            print(f"  ✗ Error en {file_path}: {e}")
            import traceback
            traceback.print_exc()

    # ─────────────────────────────────────────────
    #  Subject processing
    # ─────────────────────────────────────────────
    def process_subject(self, subject):
        """Copia la asignatura a output y procesa todos los archivos"""
        print(f"\n{'='*50}")
        print(f"  Procesando asignatura: {subject}")
        print(f"{'='*50}")

        # Copy to output directory
        if not self.dry_run:
            output_path = self.prepare_output(subject)
            
            # Copiar pel-navigation.css, pel-navigation.js y logo-pel.svg a cada unidad
            css_source = self.base_dir / "assets" / "pel-navigation.css"
            js_source = self.base_dir / "assets" / "pel-navigation.js"
            logo_source = self.base_dir / "assets" / "logo-pel.svg"
            
            if css_source.exists() and js_source.exists() and logo_source.exists():
                unit_folders = [f for f in output_path.iterdir() if f.is_dir() and self.RE_UNIT_PATTERN.match(f.name)]
                for unit in unit_folders:
                    # Copiar CSS
                    css_dest = unit / "assets" / "css" / "pel-navigation.css"
                    css_dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(css_source, css_dest)
                    
                    # Copiar JS
                    js_dest = unit / "assets" / "scripts" / "pel-navigation.js"
                    js_dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(js_source, js_dest)
                    
                    # Copiar Logo
                    logo_dest = unit / "assets" / "logo-pel.svg"
                    logo_dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(logo_source, logo_dest)
                    
                print(f"  ✓ pel-navigation.css copiado a {len(unit_folders)} unidades")
                print(f"  ✓ pel-navigation.js copiado a {len(unit_folders)} unidades")
                print(f"  ✓ logo-pel.svg copiado a {len(unit_folders)} unidades")
            else:
                if not css_source.exists():
                    print(f"  ⚠️ No se encontró assets/pel-navigation.css")
                if not js_source.exists():
                    print(f"  ⚠️ No se encontró assets/pel-navigation.js")
                if not logo_source.exists():
                    print(f"  ⚠️ No se encontró assets/logo-pel.svg")
        else:
            output_path = self.base_dir / subject
            print(f"  (DRY RUN: no se copia la asignatura)")

        html_files = self.find_html_files(output_path)

        # Clear cache for this subject
        self.unit_themes = {k: v for k, v in self.unit_themes.items() if not k.startswith(f"{subject}-")}
        self.moodle_activities = {k: v for k, v in self.moodle_activities.items() if not k.startswith(f"{subject}-")}
        self.moodle_urls = {k: v for k, v in self.moodle_urls.items() if not k.startswith(f"{subject}-")}

        print(f"  Encontrados {len(html_files)} archivos HTML")

        for file_path in sorted(html_files):
            self.process_html_file(file_path, subject)

        # Report cache stats
        print(f"  📦 Configs cacheadas: {len(self.unit_themes)} unidades")

        if not self.dry_run:
            print(f"  ✅ Output en: {output_path}")

    def run(self):
        """Ejecuta el procesamiento completo"""
        mode = "DRY RUN (sin modificar archivos)" if self.dry_run else "Procesamiento"
        print(f"=== {mode} de HTML ===\n")
        print(f"  Fuente: {self.base_dir}")
        print(f"  Output: {self.output_dir}")

        self.find_subjects()

        for subject in self.subjects:
            self.process_subject(subject)

        if not self.dry_run:
            print(f"\n{'='*50}")
            print(f"  === Archivos reparados en: {self.output_dir} ===")
            print(f"{'='*50}")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Modifica masivamente archivos HTML de cursos. '
                    'Las asignaturas originales NO se modifican — se copia todo al directorio de output.'
    )
    parser.add_argument(
        'directory', nargs='?', default='.',
        help='Directorio base donde están las asignaturas (default: directorio actual)'
    )
    parser.add_argument(
        '--output', '-o', default='out',
        help='Directorio de output para las asignaturas reparadas (default: out/)'
    )
    parser.add_argument(
        '--subject', '-s',
        help='Procesar solo una asignatura específica'
    )
    parser.add_argument(
        '--dry-run', '-n', action='store_true',
        help='Solo mostrar qué archivos se procesarían sin modificarlos'
    )

    args = parser.parse_args()

    base_dir = Path(args.directory).resolve()
    output_dir = Path(args.output).resolve()
    print(f"Directorio base: {base_dir}")
    print(f"Directorio output: {output_dir}")

    if not base_dir.exists():
        print(f"Error: El directorio base {base_dir} no existe")
        sys.exit(1)

    # Create output directory if needed
    if not args.dry_run:
        output_dir.mkdir(parents=True, exist_ok=True)

    modifier = HTMLModifier(base_dir, output_dir, dry_run=args.dry_run)

    if args.subject:
        modifier.subjects = [args.subject]
        modifier.process_subject(args.subject)
    else:
        modifier.run()


if __name__ == "__main__":
    main()
