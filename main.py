import os
import sys
import requests
import json
from datetime import datetime, timedelta

from flask import Flask, jsonify, make_response, send_file, send_from_directory
from flask import render_template

app = Flask(__name__, static_folder='files')

@app.route("/")
def hello(name=None):
    responsemusic = requests.get("https://api.deezer.com/track/3135556").json()
    preview = responsemusic["preview"]
    cover = responsemusic["album"]["cover"]
    titlemusic = responsemusic["title"]
    artist = responsemusic["artist"]["name"]
    responseinfo = requests.get("https://newsapi.org/v2/everything?domains=wsj.com&apiKey=378f666235574b82802cb27ae05424eb").json()
    article = responseinfo["articles"][0]
    title = article["title"]
    urltoimage = article["urlToImage"]
    content = article["content"].replace('\r\n', ' $ ')
    url = article["url"]
    return render_template('base.html', title = title, content = content, urltoimage = urltoimage, url = url, cover = cover,artist = artist, titlemusic = titlemusic, preview = preview)



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
