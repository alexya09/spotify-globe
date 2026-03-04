import requests
import base64
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

def get_token():
    if not CLIENT_ID or not CLIENT_SECRET:
        raise Exception("CLIENT_ID or CLIENT_SECRET missing in .env")

    auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
    auth_base64 = base64.b64encode(auth_string.encode("utf-8")).decode("utf-8")

    url = "https://accounts.spotify.com/api/token"
    
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    result = requests.post(url, headers=headers, data=data)
    
    if result.status_code != 200:
        raise Exception(f"Auth Failed: {result.text}")

    return result.json()["access_token"]

def get_track_info_from_spotify(artist_name, track_name, token):
    """Busca os metadados da música para obter a capa e o link direto da faixa."""
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}
    
    
    query = f"track:{track_name} artist:{artist_name}"
    params = {
        "q": query,
        "type": "track",
        "limit": 1
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            return {"image": "", "spotify_url": ""}
            
        data = response.json()

        if not data.get("tracks") or not data["tracks"]["items"]:
            params["q"] = track_name
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            if not data.get("tracks") or not data["tracks"]["items"]:
                return {"image": "", "spotify_url": ""}

        track = data["tracks"]["items"][0]
        
        return {
            "image": track["album"]["images"][0]["url"] if track["album"]["images"] else "",
            "spotify_url": track["external_urls"]["spotify"]
        }
    except Exception as e:
        print(f"Erro ao buscar info da música no Spotify: {e}")
        return {"image": "", "spotify_url": ""}