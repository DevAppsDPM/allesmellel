import asyncio

from utils.audio_utils import fetch_audio_data, search_youtube, format_duration
from utils.queue_utils import get_guild_queue, play_next

def setup_play_command(bot):
    @bot.command(name='play', help='Reproduce una canción desde un enlace de YouTube o busca una canción por nombre.')
    async def play(ctx, *, query: str):
        voice_channel = ctx.author.voice.channel
        if not voice_channel:
            await ctx.send('¡Debes estar en un canal de voz para usar este comando! 🤨')
            return

        queue = get_guild_queue(ctx.guild.id)

        if not query.startswith('http'):
            # Si no es un enlace, busca en YouTube
            await ctx.send(f'🔍 Buscando "{query}" en YouTube...')
            results = await search_youtube(query)

            if not results:
                await ctx.send('❌ No se encontraron resultados.')
                return

            # Mostrar opciones al usuario
            options = '\n'.join([f"{i + 1}. {result['title']} ({format_duration(result['duration'])})" for i, result in enumerate(results)])
            await ctx.send(f'🎵 Elige una opción escribiendo el número:\n{options}')

            def check(m):
                return m.author == ctx.author and m.content.isdigit() and 1 <= int(m.content) <= len(results)

            try:
                msg = await bot.wait_for('message', timeout=30.0, check=check)
                choice = int(msg.content) - 1
                song = await fetch_audio_data(results[choice]['url'])
            except asyncio.TimeoutError:
                await ctx.send('⏳ No elegiste una opción a tiempo.')
                return
        else:
            # Si es un enlace, procesarlo directamente
            await ctx.send('🔄 Procesando el enlace...')
            song = await fetch_audio_data(query)

        # Añadir canción a la cola
        queue.append({
            'source': song['url'],
            'title': song.get('title', 'Desconocido'),
        })
        await ctx.send(f'🎶 Añadido a la cola: {song["title"]}')

        # Iniciar reproducción si no está reproduciendo nada
        if not ctx.voice_client:
            vc = await voice_channel.connect()
            play_next(ctx)
        elif not ctx.voice_client.is_playing():
            play_next(ctx)
