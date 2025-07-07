from dotenv import load_dotenv
import os
from datetime import date, datetime
from connection_db import fazer_conexao
from requisicao_de_albums import requerir_albuns

def converter_unimax(inicio, final):
    sexta = inicio.timestamp()
    quinta = final.timestamp()
    requisicao(int(sexta), int(quinta))

def requisicao(data_inicial, data_final):
    album = requerir_albuns(data_inicial, data_final)

    print(album)

def consultar_datas():
    conexao = fazer_conexao()
    cursor = conexao.cursor()

    sql = '''
    SELECT start_date, end_date
    FROM weekly_chart_metadata
    WHERE user_id = %s
    '''
    cursor.execute(sql, (1,))
    semanas = cursor.fetchall()
    

    for semana in semanas:
        converter_unimax(semana[0], semana[1])

consultar_datas()




