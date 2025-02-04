def setup_leave_command(bot):
    @bot.command(name='leave', help='Desconecta el bot del canal de voz.')
    async def leave(ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send('👋 ¡Chao chao chao...!')
        else:
            await ctx.send('No estoy en un canal de voz.')
