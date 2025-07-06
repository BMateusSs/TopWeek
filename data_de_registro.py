import requests
from datetime import date

from apiKey import api_key

def data_de_registro(user):
    params = {
        'method': 'user.getInfo',
        'api_key': api_key(),
        'user': user,
        'format': 'json'
    }

    url = 'http://ws.audioscrobbler.com/2.0/'

    response = requests.get(url, params)
    dados = response.json()
    
    unixtime = dados['user']['registered']['unixtime']
    return registro(int(unixtime))

def registro(unixtime):
    registro = date.fromtimestamp(unixtime)

    return registro