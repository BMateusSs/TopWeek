from datetime import date
from semanas_validas import calcular_semana
from dotenv import load_dotenv
import os
from connection_db import fazer_conexao

load_dotenv()

USER = os.getenv('USER')

def inserir(user_id, start_date, end_date):
    conexao = fazer_conexao()

    cursor = conexao.cursor()

    sql = ("""
    INSERT INTO weekly_chart_metadata(user_id, start_date, end_date)
    VALUES(%s, %s, %s)
""")
    cursor.execute(sql, (user_id, start_date, end_date))
    conexao.commit()

