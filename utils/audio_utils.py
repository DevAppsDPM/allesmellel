import yt_dlp
import asyncio

async def fetch_audio_data(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'default_search': 'auto',
    }
    loop = asyncio.get_event_loop()
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return await loop.run_in_executor(None, lambda: ydl.extract_info(url, download=False))

async def search_youtube(query, max_results=5):
    """Busca en YouTube y devuelve una lista de opciones."""
    ydl_opts = {
        'quiet': True,
        'default_search': 'ytsearch',
        'noplaylist': True,
        'max_downloads': max_results,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        results = ydl.extract_info(query, download=False)['entries']
        return [
            {
                'title': entry.get('title', 'Desconocido'),
                'url': entry.get('webpage_url'),
                'duration': entry.get('duration', 0),
            }
            for entry in results[:max_results]
        ]

def format_duration(seconds):
    """Convierte la duración en segundos a un formato mm:ss."""
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes}:{seconds:02}"