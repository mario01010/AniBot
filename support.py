import discord
from discord.ext import commands

class Support(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #uggerimenti
    @commands.command()
    async def suggest(self, ctx, *, suggest=None):
        await ctx.message.delete()

        embed = discord.Embed(
            title= f"🔵 Suggerimento di {ctx.message.author.display_name}",
            description= f"Consiglia: ```{suggest}```",
            color=discord.Color.blue()
        )

        channel_name = "suggerimenti"
        
        # Ottenere il canale
        channel = discord.utils.get(ctx.guild.text_channels, name=channel_name)

        if channel:
            await channel.send(embed=embed)
        else:
            await ctx.send(f"Canale '{channel_name}' non trovato.")


    #Bug report
    @commands.command()
    async def bug(self, ctx, *, bug = None):
        await ctx.message.delete()

        embed = discord.Embed(
            title = f"🤖 Bug report di {ctx.message.author.display_name}",
            description= f"Segnala: ```{bug}```",
            color = discord.Color.orange()
        )

        channel_name = "bug-report"
        channel = discord.utils.get(ctx.guild.text_channels, name = channel_name)

        if channel:
            await channel.send(embed = embed)

        else:
            ctx.send(f"Canale '{channel_name}' non trovato.")


    @commands.command()
    async def web(self, ctx):
        await ctx.message.delete()

        embed = discord.Embed(
            title = "🛜 Sito Web",
            description= "Coming soon...",
            color= discord.Color.orange()
        )

        await ctx.send(embed = embed)


async def setup(bot):
    await bot.add_cog(Support(bot))
