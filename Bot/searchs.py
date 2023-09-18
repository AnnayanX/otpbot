from Bot.data import SERVICES, SERVICES2
from Bot.utils import services_markup

from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(filters.private & filters.command(['ser', 'ser1', 'ser2']) & ~filters.forwarded)
async def _search(_, message: Message):
    try:
        cmd, text = message.text.split(" ", 1)[:2]
    except:
        await message.reply_text("**Usage:** /search sᴇʀᴠɪᴄᴇ_ɴᴀᴍᴇ")
        return

    x = await message.reply_text("🔎 __Searching...__")
    results = {}
    count = 0
    serm, s = (SERVICES2, "2") if cmd[-1] == "2" else (SERVICES, "1")

    for word in text.split(" "):
        if count >= 36:
            break
        for key, service in serm.items():
            if count >= 36:
                break
            if word.lower() in service.lower():
                results[key] = service
                count += 1

    await x.delete()
    if count > 0:
        buttons = services_markup(results, 0, trailer=False, s=s)
        await message.reply_text("**Here is your <u>Searched Services</u>.**", reply_markup=buttons)
    else:
        await message.reply_text("**No Services Found for your Query.**")
