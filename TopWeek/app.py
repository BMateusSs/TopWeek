from flask import Flask, jsonify, request


from get_top5_album_home import get_top5_album_home
from get_top5_track_home import get_top5_track_home
from get_top_albuns import get_top_albuns
from get_top_tracks import get_top_tracks


app = Flask(__name__)

@app.route('/top5_album_home', methods=['GET'])
def top5_album_home():
    albuns = get_top5_album_home(1)

    dados = []
    for album in albuns:
        dados.append({
            'type': 'album',
            'album_name': album[0],
            'artist': album[1],
            'rank_position': album[2],
            'last_week': album[3],
            'total_weeks': album[4],
            'album_cover': album[5]
        })
    
    return jsonify(dados)

@app.route('/top5_track_home', methods=['GET'])
def top5_track_home():
    tracks = get_top5_track_home(1)

    dados = []
    for track in tracks:
        dados.append({
            'type': 'track',
            'track_name': track[0],
            'artist': track[1],
            'rank_position': track[2],
            'last_week': track[3],
            'total_weeks': track[4],
            'cover_track': track[5]
        })
    
    return jsonify(dados)

@app.route('/top_albuns', methods=['GET'])
def top_albuns():
    albuns = get_top_albuns(1)

    dados = []
    for album in albuns:
        dados.append({
            'type': 'album',
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

@app.route('/top_tracks', methods=['GET'])
def top_tracks():
    tracks = get_top_tracks(1)

    dados = []
    for track in tracks:
        dados.append({
            'type': 'track',
            'track_name': track[0],
            'artist': track[1],
            'rank_position': track[2],
            'last_week': track[3],
            'total_weeks': track[4],
            'cover_track': track[5],
            'peak_position': track[6],
            'weeks_on_peak': track[7],
            'playcount': track[8]
        })
    
    return jsonify(dados)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
