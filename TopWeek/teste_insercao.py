from connection_db import fazer_conexao

def testar_insercao():
    conexao = fazer_conexao()
    if conexao is None:
        print("Erro: Nao foi possivel conectar ao banco")
        return
    
    try:
        cursor = conexao.cursor()
        
        # Verificar estrutura da tabela
        cursor.execute("DESCRIBE weekly_track_items")
        colunas = cursor.fetchall()
        print("Estrutura da tabela weekly_track_items:")
        for coluna in colunas:
            print(f"  {coluna[0]} - {coluna[1]}")
        
        # Testar inserção simples
        sql = '''
        INSERT INTO weekly_track_items(
            chart_metadata_id, lastfm_track_mbid, lastfm_artist_mbid, 
            track_name, artist_name, playcount, rank_position, cover_track
        )
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
        '''
        
        dados_teste = (1, None, None, "Teste Musica", "Teste Artista", 100, 1, "http://teste.com")
        
        cursor.execute(sql, dados_teste)
        conexao.commit()
        print("Inserção de teste realizada com sucesso!")
        
        # Verificar se foi inserido
        cursor.execute("SELECT COUNT(*) FROM weekly_track_items WHERE track_name = 'Teste Musica'")
        count = cursor.fetchone()[0]
        print(f"Registros encontrados: {count}")
        
    except Exception as e:
        print(f"Erro na inserção: {e}")
    finally:
        if conexao.is_connected():
            cursor.close()
            conexao.close()

if __name__ == "__main__":
    testar_insercao() 