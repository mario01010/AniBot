import discord
from discord.ext import commands

class JoinEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Assegnazione ruolo "utente" e messaggio di benvenuto
    @commands.Cog.listener()
    async def on_member_join(self, member):
        role_name = "utente"  # Nome del ruolo che vuoi assegnare
        role = discord.utils.get(member.guild.roles, name=role_name)
        if role:
            await member.add_roles(role)
            print(f"Ruolo {role_name} assegnato a {member.name}")

        welcome_channel_name = 'benvenuto'  # Nome del canale di benvenuto
        welcome_channel = discord.utils.get(member.guild.text_channels, name=welcome_channel_name)
        if welcome_channel:
            await welcome_channel.send(f"Benvenuto {member.mention} nel server!")

async def setup(bot):
    await bot.add_cog(JoinEvent(bot))  # Aggiungi await qui per chiamare correttamente la funzione asincrona

