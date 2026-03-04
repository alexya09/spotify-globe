# 🌍 Spotify Global 3D

Um globo interativo em 3D que permite explorar a música número 1 mais tocada no Spotify em dezenas de países ao redor do mundo, atualizada em tempo real.

![Status](https://img.shields.io/badge/Status-Concluído-success)
![Python](https://img.shields.io/badge/Backend-Python_FastAPI-blue)
![JavaScript](https://img.shields.io/badge/Frontend-JavaScript-yellow)
![Deploy](https://img.shields.io/badge/Deploy-Render_%26_GitHub_Pages-purple)

🔗 **[Acesse a Aplicação ao Vivo aqui](https://alexya09.github.io/spotify-globe/)** 

---

## 🎵 Sobre o Projeto

O **Spotify Global 3D** é uma aplicação Full-Stack desenvolvida para visualizar dados musicais de forma imersiva. Através de um mapa-múndi interativo em 3D, o usuário pode clicar em diferentes países para descobrir qual é a faixa mais popular do momento, visualizar a capa oficial do álbum e ser redirecionado diretamente para o player do Spotify.

### ✨ Funcionalidades
* **Globo 3D Interativo:** Renderização de polígonos baseados em GeoJSON com controles de rotação e zoom.
* **Web Scraping Dinâmico:** Extração diária de dados do Kworb para contornar barreiras de login e obter rankings precisos.
* **Integração com API do Spotify:** Busca de metadados ricos (capas de álbuns de alta resolução e links de redirecionamento).
* **Sistema de Cache Inteligente:** O backend constrói e atualiza um arquivo `cache.json` em segundo plano, garantindo que o frontend carregue quase instantaneamente e protegendo a API contra limites de requisição (Rate Limiting).
* **Tratamento de Erros:** Respostas HTTP 503 automatizadas enquanto o cache está sendo gerado, com feedback visual no console do frontend.

---

## 🛠️ Tecnologias Utilizadas

Este projeto foi construído separando as responsabilidades de Backend e Frontend, permitindo fácil manutenção e escalabilidade.

**Frontend:**
* **JavaScript (Vanilla):** Lógica assíncrona (`fetch`, `Promises`) e manipulação do DOM.
* **HTML5 & CSS3:** Interface minimalista focada na visualização de dados.
* **Globe.gl / Three.js:** Biblioteca responsável pela renderização do globo 3D de alta performance no navegador.

**Backend:**
* **Python 3:** Linguagem base da API.
* **FastAPI & Uvicorn:** Criação de endpoints rápidos, modernos e assíncronos.
* **BeautifulSoup4 & Requests:** Raspagem e extração de dados HTML.
* **Python-dotenv:** Gerenciamento seguro de credenciais (Client ID e Secret).

---

## ⚙️ Como rodar localmente

Se você deseja clonar o repositório e rodar o projeto na sua própria máquina, siga os passos abaixo:

### Pré-requisitos
* Python 3.8+ instalado.
* Conta de desenvolvedor no [Spotify for Developers](https://developer.spotify.com/) para obter as chaves da API.

### Passo 1: Configuração do Backend
```bash
# Clone este repositório
git clone [https://github.com/alexya09/spotify-globe.git](https://github.com/alexya09/spotify-globe.git)
cd spotify-globe/backend

# Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows use: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt
