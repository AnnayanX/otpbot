import altron

from config import OWNER_ID, DEVS, FORCESUB

from os import execl, remove
from sys import executable, argv

from Bot.mongo import UsersCol, Orders, OthersCol
from Bot.data import START_TEXT, START_BUTTON, TOP_SERVICES, TOP_SERVICES2, SERVICES, SERVICES2

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


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


# Change Balance of a User
@Client.on_message(filters.command('balance') & filters.user(OWNER_ID) & ~filters.edited & ~filters.forwarded)
async def change_balance(client: Client, message: Message):
    mx = message.text.split(" ", 3)
    try:
        balance = int(mx[1])
        user = await client.get_users(mx[2])
    except:
        return await message.reply_text("**Usage:**\n/balance <Balance in Integer> <User Id>")

    check_user = UsersCol.find_one({"_id": user.id})
    if check_user:
        UsersCol.update_one({"_id": user.id}, {"$set": {"balance": balance}})
        await message.reply_text(f"✅ **Balance Updated**\n\nUser: {user.mention}\n\nPrevious Balance = `{check_user['balance']}₹`\nUpdated Balance = `{balance}₹`")
    else:
        await message.reply_text("User Not Found in Database.")


# Check Balances Greater Than of Equal to
@Client.on_message(filters.command('min') & filters.user(DEVS) & ~filters.forwarded & ~filters.edited)
async def min_balance(_, message: Message):
    try:
        balance = int(message.text.split(" ", 2)[1])
    except:
        return await message.reply_text("**Usage:**\n/min <Minimum Balance>")

    TEXT = "💳 BALANCE INFO:\n"
    count = 0
    for user in UsersCol.find({}):
        if user['balance'] >= balance:
            count += 1
            TEXT += f"\n\n{count}. {user['_id']} | {user['balance']}₹"
    
    if count == 0:
        await message.reply_text(f"No users found with Balance >= {balance}₹")
    else:
        file_path = "files/Balances.txt"
        with open(file_path, "w") as file:
            file.write(TEXT)
        await message.reply_document(file_path, caption=f"Users with Balance >= {balance}₹", file_name="Balances.txt")
        remove(file_path)


# Fetch User
@Client.on_message(filters.command('user') & filters.user(DEVS) & ~filters.forwarded & ~filters.edited)
async def fetch_user(client: Client, message: Message):
    try:
        muser = message.text.split(" ", 2)[1]
    except:
        return await message.reply_text("**Usage:**\n/user [UserId | Username]")
    
    try:
        user = await client.get_users(muser)
        balance = UsersCol.find_one({"_id": user.id})['balance']
    except:
        return await message.reply_text("Failed to Fetch User!\n\nMaybe I never met this user before.")
    
    TEXT = f"""✅ **USER_INFO:**

**Name:** {user.mention}
**UserId:** {user.id}
**Username:** @{user.username}

Balance = {balance}₹"""
    button = InlineKeyboardMarkup([[InlineKeyboardButton(f"{user.first_name}", user_id=user.id)]])
    await message.reply_text(TEXT, reply_markup=button)


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
