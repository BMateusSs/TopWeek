from flask import Flask, jsonify, request


from get_top5_album_home import get_top5_album_home

from get_top_albuns import get_top_albuns


app = Flask(__name__)

@app.route('/top5_album_home', methods=['GET'])
def top5_album_home():
    albuns = get_top5_album_home(1)

    dados = []
    for album in albuns:
        dados.append({
            'album_name': album[0],
            'artist': album[1],
            'rank_position': album[2],
            'last_week': album[3],
            'total_weeks': album[4],
            'album_cover': album[5]
        })
    
    return jsonify(dados)

@app.route('/top_albuns', methods=['GET'])
def top_albuns():
    albuns = get_top_albuns(1)

    dados = []
    for album in albuns:
        dados.append({
            'album_name': album[0],
            'artist': album[1],
            'rank_position': album[2],
            'last_week': album[3],
            'total_weeks': album[4],
            'album_cover': album[5],
            'peak_position': album[6],
            'weeks_on_peak': album[7],
            'playcount': album[8]
        })
    
    return jsonify(dados)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
