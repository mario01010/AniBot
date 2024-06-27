import discord
from discord.ext import commands

class ModEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.paroleNO = [
            "cazzo", "c4zzo", "merda", "m3rda", "stronzo", "str0nz0", "bastardo", "b4st4rd0",
            "puttana", "putt4n4", "troia", "tr0i4", "vaffanculo", "v4ff4nculo", "coglione", "c0gli0ne",
            "testa di cazzo", "t3st4 di c4zzo", "figlio di puttana", "figli0 di putt4n4", "frocio", "fr0ci0",
            "lesbica", "l3sbic4", "merdoso", "m3rd0s0", "culattone", "cul4tt0ne", "cazzone", "c4zz0ne",
            "puttanella", "putt4n3ll4", "zoccola", "z0cc0l4", "fanculo", "f4nculo", "deficiente", "d3ficient3",
            "cretino", "cr3tin0", "idiota", "idi0t4", "palle", "p4lle", "minchia", "minchi4", "pezzo di merda", 
            "p3zz0 di m3rda", "cazzata", "c4zz4ta", "rompipalle", "r0mpip4lle", "rompicoglioni", "r0mpic0gli0ni",
            "bastarda", "b4st4rd4", "scemo", "sc3m0", "stupido", "stup1d0", "imbecille", "imb3cill3", "feccia", 
            "f3cci4", "demente", "d3m3nt3", "tonta", "t0nt4", "cretina", "cr3tin4", "zoccolo", "z0cc0l0",
            "culona", "cul0n4", "stronza", "str0nz4", "sfigato", "sf1g4to", "suca", "suc4", "testa di minchia",
            "t3st4 di minchi4", "pirla", "p1rl4", "scopare", "sc0p4re", "bocchinaro", "b0cchin4r0", "bocchinara",
            "b0cchin4r4", "piscia", "pisci4", "merdata", "m3rd4t4", "cacca", "c4cc4", "cacarella", "c4c4rell4",
            "sputo", "spu70", "merdina", "m3rd1n4", "cagare", "c4g4re", "scoreggia", "sc0r3ggi4", "pervertito",
            "p3rv3rt1t0", "puttanata", "putt4n4t4", "sputtanare", "spu774n4r3", "impalare", "1mp4l4r3", "masturbarsi",
            "m4sturbar51", "onanismo", "0n4n1sm0", "pederasta", "p3d3r4st4", "pipparolo", "p1pp4r0l0", "porco",
            "p0rc0", "sborrata", "sb0rr4t4", "scopata", "sc0p4t4", "scroto", "scr0t0", "succhiacazzi", "succhi4c4zz1",
            "succhiaminchia", "succhi4minchi4", "pompino", "p0mpin0", "sega", "s3g4", "sodomita", "s0d0mit4",
            "stronzata", "str0nz4t4", "troiata", "tr0i4t4", "urina", "ur1n4", "zuzzurro", "zuzzurr0", "zuzzurellone",
            "zuzzur3ll0n3"
        ]
        
    @commands.Cog.listener()
    async def on_message(self, message):
        # Controlla che il messaggio non sia stato inviato dal bot stesso
        if message.author == self.bot.user:
            return

        contenuto_messaggio = message.content.lower()  # Converti il contenuto del messaggio in minuscolo
        
        # Controlla se il messaggio contiene una parola non valida
        for parola in self.paroleNO:
            if parola in contenuto_messaggio:
                # Cancella il messaggio dell'utente
                await message.delete()

                embed = discord.Embed(
                    title="⚠️ Avviso ⚠️",
                    description=f"Ciao {message.author.name}, la parola che hai usato non è permessa. Ti chiediamo cortesemente di usare un linguaggio consono al server per non incorrere in sanzioni. Grazie, cordiali saluti, AniBot.",
                    color=discord.Color.red()
                )

                # Invia un messaggio privato all'utente
                try:
                    await message.author.send(embed=embed)
                except discord.Forbidden:
                    print(f"Impossibile inviare un messaggio privato a {message.author.name}.")

                guild = message.guild
                log_message = (
                    f"Autore: {message.author.name} ({message.author.id})\n"
                    f"Contenuto: {message.content}\n"
                    f"Canale: {message.channel.name} ({message.channel.id})\n"
                    f"Server: {guild.name} ({guild.id})"
                )
                
                # Log
                log_channel_name = 'log' 
                log_embed = discord.Embed(
                    title="⚠️ Avviso ⚠️",
                    description=f"L'utente {message.author.name} ha usato una parola non consentita nel server {guild.name}. \n```{log_message}```",
                    color=discord.Color.red()
                )

                log_channel = discord.utils.get(guild.text_channels, name=log_channel_name)
                if log_channel:
                    try:
                        await log_channel.send(embed=log_embed)
                    except discord.Forbidden:
                        print(f"Impossibile inviare un avviso al canale di log {log_channel.name}.")
                break

async def setup(bot):
    await bot.add_cog(ModEvent(bot))
