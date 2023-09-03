from aiohttp import ClientSession

from config import PAYMENT_QR, OWNER_ID, API_KEY_S1, headers, LOGS

from asyncio import run
from threading import Thread

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery

from Bot.data import *
from Bot.mongo import UsersCol, add_service, rm_service
from Bot.transactions import payment_history, order_history
from Bot.utils import services_markup, afetch, afetchcode, getOTP, getOTP2


@Client.on_callback_query(filters.regex(r"mbalance|back|add_balance"))
async def _callbacks(_, cbq: CallbackQuery):
    if cbq.data == "mbalance":
        user = cbq.from_user
        muser = UsersCol.find_one({"_id": user.id})
        await cbq.edit_message_text(BALANCE_TEXT.format(user.first_name, user.id, muser["balance"]), reply_markup=BALANCE_BUTTON)
    
    elif cbq.data == "back":
        await cbq.edit_message_text(START_TEXT.format(cbq.from_user.mention), reply_markup=START_BUTTON)

    else:
        await cbq.message.reply_photo(PAYMENT_QR, caption=PAYMENT_TEXT)


@Client.on_callback_query(filters.regex(r"NEXT.|PREV."))
async def _np_callback(_, cbq: CallbackQuery):
    page_no = int(cbq.data.split("|", 1)[1])

    if cbq.data[4] == "P":
        buttons = services_markup(SERVICES, page_no, "P")
    
    elif cbq.data[4] == "M":
        user = UsersCol.find_one({"_id": cbq.from_user.id})
        services = dict(map(lambda x: (x, SERVICES[x]), user["fav1"]))
        buttons = services_markup(services, page_no, "M")
    
    elif cbq.data[4] == "Z":
        user = UsersCol.find_one({"_id": cbq.from_user.id})
        services = dict(map(lambda x: (x, SERVICES2[x]), user["fav2"]))
        buttons = services_markup(services, page_no, "Z", s="2")
    
    elif cbq.data[4] == "T":
        buttons = services_markup(TOP_SERVICES, page_no, "T")

    elif cbq.data[4] == "R":
        buttons = services_markup(RUMMY_SERVICES, page_no, "R")

    elif cbq.data[4] == "Y":
        buttons = services_markup(RUMMY_SERVICES2, page_no, "Y", s="2")

    elif cbq.data[4] == "K":
        buttons = services_markup(SERVICES2, page_no, "K")

    try:
        await cbq.edit_message_reply_markup(buttons)
    except:
        return


@Client.on_callback_query(filters.regex(r"SERVICE"))
async def _service_cbq(_, cbq: CallbackQuery):
    service = cbq.data.split("|", 1)[1]
    buttons = service_btn(service, cbq.data[7])
    try:
        if cbq.data.startswith("SERVICE1"):
            await cbq.edit_message_text(SERVICE_TEXT.format(SERVICES[service], service, SERVICE_PRICES[service]), reply_markup=buttons)
        else:
            await cbq.edit_message_text(SERVICE_TEXT.format(SERVICES2[service], service, SERVICE_PRICES2[service]), reply_markup=buttons)
    except:
        return


@Client.on_callback_query(filters.regex(r"FAVOURITE|REMOVEFAV"))
async def _addrmfav_cbq(_, cbq: CallbackQuery):
    query, service = cbq.data.split("|", 1)
    if query.startswith("FAVOURITE"):
        text = add_service(cbq.from_user.id, service, query[-1])
    else:
        text = rm_service(cbq.from_user.id, service, query[-1])
    await cbq.answer(text, show_alert=True)


@Client.on_callback_query(filters.regex(r"allS|topS|rummyS|favS"))
async def _s_cbq(_, cbq: CallbackQuery):
    query = cbq.data

    if query == "allS":
        buttons = services_markup(SERVICES, 0, "P")
        text = SERVICES_TEXT.format(len(SERVICES))
    
    elif query == "allS2":
        buttons = services_markup(SERVICES2, 0, "K", s="2")
        text = SERVICES_TEXT.format(len(SERVICES2))

    elif query == "topS":
        text = TSERVICES_TEXT
        buttons = services_markup(TOP_SERVICES, 0, "T")

    elif query == "topS2":
        text = TSERVICES_TEXT
        buttons = services_markup(TOP_SERVICES2, 0, "X", s="2")

    elif query.startswith("rummyS"):
        text = RSERVICES_TEXT
        if query[-1] == "2":
            buttons = services_markup(RUMMY_SERVICES2, 0, "Y", s="2")
        else:
            buttons = services_markup(RUMMY_SERVICES, 0, "R")
    
    elif query.startswith("favS"):
        s = query[-1]
        user = UsersCol.find_one({"_id": cbq.from_user.id})
        if len(user[f"fav{s}"]) == 0:
            await cbq.answer("Your Favourite Services List is empty.", show_alert=True)
            return
        await cbq.answer("Fetching your Favourite Services...", show_alert=True)
        text = FSERVICES_TEXT
        if s == "1":
            services = dict(map(lambda x: (x, SERVICES[x]), user["fav1"]))
            buttons = services_markup(services, 0, "M")
        else:
            services = dict(map(lambda x: (x, SERVICES2[x]), user["fav2"]))
            buttons = services_markup(services, 0, "Z", s="2")

    try:
        await cbq.edit_message_text(text, reply_markup=buttons)
    except:
        return


@Client.on_callback_query(filters.regex(r"BUY"))
async def _buys_cbq(bot: Client, cbq: CallbackQuery):
    service = cbq.data.split("|", 1)[1]
    balance = UsersCol.find_one({"_id": cbq.from_user.id})["balance"]
    service_price = SERVICE_PRICES[service] if cbq.data[3] == "1" else SERVICE_PRICES2[service]
    if balance < service_price:
        await cbq.edit_message_text(INSUFF_BALANCE, reply_markup=INSUFF_BUTTON)
        return

    if cbq.data[3] == "1":
        res = await afetch(f"https://fastsms.su/stubs/handler_api.php?api_key={API_KEY_S1}&action=getNumber&service={service}&country=22")

        try:
            if res == "NO_BALANCE":
                await bot.send_message(OWNER_ID, "**Please add Balance to your <u>fastsms.su</u> Account.**")
                await cbq.edit_message_text("💤 **Bot is under Maintainance. Please wait for few minutes...**", reply_markup=BACK_BUTTON)
            elif res.startswith("ACCESS_NUMBER:"):
                balance -= service_price
                UsersCol.update_one({"_id": cbq.from_user.id}, {"$set": {"balance": balance}})
                aid, number = res.split(":")[1:]
                # MULTI-THREADING
                thread = Thread(target=run, args=(getOTP(bot, cbq, service, number, aid, service_price, balance),))
                thread.start()
            else:
                await cbq.edit_message_text("❌ **There are no numbers with the specified parameters, please try again after few minutes...**", reply_markup=BACK_BUTTON)
        except:
            return
    
    else:
        async with ClientSession() as session:
            async with session.get(f'https://5sim.net/v1/user/buy/activation/india/{OPERATORS2[service]}/{service}', headers=headers) as resp:
                res = await resp.text()
                status_code = resp.status

        if (status_code == 200) and (res != "no free phones"):
            balance -= service_price
            UsersCol.update_one({"_id": cbq.from_user.id}, {"$set": {"balance": balance}})
            res = await resp.json()
            number, aid = res["phone"], res["id"]
            # MULTI-THREADING
            thread = Thread(target=run, args=(getOTP2(bot, cbq, service, number, aid, service_price, balance),))
            thread.start()
        elif res == "not enough user balance":
            await bot.send_message(OWNER_ID, "**Please add Balance to your <u>5sim.net</u> Account.**")
            await cbq.edit_message_text("💤 **Bot is under Maintainance. Please wait for few minutes...**", reply_markup=BACK_BUTTON)
        else:
            await cbq.edit_message_text("❌ **There are no numbers with the specified parameters, please try again after few minutes...**", reply_markup=BACK_BUTTON)


@Client.on_callback_query(filters.regex(r"CAS"))
async def _cas_cbq(bot: Client, cbq: CallbackQuery):
    await cbq.answer("Please Wait...", show_alert=True)
    mx = cbq.data.split("|")

    if mx[0][-1] == "2":
        if mx[2] == "8":
            try:
                res, status_code = await afetchcode('https://5sim.net/v1/user/cancel/' + mx[1])
            except:
                btn = InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data=f"SERVICE2|{mx[3]}")]])
                await cbq.edit_message_text("✅ **Successfully Cancelled OTP.**", reply_markup=btn)
                return
            if status_code == 200:
                try:
                    btn = InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data=f"SERVICE2|{mx[3]}")]])
                    await cbq.edit_message_text("✅ **Successfully Cancelled OTP.**", reply_markup=btn)
                    balance = UsersCol.find_one({"_id": cbq.from_user.id})["balance"]
                    balance += SERVICE_PRICES2[mx[3]]
                    UsersCol.update_one({"_id": cbq.from_user.id}, {"$set": {"balance": balance}})
                except:
                    return
            else:
                return
        else:
            thread = Thread(target=run, args=(getOTP2(bot, cbq, mx[4], mx[3], mx[1], lsms=int(mx[-1])),))
            thread.start()

    else:
        res = await afetch(f"https://fastsms.su/stubs/handler_api.php?api_key={API_KEY_S1}&action=setStatus&id={mx[1]}&status={mx[2]}")
        if res == "ACCESS_CANCEL":
            try:
                btn = InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data=f"SERVICE1|{mx[3]}")]])
                await cbq.edit_message_text("✅ **Successfully Cancelled OTP.**", reply_markup=btn)
                balance = UsersCol.find_one({"_id": cbq.from_user.id})["balance"]
                balance += SERVICE_PRICES[mx[3]]
                UsersCol.update_one({"_id": cbq.from_user.id}, {"$set": {"balance": balance}})
            except:
                return
        elif res == "ACCESS_CANCEL_ALREADY":
            return
        # elif res == "TIMED_OUT":
        #     await cbq.edit_message_text("⌛ **Request Timed Out.**", reply_markup=BACK_BUTTON)
        elif res == "ACCESS_WAITING":
            thread = Thread(target=run, args=(getOTP(bot, cbq, mx[4], mx[3], mx[1]),))
            thread.start()
        elif len(res) < 30:
            return


@Client.on_callback_query(filters.regex(r"history"))
async def _history_cbq(_, cbq: CallbackQuery):
    if cbq.data[0] == "p":
        await cbq.answer("Fetching Payment History...", show_alert=True)
        await payment_history(cbq.message)

    elif cbq.data[0] == "o":
        await cbq.answer("Fetching Order History...", show_alert=True)
        await order_history(cbq.message)

    else:
        try:
            await cbq.edit_message_text(HISTORY_TEXT, reply_markup=HISTORY_BUTTON)
        except:
            return
