document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('searchButton').addEventListener('click', buscarPokemon);
});

async function buscarPokemon() {
    const nombre = document.getElementById('pokemonName').value.trim().toLowerCase();
    const resultadoDiv = document.getElementById('pokemonResult');
    const errorMsg = document.getElementById('searchErrorMessage');
    resultadoDiv.innerHTML = '';
    errorMsg.textContent = '';
    errorMsg.style.display = 'none';

    if (!nombre) {
        errorMsg.textContent = 'Por favor, ingresa un nombre de Pokémon.';
        errorMsg.style.display = 'block';
        return;
    }

    try {
        const response = await fetch(`https://pokeapi.co/api/v2/pokemon/${nombre}`);
        if (!response.ok) throw new Error('Pokémon no encontrado');
        const data = await response.json();

        // Consulta el color de la especie
        const speciesResponse = await fetch(data.species.url);
        const speciesData = await speciesResponse.json();
        const color = speciesData.color.name;

        // Mapea el color de la API a un color CSS agradable
        const colorMap = {
            black:   '#2d3436',
            blue:    '#74b9ff',
            brown:   '#a0522d',
            gray:    '#636e72',
            green:   '#55efc4',
            pink:    '#fab1a0',
            purple:  '#a29bfe',
            red:     '#ff7675',
            white:   '#dfe6e9',
            yellow:  '#ffeaa7'
        };
        const cardColor = colorMap[color] || '#f6d365';

        const imagen = data.sprites.front_default || 'https://via.placeholder.com/96?text=No+Imagen';
        const nombrePokemon = data.name;
        const tipo = data.types.map(t => t.type.name).join(', ');
        const altura = data.height / 10 + ' m';
        const peso = data.weight / 10 + ' kg';

        resultadoDiv.innerHTML = `
            <div class="pokemon-card" style="background: linear-gradient(135deg, ${cardColor} 0%, #fda085 100%);">
                <img src="${imagen}" alt="${nombrePokemon}">
                <h3>${nombrePokemon.charAt(0).toUpperCase() + nombrePokemon.slice(1)}</h3>
                <p><strong>Tipo:</strong> ${tipo}</p>
                <p><strong>Altura:</strong> ${altura}</p>
                <p><strong>Peso:</strong> ${peso}</p>
            </div>
        `;
        resultadoDiv.style.display = 'block';
    } catch (error) {
        resultadoDiv.innerHTML = '';
        errorMsg.textContent = 'Pokémon no encontrado. Intenta con otro nombre.';
        errorMsg.style.display = 'block';
    }
}