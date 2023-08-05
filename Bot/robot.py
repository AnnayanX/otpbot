import altron

from config import OWNER_ID, DEVS, FORCESUB

from os import execl
from sys import executable, argv

from Bot.mongo import UsersCol, Orders, OthersCol
from Bot.data import START_TEXT, START_BUTTON, TOP_SERVICES, TOP_SERVICES2, SERVICES, SERVICES2

from pyrogram import Client, filters
from pyrogram.types import Message


# Must Join
@Client.on_message(filters.private & filters.incoming & ~filters.edited & ~filters.forwarded, group=-1)
async def must_join(bot: Client, msg: Message):
    await altron.must_join(bot, msg, FORCESUB)


# Start Message
@Client.on_message(filters.private & filters.command('start') & ~filters.edited & ~filters.forwarded)
async def main(_, msg: Message):
    await msg.reply_text(START_TEXT.format(msg.from_user.mention), reply_markup=START_BUTTON)
    try:
        UsersCol.insert_one({"_id": msg.chat.id, "balance": 0, "fav1": [], "fav2": []})
    except:
        pass


# Add to Top Service
@Client.on_message(filters.command(['top', 'top1', 'top2']) & filters.user(OWNER_ID) & ~filters.edited & ~filters.forwarded)
async def top_service(_, msg: Message):
    try:
        cmd, key = msg.text.split(" ")[:2]
        key = key.lower()
    except:
        await msg.reply_text("**Usage:  /top sᴇʀᴠɪᴄᴇ_ᴋᴇʏ**")
        return
    
    global TOP_SERVICES,TOP_SERVICES2
    serx, serm, s = (SERVICES2, TOP_SERVICES2, "2") if cmd[-1] == "2" else (SERVICES, TOP_SERVICES, "1")
    try:
        value = serx[key]
    except KeyError:
        await msg.reply_text(f"**SERVICE_KEY ( {key} ) not found in Services List.**")
        return

    if key in serm.keys():
        await msg.reply_text(f"**Already exists ( {value} ) in Top Services List.**")
    else:
        serm[key] = value
        services = OthersCol.find_one({"_id": f"top_services{s}"})["services"]
        services.append(key)
        OthersCol.update_one({"_id": f"top_services{s}"}, {"$set": {f"services": services}})
        await msg.reply_text(f"**Successfully added ( {value} ) to Top Services List.**")


# Change Price
@Client.on_message(filters.command('price') & filters.user(OWNER_ID) & ~filters.edited & ~filters.forwarded)
async def change_price(_, msg: Message):
    try:
        price = float(msg.text.split(" ")[1])
        OthersCol.update_one({"_id": "price"}, {"$set": {"price": price}})
        await msg.reply_text("✅ **PRICE UPDATED\n\nʀᴇsᴛᴀʀᴛɪɴɢ ʙᴏᴛ...**")
        execl(executable, executable, *argv)
    except:
        price = OthersCol.find_one({"_id": "price"})["price"]
        await msg.reply_text(f"**Usage:** /price <ᴠᴀʟᴜᴇ>\n\n**Current Price: {price}**")


# Stats of the Bot
@Client.on_message(filters.command('stats') & filters.user(DEVS) & filters.private & ~filters.edited & ~filters.forwarded)
async def stats(client: Client, message: Message):
    num_users = UsersCol.count_documents({})
    num_o = Orders.count_documents({})
    stats_text = f"""ㅤㅤ ▬▬▬**「ꜱᴛᴀᴛɪꜱᴛɪᴄꜱ」**▬▬▬
ㅤㅤㅤ   ≛≛ **ᴛᴏᴛᴀʟ ᴜꜱᴇʀꜱ :** {num_users}
ㅤㅤㅤ   ≛≛ **ᴛᴏᴛᴀʟ ᴏʀᴅᴇʀs :** {num_o}
ㅤㅤ ▬▬▬**「ꜱᴛᴀᴛɪꜱᴛɪᴄꜱ」**▬▬▬"""
    await altron.stats(client, message, stats_text)


# Global Cast
@Client.on_message(filters.user(OWNER_ID) & filters.command('gcast') & ~filters.edited & ~filters.forwarded)
async def gcast(client: Client, message: Message):
    all_users = UsersCol.find({}, {"_id":1})
    user_ids = [user_id["_id"] for user_id in all_users]
    await altron.gcast(client, message, user_ids)
