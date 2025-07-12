import os
from dotenv import load_dotenv
import requests

import sys
import io

from requerir_capa_musicas import requerir_capa_musica

load_dotenv()

API_KEY = os.getenv('API_KEY')
USER = os.getenv('USER')

def requisicao_de_musicas(data_inicial, data_final):
    url = 'http://ws.audioscrobbler.com/2.0/'

    params = {
        'method': 'user.getWeeklyTrackChart',
        'user': USER,
        'api_key': API_KEY,
        'from': data_inicial,
        'to': data_final,
        'format': 'json',
        'limit': 50
    }

    response = requests.get(url, params)

    dados = response.json()
    musicas = dados['weeklytrackchart']['track']

    capa_cache = {}
    musicas_info_list = []

    for musica in musicas:
        try: 
            nome = musica.get('name')
            artista = musica['artist'].get('#text')
            chave = (artista, nome)

            if chave in capa_cache:
                capa = capa_cache[chave]
            else:
                capa = requerir_capa_musica(nome, artista)
                capa_cache[chave] = capa

            musica_info = {   
                'mbid': musica.get('mbid') or None,
                'artist_mbid': musica['artist'].get('mbid') or None,
                'track_name': nome,
                'artist_name': artista,
                'playcount': musica.get('playcount'),
                'rank': musica['@attr'].get('rank'),
                'cover': capa
                }
            musicas_info_list.append(musica_info)

        except Exception as e:
            print(f"Erro ao processar música: {musica}. Erro: {e}")
            continue
    
    return musicas_info_list

requisicao_de_musicas(1750982400, 1751500800)