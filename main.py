import os
import asyncio
import discord
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

FB_GROUP_URL = os.getenv("FB_GROUP_URL")
FB_COOKIE = os.getenv("FB_COOKIE")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

last_post_id = None
spamming = False

headers = {
    "User-Agent": "Mozilla/5.0",
    "Cookie": FB_COOKIE
}

def get_latest_post_id():
    try:
        response = requests.get(FB_GROUP_URL, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if "/posts/" in href:
                post_id = href.split("/posts/")[1].split("/")[0]
                return post_id
    except Exception as e:
        print(f"[ERROR] Lỗi lấy bài viết mới: {e}")
    return None

@client.event
async def on_ready():
    print(f"✅ Bot đã đăng nhập: {client.user}")
    client.loop.create_task(monitor_facebook())

@client.event
async def on_message(message):
    global spamming
    if message.channel.id != CHANNEL_ID:
        return
    if message.content.lower() == "stop":
        spamming = False
        await message.channel.send("🛑 Đã dừng spam.")

async def monitor_facebook():
    global last_post_id, spamming
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)

    while True:
        new_post_id = get_latest_post_id()
        if new_post_id and new_post_id != last_post_id:
            print(f"[INFO] Bài mới: {new_post_id}")
            last_post_id = new_post_id
            spamming = True
            while spamming:
                await channel.send(
                    f"📢 Bài đăng mới: https://www.facebook.com/groups/{FB_GROUP_URL.split('/')[-2]}/posts/{new_post_id}"
                )
                await asyncio.sleep(5)
        await asyncio.sleep(5)

client.run(BOT_TOKEN)