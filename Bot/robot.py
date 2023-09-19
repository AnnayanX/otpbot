from config import OWNER_ID, DEVS, FORCESUB, OWNER_ID, API_KEY_S1, headers

from Bot.mongo import UsersCol, Orders, OthersCol
from Bot.utils import afetch, getOTP, getOTP2, is_buying, add_buyer, rm_buyer
from Bot.data import (
    START_TEXT, START_BUTTON, TOP_SERVICES, TOP_SERVICES2, SERVICES, SERVICES2, JOIN_MESSAGE,
    SERVICE_PRICES, SERVICE_PRICES2, INSUFF_BALANCE, INSUFF_BUTTON, BACK_BUTTON, OPERATORS2
)

from pyrogram import Client, filters
from pyrogram.errors import FloodWait, ChatAdminRequired, UserNotParticipant
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from os import execl, remove
from threading import Thread
from asyncio import run, sleep
from sys import executable, argv
from aiohttp import ClientSession


async def buy_otp(client: Client, msg: Message):
    server = msg.command[1].split("_", 1)[0]
    service = msg.command[1].split("_", 1)[1]
    balance = UsersCol.find_one({"_id": msg.from_user.id})["balance"]
    service_price = SERVICE_PRICES[service] if server == "1" else SERVICE_PRICES2[service]
    if balance < service_price:
        await rm_buyer(msg.from_user.id)
        await msg.reply_text(INSUFF_BALANCE, reply_markup=INSUFF_BUTTON)
        return

    if server == "1":
        res = await afetch(f"https://fastsms.su/stubs/handler_api.php?api_key={API_KEY_S1}&action=getNumber&service={service}&country=22")

        try:
            if res == "NO_BALANCE":
                await rm_buyer(msg.from_user.id)
                await client.send_message(OWNER_ID, "**Please add Balance to your <u>fastsms.su</u> Account.**")
                await msg.reply_text("💤 **Bot is under Maintainance. Please wait for few minutes...**", reply_markup=BACK_BUTTON)
            elif res.startswith("ACCESS_NUMBER:"):
                aid, number = res.split(":")[1:]
                # MULTI-THREADING
                thread = Thread(target=run, args=(getOTP(client, msg, msg.from_user, service, number, aid, service_price, balance),))
                thread.start()
            else:
                await rm_buyer(msg.from_user.id)
                await msg.reply_text("❌ **There are no numbers with the specified parameters, please try again after few minutes...**", reply_markup=BACK_BUTTON)
        except:
            await rm_buyer(msg.from_user.id)
            return

    else:
        async with ClientSession() as session:
            async with session.get(f'https://5sim.net/v1/user/buy/activation/india/{OPERATORS2[service]}/{service}', headers=headers) as resp:
                res = await resp.text()
                status_code = resp.status

        if (status_code == 200) and (res != "no free phones"):
            res = await resp.json()
            number, aid = res["phone"], res["id"]
            # MULTI-THREADING
            thread = Thread(target=run, args=(getOTP2(client, msg, msg.from_user, service, number, aid, service_price, balance),))
            thread.start()
        elif res == "not enough user balance":
            await rm_buyer(msg.from_user.id)
            await client.send_message(OWNER_ID, "**Please add Balance to your <u>5sim.net</u> Account.**")
            await msg.reply_text("💤 **Bot is under Maintainance. Please wait for few minutes...**", reply_markup=BACK_BUTTON)
        else:
            await rm_buyer(msg.from_user.id)
            await msg.reply_text("❌ **There are no numbers with the specified parameters, please try again after few minutes...**", reply_markup=BACK_BUTTON)



# Must Join
@Client.on_message(filters.private & filters.incoming & ~filters.forwarded, group=-1)
async def must_join(client: Client, message: Message):
    try:
        await client.get_chat_member(FORCESUB, message.from_user.id)
    except UserNotParticipant:
        await message.reply_text(
            JOIN_MESSAGE,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✘ ᴊᴏɪɴ ᴜᴘᴅᴀᴛᴇꜱ ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/{FORCESUB}")]
            ]),
        )
        await message.stop_propagation()
    except ChatAdminRequired:
        print(f"I'm not admin in the MUST_JOIN chat : @{FORCESUB} !")


# Start Message
@Client.on_message(filters.private & filters.command('start') & ~filters.forwarded)
async def main(client: Client, msg: Message):
    if len(msg.command) > 1:
        await sleep(0.5)
        if is_buying(msg.from_user.id):
            await msg.reply_text("⚠ **Please Cancel Your First Order To Receive New Number.**")
            return
        await add_buyer(msg.from_user.id)
        await buy_otp(client, msg)
    else:
        await msg.reply_text(START_TEXT.format(msg.from_user.mention), reply_markup=START_BUTTON)
        try:
            UsersCol.insert_one({"_id": msg.chat.id, "balance": 0, "fav1": [], "fav2": []})
        except:
            pass


# Add to Top Service
@Client.on_message(filters.command(['top', 'top1', 'top2']) & filters.user(OWNER_ID) & ~filters.forwarded)
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
@Client.on_message(filters.command('price') & filters.user(OWNER_ID) & ~filters.forwarded)
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
@Client.on_message(filters.command('balance') & filters.user(OWNER_ID) & ~filters.forwarded)
async def change_balance(client: Client, message: Message):
    mx = message.text.split(" ", 3)
    try:
        balance = int(mx[1])
        user = await client.get_users(int(mx[2]))
        name = user.first_name
        mention = user.mention
        user_id = user.id
    except (ValueError, IndexError):
        await message.reply_text("**Usage:**\n/balance [Balance in Integer] [User Id]")
        return
    except:
        mention = "Unknown User"
        name = "Unknown User"
        user_id = int(mx[2])

    check_user = UsersCol.find_one({"_id": user_id})
    if check_user:
        UsersCol.update_one({"_id": user_id}, {"$set": {"balance": balance}})
        try:
            button = InlineKeyboardMarkup([[InlineKeyboardButton(f"{name}", user_id=user_id)]])
        except:
            button = None
        await message.reply_text(f"✅ **Balance Updated**\n\nUser: {mention}\n\nPrevious Balance = `{check_user['balance']}₹`\nUpdated Balance = `{balance}₹`", reply_markup=button)
    else:
        await message.reply_text("User Not Found in Database.")


# Check Balances Greater Than of Equal to
@Client.on_message(filters.command('min') & filters.user(DEVS) & ~filters.forwarded)
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
@Client.on_message(filters.command('user') & filters.user(DEVS) & ~filters.forwarded)
async def fetch_user(client: Client, message: Message):
    try:
        muser = message.text.split(" ", 2)[1]
        user = await client.get_users(muser)
        balance = UsersCol.find_one({"_id": user.id})['balance']
    except IndexError:
        await message.reply_text("**Usage:** /user [UserId|Username]")
        return
    except:
        await message.reply_text("Failed to Fetch User!\n\nMaybe I never met this user before.")
        return
    
    TEXT = f"""✅ **USER_INFO:**

**Name:** {user.mention}
**UserId:** {user.id}
**Username:** @{user.username}

Balance = {balance}₹"""
    button = InlineKeyboardMarkup([[InlineKeyboardButton(f"{user.first_name}", user_id=user.id)]])
    await message.reply_text(TEXT, reply_markup=button)


# Stats of the Bot
@Client.on_message(filters.command('stats') & filters.user(DEVS) & filters.private & ~filters.forwarded)
async def stats(client: Client, message: Message):
    num_users = UsersCol.count_documents({})
    num_o = Orders.count_documents({})
    stats_text = f"""ㅤㅤ ▬▬▬**「ꜱᴛᴀᴛɪꜱᴛɪᴄꜱ」**▬▬▬
ㅤㅤㅤ   ≛≛ **ᴛᴏᴛᴀʟ ᴜꜱᴇʀꜱ :** {num_users}
ㅤㅤㅤ   ≛≛ **ᴛᴏᴛᴀʟ ᴏʀᴅᴇʀs :** {num_o}
ㅤㅤ ▬▬▬**「ꜱᴛᴀᴛɪꜱᴛɪᴄꜱ」**▬▬▬"""
    await message.reply_photo("https://te.legra.ph/file/04e8f8e6bbf74c54f3f9d.jpg", caption=stats_text)


# Global Cast
@Client.on_message(filters.user(OWNER_ID) & filters.command('gcast') & ~filters.forwarded)
async def gcast(client: Client, message: Message):
    all_users = UsersCol.find({}, {"_id":1})
    user_ids = [user_id["_id"] for user_id in all_users]
    if message.reply_to_message:
        m = message.reply_to_message_id
        p = message.chat.id
    else:
        query = message.text.split(" ", 1)
        if len(query) == 1:
            await message.reply_text(f"𝗨𝘀𝗮𝗴𝗲:\n » /gcast [MESSAGE] ᴏʀ [Reply to a Message]")
            return
        gcast_msg = query[1]

    alt = 0
    for uid in user_ids:
        try:
            if message.reply_to_message:
                await client.forward_messages(uid, p, m)
            else:
                await client.send_message(uid, text=gcast_msg)
            alt += 1
            await sleep(0.3)
        except FloodWait as e:
            flood_time = int(e.value)
            await sleep(flood_time)
        except Exception:
            pass
    try:
        await message.reply_text(f"**» ʙʀᴏᴀᴅᴄᴀꜱᴛᴇᴅ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ {alt} ᴄʜᴀᴛꜱ.**")
    except:
        pass
