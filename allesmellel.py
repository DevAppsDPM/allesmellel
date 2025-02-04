import discord
from discord.ext import commands
from config import TOKEN
from commands import load_commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅  Bot listo como {bot.user}!')

# Cargar todos los comandos
load_commands(bot)

bot.run(TOKEN)
