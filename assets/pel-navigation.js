/**
 * PEL Navigation - Script para hacer funcionar las flechas de navegación
 */

// Esperar a que el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    
    // Función para convertir data-link en href navegable
    const setupNavigationArrows = () => {
        const pLeft = document.getElementById('pLeft');
        const pRight = document.getElementById('pRight');
        
        if (pLeft) {
            const dataLink = pLeft.getAttribute('data-link');
            if (dataLink) {
                // Construir URL relativa desde la ubicación actual
                // Estamos en: /mate3/u5/t2/1.html
                // data-link viene en formato: "u5/t1/4.html" o "u1/t5/2.html"
                // Necesitamos ir 2 niveles arriba: ../../u5/t1/4.html
                const href = `../../${dataLink}`;
                pLeft.setAttribute('href', href);
                pLeft.style.cursor = 'pointer';
            } else {
                // No hay página anterior, ocultar
                pLeft.style.display = 'none';
            }
        }
        
        if (pRight) {
            const dataLink = pRight.getAttribute('data-link');
            if (dataLink) {
                // Construir URL relativa desde la ubicación actual
                const href = `../../${dataLink}`;
                pRight.setAttribute('href', href);
                pRight.style.cursor = 'pointer';
            } else {
                // No hay página siguiente, ocultar
                pRight.style.display = 'none';
            }
        }
    };
    
    // Ejecutar setup
    setupNavigationArrows();
});
