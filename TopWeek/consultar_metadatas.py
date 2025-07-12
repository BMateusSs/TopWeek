from connection_db import fazer_conexao

def consultar_metadatas(user):
    conexao = fazer_conexao()
    if conexao is None:
        return []
    
    try:
        cursor = conexao.cursor()

        sql = '''
        SELECT id, start_date, end_date
        FROM weekly_chart_metadata
        WHERE user_id = %s
        '''
        cursor.execute(sql, (user,))
        dados = cursor.fetchall()
        return dados
    except Exception as e:
        return []
    finally:
        if conexao.is_connected():
            cursor.close()
            conexao.close()