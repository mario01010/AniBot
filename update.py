import discord
from discord.ext import commands

class Update(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def update(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(
                title="🌐 Aggiornamento",
            description=(
                "Update Alpha 1.2.0 \n"
                        "(+) Guild system\n"
                        "(+) Quest gioranaliere e settimanali\n"
                        "(+) comando !inventario\n"
                        "(+) Level system (battle)\n"
                        "(-) Boss\n"
                        "(+) Bug Fix\n"
                        "- Ora i comandi delle gilde sono eseguibili solo con i permessi necessari\n"
                        "- Salvataggio degli oggetti ricevuti\n"
                        "- Sistemato utilizzo degli oggetti"
            ),
            color=discord.Color.blue(),
            timestamp=ctx.message.created_at
        )

        # Nome del canale
        channel_name = "changelog"
        
        # Ottenere il canale
        channel = discord.utils.get(ctx.guild.text_channels, name=channel_name)

        if channel:
            await channel.send(embed=embed)
        else:
            await ctx.send(f"Canale '{channel_name}' non trovato.")

    
    @commands.command()
    async def versione(self, ctx):
        embed = discord.Embed(
            title = "🌀 Versione del bot",
            description= "Alpha 1.2.0",
            color = discord.Color.blue()
        )
        await ctx.send(embed = embed)

async def setup(bot):
    await bot.add_cog(Update(bot))
