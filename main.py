Flask backend to convert YouTube to MP3 and serve as download
from flask import Flask, request, send_file
from yt_dlp import YoutubeDL
import os
import uuid

app = Flask(__name__)

@app.route("/")
def home():
    return "YouTube MP3 Downloader Backend is Running"

@app.route("/download", methods=["GET"])
def download():
    url = request.args.get("url")
    if not url:
        return "Missing URL", 400

    temp_id = str(uuid.uuid4())
    output_path = f"/tmp/{temp_id}.mp3"

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
        except Exception as e:
            return f"Error: {e}", 500

    return send_file(output_path, as_attachment=True, download_name="music.mp3")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
