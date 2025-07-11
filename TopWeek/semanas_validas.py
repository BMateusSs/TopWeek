from datetime import datetime, timedelta, date, time
from data_de_registro import data_de_registro

def calcular_primeira_sexta(dia_atual):
    dia_da_semana = dia_atual.weekday()

    if dia_da_semana >= 4:
        sexta = dia_atual - timedelta(days=(dia_da_semana - 4))
        return sexta
    else:
        sexta = dia_atual - timedelta(days=(dia_da_semana + 3))
        return sexta
        
def calcular_semana(user, hoje):
    data = data_de_registro(user)
    sexta = calcular_primeira_sexta(data)
    semanas = []

    while True:
        quinta = sexta + timedelta(days=6)
        if quinta >= hoje:
            break
        semanas.append((sexta, quinta))
        sexta = quinta + timedelta(days=1)

    return semanas



if __name__ == '__main__':
    data = date(2025, 6, 7)
    hoje = data.today()

    semanas = calcular_semana(hoje)

    for s in semanas:
        print(s)