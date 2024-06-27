import discord
from discord.ext import commands

class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, num_messages: int = 1):
        deleted = await ctx.channel.purge(limit=num_messages + 1)  # +1 per includere il comando stesso
        await ctx.send(f'Ho cancellato {len(deleted) - 1} messaggi.', delete_after=5)

async def setup(bot):
    await bot.add_cog(Clear(bot))
