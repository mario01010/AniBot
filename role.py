import discord
from discord.ext import commands


class Role(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def addrole(self, ctx, member: discord.Member, role: discord.Role):


            try:
                await member.add_roles(role)
                await ctx.send(f'Ho aggiunto il ruolo {role.name} da {member.display_name}')

            except discord.Forbidden:
                await ctx.send('Non ho il permesso di fare questo.')
                
            except discord.HTTPException as e:
                await ctx.send(f'Errore durante l\'aggiunta del ruolo: {str(e)}')



    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def removerole(self, ctx, member: discord.Member, role: discord.Role):
        try:
            await member.remove_roles(role)
            await ctx.send(f'Ho rimosso il ruolo {role.name} da {member.display_name}')
        except discord.Forbidden:
            await ctx.send('Non ho il permesso di fare questo.')
        except discord.HTTPException as e:
            await ctx.send(f'Errore durante la rimozione del ruolo: {str(e)}')



    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def createrole(self, ctx, name: str, *permissions):
        try:
            # Converti la lista di permessi in un oggetto discord.Permissions
            perms = discord.Permissions()
            for perm in permissions:
                setattr(perms, perm, True)
            
            # Crea il ruolo
            guild = ctx.guild
            await guild.create_role(name=name, permissions=perms)
            await ctx.send(f'Ruolo {name} creato con permessi: {", ".join(permissions)}')
        except discord.Forbidden:
            await ctx.send('Non ho il permesso di fare questo.')
        except discord.HTTPException as e:
            await ctx.send(f'Errore durante la creazione del ruolo: {str(e)}')

async def setup(bot):
    await bot.add_cog(Role(bot))