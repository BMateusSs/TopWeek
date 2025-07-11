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

    chart = []
    capa_cache = {}  # ← dicionário para armazenar capas já buscadas

    for album in albuns:
        try:
            nome = album.get('name')
            artista = album['artist'].get('#text')
            chave = (nome, artista)

            if chave in capa_cache:
                capa = capa_cache[chave]
            else:
                capa = requerir_capa_album(nome, artista)
                capa_cache[chave] = capa  # armazena no cache

            album_info = {
                'mbid': album.get('mbid') or None,
                'artist_mbid': album['artist'].get('mbid') or None,
                'album_name': nome,
                'artist_name': artista,
                'playcount': album.get('playcount'),
                'rank': album['@attr'].get('rank'),
                'cover': capa
            }

            chart.append(album_info)

        except Exception as e:
            print(f"Erro ao processar álbum: {album}. Erro: {e}")
            continue

    return chart
