import discord
import smtplib
from keep_alive import keep_alive
from email.mime.text import MIMEText
import ssl
import os
import pandas as pd
from dotenv import load_dotenv

# .envファイルから環境変数を読み込み
load_dotenv()

# ローカルのCSVファイルを読み込む
csv_file_path = "channelmailreference.csv"
df = pd.read_csv(csv_file_path, dtype=str)

# discordにlogin
client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_ready():
    print("ログインしました")


# 自分のメッセージに反応しないようにする
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    channel_name = message.channel.name  # channel_nameを定義
    filtered_rows = df[df["channelname"] == channel_name]  # チャンネル名で検索

    if filtered_rows.empty:
        return

    print(channel_name)  # 本番では不要

    BKLG_MAILADDRESS = filtered_rows.iloc[0]["mailaddress"]  # 宛先の指定

    # メッセージの内容を取得
    contents = message.content

    # メッセージをパースして件名と本文を代入する
    lines = contents.splitlines()

    # 件名と本文があるか確認
    if len(lines) > 1 and "件名：" in lines[0] and "本文：" in lines[1]:
        # 件名の後のテキストを抽出
        subject = lines[0].split("件名：", 1)[1].strip()
        # 本文の後のテキストを抽出
        body = lines[1].split("本文：", 1)[1].strip()

        await send_email(subject, body, BKLG_MAILADDRESS, message.channel)


# メール送信関数
async def send_email(subject, body, receiver_email, channel):
    # GmailのSMTPサーバー情報
    smtp_server = "smtp.gmail.com"
    smtp_port = 465  # SSL のポート

    # Gmailアカウントとアプリパスワードを取得
    sender_email = os.getenv("EMAIL_ADDRESS")
    gmail_password = os.getenv("MY_APPPASSWORD")

    # メールの作成
    msg = MIMEText(body, "html")
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    # メールの送信
    try:
        server = smtplib.SMTP_SSL(
            smtp_server, smtp_port, context=ssl.create_default_context()
        )
        server.login(sender_email, gmail_password)
        server.send_message(msg)
        await channel.send(
            "お疲れ様です。タスクを登録しておきますね！"
        )  # discord上に表示
        print("Email sent successfully!")
    except Exception as e:
        await channel.send(f"すみません💦もう一度試していただけますか？{e}")
        print(f"Failed to send email: {e}")
    finally:
        server.quit()


# DiscordのTOKENを取得
TOKEN = os.getenv("DISCORD_TOKEN")

# Webサーバの立ち上げ
keep_alive()
client.run(TOKEN)
