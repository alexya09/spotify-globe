import os
import base64
import requests
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:8000/callback"

router = APIRouter()

SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"

#  Rota de login
@router.get("/login")
def login():
    scope = "playlist-read-private playlist-read-collaborative"
    
    auth_url = (
        f"{SPOTIFY_AUTH_URL}"
        f"?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&scope={scope}"
        f"&redirect_uri={REDIRECT_URI}"
    )

    return RedirectResponse(auth_url)


# Callback
@router.get("/callback")
def callback(code: str):
    auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
    auth_base64 = base64.b64encode(auth_string.encode()).decode()

    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }

    response = requests.post(SPOTIFY_TOKEN_URL, headers=headers, data=data)

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail=response.text)

    token_data = response.json()

    return {
        "access_token": token_data["access_token"],
        "refresh_token": token_data["refresh_token"]
    }
