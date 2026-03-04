import requests
from bs4 import BeautifulSoup

def get_all_top_1_from_official_charts(country_codes):
    """Lê os rankings através do Kworb (estável e sem login)."""
    results = {}
    headers = {'User-Agent': 'Mozilla/5.0'}

    for code in country_codes:
        url_code = code.lower()
        url = f"https://kworb.net/spotify/country/{url_code}_daily.html"
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"País {code} não disponível no Kworb.")
                continue
            
            response.encoding = 'utf-8'

            soup = BeautifulSoup(response.text, 'html.parser')
            first_row = soup.select_one('table.sortable tbody tr')
            
            if first_row:
                full_text = first_row.select_one('td.text').get_text()
                if " - " in full_text:
                    artist_name, track_name = full_text.split(" - ", 1)
                else:
                    artist_name = full_text
                    track_name = "Desconhecido"
                
                results[code.upper()] = {
                    "artist": artist_name.strip(),
                    "track": track_name.strip()
                }
                print(f" {code.upper()} carregado: {artist_name.strip()}")
        except Exception as e:
            print(f" Erro em {code.upper()}: {e}")

    return results