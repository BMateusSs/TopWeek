from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv()

config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'database': os.getenv('DB_NAME'),
    'charset': 'utf8mb4'
}

def fazer_conexao():
    try:
        conexao = mysql.connector.connect(**config)
        if conexao.is_connected():
            return conexao
        else:
            return None
        
    except mysql.connector.Error as err:
        return None