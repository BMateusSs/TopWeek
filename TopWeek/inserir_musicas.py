from dotenv import load_dotenv
import os
from datetime import date, datetime
from connection_db import fazer_conexao
from requisicao_de_musicas import requisicao_de_musicas
from consultar_metadatas import consultar_metadatas


def converter_unimax(inicio, final):

    inicio_unixtime = inicio.timestamp()
    final_unixtime = final.timestamp()

    return (int(inicio_unixtime), int(final_unixtime))

def verificar_tabela():
    conexao = fazer_conexao()
    if conexao is None:
        return False
    
    try:
        cursor = conexao.cursor()
        cursor.execute("SHOW TABLES LIKE 'weekly_track_items'")
        resultado = cursor.fetchone()
        
        if resultado:
            return True
        else:
            return False
    except Exception as e:
        return False
    finally:
        if conexao.is_connected():
            cursor.close()
            conexao.close()

def dissecar_musicas(id, musicas):
    for musica in musicas:
        mbid = musica['mbid'] if musica['mbid'] else None
        artista_mbid = musica['artist_mbid'] if musica['artist_mbid'] else None
        musica_nome = musica['track_name']
        artista = musica['artist_name']
        plays = musica['playcount']
        rank = musica['rank']
        capa = musica['cover']
        inserir_albuns(id, mbid, artista_mbid, musica_nome, artista, plays, rank, capa)

def inserir_albuns(id, album_mbid, artista_mbid, musica_nome, artista, playcount, rank, capa):
    conexao = fazer_conexao()
    if conexao is None:
        return
    
    try:
        cursor = conexao.cursor()

        sql = '''
INSERT INTO weekly_track_items(
    chart_metadata_id, lastfm_track_mbid, lastfm_artist_mbid, 
    track_name, artist_name, playcount, rank_position, cover_track, album_track
)
VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
    playcount = VALUES(playcount),
    rank_position = VALUES(rank_position),
    cover_track = VALUES(cover_track),
    album_track = VALUES(album_track)
'''

        cursor.execute(sql, (id, album_mbid, artista_mbid, musica_nome, artista, playcount, rank, capa, None))
        conexao.commit()
        
    except Exception as e:
        pass
    finally:
        if conexao.is_connected():
            cursor.close()
            conexao.close()

def consultar_datas():
    if not verificar_tabela():
        return
    
    dados = consultar_metadatas(1)
    
    if not dados:
        return
    
    for id, inicio, final in dados:
        data_inicial, data_final = converter_unimax(inicio, final)
        albuns = requisicao_de_musicas(data_inicial, data_final)
        dissecar_musicas(id, albuns)

consultar_datas()