import discord
from discord.ext import commands
from collections import defaultdict
import datetime

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warnings = {}


    #Kick
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.message.delete()

        log_channel_name = 'sanzioni'
        log_channel = discord.utils.get(ctx.guild.text_channels, name=log_channel_name)
        if log_channel:
            embed = discord.Embed(
                title="Utente Kickato",
                description=f"{member.mention} è stato kickato da {ctx.author.mention}.\n ```Motivo: {reason}```",
                color=discord.Color.orange()
            )
            await log_channel.send(embed=embed)


    #Ban
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.message.delete()

        log_channel_name = 'sanzioni'
        log_channel = discord.utils.get(ctx.guild.text_channels, name=log_channel_name)
        if log_channel:
            embed = discord.Embed(
                title="Utente Bannato",
                description=f"{member.mention} è stato bannato da {ctx.author.mention}.\n ```Motivo: {reason}```",
                color=discord.Color.red()
            )
            await log_channel.send(embed=embed)


    #UnBan
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: int, *, reason=None):
        user = await self.bot.fetch_user(user_id)
        await ctx.guild.unban(user, reason=reason)
        await ctx.message.delete()

        log_channel_name = 'sanzioni'
        log_channel = discord.utils.get(ctx.guild.text_channels, name=log_channel_name)
        if log_channel:
            embed = discord.Embed(
                title="Utente sbannato",
                description=f"{user.mention} è stato sbannato da {ctx.author.mention}.\n ```Motivo: {reason}```",
                color=discord.Color.green()
            )
            await log_channel.send(embed=embed)

    
    #Warn
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        if member.id not in self.warnings:
            self.warnings[member.id] = []
        await ctx.message.delete()
        # Dettagli del warning
        warning_details = {
            "reason": reason,
            "issued_by": ctx.author.name,
            "time": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.warnings[member.id].append(warning_details)
        embed = discord.Embed(
            title = "Avvertimento",
            description= f"L'utente {member.mention} ha ricevuto un avvertimento\n ```Motivo: {reason}```",
            color = discord.Color.yellow()
        )

        log_channel_name = 'sanzioni'
        log_channel = discord.utils.get(ctx.guild.text_channels, name=log_channel_name)
        
        await log_channel.send(embed=embed)
        
        if len(self.warnings[member.id]) >= 3:
            await member.kick(reason="Ha ricevuto 3 avvertimenti.")
            log_channel_name = 'sanzioni'
            log_channel = discord.utils.get(ctx.guild.text_channels, name=log_channel_name)

            embed = discord.Embed(
                title="Utente Kickato",
                description=f"{member.mention} è stato kickato da {ctx.author.mention}. Motivo: Ha ricevuto 3 warn",
                color=discord.Color.orange()
            )
            await log_channel.send(embed=embed)


    #WarnList
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def warnlist(self,ctx, member: discord.Member):
        if member.id in self.warnings and self.warnings[member.id]:
            embed = discord.Embed(
                title=f"Lista avvertimenti per {member.display_name}",
                description=f"Totale avvertimenti: {len(self.warnings[member.id])}",
                color=discord.Color.orange()
            )
            
            for i, warning in enumerate(self.warnings[member.id], 1):
                embed.add_field(
                    name=f"Avvertimento {i}",
                    value=f"Motivo: {warning['reason']}\nEmesso da: {warning['issued_by']}\nData: {warning['time']}",
                    inline=False
                )
            
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{member.mention} non ha nessun avvertimento.")

    #Report
    @commands.command()
    async def report(self, ctx, member: discord.Member, reason = None):
        await ctx.message.delete()
        log_channel_name = "report"
        log_channel = discord.utils.get(ctx.guild.text_channels, name=log_channel_name)

        embed = discord.Embed(
            title = "Report",
            description= f"L'utente {member.mention} è stato segnalato da {ctx.message}. ```Motivo: {reason}```",
            color = discord.Color.dark_red()
        )

        await log_channel.send(embed = embed)


    @commands.Cog.listener()
    async def on_message(self, message):
        self.spam_count = defaultdict(lambda: defaultdict(int))
        self.MAX_MESSAGES = 5  # Numero massimo di messaggi consentiti
        self.TIMEFRAME = 10  # Intervallo di tempo in secondi per il limite di spam
    
        if message.author == self.bot.user:
            return  # Ignora i messaggi del bot stesso

        author_id = message.author.id
        current_time = datetime.datetime.utcnow()

        if author_id not in self.spam_count:
            self.spam_count[author_id] = defaultdict(int)

        if self.spam_count[author_id]['last_message_time']:
            delta = current_time - self.spam_count[author_id]['last_message_time']
            if delta.total_seconds() <= self.TIMEFRAME:
                self.spam_count[author_id]['count'] += 1
            else:
                self.spam_count[author_id]['count'] = 1
        else:
            self.spam_count[author_id]['count'] = 1

        self.spam_count[author_id]['last_message_time'] = current_time

        if self.spam_count[author_id]['count'] > self.MAX_MESSAGES:
            # Eseguire azioni anti-spam
            await message.delete()
            fake_ctx = await self.bot.get_context(message)
            await self.moderation_cog.warn(fake_ctx, message.author, reason="Spam")


async def setup(bot):
    await bot.add_cog(Moderation(bot))
