import discord
from discord.ext import commands
import asyncio  # Importa il modulo asyncio per gestire le operazioni asincrone

class Custom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def annuncio(self, ctx, *, annuncio=None):
        await ctx.message.delete()

            # Controlla se è stato fornito un annuncio
        if not annuncio:
            await ctx.send("Utilizzo corretto: !annuncio <annuncio>")
            return

        embed = discord.Embed(
            description=annuncio,
            color=discord.Color.blue()
        )
        await ctx.send(embed = embed)
            

    @commands.command()
    async def setrules(self, ctx):
        await ctx.send("Quante regole vuoi impostare?")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()

        try:
            msg = await self.bot.wait_for('message', check=check, timeout=60.0)
        except asyncio.TimeoutError:
            await ctx.send("Tempo scaduto. Riprova.")
            return

        num_rules = int(msg.content)
        if num_rules <= 0:
            await ctx.send("Il numero di regole deve essere maggiore di zero.")
            return

        rules = []
        for i in range(num_rules):
            await ctx.send(f"Inserisci la regola {i + 1}:")
            try:
                rule_msg = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=120.0)
                rules.append(rule_msg.content)
            except asyncio.TimeoutError:
                await ctx.send(f"Tempo scaduto. Hai inserito fino ad ora le seguenti regole:\n{self.format_rules(rules)}")
                return

        rules_list = self.format_rules(rules)

        embed = discord.Embed(
            title = "📒 Regole Server",
            description= rules_list,
            color = discord.Color.blue()
        )
        await ctx.send(embed = embed)

    def format_rules(self, rules):
        formatted = ""
        for i, rule in enumerate(rules):
            formatted += f"{i + 1}. {rule}\n"
        return formatted

async def setup(bot):
    await bot.add_cog(Custom(bot))
