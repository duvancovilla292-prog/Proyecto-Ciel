import os
import yt_dlp

CARPETA_IMAGENES = os.path.join(os.path.dirname(__file__), 'imagenes')
os.makedirs(CARPETA_IMAGENES, exist_ok=True)

class MiLoggerMudo:
    def debug(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): pass

def descargar_youtube(args, es_audio=False):
    """Descarga video o audio de YouTube usando yt-dlp"""
    if not args:
        return "《✧》Debes proporcionar un enlace de YouTube o el nombre de la canción.", None

    archivo_salida = os.path.join(CARPETA_IMAGENES, 'descarga_yt.mp3' if es_audio else 'descarga_yt.mp4')
    
    if os.path.exists(archivo_salida): 
        os.remove(archivo_salida)

    ydl_opts = {
        'outtmpl': archivo_salida.replace('.mp3', '') if es_audio else archivo_salida,
        'quiet': True,
        'no_warnings': True,
        'logger': MiLoggerMudo()  
    }

    if es_audio:
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
        url_descarga = f"ytsearch1:{args}" if not args.startswith("http") else args
    else:
        ydl_opts.update({'format': 'best[ext=mp4]/best'})
        url_descarga = args

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url_descarga])
        
        nombre_final = 'descarga_yt.mp3' if es_audio else 'descarga_yt.mp4'
        return f"✨ ¡Descarga mística completada con éxito! Aquí tienes", nombre_final
    except Exception as e:
        return f"❌ Error cósmico al procesar la descarga de YouTube: {str(e)}", None


def descargar_tiktok(link, pushName):
    """Descarga videos de TikTok sin marca de agua"""
    if not link or "tiktok.com" not in link:
        return "《✧》Por favor, proporciona un enlace válido de TikTok.", None

    archivo_salida = os.path.join(CARPETA_IMAGENES, 'descarga_tiktok.mp4')
    if os.path.exists(archivo_salida): 
        os.remove(archivo_salida)

    ydl_opts = {
        'outtmpl': archivo_salida,
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'logger': MiLoggerMudo() 
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        return f"👤 *TikTok solicitado por:* {pushName}", "descarga_tiktok.mp4"
    except Exception as e:
        return "❌ No logré extraer ese video de TikTok. Puede que sea privado.", None


def descargar_redes_sociales(link):
    """Descarga videos públicos de Facebook o Instagram Reels"""
    if not link:
        return "《✧》Envía el enlace del video o Reel que deseas descargar.", None

    archivo_salida = os.path.join(CARPETA_IMAGENES, 'descarga_redes.mp4')
    if os.path.exists(archivo_salida): 
        os.remove(archivo_salida)

    ydl_opts = {
        'outtmpl': archivo_salida,
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'logger': MiLoggerMudo()
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        return f"🎥 Aquí tienes tu video solicitado", "descarga_redes.mp4"
    except Exception as e:
        return "❌ Error al descargar de la red social. Verifica que el enlace sea público o válido.", None