# UI/UX Spec – Interfaz LMS (Layout centrado de lectura)

## 🧩 1. Estructura general (layout)

La interfaz está basada en un patrón **content-first**, sin sidebar, con un contenedor central optimizado para lectura.

```
[ Header institucional ]
[ Subheader navegación ]
[ Header de curso ]
[ Main centrado ]
    [ Contenido educativo ]
    [ Elementos destacados (callouts) ]
    [ Actividades embebidas ]
[ Footer ]
```

### Principio clave

Todo gira alrededor de un **bloque central de lectura**, con ancho controlado para optimizar legibilidad.

---

## 📐 2. Contenedor principal

### Ancho óptimo

- Max-width: 720px – 840px  
- Ideal: 760px  

```css
max-width: 760px;
margin: 0 auto;
padding: 24px;
```

---

## 📏 3. Ritmo vertical

```css
--space-xs: 8px;
--space-sm: 16px;
--space-md: 24px;
--space-lg: 32px;
--space-xl: 48px;
```

Uso:

- Entre párrafos → 16–20px  
- Entre secciones → 32–48px  
- Títulos → 24px abajo  

---

## 🎨 4. Sistema de color

```css
--color-primary: #2F8F8B;
--color-accent: #F26C4F;
--color-dark: #1E1E1E;
--color-light: #F5F5F5;
--color-text: #2B2B2B;
--color-muted: #6B7280;
--color-highlight: #EDE9FE;
```

---

## ✍️ 5. Tipografía

### Familia

- Inter / Roboto / Open Sans

### Escala

```css
--text-sm: 14px;
--text-base: 16px;
--text-md: 18px;
--text-lg: 22px;
--text-xl: 26px;
```

### Uso

- Párrafos → 16–18px  
- Line-height → 1.6 – 1.75  
- Títulos → 22–26px bold  
- Subtítulos → 18px semibold  

---

## 📖 6. Bloques de contenido

### Párrafos

```css
max-width: 65ch;
line-height: 1.7;
margin-bottom: 16px;
```

---

### Listas educativas

Ejemplo:

```
je → -e
tu → -es
nous → -ons
```

---

### Ejemplos

- Separados del texto  
- Espaciado adicional  

---

## 🧩 7. Callouts

```css
padding: 16px 20px;
border-radius: 8px;
background: #EDE9FE;
font-size: 14px;
line-height: 1.5;
```

- Pueden sobresalir ligeramente del contenedor  
- No rompen el flujo principal  

---

## 🧪 8. Actividades embebidas

- Bloques externos (Moodle)
- No forman parte del sistema visual principal

```css
border: 1px solid #E0E0E0;
border-radius: 12px;
background: white;
```

---

## 🧱 9. Header

Tres niveles:

1. Negro (institucional)  
2. Coral (navegación)  
3. Verde (curso)  

---

## 🧱 10. Footer

- Fondo oscuro  
- Texto blanco  
- Estructura simple  

---

## 🧠 11. Principios UX

- Content-first  
- Alta legibilidad  
- Sin distracciones  
- Flujo vertical natural  
- Jerarquía clara  

---

## 🧭 12. Resumen

Interfaz educativa centrada en lectura con contenedor estrecho, tipografía optimizada y flujo tipo editorial.
