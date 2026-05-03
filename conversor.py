from flask import Flask, request, send_file
import yt_dlp

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]

        opcoes = {
            "format": "bestaudio/best",
            "outtmpl": "audio.%(ext)s",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }

        with yt_dlp.YoutubeDL(opcoes) as ydl:
            ydl.download([url])

        return send_file("audio.mp3", as_attachment=True)

    return """
    <h1>Conversor Online para MP3</h1>
    <form method="post">
        <input name="url" placeholder="Cole o link aqui" style="width:350px;padding:10px;">
        <button type="submit">Converter</button>
    </form>
    <p>Use apenas vídeos próprios, livres ou com autorização.</p>
    """
