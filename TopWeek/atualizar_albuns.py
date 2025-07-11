from dotenv import load_dotenv
import os
from datetime import date, datetime
from connection_db import fazer_conexao
from requisicao_de_albums import requerir_albuns
from consultar_metadatas import consultar_metadatas

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def converter_unimax(inicio, final):

    inicio_unixtime = inicio.timestamp()
    final_unixtime = final.timestamp()

    return (int(inicio_unixtime), int(final_unixtime))

def dissecar_albuns(id, albuns):
    for album in albuns:
        mbid = album['mbid'] if album['mbid'] else None
        artista_mbid = album['artist_mbid'] if album['artist_mbid'] else None
        album_nome = album['album_name']
        artista = album['artist_name']
        plays = album['playcount']
        rank = album['rank']
        capa = album['cover']
        inserir_albuns(id, mbid, artista_mbid, album_nome, artista, plays, rank, capa)

    print(album)

def inserir_albuns(id, album_mbid, artista_mbid, album_nome, artista, playcount, rank, capa):
    conexao = fazer_conexao()
    cursor = conexao.cursor()

    sql = '''
INSERT INTO weekly_album_items(
    chart_metadata_id, lastfm_album_mbid, lastfm_artist_mbid, 
    album_name, artist_name, playcount, rank_position, album_cover
)
VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
    playcount = VALUES(playcount),
    rank_position = VALUES(rank_position),
    album_cover = VALUES(album_cover)
'''


    cursor.execute(sql, (id, album_mbid, artista_mbid, album_nome, artista, playcount, rank, capa,))
    conexao.commit()
    
    print(f'{id} - {rank} - {album_nome} - {artista} - {playcount}')

def consultar_datas():
    user=1

    conexao = fazer_conexao()
    cursor = conexao.cursor()

    sql = '''
    SELECT id, start_date, end_date
    FROM weekly_chart_metadata
    WHERE user_id = %s
    ORDER BY start_date DESC, end_date DESC
    LIMIT 1
    '''
    cursor.execute(sql, (user,))
    dados = cursor.fetchall()
    
    for id, inicio, final in dados:
        data_inicial, data_final = converter_unimax(inicio, final)
        albuns = requerir_albuns(data_inicial, data_final)
        dissecar_albuns(id, albuns)

    print('acabou')
        
    

consultar_datas()




