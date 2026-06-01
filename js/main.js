// Datos de los mini HTMLs
const lecciones = {
    castellano: [
        { nombre: "Sujeto y Predicado", archivo: "sujeto_predicado.html", descripcion: "Aprende a identificar el sujeto y predicado en oraciones" },
        { nombre: "Diptongos e Hiatos", archivo: "diptongos_hiatos.html", descripcion: "Diferencia entre diptongos y hiatos" }
    ],
    ingles: [
        { nombre: "Present Simple", archivo: "present_simple.html", descripcion: "Aprende el presente simple en inglés" },
        { nombre: "Verbo To Be", archivo: "to_be.html", descripcion: "Conjugación y uso del verbo to be" }
    ],
    latin: [
        { nombre: "Primera Declinación", archivo: "primera_declinacion.html", descripcion: "Aprende la primera declinación latina" },
        { nombre: "Verbos en Latín", archivo: "verbos_latin.html", descripcion: "Introducción a los verbos latinos" }
    ]
};

// Cargar cards dinámicamente
document.addEventListener('DOMContentLoaded', function() {
    for (const [idioma, leccionesLista] of Object.entries(lecciones)) {
        const container = document.getElementById(`${idioma}-cards`);
        if (container) {
            leccionesLista.forEach(leccion => {
                const card = document.createElement('div');
                card.className = 'card';
                card.innerHTML = `
                    <h3>📖 ${leccion.nombre}</h3>
                    <p>${leccion.descripcion}</p>
                    <a href="lenguas/${idioma}/${leccion.archivo}" class="btn">Ver lección →</a>
                `;
                container.appendChild(card);
            });
        }
    }
    
    console.log('📚 Mini HTMLs Educativos cargados');
});
