import discord
from discord.ext import commands, tasks
from discord.utils import get
import random
from datetime import datetime, timedelta
import json
import os


class Combat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = 'user_data.json'
        self.user_data = self.load_data()
        self.last_command_time = {}
        self.update_leaderboard.start()

        LEVEL_REWARDS = [
       "Poneglyphs",
        "Oro Jackson",
        "Pluton",
        "Poseidon",
        "Soul Solid",
        "La Corona di Nefertari",
        "La Bibbia di Ohara",
        "Il Rio Poneglyph",
        "Frutto del Diavolo Gom Gom",
        "Frutto del Diavolo Mera Mera",
        "Frutto del Diavolo Yami Yami",
        "Frutto del Diavolo Hie Hie",
        "Frutto del Diavolo Pika Pika",
        "Frutto del Diavolo Gura Gura",
        "Frutto del Diavolo Ope Ope",
        "Frutto del Diavolo Goro Goro",
        "Frutto del Diavolo Magu Magu",
        "Frutto del Diavolo Bara Bara",
        "Frutto del Diavolo Noro Noro",
        "Frutto del Diavolo Giro Giro",
        "Frutto del Diavolo Hana Hana",
        "Frutto del Diavolo Hobi Hobi",
        "Frutto del Diavolo Bari Bari",
        "Frutto del Diavolo Ishi Ishi",
        "Frutto del Diavolo Nagi Nagi",
        "Frutto del Diavolo Soru Soru",
        "Frutto del Diavolo Juku Juku",
        "Frutto del Diavolo Fuku Fuku",
        "Frutto del Diavolo Mochi Mochi",
        "Frutto del Diavolo Hoya Hoya"

    ]
        
        self.   QUESTS = {
            "giornaliera": {
                "description": "Combatti 5 volte oggi!",
                "exp": 100,
                "reward": random.choice(LEVEL_REWARDS)
            },
            "settimanale": {
                "description": "Raggiungi il livello 10 entro la fine della settimana!",
                "exp": 500,
                "reward": "Ricompensa Speciale"
            }
        }

        self.bosses = {
            "alvida": {'difficulty': 1, 'reward': 100, 'cooldown': 6},
            "buggy": {'difficulty': 2, 'reward': 150, 'cooldown': 8},
            "arlong": {'difficulty': 3, 'reward': 200, 'cooldown': 10},
            "crocodile": {'difficulty': 4, 'reward': 250, 'cooldown': 12},
            "ener": {'difficulty': 5, 'reward': 300, 'cooldown': 14},
            "lucci": {'difficulty': 6, 'reward': 400, 'cooldown': 16},
            "moria": {'difficulty': 7, 'reward': 500, 'cooldown': 18},
            "magellan": {'difficulty': 8, 'reward': 600, 'cooldown': 20},
            "akainu": {'difficulty': 9, 'reward': 750, 'cooldown': 22},
            "doflamingo": {'difficulty': 10, 'reward': 1000, 'cooldown': 24},
            "bigmum": {'difficulty': 11, 'reward': 1300, 'cooldown': 27},
            "kaido": {'difficulty': 12, 'reward': 2000, 'cooldown': 30}
        }
    def load_data(self):
        if not os.path.exists(self.data_file) or os.path.getsize(self.data_file) == 0:
            return {}
        with open(self.data_file, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}

    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.user_data, f, indent=4)

    # Ruoli speciali
    SPECIAL_ROLES = {
        0: "Re dei Pirati",
        1: "Vice Capitano",
        2: "Ufficiale",
        3: "Ufficiale",
        4: "Ufficiale"
    }

    # Premi casuali

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setlevel(self, ctx, member: discord.Member, level: int):
        user = member

        if str(user.id) not in self.user_data:
            self.user_data[str(user.id)] = {'level': 1, 'exp': 0, 'rewards': []}

        current_level = self.user_data[str(user.id)]['level']

        self.user_data[str(user.id)]['level'] = level
        self.user_data[str(user.id)]['exp'] = 0

        await ctx.send(f"{user.mention}, il tuo livello è stato impostato a {level}.")

        # Assegna ricompensa solo se il nuovo livello è multiplo di 5 e maggiore di quello attuale
        if level > current_level and level % 5 == 0:
            reward = random.choice(self.LEVEL_REWARDS)
            self.user_data[str(user.id)]['rewards'].append(reward)
            await ctx.send(f"Congratulazioni {user.mention}, hai ricevuto {reward}")

        self.save_data()

    @commands.command()
    async def combatti(self, ctx):
        user = ctx.author
        current_time = datetime.now()

        if user.id in self.last_command_time:
            time_diff = current_time - self.last_command_time[user.id]
            if time_diff < timedelta(minutes=3):
                await ctx.send("Devi aspettare prima di combattere di nuovo!")
                return

        self.last_command_time[user.id] = current_time

        if str(user.id) not in self.user_data:
            self.user_data[str(user.id)] = {'level': 1, 'exp': 0, 'rewards': []}

        exp_gained = random.randint(20, 90)
        self.user_data[str(user.id)]['exp'] += exp_gained
        await ctx.send(f"Hai ottenuto {exp_gained} esperienza!")

        if self.user_data[str(user.id)]['exp'] >= 100:
            self.user_data[str(user.id)]['exp'] = 0
            self.user_data[str(user.id)]['level'] += 1
            level = self.user_data[str(user.id)]['level']

            await ctx.send(f"{user.mention} è salito al livello {level}!")

            if level % 5 == 0:
                reward = random.choice(self.LEVEL_REWARDS)
                self.user_data[str(user.id)]['rewards'].append(reward)
                await ctx.send(f"Congratulazioni {user.mention}, hai ricevuto {reward}!")

        self.save_data()

    @commands.command()
    async def livello(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        if str(member.id) not in self.user_data:
            await ctx.send(f"{member.mention} non ha ancora iniziato a combattere!")
            return

        level = self.user_data[str(member.id)]['level']
        rewards = "\n".join(self.user_data[str(member.id)]['rewards'])
        avatar_url = member.avatar.url
        position = self.get_position(member.id)
        role = self.get_special_role(position)

        embed = discord.Embed(title=f"Livello di {member.name}", description=f"Livello: {level}", color=discord.Color.blue())
        embed.set_thumbnail(url=avatar_url)
        embed.add_field(name="Ricompense", value=f"{rewards}" if rewards else "Nessuna ricompensa", inline=False)
        embed.add_field(name="Posizione in classifica", value=position + 1, inline=False)
        embed.add_field(name="Ruolo speciale", value=role, inline=False)

        await ctx.send(embed=embed)

    def get_position(self, user_id):
        sorted_users = sorted(self.user_data.items(), key=lambda x: x[1]['level'], reverse=True)
        for i, (uid, data) in enumerate(sorted_users):
            if uid == str(user_id):
                return i
        return -1

    def get_special_role(self, position):
        return self.SPECIAL_ROLES.get(position, "Equipaggio")
    


    @commands.command()
    async def top(self, ctx):
        sorted_users = sorted(self.user_data.items(), key=lambda x: x[1]['level'], reverse=True)[:10]
        embed = discord.Embed(title="Top 10 Giocatori", color=discord.Color.gold())
        for i, (user_id, data) in enumerate(sorted_users):
            user = self.bot.get_user(int(user_id))
            role = self.get_special_role(i)
            embed.add_field(name=f"{i+1} - {role}", value=user.mention if user else f"Utente ID: {user_id}", inline=False)
        await ctx.send(embed=embed)

    def get_position(self, user_id):
        sorted_users = sorted(self.user_data.items(), key=lambda x: x[1]['level'], reverse=True)
        for i, (uid, data) in enumerate(sorted_users):
            if uid == str(user_id):
                return i
        return -1

    def get_special_role(self, position):
        return self.SPECIAL_ROLES.get(position, "Equipaggio")




    @tasks.loop(minutes=1)
    async def update_leaderboard(self):
        guild = self.bot.guilds[0]
        
        # Filtra gli utenti che non hanno il campo 'level'
        filtered_users = {user_id: data for user_id, data in self.user_data.items() if 'level' in data}

        sorted_users = sorted(filtered_users.items(), key=lambda x: x[1]['level'], reverse=True)

        for i, (user_id, data) in enumerate(sorted_users):
            user = self.bot.get_user(int(user_id))
            if user is None:
                continue
            role_name = self.get_special_role(i)

            role = get(guild.roles, name=role_name)
            if role:
                member = guild.get_member(user.id)
                if member:
                    # Rimuove tutti i ruoli speciali prima di assegnare quello nuovo
                    for special_role_name in self.SPECIAL_ROLES.values():
                        special_role = get(guild.roles, name=special_role_name)
                        if special_role and special_role in member.roles:
                            await member.remove_roles(special_role)
                    # Assegna il nuovo ruolo speciale
                    await member.add_roles(role)



    @commands.command()
    async def quest(self, ctx):
        user_id = str(ctx.author.id)
        user_data = self.user_data.get(user_id, {'level': 1, 'exp': 0, 'rewards': [], 'quests': {}})
        
        # Display current quests
        embed = discord.Embed(title="Quests Disponibili", color=discord.Color.green())
        for quest_name, quest_data in self.QUESTS.items():
            embed.add_field(name=quest_name.capitalize(), value=f"{quest_data['description']}\nExp: {quest_data['exp']}\nRicompensa: {quest_data['reward']}", inline=False)
        
        await ctx.send(embed=embed)

    @tasks.loop(hours=24)
    async def check_daily_quests(self):
        for user_id, data in self.user_data.items():
            if "quest_completions" not in data:
                data["quest_completions"] = {"giornaliera": 0, "settimanale": 0}
            user_data = self.user_data[user_id]
            # Check daily quest
            if user_data["quest_completions"]["giornaliera"] < 5:
                continue
            user_data["quest_completions"]["giornaliera"] = 0
            user_data["exp"] += self.QUESTS["giornaliera"]["exp"]
            user_data["rewards"].append(self.QUESTS["giornaliera"]["reward"])
        
        self.save_data()

    @tasks.loop(hours=168)  # 168 hours = 1 week
    async def check_weekly_quests(self):
        for user_id, data in self.user_data.items():
            user_data = self.user_data[user_id]
            # Check weekly quest
            if user_data["level"] >= 10:
                user_data["exp"] += self.QUESTS["settimanale"]["exp"]
                user_data["rewards"].append(self.QUESTS["settimanale"]["reward"])
        
        self.save_data()

    @commands.command()
    async def sfida(self, ctx, member: discord.Member):
        if member.bot:
            await ctx.send("Non puoi sfidare un bot!")
            return

        if str(member.id) not in self.user_data:
            await ctx.send(f"{member.mention} non ha ancora iniziato a combattere!")
            return

        if str(ctx.author.id) not in self.user_data:
            self.user_data[str(ctx.author.id)] = {'level': 1, 'exp': 0, 'rewards': []}

        # Determine winner
        user1_data = self.user_data[str(ctx.author.id)]
        user2_data = self.user_data[str(member.id)]
        winner = ctx.author if user1_data['level'] >= user2_data['level'] else member

        # Update exp
        exp_gained = random.randint(30, 100)
        self.user_data[str(winner.id)]['exp'] += exp_gained

        await ctx.send(f"{winner.mention} ha vinto la sfida e ha ottenuto {exp_gained} esperienza!")
        
        if self.user_data[str(winner.id)]['exp'] >= 100:
            self.user_data[str(winner.id)]['exp'] = 0
            self.user_data[str(winner.id)]['level'] += 1
            level = self.user_data[str(winner.id)]['level']
            await ctx.send(f"{winner.mention} è salito al livello {level}!")

            if level % 5 == 0:
                reward = random.choice(self.LEVEL_REWARDS)
                self.user_data[str(winner.id)]['rewards'].append(reward)
                await ctx.send(f"Congratulazioni {winner.mention}, hai ricevuto {reward}!")

        self.save_data()



    @commands.command()
    async def inventario(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        if str(member.id) not in self.user_data:
            await ctx.send(f"{member.mention} non ha ancora iniziato a combattere!")
            return

        items = "\n".join(self.user_data[str(member.id)].get('rewards', []))
        embed = discord.Embed(
            title = f"Inventario di {member}",
            description= f"{items if items else 'Vuoto'}",
            color = discord.Color.blue()
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def usa(self, ctx, *, item_name):
        user_id = str(ctx.author.id)
        if user_id not in self.user_data or item_name not in self.user_data[user_id].get('rewards', []):
            await ctx.send(f"Non possiedi {item_name}!")
            return

        self.user_data[user_id]['rewards'].remove(item_name)
        await ctx.send(f"Hai usato {item_name}!")

        # Effect of the item
        if item_name in self.LEVEL_REWARDS:
            self.user_data[user_id]['exp'] += 50
            await ctx.send(f"Hai ottenuto 50 esperienza!")
        # Additional item effects can be added here

        self.save_data()

    @commands.command()
    async def scambia(self, ctx, member: discord.Member, *, item_name):
        user_id = str(ctx.author.id)
        if user_id not in self.user_data or item_name not in self.user_data[user_id].get('rewards', []):
            await ctx.send(f"Non possiedi {item_name}!")
            return

        if str(member.id) not in self.user_data:
            self.user_data[str(member.id)] = {'level': 1, 'exp': 0, 'rewards': []}

        self.user_data[user_id]['rewards'].remove(item_name)
        self.user_data[str(member.id)]['rewards'].append(item_name)

        await ctx.send(f"Hai scambiato {item_name} con {member.mention}!")
        self.save_data()

    @commands.command()
    async def Gcreate(self, ctx, *, nome_gilda):
        user_id = str(ctx.author.id)
        if 'gilda' in self.user_data.get(user_id, {}):
            await ctx.send("Sei già in una gilda!")
            return

        self.user_data[user_id]['gilda'] = nome_gilda
        if nome_gilda not in self.user_data:
            self.user_data[nome_gilda] = {'membri': [user_id]}
        else:
            self.user_data[nome_gilda]['membri'].append(user_id)

        await ctx.send(f"{ctx.author.mention} ha creato la gilda {nome_gilda}!")
        self.save_data()

    @commands.command()
    async def Gleft(self, ctx):
        user_id = str(ctx.author.id)
        if 'gilda' not in self.user_data.get(user_id, {}):
            await ctx.send("Non sei in nessuna gilda!")
            return

        nome_gilda = self.user_data[user_id].pop('gilda')
        self.user_data[nome_gilda]['membri'].remove(user_id)
        await ctx.send(f"{ctx.author.mention} ha lasciato la gilda {nome_gilda}!")
        self.save_data()

    @commands.command()
    async def Ginfo(self, ctx, *, nome_gilda):
        if nome_gilda not in self.user_data:
            await ctx.send("Questa gilda non esiste!")
            return

        gilda_data = self.user_data[nome_gilda]
        membri = gilda_data.get('membri', [])

        # Calcola il livello medio della gilda
        livelli_membri = [self.user_data[membro]['level'] for membro in membri]
        livello_medio = sum(livelli_membri) / len(livelli_membri) if livelli_membri else 0

        # Ordina i membri per livello (decrescente)
        membri_ordinati = sorted(membri, key=lambda membro: self.user_data[membro]['level'], reverse=True)

        # Formatta l'output
        embed = discord.Embed(title=f"Informazioni su {nome_gilda}", color=discord.Color.purple())
        embed.add_field(name="Data di Creazione", value=gilda_data.get('data_creazione', 'Non disponibile'))
        embed.add_field(name="Livello", value=f"{livello_medio:.0f}")
        embed.add_field(name="Membri", value="\n".join([f"{self.bot.get_user(int(membro))} - Livello {self.user_data[membro]['level']}" for membro in membri_ordinati]), inline=False)

        await ctx.send(embed=embed)


    @commands.command()
    async def Ginvite(self, ctx, member: discord.Member, *, gilda_nome):
        if 'gilda' not in self.user_data.get(str(ctx.author.id), {}):
            await ctx.send("Non sei in nessuna gilda!")
            return

        if self.user_data[str(ctx.author.id)]['gilda'] != gilda_nome:
            await ctx.send("Non sei il creatore di questa gilda!")
            return

        if str(member.id) in self.user_data and 'gilda' in self.user_data[str(member.id)]:
            await ctx.send(f"{member.mention} è già in una gilda!")
            return

        if gilda_nome not in self.user_data:
            await ctx.send(f"La gilda {gilda_nome} non esiste!")
            return

        self.user_data[gilda_nome].setdefault('inviti', {})
        self.user_data[gilda_nome]['inviti'][str(member.id)] = member
        await ctx.send(f"{member.mention}, sei stato invitato nella gilda {gilda_nome}! Usa !Gaccept per accettare l'invito o !Grefuse per rifiutarlo.")

    @commands.command()
    async def Gaccept(self, ctx):
        user_id = str(ctx.author.id)
        gilda_invitato = None

        for gilda, data_gilda in self.user_data.items():
            if 'inviti' in data_gilda and user_id in data_gilda['inviti']:
                gilda_invitato = gilda
                break

        if not gilda_invitato:
            await ctx.send("Non hai inviti pendenti per una gilda!")
            return

        # Aggiungi utente alla gilda
        self.user_data[user_id]['gilda'] = gilda_invitato
        self.user_data[gilda_invitato]['membri'].append(user_id)

        # Rimuovi l'invito
        del self.user_data[gilda_invitato]['inviti'][user_id]

        await ctx.send(f"{ctx.author.mention} hai accettato l'invito per entrare nella gilda {gilda_invitato}!")

    @commands.command()
    async def Grefuse(self, ctx):
        user_id = str(ctx.author.id)
        gilda_invitato = None

        for gilda, data_gilda in self.user_data.items():
            if 'inviti' in data_gilda and user_id in data_gilda['inviti']:
                gilda_invitato = gilda
                break

        if not gilda_invitato:
            await ctx.send("Non hai inviti pendenti per una gilda!")
            return

        # Rimuovi l'invito
        del self.user_data[gilda_invitato]['inviti'][user_id]

        await ctx.send(f"{ctx.author.mention} hai rifiutato l'invito per entrare nella gilda {gilda_invitato}.")

    @commands.command()
    async def Gkick(self, ctx, member: discord.Member):
        user_id = str(member.id)
        if 'gilda' not in self.user_data.get(user_id, {}):
            await ctx.send(f"{member.mention} non è in nessuna gilda!")
            return

        gilda_nome = self.user_data[user_id]['gilda']
        if 'gilda' not in self.user_data.get(str(ctx.author.id), {}):
            await ctx.send(f"Non sei in nessuna gilda!")
            return

        if self.user_data[str(ctx.author.id)]['gilda'] != gilda_nome:
            await ctx.send(f"Non sei autorizzato a eseguire questa azione!")
            return

        self.user_data[user_id].pop('gilda')
        self.user_data[gilda_nome]['membri'].remove(user_id)
        await ctx.send(f"{member.mention} è stato espulso dalla gilda {gilda_nome}!")
        self.save_data()


    @commands.Cog.listener()
    async def on_ready(self):
        self.check_daily_quests.start()
        self.check_weekly_quests.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is ready and connected to Discord!")

    @commands.Cog.listener()
    async def on_disconnect(self):
        self.save_data()

    @commands.Cog.listener()
    async def on_resumed(self):
        self.user_data = self.load_data()

async def setup(bot):
    await bot.add_cog(Combat(bot))
