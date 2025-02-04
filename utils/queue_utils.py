import asyncio
from collections import deque
from discord import FFmpegPCMAudio

current_song = {}  # Diccionario para almacenar la canción actual por guild_id
queues = {}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

def get_guild_queue(guild_id):
    if guild_id not in queues:
        queues[guild_id] = deque()
    return queues[guild_id]


def play_next(ctx):
    queue = get_guild_queue(ctx.guild.id)
    if not queue:
        current_song.pop(ctx.guild.id, None)  # Elimina la canción actual si la cola está vacía
        return

    song = queue.popleft()
    print(f'play_next -> song: {song}')
    current_song[ctx.guild.id] = song  # Almacena la canción actual
    source = FFmpegPCMAudio(song['source'], **FFMPEG_OPTIONS)
    ctx.voice_client.play(
        source,
        after=lambda e: play_next(ctx)
    )
    asyncio.run_coroutine_threadsafe(
        ctx.send(f'🎵 Reproduciendo ahora: {song["title"]}'),
        ctx.bot.loop,
    )