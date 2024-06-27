import discord
from discord.ext import commands

class ModEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.paroleNO = [
            "Banned words"
        ]
        
    @commands.Cog.listener()
    async def on_message(self, message):
        # Controlla che il messaggio non sia stato inviato dal bot stesso
        if message.author == self.bot.user:
            return

        contenuto_messaggio = message.content.lower()  # Converti il contenuto del messaggio in minuscolo
        
        # Controlla se il messaggio contiene una parola non valida
        for parola in self.paroleNO:
            if parola in contenuto_messaggio:
                # Cancella il messaggio dell'utente
                await message.delete()

                embed = discord.Embed(
                    title="⚠️ Avviso ⚠️",
                    description=f"Ciao {message.author.name}, la parola che hai usato non è permessa. Ti chiediamo cortesemente di usare un linguaggio consono al server per non incorrere in sanzioni. Grazie, cordiali saluti, AniBot.",
                    color=discord.Color.red()
                )

                # Invia un messaggio privato all'utente
                try:
                    await message.author.send(embed=embed)
                except discord.Forbidden:
                    print(f"Impossibile inviare un messaggio privato a {message.author.name}.")

                guild = message.guild
                log_message = (
                    f"Autore: {message.author.name} ({message.author.id})\n"
                    f"Contenuto: {message.content}\n"
                    f"Canale: {message.channel.name} ({message.channel.id})\n"
                    f"Server: {guild.name} ({guild.id})"
                )
                
                # Log
                log_channel_name = 'log' 
                log_embed = discord.Embed(
                    title="⚠️ Avviso ⚠️",
                    description=f"L'utente {message.author.name} ha usato una parola non consentita nel server {guild.name}. \n```{log_message}```",
                    color=discord.Color.red()
                )

                log_channel = discord.utils.get(guild.text_channels, name=log_channel_name)
                if log_channel:
                    try:
                        await log_channel.send(embed=log_embed)
                    except discord.Forbidden:
                        print(f"Impossibile inviare un avviso al canale di log {log_channel.name}.")
                break

async def setup(bot):
    await bot.add_cog(ModEvent(bot))
