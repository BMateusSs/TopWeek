from datetime import date
from semanas_validas import calcular_semana

def inserir():
    hoje = date.today()
    return calcular_semana('T4RG', hoje)

semanas = inserir()
for s in semanas:
    print(s)