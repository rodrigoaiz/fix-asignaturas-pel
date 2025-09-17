#!/usr/bin/env node

/**
 * Script para realizar cambios masivos en archivos HTML de las asignaturas
 * Realiza las siguientes modificaciones:
 * 1. Quita las ligas del breadcrumb course__header--breadcrumb
 * 2. Arregla la navegación course__content__nav para continuar correctamente
 * 3. Reemplaza nav__menu con un menú que navegue por unidades
 * 4. Convierte actividades de ligas a iframes con ?theme=photo
 */

const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

class HTMLModifier {
    constructor(baseDir) {
        this.baseDir = baseDir;
        this.subjects = [];
        this.unitThemes = new Map();
        this.moodleActivities = new Map();
    }

    /**
     * Encuentra todas las asignaturas en el directorio base
     */
    findSubjects() {
        const entries = fs.readdirSync(this.baseDir, { withFileTypes: true });
        this.subjects = entries
            .filter(entry => entry.isDirectory())
            .map(entry => entry.name);
        
        console.log(`Encontradas asignaturas: ${this.subjects.join(', ')}`);
        return this.subjects;
    }

    /**
     * Carga la configuración de activities_moodle.js para una unidad específica
     */
    loadActivityConfig(subjectPath, unit) {
        const configPath = path.join(subjectPath, unit, 'assets', 'scripts', 'activities_moodle.js');
        
        if (!fs.existsSync(configPath)) {
            console.warn(`No se encontró ${configPath}`);
            return null;
        }

        try {
            // Leer el archivo y extraer la configuración
            const content = fs.readFileSync(configPath, 'utf8');
            
            // Extraer unit_themes
            const unitThemesMatch = content.match(/export const unit_themes\s*=\s*(\[[\s\S]*?\]);/);
            const moodleActivitiesMatch = content.match(/export const moodleActivities\s*=\s*(\[[\s\S]*?\]);/);
            
            if (unitThemesMatch) {
                // Evaluar de forma segura el contenido JavaScript
                const unitThemesStr = unitThemesMatch[1];
                const unitThemes = eval(`(${unitThemesStr})`);
                this.unitThemes.set(`${subjectPath}-${unit}`, unitThemes);
            }
            
            if (moodleActivitiesMatch) {
                const moodleActivitiesStr = moodleActivitiesMatch[1];
                const moodleActivities = eval(`(${moodleActivitiesStr})`);
                this.moodleActivities.set(`${subjectPath}-${unit}`, moodleActivities);
            }
            
            return { unitThemes: unitThemesMatch?.[1], moodleActivities: moodleActivitiesMatch?.[1] };
        } catch (error) {
            console.error(`Error cargando configuración de ${configPath}:`, error);
            return null;
        }
    }

    /**
     * Encuentra todos los archivos HTML en una asignatura
     */
    findHTMLFiles(subjectPath) {
        const htmlFiles = [];
        
        const scanDirectory = (dir) => {
            const entries = fs.readdirSync(dir, { withFileTypes: true });
            
            for (const entry of entries) {
                const fullPath = path.join(dir, entry.name);
                
                if (entry.isDirectory()) {
                    scanDirectory(fullPath);
                } else if (entry.name.endsWith('.html')) {
                    htmlFiles.push(fullPath);
                }
            }
        };
        
        scanDirectory(subjectPath);
        return htmlFiles;
    }

    /**
     * Quita las ligas del breadcrumb manteniendo solo el texto
     */
    removeBreadcrumbLinks(dom) {
        const breadcrumb = dom.window.document.querySelector('.course__header--breadcrumb');
        if (breadcrumb) {
            // Remover todos los enlaces pero mantener el texto
            const links = breadcrumb.querySelectorAll('a');
            links.forEach(link => {
                const textNode = dom.window.document.createTextNode(link.textContent);
                link.parentNode.replaceChild(textNode, link);
            });
        }
    }

    /**
     * Genera el nuevo menú de navegación por unidades
     */
    generateUnitsMenu(subject, currentUnit, unitThemes) {
        const menuHTML = `
            <ul class="nav__menu--units">
                ${unitThemes.map(unit => `
                    <li class="nav__menu--item ${unit.unit === currentUnit ? 'nav__menu--item--active' : ''}">
                        <a class="nav__menu__item--link" href="../${unit.unit}/${unit.unit}/t1/1.html">
                            <span>${unit.unit.toUpperCase()}</span>
                        </a>
                        <ul class="nav__menu--themes">
                            ${unit.themes.map(theme => `
                                <li class="nav__menu--theme">
                                    <a href="../${unit.unit}/${unit.unit}/${theme.themeURL}/1.html">
                                        ${theme.themeName}
                                    </a>
                                </li>
                            `).join('')}
                        </ul>
                    </li>
                `).join('')}
            </ul>
        `;
        return menuHTML;
    }

    /**
     * Reemplaza el nav__menu existente con el nuevo menú de unidades
     */
    replaceNavMenu(dom, subject, currentUnit, unitThemes) {
        const navMenu = dom.window.document.querySelector('.nav__menu');
        if (navMenu && unitThemes) {
            const newMenuHTML = this.generateUnitsMenu(subject, currentUnit, unitThemes);
            navMenu.innerHTML = newMenuHTML;
        }
    }

    /**
     * Calcula la navegación siguiente basada en la estructura de temas
     */
    calculateNextNavigation(currentPath, unitThemes) {
        // Extraer información del path actual
        const pathParts = currentPath.split('/');
        const fileName = pathParts[pathParts.length - 1];
        const currentTheme = pathParts[pathParts.length - 2];
        const currentUnit = pathParts[pathParts.length - 3];
        const currentPage = parseInt(fileName.replace('.html', ''));

        // Encontrar la unidad actual en unitThemes
        const currentUnitData = unitThemes.find(unit => unit.unit === currentUnit);
        if (!currentUnitData) return null;

        // Encontrar el tema actual
        const currentThemeData = currentUnitData.themes.find(theme => theme.themeURL === currentTheme);
        if (!currentThemeData) return null;

        const maxPages = parseInt(currentThemeData.pages);
        
        // Si no es la última página del tema, ir a la siguiente página
        if (currentPage < maxPages) {
            return `${currentPage + 1}.html`;
        }

        // Si es la última página del tema, ir al siguiente tema
        const currentThemeIndex = currentUnitData.themes.findIndex(theme => theme.themeURL === currentTheme);
        if (currentThemeIndex < currentUnitData.themes.length - 1) {
            const nextTheme = currentUnitData.themes[currentThemeIndex + 1];
            return `../${nextTheme.themeURL}/1.html`;
        }

        // Si es el último tema de la unidad, ir a la siguiente unidad
        const currentUnitIndex = unitThemes.findIndex(unit => unit.unit === currentUnit);
        if (currentUnitIndex < unitThemes.length - 1) {
            const nextUnit = unitThemes[currentUnitIndex + 1];
            return `../../${nextUnit.unit}/${nextUnit.unit}/${nextUnit.themes[0].themeURL}/1.html`;
        }

        // Si es la última página de la última unidad, no hay siguiente
        return null;
    }

    /**
     * Arregla la navegación de las flechas
     */
    fixContentNavigation(dom, currentPath, unitThemes) {
        const rightArrow = dom.window.document.querySelector('.course__content__nav--right');
        if (rightArrow && unitThemes) {
            const nextPath = this.calculateNextNavigation(currentPath, unitThemes);
            if (nextPath) {
                rightArrow.setAttribute('data-link', nextPath);
                rightArrow.href = nextPath;
            }
        }
    }

    /**
     * Convierte actividades de enlaces a iframes
     */
    convertActivitiesToIframes(dom, moodleActivities, moodleURL) {
        if (!moodleActivities) return;

        moodleActivities.forEach(activity => {
            const element = dom.window.document.getElementById(activity.idHTML);
            if (element && element.tagName === 'A') {
                // Crear iframe
                const iframe = dom.window.document.createElement('iframe');
                const fullURL = `${moodleURL}${activity.url}${activity.id}?theme=photo`;
                
                iframe.src = fullURL;
                iframe.width = '100%';
                iframe.height = '600';
                iframe.style.border = 'none';
                iframe.title = activity.idHTML;
                
                // Reemplazar el enlace con el iframe
                element.parentNode.replaceChild(iframe, element);
            }
        });
    }

    /**
     * Procesa un archivo HTML individual
     */
    processHTMLFile(filePath, subject) {
        console.log(`Procesando: ${filePath}`);
        
        try {
            // Leer el archivo HTML
            const htmlContent = fs.readFileSync(filePath, 'utf8');
            const dom = new JSDOM(htmlContent);

            // Extraer información del path
            const pathParts = filePath.split('/');
            const unitIndex = pathParts.findIndex(part => part.startsWith('u') && part.match(/^u\d+$/));
            const currentUnit = pathParts[unitIndex];
            
            // Cargar configuración para esta unidad
            const subjectPath = pathParts.slice(0, unitIndex).join('/');
            const config = this.loadActivityConfig(subjectPath, currentUnit);
            const unitThemes = this.unitThemes.get(`${subjectPath}-${currentUnit}`);
            const moodleActivities = this.moodleActivities.get(`${subjectPath}-${currentUnit}`);

            // Aplicar modificaciones
            this.removeBreadcrumbLinks(dom);
            
            if (unitThemes) {
                this.replaceNavMenu(dom, subject, currentUnit, unitThemes);
                this.fixContentNavigation(dom, filePath, unitThemes);
            }
            
            if (moodleActivities) {
                this.convertActivitiesToIframes(dom, moodleActivities, 'https://pel.cch.unam.mx/');
            }

            // Guardar el archivo modificado
            const modifiedHTML = dom.serialize();
            fs.writeFileSync(filePath, modifiedHTML);
            
            console.log(`✓ Procesado: ${filePath}`);
        } catch (error) {
            console.error(`Error procesando ${filePath}:`, error);
        }
    }

    /**
     * Procesa todos los archivos de una asignatura
     */
    processSubject(subject) {
        console.log(`\n=== Procesando asignatura: ${subject} ===`);
        
        const subjectPath = path.join(this.baseDir, subject);
        const htmlFiles = this.findHTMLFiles(subjectPath);
        
        console.log(`Encontrados ${htmlFiles.length} archivos HTML`);
        
        htmlFiles.forEach(filePath => {
            this.processHTMLFile(filePath, subject);
        });
    }

    /**
     * Ejecuta el procesamiento completo
     */
    run() {
        console.log('=== Iniciando procesamiento masivo de HTML ===\n');
        
        this.findSubjects();
        
        this.subjects.forEach(subject => {
            this.processSubject(subject);
        });
        
        console.log('\n=== Procesamiento completado ===');
    }
}

// Verificar argumentos de línea de comandos
const args = process.argv.slice(2);
const baseDir = args[0] || process.cwd();

console.log(`Directorio base: ${baseDir}`);

// Verificar que jsdom esté disponible
try {
    require('jsdom');
} catch (error) {
    console.error('Error: jsdom no está instalado. Ejecuta: npm install jsdom');
    process.exit(1);
}

// Ejecutar el modificador
const modifier = new HTMLModifier(baseDir);
modifier.run();
