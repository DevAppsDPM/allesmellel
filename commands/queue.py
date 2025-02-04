from utils.queue_utils import get_guild_queue, current_song


def setup_queue_command(bot):
    @bot.command(name='queue', help='Muestra las canciones en la cola.')
    async def show_queue(ctx):
        current = current_song.get(ctx.guild.id)
        queue = get_guild_queue(ctx.guild.id)
        if not queue and not current:
            await ctx.send('La cola está vacía.')
        else:
            queue_list = '\n'.join([f"{i + 1}. {song['title']}" for i, song in enumerate(queue)])
            await ctx.send(f'▶ Sonando: {current["title"]}\n📜 Cola de reproducción:\n{queue_list}')
