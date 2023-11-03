import requests

from Bot.mongo import OthersCol
from config import CHANNEL, SUPPORT, API_KEY_S1, BOT_USERNAME
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


try:
    OTP_PRICE = OthersCol.find_one({"_id": "price"})["price"]
except:
    OthersCol.insert_one({"_id": "price", "price": 1.5})
    OTP_PRICE = 1.5

JOIN_MESSAGE = """**Please Join My Updates Channel to use this Bot!**

Due to Telegram Users Traffic, Only Channel Subscribers can use the Bot!"""

START_TEXT = """**Hey, {0} !

‣ This is a Biggest <u>OTP Seller Bot</u>.

‣ It has an Amazing Collection of All Application Otp and Ready Made Account with Automated/Instant System Got Deposit and Trusted Shop.**"""


START_BUTTON = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("All Services (S1)", callback_data="allS"),
        InlineKeyboardButton("Top Services (S1)", callback_data="topS")
    ],
    [
        InlineKeyboardButton("Rummy Services (S1)", callback_data="rummyS"),
        InlineKeyboardButton("Favourite Services (S1)", callback_data="favS1")
    ],
    [
        InlineKeyboardButton("All Services (S2)", callback_data="allS2"),
        InlineKeyboardButton("Top Services (S2)", callback_data="topS2")
    ],
    [
        InlineKeyboardButton("Rummy Services (S2)", callback_data="rummyS2"),
        InlineKeyboardButton("Favourite Services (S2)", callback_data="favS2")
    ],
    [InlineKeyboardButton("Balance / Add Balance", callback_data="mbalance")],
    [InlineKeyboardButton("History", callback_data="history")],
    [
        InlineKeyboardButton("Updates", url=CHANNEL),
        InlineKeyboardButton("Support", url=SUPPORT)
    ]
  ])

BACK_BUTTON = InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="back")]])

BALANCE_TEXT = "**💳 <u>Your Balance</u>\n\n► Name: `{0}`\n► Id: `{1}`\n► Balance: `{2} ₹`**"

BALANCE_BUTTON = InlineKeyboardMarkup([
    [InlineKeyboardButton("Add Balance", callback_data="add_balance")],
    [InlineKeyboardButton("⬅ Back", callback_data="back")]
])

PAYMENT_TEXT = "🔎 **Scan This QR And Pay.\n‣ After it use command mentioned below.\n\n‣ /pay <u>ᴛʀᴀɴsᴀᴄᴛɪᴏɴ-ɪᴅ (ᴜᴛʀ)</u>**"

BAL_BUTTON = InlineKeyboardMarkup([[InlineKeyboardButton("💳 Balance", callback_data="mbalance")]])

INSUFF_BALANCE = "**❌ <u>Insufficient Balance</u>\n\nClick on below button to <u>Check</u> or <u>Add Balance</u>.**"

INSUFF_BUTTON = InlineKeyboardMarkup([[InlineKeyboardButton("Balance / Add Balance", callback_data="mbalance")]])

SERVICES_TEXT = "🚀 **<u>Services</u> (Total Services: {0})\n\nClick on Service button to get it's <u>OTP</u>.**"

SERVICES = requests.get(f"https://fastsms.su/stubs/handler_api.php?api_key={API_KEY_S1}&action=getServices").json()
SERVICES = dict(sorted(SERVICES.items(), key=lambda x:x[1]))

SERVICE_TEXT = "🚀 **<u>Service Info</u>\n\n► Name: `{0}`\n► Key: `{1}`\n► Price Per OTP:  `{2} ₹`**"

def service_btn(service, s="1"):
    btn = InlineKeyboardMarkup([
        [InlineKeyboardButton("💳 Get OTP", url=f"https://t.me/{BOT_USERNAME}?start={s}_{service}")],
        [InlineKeyboardButton("🌟 Add to Favourite", callback_data=f"FAVOURITE{s}|{service}")],
        [InlineKeyboardButton("🗑 Remove from Favourite", callback_data=f"REMOVEFAV{s}|{service}")],
        [InlineKeyboardButton("⬅ Back", callback_data="back")]
    ])
    return btn

def getPrices():
    res = requests.get(f"https://fastsms.su/stubs/handler_api.php?api_key={API_KEY_S1}&action=getPrices&country=22").json()
    prices = {}
    for key, value in res["22"].items():
        prices[key] = float(list(value.keys())[0]) + OTP_PRICE
    return prices
SERVICE_PRICES = getPrices()

FSERVICES_TEXT = "🚀 **<u>Favourite Services</u>\n\nClick on Service button to get it's <u>OTP</u>.**"

TSERVICES_TEXT = "🚀 **<u>Top Services</u>\n\nClick on Service button to get it's <u>OTP</u>.**"

TOP_SERVICES = dict(map(lambda x: (x, SERVICES[x]), OthersCol.find_one({"_id": "top_service1"})["service"]))

NUMBER_TEXT = "🔁 **<u>GETTING OTP</u>\n\n► Service: `{0}`\n► Number: +{1}\n► Status: `STATUS_WAIT_CODE`**"
OTP_RECEIVED = "✅ **<u>OTP RECEIVED</u>\n\n► Service: `{0}`\n► Number: +{1}\n► OTP: `{2}`**"

RUMMY_SERVICES = {'nrm': '9 Rummy', 'crm': 'Classicrummy', 'der': 'Deccan Rummy', 'gru': 'Grummy', 'mmt': 'HolyRummy', 'jor': 'Joy Rummy', 'jgr': 'JungleeRummy', 'kpr': 'KhelPay rummy', 'rrm': 'Royally Rummy', 'rbr': 'RubyRummy', 'rua': 'Rummy Apna', 'rms': 'Rummy Ares', 'rmu': 'Rummy Bloc', 'rme': 'Rummy East', 'rsj': 'Rummy Glee', 'rmg': 'Rummy Gold', 'ruk': 'Rummy Khel', 'rmr': 'Rummy Master', 'rmd': 'Rummy Modern', 'rmn': 'Rummy Nabob', 'rmb': 'Rummy Noble', 'rmo': 'Rummy Tour', 'rmw': 'Rummy Wealth', 'rux': 'Rummy XL', 'rmp': 'Rummy perfect', 'rub': 'RummyBest', 'rmc': 'RummyCircle', 'ec': 'RummyCulture', 'fl': 'RummyLoot', 'ymy': 'RummyOla', 'rmy': 'Rummyes', 'rmt': 'Rummytime', 'tar': 'TapRummy'}
# RUMMY_SERVICES = dict(sorted(RUMMY_SERVICES.items(), key=lambda x:x[1]))

RSERVICES_TEXT = "🚀 **<u>Rummy Services</u>\n\nClick on Service button to get it's <u>OTP</u>.**"

HISTORY_TEXT = "📂 **<u>History</u>\n\nClick on below button to show it's History.**"

HISTORY_BUTTON = InlineKeyboardMarkup([
    [InlineKeyboardButton("💳 Payment History", callback_data="phistory")],
    [InlineKeyboardButton("🌟 Order History", callback_data="ohistory")],
    [InlineKeyboardButton("⬅ Back", callback_data="back")]
])

HISTORY_BACK = InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="history")]])


# ------------- SERVER 2 -------------
def m2():
    x = requests.get('https://5sim.net/v1/guest/products/india/any', headers={'Accept': 'application/json'}).json()
    mx = {}
    mx2 = {}
    mx3 = {}

    for m in x.items():
        mx[m[0]] = m[0].capitalize()
        mx2[m[0]] = m[1]['Price'] + OTP_PRICE
        mx3[m[0]] = "any"

    response = requests.get('https://5sim.net/v1/guest/prices', headers={'Accept': 'application/json',}).json()["india"]
    mx4 = {}

    for _, __ in response.items():
        try:
            mx[_]
            mx5 = {}
            for operator, value in __.items():
                mx5[operator] = value['cost']
            mx4[_] = mx5
        except:
            continue

    for service, operators in mx4.items():
        mx13 = min(operators, key=operators.get)
        mx2[service] = operators[mx13] + OTP_PRICE
        mx3[service] = mx13

    return mx, mx2, mx3

SERVICES2, SERVICE_PRICES2, OPERATORS2 = m2()

TOP_SERVICES2 = dict(map(lambda x: (x, SERVICES2[x]), OthersCol.find_one({"_id": "top_services2"})["services"]))

RUMMY_SERVICES2 = {'classicrummy': 'ClassicRummy', 'gullyrummy': 'GullyRummy', 'jungleerummy': 'JungleeRummy', 'royallyrummy': 'RoyallyRummy', 'rummy': 'Rummy', 'rummycircle': 'Rummycircle', 'rummyculture': 'Rummyculture', 'rummygold': 'Rummygold', 'rummyloot': 'Rummyloot', 'teenpattirummy3': 'TeenpattiRummy3'}
# RUMMY_SERVICES2 = dict(sorted(RUMMY_SERVICES2.items(), key=lambda x:x[1]))
