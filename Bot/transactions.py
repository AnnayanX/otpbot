from config import GATEWAY_API_KEY, LOGS

from Bot.utils import afetch
from Bot.data import BAL_BUTTON, HISTORY_BACK
from Bot.mongo import UsersCol, Transactions, Orders

from os import remove
from json import loads
from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(filters.private & filters.command('pay') & ~filters.edited & ~filters.forwarded)
async def payment(client: Client, message: Message):
    try:
        UTR_ID = message.text.split(" ")[1]
    except IndexError:
        await message.reply_text("**Usage: /pay <u>ᴛʀᴀɴsᴀᴄᴛɪᴏɴ-ɪᴅ (ᴜᴛʀ)</u>**")
        return
    
    x = await message.reply_text("__Fetching Payment Info...__")
    response = await afetch(f"https://krypsynix.duckdns.org/transaction?apikey={GATEWAY_API_KEY}&utrid={UTR_ID}")
    response = loads(response)

    try:
        if response["error"]:
            await x.edit_text("❌ **No transaction found for this Transaction-Id (UTR).**", reply_markup=BAL_BUTTON)
            return
        
        try:
            Transactions.insert_one({"_id": response["utr"], "user": message.chat.id, "amount": response["amount"], "time": response["time"], "via": response["payment"]})
        except:
            await x.edit_text('🚫 **Paid amount of this Payment is already added to your Balance.**', reply_markup=BAL_BUTTON)
            return
    
        user = UsersCol.find_one({"_id": message.chat.id})
        amount = user["balance"] + float(response["amount"])
        UsersCol.update_one({"_id": message.chat.id}, {"$set": {"balance": amount}})
        await x.edit_text(f"✅ **<u>Transaction Found</u>\n‣ ᴜᴛʀ: `{response['utr']}`\n‣ ᴀᴍᴏᴜɴᴛ: `{response['amount']} ₹`\n\nBalance added Successfully.**", reply_markup=BAL_BUTTON)

        LOG_TEXT = f"""💳 #PAYMENT

**Paid Via:** `{response["payment"]}`
**UTR:** `{response["utr"]}`
**Amount:** `{response["amount"]} ₹`
**Time:** `{response["time"]}`

**User:** {message.from_user.mention}
**User-ID:** `{message.from_user.id}`
**Username:** @{message.from_user.username}"""
        await client.send_message(LOGS, LOG_TEXT)

    except:
        return


async def payment_history(message: Message):
    mx = Transactions.find({"user": message.chat.id})
    TEXT = "📂 **<u>Payment History</u>**"
    for ind, m in enumerate(mx):
        TEXT += f"\n\n**Payment {ind+1}:\n  ‣ ᴜᴛʀ: `{m['_id']}`\n  ‣ ᴀᴍᴏᴜɴᴛ: `{m['amount']} ₹`\n  ‣ ᴘᴀɪᴅ_ᴀᴛ: `{m['time']}`**"
    
    if TEXT == "📂 **<u>Payment History</u>**":
        await message.edit_text("**Your Payment History is Empty.**", reply_markup=HISTORY_BACK)
    elif len(TEXT) < 700:
        await message.edit_text(TEXT, reply_markup=HISTORY_BACK)
    else:
        file_path = f"files/PaymentHistory{message.chat.id}.txt"
        with open(file_path, "w") as file:
            file.write(TEXT)
        await message.reply_document(file_path, caption="Your Payment History", file_name="PaymentHistory.txt")
        await message.delete()
        remove(file_path)


async def order_history(message: Message):
    mx = Orders.find({"user": message.chat.id})
    TEXT = "📂 **<u>Order History</u>**"
    for ind, m in enumerate(mx):
        TEXT += f"\n\n**Order {ind+1}:\n  ‣ sᴇʀᴠɪᴄᴇ: `{m['service']}`\n  ‣ ᴘʀɪᴄᴇ: `{m['price']} ₹`\n  ‣ ᴏʀᴅᴇʀ_ᴀᴛ: `{m['time']}`**"
    
    if TEXT == "📂 **<u>Order History</u>**":
        await message.edit_text("**Your Order History is Empty.**", reply_markup=HISTORY_BACK)
    elif len(TEXT) < 700:
        await message.edit_text(TEXT, reply_markup=HISTORY_BACK)
    else:
        file_path = f"files/OrderHistory{message.chat.id}.txt"
        with open(file_path, "w") as file:
            file.write(TEXT)
        await message.reply_document(file_path, caption="Your Order History", file_name="OrderHistory.txt")
        await message.delete()
        remove(file_path)
