// Cargar mini HTMLs dinámicamente
document.addEventListener('DOMContentLoaded', function() {
    console.log('📚 Mini HTMLs Educativos cargados');
    
    // Ejemplo de función para cargar ejercicios
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('click', function() {
            const link = this.querySelector('a');
            if(link) {
                window.open(link.href, '_blank');
            }
        });
    });
});
