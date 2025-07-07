from datetime import date
from semanas_validas import calcular_semana
from dotenv import load_dotenv
import os

load_dotenv()

USER = os.getenv('USER')

def inserir():
    hoje = date.today()
    return calcular_semana(USER, hoje)

semanas = inserir()
for s in semanas:
    print(s)