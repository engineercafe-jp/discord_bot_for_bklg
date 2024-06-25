import discord
from keep_alive import keep_alive
import smtplib
from email.mime.text import MIMEText
import ssl
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv("/etc/secrets/myenvfile")

client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_ready():
    print("ログインしました")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    df_web = pd.read_csv("/etc/secrets/channelmailreference.csv")
    channel_name = message.channel.name
    filtered_rows = df_web[df_web["channelname"] == channel_name]  # スペルミス修正
    BKLG_MAILADDRESS = filtered_rows["mailaddress"].values[0]  # スペルミス修正

    contents = message.content
    lines = contents.splitlines()

    if len(lines) > 1 and "件名：" in lines[0] and "本文:" in lines[1]:  # 修正
        subject = lines[0].split("件名：", 1)[1].strip()
        body = lines[1].split("本文:", 1)[1].strip()

        await message.channel.send("メールを送信しています...")  # 修正

        send_email(subject, body, BKLG_MAILADDRESS)  # 修正


def send_email(subject, body, receiver_email):  # 修正
    smtp_server = "smtp.gmail.com"
    smtp_port = 465
    gmail_user = os.getenv("MY_EMAIL_ADDRESS")
    gmail_password = os.getenv("MY_APP_PASSWORD")
    sender_email = gmail_user

    msg = MIMEText(body, "html")
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    try:
        server = smtplib.SMTP_SSL(
            smtp_server, smtp_port, context=ssl.create_default_context()
        )
        server.login(gmail_user, gmail_password)
        server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        server.quit()


TOKEN = os.getenv("DISCORD_TOKEN")

keep_alive()
client.run(TOKEN)
