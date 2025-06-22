import os
import discord
from dotenv import load_dotenv
from datetime import datetime, timedelta
import asyncio

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
# lista de IDs de amigos que receberão a DM
FRIENDS = [int(x) for x in os.getenv("FRIEND_IDS", "").split(",") if x]

intents = discord.Intents.default()
intents.members = True
intents.voice_states = True

client = discord.Client(intents=intents)

now = datetime.now()
weekday = now.weekday()  # segunda = 0, domingo = 6

if weekday in [5, 6]:  # sábado ou domingo
    DESLIGAR_DEPOIS = 24
else:
    DESLIGAR_DEPOIS = 6

@client.event
async def on_ready():
    print(f"[✅] Bot online como {client.user}")
    desligar_em = datetime.now() + timedelta(hours=DESLIGAR_DEPOIS)
    await desligar_quando(desligar_em)

async def desligar_quando(tempo):
    while datetime.now() < tempo:
        await asyncio.sleep(60)
    print("[⏹️] Tempo limite atingido. Saindo.")
    await client.close()


@client.event
async def on_voice_state_update(member, before, after):
    msg = None

    if before.channel is None and after.channel:
        msg = f"🔔 **{member.display_name}** entrou no canal: **{after.channel.name}**"

    elif before.channel and after.channel is None:
        msg = f"❌ **{member.display_name}** saiu do canal: **{before.channel.name}**"

    elif before.channel != after.channel:
        msg = f"🔄 **{member.display_name}** mudou de canal: **{before.channel.name} → {after.channel.name}**"

    if msg:
        for uid in FRIENDS:
            try:
                user = await client.fetch_user(uid)
                await user.send(msg)
            except Exception as e:
                print(f"🚫 Erro DM para {uid}: {e}")


client.run(DISCORD_TOKEN)
