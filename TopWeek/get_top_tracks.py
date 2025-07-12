from connection_db import fazer_conexao

def get_top_tracks(user):
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
),

-- Melhor posição alcançada (peak_position)
peak_position AS (
    SELECT 
        t.track_name,
        t.artist_name,
        MIN(t.rn) AS peak_position
    FROM (
        SELECT
            wti.track_name,
            wti.artist_name,
            wcm.start_date,
            ROW_NUMBER() OVER (PARTITION BY wcm.start_date ORDER BY wti.playcount DESC, wti.track_name) AS rn
        FROM weekly_track_items wti
        JOIN weekly_chart_metadata wcm ON wti.chart_metadata_id = wcm.id
        WHERE wcm.user_id = %s
    ) t
    GROUP BY t.track_name, t.artist_name
),

-- Total de semanas no pico (weeks_on_peak)
weeks_on_peak AS (
    SELECT 
        t.track_name,
        t.artist_name,
        COUNT(DISTINCT t.start_date) AS weeks_on_peak
    FROM (
        SELECT
            wti.track_name,
            wti.artist_name,
            wcm.start_date,
            ROW_NUMBER() OVER (PARTITION BY wcm.start_date ORDER BY wti.playcount DESC, wti.track_name) AS rn
        FROM weekly_track_items wti
        JOIN weekly_chart_metadata wcm ON wti.chart_metadata_id = wcm.id
        WHERE wcm.user_id = %s
    ) t
    JOIN (
        SELECT 
            t2.track_name, 
            t2.artist_name, 
            MIN(t2.rn) AS peak_position
        FROM (
            SELECT
                wti2.track_name,
                wti2.artist_name,
                wcm2.start_date,
                ROW_NUMBER() OVER (PARTITION BY wcm2.start_date ORDER BY wti2.playcount DESC, wti2.track_name) AS rn
            FROM weekly_track_items wti2
            JOIN weekly_chart_metadata wcm2 ON wti2.chart_metadata_id = wcm2.id
            WHERE wcm2.user_id = %s
        ) t2
        GROUP BY t2.track_name, t2.artist_name
    ) p ON t.track_name = p.track_name AND t.artist_name = p.artist_name
    WHERE t.rn = p.peak_position
    GROUP BY t.track_name, t.artist_name
)

-- Consulta final com tudo
SELECT 
    sa.track_name,
    sa.artist_name,
    sa.current_rank,
    sp.last_week_rank,
    ts.total_weeks,
    sa.cover_track,
    pp.peak_position,
    wp.weeks_on_peak,
    sa.playcount
    
FROM semana_atual sa
LEFT JOIN semana_passada sp
    ON sa.track_name = sp.track_name
    AND sa.artist_name = sp.artist_name
LEFT JOIN total_semanas_track ts
    ON sa.track_name = ts.track_name
    AND sa.artist_name = ts.artist_name
LEFT JOIN peak_position pp
    ON sa.track_name = pp.track_name
    AND sa.artist_name = pp.artist_name
LEFT JOIN weeks_on_peak wp
    ON sa.track_name = wp.track_name
    AND sa.artist_name = wp.artist_name
ORDER BY sa.current_rank;
    '''
    cursor.execute(sql, (user, user, user, user, user, user))
    dados = cursor.fetchall()
    conexao.close()

    return dados 