import requests
import subprocess
import os

# Configurações
UNSPLASH_ACCESS_KEY = os.environ.get('UNSPLASH_KEY')
VIDEO_QUERY = "nature technology city abstract" # Tópicos populares
OUTPUT_FILENAME = "final_video.mp4"

def download_unsplash_video():
    """Baixa um vídeo aleatório do Unsplash."""
    url = f"https://api.unsplash.com/videos/random?query={VIDEO_QUERY}&per_page=1"
    headers = {"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if 'video_files' in data and len(data['video_files']) > 0:
            # Escolhe o vídeo com melhor qualidade disponível
            videos = data['video_files']
            # Filtra para ter pelo menos 720p se possível
            for v in videos:
                if v.get('width', 0) >= 1280:
                    return v['link']
            # Se não houver HD, devolve o primeiro disponível
            return videos[0]['link']
        else:
            print("Nenhum vídeo encontrado.")
            return None
            
    except Exception as e:
        print(f"Erro ao aceder Unsplash: {e}")
        return None

def generate_audio():
    """Gera áudio usando TTS simples (Google Translate TTS gratuito)."""
    from gtts import gTTS
    text = "Esta é uma automação feita com código aberto. O futuro é agora."
    tts = gTTS(text)
    tts.save("audio.mp3")
    return "audio.mp3"

def merge_videos_and_audio(video_url, audio_file):
    """Junta vídeo e áudio usando FFmpeg."""
    video_name = "input_video.mp4"
    
    # 1. Download do vídeo
    print("A descarregar vídeo...")
    with open(video_name, 'wb') as f:
        f.write(requests.get(video_url).content)
        
    # 2. Verificar se o áudio existe
    if not os.path.exists(audio_file):
        raise FileNotFoundError("Ficheiro de áudio não encontrado.")

    # 3. Usar FFmpeg para juntar
    command = [
        "ffmpeg", 
        "-y", 
        "-i", video_name, 
        "-i", audio_file, 
        "-c:v", "copy", 
        "-c:a", "aac", 
        "-strict", "experimental", 
        OUTPUT_FILENAME
    ]
    
    subprocess.run(command, check=True)
    print(f"Sucesso! Vídeo guardado como '{OUTPUT_FILENAME}'")

if __name__ == "__main__":
    print("Iniciando geração de vídeo...")
    
    # Obter vídeo
    video_link = download_unsplash_video()
    if not video_link:
        exit(1)
        
    # Gerar áudio
    audio_path = generate_audio()
    
    # Juntar tudo
    merge_videos_and_audio(video_link, audio_path)
    
    # Limpeza básica
    os.remove("input_video.mp4")
    os.remove("audio.mp3")
    print("Processo concluído!")
