import discord
from keep_alive import keep_alive
import smtplib
from email.mime.text import MIMEText
import ssl
import os

client = discord.Client(intents=discord.Intents.all())

# webサーバー上の環境変数として設定したメアドを代入
EMAIL_ADDRESS = os.getenv(MY_EMAIL_ADDRESS) 

@client.event
async def on_ready():
    print('ログインしました')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    # メッセージの内容を取得
    contents = message.content
    
    # メッセージをパースして件名と本文を代入する
    lines = contents.splitlines()
    subject = lines[0]
    body = lines[1] if len(lines) > 1 else ''
    
    # メールの送信
    send_email(subject, body)

# メール送信関数
def send_email(subject, body):
    # GmailのSMTPサーバー情報
    smtp_server = "smtp.gmail.com"
    smtp_port = 465  # SSL のポート
    gmail_user = EMAIL_ADDRESS
    gmail_password = MY_APPPASSWORD

    # 送信先と送信元の情報
    sender_email = EMAIL_ADDRESS
    receiver_email = BKLG_MAILADRESS

    # メールの作成
    msg = MIMEText(body, 'html')
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # メールの送信
    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port, context=ssl.create_default_context())
        server.login(gmail_user, gmail_password)
        server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        server.quit()

# DiscordのTOKEN（実装時には環境変数にする）
TOKEN = DISCORD_TOKEN # os.getenv("DISCORD_TOKEN")

# Web サーバの立ち上げ
keep_alive()
client.run(TOKEN)
