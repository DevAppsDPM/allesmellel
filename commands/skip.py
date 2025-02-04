from utils.queue_utils import current_song

def setup_skip_command(bot):
    @bot.command(name='skip', help='Salta la canción actual.')
    async def skip(ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            current_song.pop(ctx.guild.id, None)  # Limpia la canción actual
            ctx.voice_client.stop()
            await ctx.send('⏭ Canción saltada.')
        else:
            await ctx.send('No hay ninguna canción reproduciéndose.')
