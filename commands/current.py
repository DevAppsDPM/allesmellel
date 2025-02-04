from utils.queue_utils import current_song

def setup_current_command(bot):
    @bot.command(name='current', help='Muestra la canción que se está reproduciendo actualmente.')
    async def current(ctx):
        song = current_song.get(ctx.guild.id)
        if not song:
            await ctx.send('⏹ No hay ninguna canción reproduciéndose.')
        else:
            await ctx.send(f'▶ Actualmente reproduciendo: {song["title"]} 🎵')
