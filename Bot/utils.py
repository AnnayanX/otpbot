from aiohttp import ClientSession

from config import API_KEY_S1, LOGS, headers

from Bot.mongo import Orders, UsersCol
from Bot.data import SERVICES, SERVICES2, OTP_RECEIVED, NUMBER_TEXT, SERVICE_PRICES

from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from time import time
from pytz import timezone
from asyncio import sleep
from threading import RLock
from datetime import datetime


OTPS = {}
OTP_LOCK = RLock()


async def afetch(url):
    async with ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()


async def afetchcode(url):
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            return await resp.json(), resp.status


async def getOTP(client: Client, msg: Message, service, number, aid, service_price=None, balance=None):
    user_id = msg.from_user.id
    global OTPS
    with OTP_LOCK:
        OTPS[aid] = time() + 300
    number = number[1:] if number[0] == "+" else number
    await msg.reply_text(NUMBER_TEXT.format(SERVICES[service], number))

    text = "STATUS_WAIT_CODE"
    while text == "STATUS_WAIT_CODE":
        if (aid in OTPS.keys()) and (time() >= OTPS[aid]):
            text = await afetch(f"https://fastsms.su/stubs/handler_api.php?api_key={API_KEY_S1}&action=setStatus&id={aid}&status=8")
            if text == "ACCESS_CANCEL":
                try:
                    btn = InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data=f"SERVICE1|{service}")]])
                    await msg.reply_text("✅ **Successfully Cancelled OTP.**", reply_markup=btn)
                except:
                    try:
                        await msg.reply_text("✅ **Successfully Cancelled OTP.**", reply_markup=btn)
                    except:
                        pass
                if service_price:
                    balance = UsersCol.find_one({"_id": user_id})["balance"]
                    balance += service_price
                    UsersCol.update_one({"_id": user_id}, {"$set": {"balance": balance}})
                LOG_TEXT = f"""❌ #OTP_CANCELLED

**Service:** `{SERVICES[service]}`
**Number:** +{number}
**Server:** `1`

**User:** {msg.from_user.mention}
**User-ID:** `{user_id}`
**Username:** @{msg.from_user.username}"""
                await client.send_message(LOGS, LOG_TEXT)
            await dlt_buying(aid)
            return
        if text == "STATUS_CANCEL":
            await dlt_buying(aid)
            return
        await sleep(3)
        text = await afetch(f"https://fastsms.su/stubs/handler_api.php?api_key={API_KEY_S1}&action=getStatus&id={aid}")

    otp_buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("💳 New Number", url=f"https://t.me/Hindustan_Otp_bot?start=1_{service}")],
        [InlineKeyboardButton("⏭ Next OTP", callback_data=f"CAS|{aid}|{number}|{service}")],
        [InlineKeyboardButton("⬅ Back", callback_data=f"SERVICE1|{service}")]
    ])
    await msg.reply_text(OTP_RECEIVED.format(SERVICES[service], number, text.split(":")[1]), reply_markup=otp_buttons)

    if service_price:
        curr_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')
        Orders.insert_one({"user": user_id, "service": SERVICES[service], "price": service_price, "time": curr_time})

        LOG_TEXT = f"""🌟 #PURCHASED

**Service:** `{SERVICES[service]}`
**Price:** `{service_price} ₹`
**Number:** +{number}
**Server:** `1`

**User:** {msg.from_user.mention}
**User-ID:** `{user_id}`
**Username:** @{msg.from_user.username}"""
    
    else:
        LOG_TEXT = f"""🔁 #NEW_OTP

**Service:** `{SERVICES[service]}`
**Number:** +{number}
**Server:** `1`

**User:** {msg.from_user.mention}
**User-ID:** `{user_id}`
**Username:** @{msg.from_user.username}"""

    await client.send_message(LOGS, LOG_TEXT)
    await dlt_buying(aid)


async def getOTP2(client: Client, msg: Message, service, number, aid, service_price=None, balance=None, lsms=0):
    user_id = msg.from_user.id
    global OTPS
    with OTP_LOCK:
        OTPS[aid] = time() + 300
    number = number[1:] if number[0] == "+" else number
    await msg.reply_text(NUMBER_TEXT.format(SERVICES2[service], number))

    sms = []
    while len(sms) <= lsms:
        if (aid in OTPS.keys()) and (time() >= OTPS[aid]):
            try:
                res, status_code = await afetchcode(f'https://5sim.net/v1/user/cancel/{aid}')
            except:
                status_code = 200
            if status_code == 200:
                try:
                    btn = InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data=f"SERVICE2|{service}")]])
                    await msg.reply_text("✅ **Successfully Cancelled OTP.**", reply_markup=btn)
                except:
                    try:
                        await msg.reply_text("✅ **Successfully Cancelled OTP.**", reply_markup=btn)
                    except:
                        pass
                if service_price:
                    balance = UsersCol.find_one({"_id": user_id})["balance"]
                    balance += service_price
                    UsersCol.update_one({"_id": user_id}, {"$set": {"balance": balance}})

                LOG_TEXT = f"""❌ #OTP_CANCELLED

**Service:** `{SERVICES2[service]}`
**Number:** +{number}
**Server:** `2`

**User:** {msg.from_user.mention}
**User-ID:** `{msg.from_user.id}`
**Username:** @{msg.from_user.username}"""
                await client.send_message(LOGS, LOG_TEXT)
            await dlt_buying(aid)
            return
        await sleep(3)
        text, status_code = await afetchcode(f'https://5sim.net/v1/user/check/{aid}')

        if text["status"] == "CANCELED":
            await dlt_buying(aid)
            return

        elif text["status"] in ("FINISHED", "TIMEOUT"):
            order_buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("💳 New Number", url=f"https://t.me/Hindustan_Otp_bot?start=2_{service}")],
                [InlineKeyboardButton("⬅ Back", callback_data=f"SERVICE2|{service}")]
            ])
            await msg.reply_text("✅ ** This order is Completed.**", reply_markup=order_buttons)
            await dlt_buying(aid)
            return

        elif len(text["sms"]) == (lsms + 1):
            lsms += 1
            sms = text["sms"]
            break

    otp_buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("💳 New Number", url=f"https://t.me/Hindustan_Otp_bot?start=2_{service}")],
        [InlineKeyboardButton("⏭ Next OTP", callback_data=f"CAS2|{aid}|{number}|{service}|{lsms}")],
        [InlineKeyboardButton("⬅ Back", callback_data=f"SERVICE2|{service}")]
    ])
    await msg.reply_text(OTP_RECEIVED.format(SERVICES2[service], number, sms[-1]["code"]), reply_markup=otp_buttons)

    if service_price:
        curr_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')
        Orders.insert_one({"user": user_id, "service": SERVICES2[service], "price": service_price, "time": curr_time})

        LOG_TEXT = f"""🌟 #PURCHASED

**Service:** `{SERVICES2[service]}`
**Price:** `{service_price} ₹`
**Number:** +{number}
**Server:** `2`

**User:** {msg.from_user.mention}
**User-ID:** `{msg.from_user.id}`
**Username:** @{msg.from_user.username}"""
    
    else:
        LOG_TEXT = f"""🔁 #NEW_OTP

**Service:** `{SERVICES2[service]}`
**Number:** +{number}
**Server:** `2`

**User:** {msg.from_user.mention}
**User-ID:** `{msg.from_user.id}`
**Username:** @{msg.from_user.username}"""

    await client.send_message(LOGS, LOG_TEXT)
    await dlt_buying(aid)

async def dlt_buying(aid):
    global OTPS
    try:
        del OTPS[aid]
    except:
        pass


def services_markup(services: dict, page_no: int, suffix: str = None, trailer=True, s="1"):
    keys, values = list(services.keys()), list(services.values())
    keys_len = len(keys)
    keys, values = (keys[(page_no * 18):((page_no + 1) * 18)]), values[(page_no * 18):((page_no + 1) * 18)]
    services_btn = []
    for i in range(9 if len(keys) >= 18 else len(keys)//2):
        btn = [
            InlineKeyboardButton(values[i * 2], callback_data=f"SERVICE{s}|{keys[i * 2]}"),
            InlineKeyboardButton(values[(i * 2) + 1], callback_data=f"SERVICE{s}|{keys[(i * 2) + 1]}")
        ]
        services_btn.append(btn)

    if len(keys) % 2:
        services_btn.append([InlineKeyboardButton(values[-1], callback_data=f"SERVICE{s}|{keys[-1]}")])

    if trailer:
        nextm = "NEXT"
        prevm = "PREV"
        if suffix:
            nextm += suffix
            prevm += suffix
        if page_no == 0:
            if len(services) < 18:
                trailer = [InlineKeyboardButton("• ʙᴀᴄᴋ •", callback_data="back")]
            else:
                trailer = [
                    InlineKeyboardButton("• ʙᴀᴄᴋ •", callback_data="back"),
                    InlineKeyboardButton("▷", callback_data=f"{nextm}|{page_no+1}")
                ]
        elif ((keys_len%18 == 0) and (page_no == ((keys_len//18) - 1))) or (len(services_btn) < 9):
            trailer = [
                InlineKeyboardButton("◁", callback_data=f"{prevm}|{page_no-1}"),
                InlineKeyboardButton("• ʙᴀᴄᴋ •", callback_data="back")
            ]
        else:
            trailer = [
                InlineKeyboardButton("◁", callback_data=f"{prevm}|{page_no-1}"),
                InlineKeyboardButton("• ʙᴀᴄᴋ •", callback_data="back"),
                InlineKeyboardButton("▷", callback_data=f"{nextm}|{page_no+1}")
            ]
        services_btn.append(trailer)
    
    return InlineKeyboardMarkup(services_btn)
