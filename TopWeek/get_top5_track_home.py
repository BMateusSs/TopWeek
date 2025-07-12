from connection_db import fazer_conexao

def get_top5_track_home(user):
    conexao = fazer_conexao()
    cursor = conexao.cursor()

    sql = '''
    WITH semana_atual AS (
    SELECT 
        wti.track_name, 
        wti.artist_name, 
        wti.playcount,
        wti.cover_track,
        ROW_NUMBER() OVER (ORDER BY wti.playcount DESC, wti.track_name) AS current_rank
    FROM weekly_chart_metadata wcm
    LEFT JOIN weekly_track_items wti ON wti.chart_metadata_id = wcm.id
    WHERE wcm.start_date = (SELECT MAX(start_date) FROM weekly_chart_metadata)
    AND wcm.user_id = %s
),

-- Ranking da semana anterior
    semana_passada AS (
        SELECT 
            wti.track_name, 
            wti.artist_name,
            ROW_NUMBER() OVER (ORDER BY wti.playcount DESC, wti.track_name) AS last_week_rank
        FROM weekly_chart_metadata wcm
        LEFT JOIN weekly_track_items wti ON wti.chart_metadata_id = wcm.id
        WHERE wcm.start_date = (
            SELECT MAX(start_date) - INTERVAL 7 DAY FROM weekly_chart_metadata
        )
        AND wcm.user_id = %s
    ),

    -- Total de semanas que a track apareceu
    total_semanas_track AS (
        SELECT 
            wti.track_name,
            wti.artist_name,
            COUNT(DISTINCT wcm.start_date) AS total_weeks
        FROM weekly_track_items wti
        JOIN weekly_chart_metadata wcm ON wti.chart_metadata_id = wcm.id
        WHERE wcm.user_id = %s
        GROUP BY wti.track_name, wti.artist_name
    )

    -- Consulta final com tudo
    SELECT 
        sa.track_name,
        sa.artist_name,
        sa.current_rank,
        sp.last_week_rank,
        ts.total_weeks,
        sa.cover_track
    FROM semana_atual sa
    LEFT JOIN semana_passada sp
        ON sa.track_name = sp.track_name
        AND sa.artist_name = sp.artist_name
    LEFT JOIN total_semanas_track ts
        ON sa.track_name = ts.track_name
        AND sa.artist_name = ts.artist_name
    ORDER BY sa.current_rank
    LIMIT 5;
    '''
    cursor.execute(sql, (user, user, user,))
    dados = cursor.fetchall()
    conexao.close()

    return dados 