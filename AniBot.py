import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import datetime
import os
import asyncio

# Configura gli intents necessari
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Abilita l'intento per i membri

# Crea un'istanza di Bot
bot = commands.Bot(command_prefix='!', intents=intents)

# Evento che viene chiamato quando il bot è pronto
@bot.event
async def on_ready():
    print(f'Bot connesso come {bot.user}')
    # Carica le estensioni
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'Estensione {filename} caricata con successo.')
            except Exception as e:
                print(f'Errore nel caricamento dell\'estensione {filename}: {e}')
                


# Comandi segreti
@bot.command()
@commands.has_permissions(administrator=True)
async def pela(ctx):
    await ctx.send("Frocio")

@bot.command()
@commands.has_permissions(administrator=True)
async def carbonara(ctx):
    await ctx.message.delete()
    await ctx.send("Chri <3 Carbo")

@bot.command()
@commands.has_permissions(administrator=True)
async def bestemmia(ctx):
    await ctx.message.delete()
    await ctx.send("Porco Dio")



# Esegui il bot
async def main():
    async with bot:
        await bot.start('TOKEN')

try:
    asyncio.run(main())
except KeyboardInterrupt:
    asyncio.run(bot.close())

