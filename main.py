import discord
import os
from keep_alive import keep_alive

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print('ログインしました')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    content = message.content
    subject = ""
    body = ""
    
    if "件名：" in content and "本文：" in content:
        try:
            subject_start = content.index("件名：") + len("件名：")
            subject_end = content.index("本文：")
            subject = content[subject_start:subject_end].strip()
            
            body_start = content.index("本文：") + len("本文：")
            body = content[body_start:].strip()
            
            await message.channel.send(f"Subject: {subject}")
            await message.channel.send(f"Body: {body}")
        except ValueError:
            await message.channel.send("メッセージの形式が正しくありません")
    
    emoji = "✋"
    await message.add_reaction(emoji)

TOKEN = os.getenv("DISCORD_TOKEN")
# Web サーバの立ち上げ
keep_alive()
client.run(TOKEN)
