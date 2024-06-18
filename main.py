import re
import discord
import os
import base64
import pickle
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from requests import Request
from keep_alive import keep_alive

client = discord.Client(intents=discord.Intents.default())
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
TOKEN_FILE = 'token.pickle'

# ログインできたことを知らせる（非同期）
@client.event
async def on_ready():
    print('ログインしました')

# なんらかのメッセージに反応して、リアクション"✋"をつける（非同期）
@client.event
async def on_message(message):
    # "件名："を含むメッセージがあったら
    if "件名：" in message.content:
        #  "件名："移行の文字列をtitleに代入する
        match = re.search(r"件名：(.*)", message.content)
        if match:
            title = match.group(1).strip()
            print(f"Title: {title}")
            
# 認証情報を読み込む           
def load_credentials():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    return creds

# メッセージを作成する（sender,to,sbject,messaage_textに代入する）
def create_message(sender, to, subject, message_text):

    # MIME形式のmessage_textをmessageに代入する
    message = MIMEText(message_text)
    message['to'] = to  # 送信先
    message['from'] = sender # 送信者（じぶん）
    message['subject'] = subject # 件名
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()} # base64でエンコード

# メールを送信する（具体的な構造の指示）
def send_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except Exception as error:
        print(f'An error occurred: {error}')
        
# メールを送信する（GmailAPIを操作）
def send_email():
    creds = load_credentials()
    service = build('gmail', 'v1', credentials=creds)
    
    sender = "EMAIL_ADRESS"
    to = "EMAIL_ADRESS"
    subject = "Test"
    message_text = "Hello, this is a test email from Python."
    message = create_message(sender, to, subject, message_text)
    send_message(service, 'me', message)

    if __name__ == '__main__':
        send_email()
        
# renderに保存したトークンとアドレスを取得する
TOKEN = os.getenv("DISCORD_TOKEN")
ADRESS = os.getenv("EMAIL_ADRESS")

# Web サーバの立ち上げ
keep_alive()
client.run(TOKEN)
