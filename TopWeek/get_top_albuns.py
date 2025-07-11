from connection_db import fazer_conexao

def get_top_albuns(user):
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
),

-- Melhor posição alcançada (peak_position)
peak_position AS (
    SELECT 
        t.album_name,
        t.artist_name,
        MIN(t.rn) AS peak_position
    FROM (
        SELECT
            wai.album_name,
            wai.artist_name,
            wcm.start_date,
            ROW_NUMBER() OVER (PARTITION BY wcm.start_date ORDER BY wai.playcount DESC, wai.album_name) AS rn
        FROM weekly_album_items wai
        JOIN weekly_chart_metadata wcm ON wai.chart_metadata_id = wcm.id
        WHERE wcm.user_id = %s
    ) t
    GROUP BY t.album_name, t.artist_name
),

-- Total de semanas no pico (weeks_on_peak)
weeks_on_peak AS (
    SELECT 
        t.album_name,
        t.artist_name,
        COUNT(DISTINCT t.start_date) AS weeks_on_peak
    FROM (
        SELECT
            wai.album_name,
            wai.artist_name,
            wcm.start_date,
            ROW_NUMBER() OVER (PARTITION BY wcm.start_date ORDER BY wai.playcount DESC, wai.album_name) AS rn
        FROM weekly_album_items wai
        JOIN weekly_chart_metadata wcm ON wai.chart_metadata_id = wcm.id
        WHERE wcm.user_id = %s
    ) t
    JOIN (
        SELECT 
            t2.album_name, 
            t2.artist_name, 
            MIN(t2.rn) AS peak_position
        FROM (
            SELECT
                wai2.album_name,
                wai2.artist_name,
                wcm2.start_date,
                ROW_NUMBER() OVER (PARTITION BY wcm2.start_date ORDER BY wai2.playcount DESC, wai2.album_name) AS rn
            FROM weekly_album_items wai2
            JOIN weekly_chart_metadata wcm2 ON wai2.chart_metadata_id = wcm2.id
            WHERE wcm2.user_id = %s
        ) t2
        GROUP BY t2.album_name, t2.artist_name
    ) p ON t.album_name = p.album_name AND t.artist_name = p.artist_name
    WHERE t.rn = p.peak_position
    GROUP BY t.album_name, t.artist_name
)

-- Consulta final com tudo
SELECT 
    sa.album_name,
    sa.artist_name,
    sa.current_rank,
    sp.last_week_rank,
    ts.total_weeks,
    sa.album_cover,
    pp.peak_position,
    wp.weeks_on_peak,
    sa.playcount
    
FROM semana_atual sa
LEFT JOIN semana_passada sp
    ON sa.album_name = sp.album_name
    AND sa.artist_name = sp.artist_name
LEFT JOIN total_semanas_album ts
    ON sa.album_name = ts.album_name
    AND sa.artist_name = ts.artist_name
LEFT JOIN peak_position pp
    ON sa.album_name = pp.album_name
    AND sa.artist_name = pp.artist_name
LEFT JOIN weeks_on_peak wp
    ON sa.album_name = wp.album_name
    AND sa.artist_name = wp.artist_name
ORDER BY sa.current_rank;
    '''
    cursor.execute(sql, (user, user, user, user, user, user))
    dados = cursor.fetchall()
    conexao.close()

    return dados
