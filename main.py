import discord
from keep_alive import keep_alive
import smtplib
from email.mime.text import MIMEText
import ssl
import os
import pandas as pd

client = discord.Client(intents=discord.Intents.all())

# webサーバー上の環境変数として設定したメアドを代入（今後使わない）
# EMAIL_ADDRESS = os.getenv("MY_EMAIL_ADRESS")

@client.event
async def on_ready():
    print('ログインしました')

@client.event
async def on_message(message):
    # bot自身のメッセージには反応しない
    if message.author == client.user:
        return

    df_web = pd.read_csv(
        "/etc/secrets/<channelmailreference.csv>"
    )  # タスク登録をするプロジェクトを選択
    channel_name = message.channel.name # メッセージが送信されたチャンネル名をchannel_nameとする
    filtered_rows = df_web[df_web['channnelname'] == channel_name]  # チャンネル名で検索
    BKLG_MAILADRESS = filtered_rows["mailadress"]

    # メッセージの内容を取得
    contents = message.content

    # メッセージをパースして件名と本文を代入する
    lines = message.content.splitlines()

    # 件名と本文があるか確認
    if len(lines) >1 and'件名：'in lines[0]and'本文'in lines[1]:
        # 件名の後のテキストを抽出
        subject = lines[0].split('件名：',1)[1].strip()
        # 本文の後のテキストを抽出
        body = lines[1] .split('本文:', 1)[1].strip()

        await message.channel.send

    # メールの送信
    send_email(subject, body)

# メール送信関数
def send_email(subject, body):
    # GmailのSMTPサーバー情報
    smtp_server = "smtp.gmail.com"
    smtp_port = 465  # SSL のポート
    gmail_user = EMAIL_ADRESS # type: ignore
    gmail_password = MY_APPPASSWORD # type: ignore

    # 送信先と送信元の情報
    sender_email = EMAIL_ADRESS # type: ignore
    receiver_email = BKLG_MAILADRESS # type: ignore

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
TOKEN = os.getenv("DISCORD_TOKEN")


# Web サーバの立ち上げ
keep_alive()
client.run(TOKEN)
