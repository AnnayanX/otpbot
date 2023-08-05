from os import getenv

ENVIRONMENT = True

API_ID = 25981592
API_HASH = "709f3c9d34d83873d3c7e76cdd75b866"

if ENVIRONMENT:
    BOT_TOKEN = getenv('BOT_TOKEN')
    OWNER_ID = int(getenv('OWNER_ID', 5836841532))
    CHANNEL = getenv('CHANNEL')
    SUPPORT = getenv('SUPPORT')
    PAYMENT_QR = getenv('PAYMENT_QR')
    GATEWAY_API_KEY = getenv('GATEWAY_API_KEY')
    API_KEY_S1 = getenv('API_KEY_S1')
    API_KEY_S2 = getenv('API_KEY_S2')
    LOGS = int(getenv("LOGS", -1001983402883))

else:
    BOT_TOKEN = ""   # Fill BOT_TOKEN here ( Get it from @BotFather )
    API_KEY_S1 = ""
    API_KEY_S2 = ""
    GATEWAY_API_KEY = ""
    OWNER_ID = 5836841532
    CHANNEL = "https://t.me/HindustanOtp"
    SUPPORT = "https://t.me/Hindustansuppourt"
    PAYMENT_QR = "https://te.legra.ph/file/8e9dd918a8e9a90e44458.jpg"
    LOGS = -1001983402883

DEVS = [5518687442]
DEVS.append(OWNER_ID)
FORCESUB = CHANNEL.split("/")[-1]

headers = {
    'Authorization': f'Bearer {API_KEY_S2}',
    'Accept': 'application/json',
}