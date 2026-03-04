from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import asyncio
from pathlib import Path
from contextlib import asynccontextmanager

from auth import router as auth_router
from charts import get_all_top_1_from_official_charts
from spotify import get_token, get_track_info_from_spotify

BASE_DIR = Path(__file__).resolve().parent
CACHE_FILE = BASE_DIR / "data" / "cache.json"

with open(BASE_DIR / "data" / "top_artists.json", "r", encoding="utf-8") as f:
    PAISES_DATA = json.load(f)

async def update_cache_daily():
    while True:
        print("Iniciando a atualização do cache de todos os países...")
        countries = list(PAISES_DATA.keys())
        
        charts_data = await asyncio.to_thread(get_all_top_1_from_official_charts, countries)
        
        try:
            token = get_token()
        except Exception as e:
            print(f"Erro ao pegar token do Spotify: {e}")
            await asyncio.sleep(60)
            continue
            
        new_cache = {}
        for country, data in charts_data.items():
            spotify_data = get_track_info_from_spotify(data["artist"], data["track"], token)
            new_cache[country] = {
                "country": country,
                "track": data["track"],
                "artist_name": data["artist"],
                "image": spotify_data["image"],
                "spotify_url": spotify_data["spotify_url"]
            }
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(new_cache, f, ensure_ascii=False, indent=4)
            
        print("Cache atualizado com sucesso!")
        await asyncio.sleep(86400)

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(update_cache_daily())
    yield
    task.cancel()

app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/countries")
def get_countries():
    return list(PAISES_DATA.keys())

@app.get("/top-artist/{country_code}")
def top_artist(country_code: str):
    country_code = country_code.upper()
    
    if not CACHE_FILE.exists():
        raise HTTPException(status_code=503, detail="Cache sendo gerado. Tente novamente em alguns segundos.")
        
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        cache = json.load(f)
        
    if country_code not in cache:
        raise HTTPException(status_code=404, detail="País não encontrado no cache atual.")
        
    return cache[country_code]