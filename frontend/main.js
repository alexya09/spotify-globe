// main.js

const GEOJSON_URL = 'https://raw.githubusercontent.com/vasturiano/globe.gl/master/example/datasets/ne_110m_admin_0_countries.geojson';
const API_URL = 'http://127.0.0.1:8000'; // Endereço do Uvicorn

const card = document.getElementById('card-spotify');
const nomePaisEl = document.getElementById('pais-nome');
const nomeArtistaEl = document.getElementById('artista-nome');
// ADICIONEI ISSO AQUI 👇
const musicaNomeEl = document.getElementById('musica-nome'); 
const capaAlbumEl = document.getElementById('capa-album');
const spotifyLinkEl = document.getElementById('spotify-link');

// Função Principal
async function iniciarApp() {
    try {
        console.log("⏳ Iniciando carregamento...");

        // 1. Pega o Mapa Mundi
        const geoJsonReq = fetch(GEOJSON_URL).then(res => res.json());

        // 2. Pergunta ao Python quais países estão na lista
        const paisesReq = fetch(`${API_URL}/countries`)
            .then(res => res.json())
            .catch(() => []); 

        const [countries, listaPaises] = await Promise.all([geoJsonReq, paisesReq]);

        console.log("🌍 Países para carregar:", listaPaises);

        // 3. Pega os detalhes de cada país
        const requests = listaPaises.map(sigla => 
            fetch(`${API_URL}/top-artist/${sigla}`)
                .then(res => res.json())
                .catch(err => null)
        );

        const dadosDetalhados = await Promise.all(requests);

        const mapaSpotify = {};
        dadosDetalhados.forEach(dado => {
            // Verificamos apenas se o dado existe e se tem a propriedade 'country'
            if (dado && !dado.detail && dado.country) {
                mapaSpotify[dado.country] = {
                    // Agora lemos direto da raiz do objeto 'dado'
                    artista: dado.artist_name || 'Artista desconhecido',
                    track: dado.track || 'Música desconhecida',
                    img: dado.image || '', 
                    link: dado.spotify_url || '#'
                };
            } else {
                console.warn("⚠️ Um dos países falhou ao carregar:", dado);
            }
        });

        // 5. Cruza os dados com o GeoJSON
        countries.features.forEach(feat => {
            const sigla = feat.properties.ISO_A2;
            if (mapaSpotify[sigla]) {
                feat.properties.spotifyData = mapaSpotify[sigla];
                feat.properties.temDados = true;
            } else {
                feat.properties.temDados = false;
            }
        });

        desenharGlobo(countries);

    } catch (erro) {
        console.error("❌ Erro fatal:", erro);
    }
}

function desenharGlobo(data) {
    const world = Globe()
      (document.getElementById('globeViz'))
      .globeImageUrl('//unpkg.com/three-globe/example/img/earth-dark.jpg')
      .backgroundImageUrl('//unpkg.com/three-globe/example/img/night-sky.png')
      .hexPolygonsData(data.features)
      .hexPolygonResolution(3)
      .hexPolygonMargin(0.3)
      .hexPolygonUseDots(true)
      .hexPolygonColor(d => d.properties.temDados ? '#1DB954' : '#3a3a3a')
      .hexPolygonLabel(({ properties: d }) => `
        <div style="background: rgba(0,0,0,0.8); color: white; padding: 5px; border-radius: 4px;">
          <b>${d.ADMIN}</b> <br />
          ${d.temDados ? '🎵 Clique para ver' : '🚫 Sem dados'}
        </div>
      `)
      .onHexPolygonClick((polygon, event, { lat, lng }) => {
          if (polygon.properties.temDados) {
              mostrarCard(polygon.properties.ADMIN, polygon.properties.spotifyData);
              world.pointOfView({ lat, lng, altitude: 1.6 }, 1000);
          } else {
              card.style.display = 'none';
          }
      });
      
    world.controls().autoRotate = false;
    world.controls().enableZoom = true;
}

function mostrarCard(pais, dados) {
    nomePaisEl.innerText = pais;
    nomeArtistaEl.innerText = dados.artista;
    musicaNomeEl.innerText = "🎵 " + dados.track; 

    if (dados.img) {
        capaAlbumEl.style.backgroundImage = `url('${dados.img}')`;
        capaAlbumEl.style.backgroundColor = 'transparent';
    } else {
        capaAlbumEl.style.backgroundImage = 'none';
        capaAlbumEl.style.backgroundColor = '#333';
    }
    
    // <--- 3. ATUALIZA O LINK DO BOTÃO
    if (dados.link) {
        spotifyLinkEl.href = dados.link;
        spotifyLinkEl.style.display = 'block'; // Mostra o botão
    } else {
        spotifyLinkEl.style.display = 'none'; // Esconde se não tiver link
    }
    
    card.style.display = 'block';
}

// Inicia tudo
iniciarApp();