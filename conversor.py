import tkinter as tk
from tkinter import messagebox
import yt_dlp
import os
import sys

# Função para localizar arquivos dentro do .exe
def caminho_recurso(caminho):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, caminho)
    return os.path.join(os.path.abspath("."), caminho)

# Caminho do FFmpeg (vai funcionar dentro do .exe também)
CAMINHO_FFMPEG = caminho_recurso(r"ffmpeg\bin")

def baixar_audio():
    url = entrada_url.get().strip()

    if not url:
        messagebox.showwarning("Aviso", "Cole um link do YouTube!")
        return

    # Verifica FFmpeg
    if not os.path.exists(os.path.join(CAMINHO_FFMPEG, "ffmpeg.exe")):
        messagebox.showerror(
            "FFmpeg não encontrado",
            f"Não achei o ffmpeg.exe em:\n{CAMINHO_FFMPEG}\n\n"
            "Coloque a pasta ffmpeg corretamente."
        )
        return

    try:
        status_label.config(text="Baixando e convertendo...")

        opcoes = {
            "format": "bestaudio/best",
            "outtmpl": "%(title)s.%(ext)s",
            "ffmpeg_location": CAMINHO_FFMPEG,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }

        with yt_dlp.YoutubeDL(opcoes) as ydl:
            ydl.download([url])

        status_label.config(text="Concluído ✅")
        messagebox.showinfo("Sucesso", "MP3 baixado com sucesso!")

    except Exception as e:
        status_label.config(text="Erro ❌")
        messagebox.showerror("Erro", str(e))


# ===== Interface =====
janela = tk.Tk()
janela.title("Conversor YouTube → MP3")
janela.geometry("450x230")

titulo = tk.Label(janela, text="YouTube para MP3", font=("Arial", 16, "bold"))
titulo.pack(pady=15)

entrada_url = tk.Entry(janela, width=55)
entrada_url.pack(pady=5)

botao = tk.Button(janela, text="Baixar MP3", command=baixar_audio)
botao.pack(pady=15)

status_label = tk.Label(janela, text="")
status_label.pack(pady=5)

janela.mainloop()