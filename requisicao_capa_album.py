from dotenv import load_dotenv
import requests
import os

load_dotenv()

USER = os.getenv('USER')
API_KEY = os.getenv('API_KEY')

def requerir_capa_album(album, artista):
    params = {
        'method': 'album.getInfo',
        'api_key': API_KEY,
        'user': USER,
        'album': album,
        'artist': artista,
        'format': 'json'
    }

    url = 'http://ws.audioscrobbler.com/2.0/'

    response = requests.get(url, params)
    dados = response.json()
    image = dados['album']['image']
    return next((item['#text'] for item in image if item['size'] == 'extralarge'), None)
