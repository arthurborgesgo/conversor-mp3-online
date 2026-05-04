from flask import Flask, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")

        if not url:
            return "Cole um link válido"

        try:
            # Remove arquivo antigo se existir
            if os.path.exists("audio.mp3"):
                os.remove("audio.mp3")

            opcoes = {
                "format": "bestaudio/best",
                "outtmpl": "audio.%(ext)s",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
                "quiet": True
            }

            with yt_dlp.YoutubeDL(opcoes) as ydl:
                ydl.download([url])

            if os.path.exists("audio.mp3"):
                return send_file("audio.mp3", as_attachment=True)

            return "Erro ao gerar MP3"

        except Exception as e:
            return f"Erro: {str(e)}"

    return """
    <h1>Conversor Online para MP3</h1>
    <form method="post">
        <input name="url" placeholder="Cole o link aqui" style="width:350px;padding:10px;">
        <button type="submit">Converter</button>
    </form>
    <p>Use apenas vídeos próprios, livres ou com autorização.</p>
    """

if __name__ == "__main__":
    app.run(debug=True)
