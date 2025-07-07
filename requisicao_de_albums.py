import os
from dotenv import load_dotenv
import requests

load_dotenv()

USER = os.getenv('USER')
API_KEY = os.getenv('API_KEY')

def requerir_albuns(start_date, end_date):
    params = {
        'method': 'user.getWeeklyAlbumChart',
        'api_key': API_KEY,
        'user': USER,
        'from': start_date,
        'to': end_date,
        'limit': 30,
        'format': 'json'
    }
    url = 'http://ws.audioscrobbler.com/2.0/'
    response = requests.get(url, params)
    dados = response.json()

    albuns = dados['weeklyalbumchart']['album']
    
    # Ordena por playcount (decrescente) e nome do álbum (A-Z)
    albuns_ordenados = sorted(
        albuns,
        key=lambda x: (-int(x['playcount']), x['name'].lower())
    )

    # Adiciona um novo rank baseado na ordenação
    for i, album in enumerate(albuns_ordenados, start=1):
        album['novo_rank'] = i  # Atribui a posição correta

    # Exibe os resultados
    for album in albuns_ordenados:
        print(f"Rank: {album['novo_rank']}")
        print(f"Plays: {album['playcount']}")
        print(f"Artista: {album['artist']['#text']}")
        print(f"Álbum: {album['name']}")
        print('=-' * 50)
        
requerir_albuns(1750982400, 1751587199)