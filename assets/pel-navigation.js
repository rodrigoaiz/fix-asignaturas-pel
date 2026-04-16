/**
 * PEL Navigation - Script para hacer funcionar las flechas de navegación
 * Incluye navegación con teclado (flechas izquierda/derecha)
 */

// Esperar a que el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    
    // Función para validar flechas de navegación
    const setupNavigationArrows = () => {
        const pLeft = document.getElementById('pLeft');
        const pRight = document.getElementById('pRight');
        
        if (pLeft) {
            const href = pLeft.getAttribute('href');
            if (href && href.trim() !== '') {
                // Ya tiene href correcto del HTML
                pLeft.style.cursor = 'pointer';
            } else {
                // No hay página anterior, ocultar
                pLeft.style.display = 'none';
            }
        }
        
        if (pRight) {
            const href = pRight.getAttribute('href');
            if (href && href.trim() !== '') {
                // Ya tiene href correcto del HTML
                pRight.style.cursor = 'pointer';
            } else {
                // No hay página siguiente, ocultar
                pRight.style.display = 'none';
            }
        }
    };
    
    // Función para navegación con teclado
    const setupKeyboardNavigation = () => {
        document.addEventListener('keydown', function(e) {
            // Ignorar si el usuario está escribiendo en un input, textarea, o select
            const activeElement = document.activeElement;
            const isTyping = activeElement.tagName === 'INPUT' || 
                           activeElement.tagName === 'TEXTAREA' || 
                           activeElement.tagName === 'SELECT' ||
                           activeElement.isContentEditable;
            
            if (isTyping) return;
            
            const pLeft = document.getElementById('pLeft');
            const pRight = document.getElementById('pRight');
            
            // Flecha izquierda (←) - Página anterior
            if (e.key === 'ArrowLeft' && pLeft) {
                const href = pLeft.getAttribute('href');
                if (href && pLeft.style.display !== 'none') {
                    e.preventDefault();
                    window.location.href = href;
                }
            }
            
            // Flecha derecha (→) - Página siguiente
            if (e.key === 'ArrowRight' && pRight) {
                const href = pRight.getAttribute('href');
                if (href && pRight.style.display !== 'none') {
                    e.preventDefault();
                    window.location.href = href;
                }
            }
        });
    };
    
    // Ejecutar setup
    setupNavigationArrows();
    setupKeyboardNavigation();
});
