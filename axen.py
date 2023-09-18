from config import API_ID, API_HASH, BOT_TOKEN

from os import path, mkdir
from pyrogram import Client, idle


if not path.exists("files/"):
    mkdir("files/")

app = Client(
    "HindustanOtpBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="Bot"),
)

# Run Bot
if __name__ == "__main__":
    app.start()
    print("Altron Started Successfully!")
    idle()
    app.stop()
    print("Bot Stopped!")
