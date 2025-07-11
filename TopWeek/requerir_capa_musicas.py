from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

def requerir_capa_musica(nome, artista):
    query = f'track:"{nome}" artist:"{artista}"'

    resultado = sp.search(q=query, type='track', limit=1)

    if resultado['tracks']['items']:
        track = resultado['tracks']['items'][0]
        capa = track['album']['images'][0]['url']
        return capa
    else:
        print("❌ Nenhuma música encontrada.")

requerir_capa_musica('it girl', 'jade')