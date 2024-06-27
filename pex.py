import discord
from discord.ext import commands

class Pex(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    #Comando per pexare
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def pex(self, ctx, member: discord.Member, reason=None):
        role_hierarchy = ["Your roles"]
        # Ottieni i ruoli dell'utente in ordine di priorità
        member_roles = [role.name for role in member.roles]
        await ctx.message.delete()
        # Trova il ruolo attuale dell'utente basato sulla gerarchia
        current_role = None
        for role in role_hierarchy:
            if role in member_roles:
                current_role = role
                break

        if current_role is None:
            await ctx.send(f"{member.mention} non ha nessun ruolo che può essere promosso.")
            return

        # Trova il prossimo ruolo nella gerarchia
        try:
            next_role_index = role_hierarchy.index(current_role) + 1
            next_role_name = role_hierarchy[next_role_index]
        except IndexError:
            await ctx.send(f"{member.mention} ha già il ruolo più alto.")
            return

        # Ottieni l'oggetto del ruolo successivo
        next_role = discord.utils.get(ctx.guild.roles, name=next_role_name)
        
        if next_role is None:
            await ctx.send(f"Il ruolo {next_role_name} non esiste nel server.")
            return

        # Rimuovere il ruolo attuale e assegnare il ruolo successivo
        current_role_obj = discord.utils.get(ctx.guild.roles, name=current_role)
        await member.remove_roles(current_role_obj)
        await member.add_roles(next_role)
        
        embed = discord.Embed(
            title="Pex",
            description=f"{member.mention} è stato promosso a {next_role.name}.  \n ```Motivo: {reason}```",
            color=discord.Color.green()
        )

        pex_channel = discord.utils.get(ctx.guild.text_channels, name='pex')

        if pex_channel is None:
            await ctx.send("Canale 'pex' non trovato.")
            return
        
        await pex_channel.send(embed=embed)

    #comando per depexare
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def depex(self, ctx, member: discord.Member, reason=None):
        role_hierarchy = ['utente', 'helper', 'mod', 'admin']
        member_roles = [role.name for role in member.roles]
        await ctx.message.delete()

        # Trova il ruolo attuale dell'utente basato sulla gerarchia
        current_role = None
        for role in role_hierarchy:
            if role in member_roles:
                current_role = role
                break

        if current_role is None:
            await ctx.send(f"{member.mention} non può essere depexato")
            return

        # Trova il prossimo ruolo nella gerarchia (ruolo inferiore)
        try:
            next_role_index = role_hierarchy.index(current_role) - 1
            next_role_name = role_hierarchy[next_role_index]
        except IndexError:
            await ctx.send(f"{member.mention} ha già il ruolo più basso.")
            return

        # Ottieni l'oggetto del ruolo successivo
        next_role = discord.utils.get(ctx.guild.roles, name=next_role_name)
        
        if next_role is None:
            await ctx.send(f"Il ruolo {next_role_name} non esiste nel server.")
            return
        
        if current_role == "utente":
            await ctx.send(f"L'utente non può essere depexato.")
            return

        # Rimuovere il ruolo attuale e assegnare il ruolo successivo
        current_role_obj = discord.utils.get(ctx.guild.roles, name=current_role)
        await member.remove_roles(current_role_obj)
        await member.add_roles(next_role)
        
        embed = discord.Embed(
            title="Depex",
            description=f"{member.mention} è stato retrocesso a {next_role.name}. \n ```Motivo: {reason}```",
            color=discord.Color.red()
        )

        pex_channel = discord.utils.get(ctx.guild.text_channels, name='pex')

        if pex_channel is None:
            await ctx.send("Canale 'pex' non trovato.")
            return
        
        await pex_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Pex(bot))
