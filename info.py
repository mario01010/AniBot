import discord
from discord.ext import commands

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Info server
    @commands.command()
    async def info(self, ctx):
        try:
            await ctx.message.delete()
        except discord.errors.NotFound:
            pass

        server = ctx.guild
        num_channels = len(server.channels)
        num_members = server.member_count
        server_owner = server.owner

        server_creation_date = server.created_at.strftime("%d-%m-%Y")

        # Costruisci l'embed per il messaggio decorato
        embed = discord.Embed(title=f"ℹ️ Informazioni su {server.name}", color=discord.Color.blue())
        embed.add_field(name="🔹 Nome del Server", value=server.name, inline=False)
        embed.add_field(name="💻 Data do creazione", value=server_creation_date, inline=False)
        embed.add_field(name="👥 Numero di Membri", value=num_members, inline=False)
        embed.add_field(name="👑 Proprietario del Server", value=server_owner, inline=False)
        await ctx.send(embed=embed)

    # Info bot
    @commands.command()
    async def botinfo(self, ctx):
        try:
            await ctx.message.delete()
        except discord.errors.NotFound:
            pass


        creator_id = "860170106804764702"
        creator = await self.bot.fetch_user(creator_id)
        num_guilds = len(self.bot.guilds)
        bot_avatar_url = self.bot.user.avatar.url if self.bot.user.avatar else None
        
        embed = discord.Embed(title=f"ℹ️ Informazioni su {self.bot.user.name}", 
                            color=discord.Color.blue()
                            )
        
        embed.add_field(name="🔹 Nome del Bot", value=self.bot.user.name, inline=False)
        embed.add_field(name="🆔 ID del Bot", value=self.bot.user.id, inline=False)
        embed.add_field(name="👤 Creatore", value=creator, inline=False)
        embed.add_field(name="🌐 Numero di Server", value=num_guilds, inline=False)
        
        if bot_avatar_url:
            embed.set_thumbnail(url=bot_avatar_url)
        
        await ctx.send(embed=embed)


    @commands.command()
    async def aiuto(self, ctx):


        embed = discord.Embed(
            title="ℹ️ Info comandi",
            color=discord.Color.dark_blue()
        )
        embed.add_field(name="🛠️ Moderazione ", value="Comandi di moderazione della chat.", inline=False)
        embed.add_field(name="!warn [Utente] [Motivo]", value="Avvisa un utente", inline=False)
        embed.add_field(name="!warnlist [Utente]", value="Mostra la lista di avvisi di un utente", inline=False)
        embed.add_field(name="!kick [Utente] [Motivo]", value="Espelle un utente dal server", inline=False)
        embed.add_field(name="!ban [Utente] [Motivo]", value="Banna un utente dal server", inline=False)
        embed.add_field(name="!unban [Utente]", value="Rimuove il ban di un utente bannato dal server", inline=False)
        embed.add_field(name="!clear [Numero]", value="Cancella un numero di messaggi specifico", inline=False)
        
        embed.add_field(name="🛡️ Gestione Ruoli", value="Comandi per gestire il grado degli utenti.", inline=False)
        embed.add_field(name="!pex [Utente] [Quantità]", value="Aumenta il grado ad un utente", inline=False)
        embed.add_field(name="!depex [Utente] [Quantità]", value="Diminuisce il grado ad un utente", inline=False)
        
        embed.add_field(name="⚙️ Utility", value="Comandi utili per suggerimenti, bug e altro.", inline=False)
        embed.add_field(name="!suggest [Suggerimento]", value="Invia un suggerimento al server", inline=False)
        embed.add_field(name="!bug [Descrizione del Bug]", value="Reporta un bug", inline=False)
        embed.add_field(name="!annuncio [Annuncio]", value="Crea un annuncio custom", inline=False)
        embed.add_field(name="!setrules", value="Crea regole custom", inline=False)
        embed.add_field(name="!web", value="Vedi il sito web ufficiale del server", inline=False)
        
        embed.add_field(name="ℹ️ Informazioni", value="Comandi per ottenere informazioni.", inline=False)
        embed.add_field(name="!info", value="Mostra informazioni generali sul server", inline=False)
        embed.add_field(name="!botinfo", value="Mostra informazioni generali di AniBot", inline=False)
        embed.add_field(name="!userinfo [Utente]", value="Mostra informazione generali su un utente", inline=False)
        
        embed.add_field(name="⛔ Segnalazioni", value="Comandi per segnalare utenti ai moderatori.", inline=False)
        embed.add_field(name="!report [Utente] [Motivo]", value="Segnala un utente agli amministratori", inline=False)

        await ctx.send(embed=embed)


    #userinfo
    
    @commands.command()
    async def userinfo(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        await ctx.message.delete()

        embed = discord.Embed(
            title=f"Informazioni su {member.display_name}",
            color=discord.Color.blurple(),
            timestamp=ctx.message.created_at
        )

        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="🆔 ID Utente", value=member.id, inline=True)
        embed.add_field(name="👤 Nome", value=member.display_name, inline=True)
        embed.add_field(name="🪪 Account creato il", value=member.created_at.strftime("%d-%m-%Y"), inline=False)
        embed.add_field(name="🚪 Entrato nel server il", value=member.joined_at.strftime("%d-%m-%Y"), inline=True)
        embed.add_field(name="⚙️ Ruoli", value=", ".join([role.name for role in member.roles if role.name != "@everyone"]), inline=True)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Info(bot))
