from flask import Flask

app = Flask(__name__)

@app.route('/')
def top5_album_home():
    return 'Home'


if __name__ == '__main__':
    app.run(debug=True)
