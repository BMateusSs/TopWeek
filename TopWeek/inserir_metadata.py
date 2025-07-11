from datetime import date, datetime
from semanas_validas import calcular_semana
from dotenv import load_dotenv
import os
from connection_db import fazer_conexao

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv()

USER = os.getenv('USER')

def chart_metadata(user_id, start_date, end_date):
    conexao = fazer_conexao()

    cursor = conexao.cursor()

    sql = ("""
    INSERT INTO weekly_chart_metadata(user_id, start_date, end_date)
    VALUES(%s, %s, %s)
    ON DUPLICATE KEY UPDATE
    start_date = VALUES(start_date),
    end_date = VALUES(end_date),
    user_id = VALUES(user_id)
""")
    cursor.execute(sql, (user_id, start_date, end_date))
    conexao.commit()
    cursor.close()
    conexao.close()

def inserir_valores():
    semanas = encontrar_semanas_validas()

    for start_date, end_date in semanas:
        chart_metadata(1, start_date, end_date)


def encontrar_semanas_validas():
    hoje = date.today()
    semanas = calcular_semana(USER, hoje)

    semanas_datetime = []
    for s in semanas:
        sexta, quinta = converter_para_datetime(s[0], s[1])
        semanas_datetime.append((sexta, quinta))
    return semanas_datetime

def converter_para_datetime(sexta, quinta):
    sexta_datetime = datetime(sexta.year, sexta.month, sexta.day, hour=0, minute=0, second=0)
    quinta_datetime = datetime(quinta.year, quinta.month, quinta.day, hour=23, minute=59, second=59)
    return sexta_datetime, quinta_datetime

inserir_valores()