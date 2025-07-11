from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv()

config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'database': os.getenv('DB_NAME')
}

def fazer_conexao():
    try:
        conexao = mysql.connector.connect(**config)
        if conexao.is_connected():
            print('Conexão ao MySQL estabelecida com sucesso!')

            return conexao
        
    except mysql.connector.Error as err:
        print(f'Erro de conexão: {err}')