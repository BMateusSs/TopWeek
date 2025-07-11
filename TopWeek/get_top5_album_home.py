from connection_db import fazer_conexao

def get_top5_album_home(user):
    conexao = fazer_conexao()
    cursor = conexao.cursor()

    sql = '''
    WITH semana_atual AS (
    SELECT 
        wai.album_name, 
        wai.artist_name, 
        wai.playcount,
        wai.album_cover,
        ROW_NUMBER() OVER (ORDER BY wai.playcount DESC, wai.album_name) AS current_rank
    FROM weekly_chart_metadata wcm
    LEFT JOIN weekly_album_items wai ON wai.chart_metadata_id = wcm.id
    WHERE wcm.start_date = (SELECT MAX(start_date) FROM weekly_chart_metadata)
    AND wcm.user_id = %s
),

-- Ranking da semana anterior
    semana_passada AS (
        SELECT 
            wai.album_name, 
            wai.artist_name,
            ROW_NUMBER() OVER (ORDER BY wai.playcount DESC, wai.album_name) AS last_week_rank
        FROM weekly_chart_metadata wcm
        LEFT JOIN weekly_album_items wai ON wai.chart_metadata_id = wcm.id
        WHERE wcm.start_date = (
            SELECT MAX(start_date) - INTERVAL 7 DAY FROM weekly_chart_metadata
        )
        AND wcm.user_id = %s
    ),

    -- Total de semanas que o álbum apareceu
    total_semanas_album AS (
        SELECT 
            wai.album_name,
            wai.artist_name,
            COUNT(DISTINCT wcm.start_date) AS total_weeks
        FROM weekly_album_items wai
        JOIN weekly_chart_metadata wcm ON wai.chart_metadata_id = wcm.id
        WHERE wcm.user_id = %s
        GROUP BY wai.album_name, wai.artist_name
    )

    -- Consulta final com tudo
    SELECT 
        sa.album_name,
        sa.artist_name,
        sa.current_rank,
        sp.last_week_rank,
        ts.total_weeks,
        sa.album_cover
    FROM semana_atual sa
    LEFT JOIN semana_passada sp
        ON sa.album_name = sp.album_name
        AND sa.artist_name = sp.artist_name
    LEFT JOIN total_semanas_album ts
        ON sa.album_name = ts.album_name
        AND sa.artist_name = ts.artist_name
    ORDER BY sa.current_rank
    LIMIT 5;
    '''
    cursor.execute(sql, (user, user, user,))
    dados = cursor.fetchall()
    conexao.close()

    return dados
