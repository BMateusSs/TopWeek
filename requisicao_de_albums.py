import os
from dotenv import load_dotenv
import requests

from requisicao_capa_album import requerir_capa_album

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
    chart = []
    for album in albuns_ordenados:

        rank = album['novo_rank']
        plays = album['playcount']
        artista = album['artist']['#text']
        album_nome = album['name']
        artista_mbid = album['artist']['mbid']
        mbid = album['mbid']
        capa = requerir_capa_album(album['name'], album['artist']['#text'])
        album['cover'] = capa
        chart.append(album)
    
    return chart
        
requerir_albuns(1750982400, 1751587199)