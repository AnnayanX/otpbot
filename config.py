from os import getenv

ENVIRONMENT = False

API_ID = 25981592
API_HASH = "709f3c9d34d83873d3c7e76cdd75b866"

if ENVIRONMENT:
    BOT_TOKEN = getenv('BOT_TOKEN')
    BOT_USERNAME = getenv("BOT_USERNAME")
    OWNER_ID = int(getenv('OWNER_ID', 5836841532))
    CHANNEL = getenv('CHANNEL')
    SUPPORT = getenv('SUPPORT')
    PAYMENT_QR = getenv('PAYMENT_QR')
    GATEWAY_API_KEY = getenv('GATEWAY_API_KEY')
    API_KEY_S1 = getenv('API_KEY_S1')
    API_KEY_S2 = getenv('API_KEY_S2')
    LOGS = int(getenv("LOGS", -1001983402883))

else:
    BOT_TOKEN = "6693127174:AAGaP__6UcbFo0VfHF1Sa213VJtC5T2ZlPU"   # Fill BOT_TOKEN here ( Get it from @BotFather )
    BOT_USERNAME = "Hindustan_Otp_bot"
    API_KEY_S1 = "8605865c98cf0d954b2b1f93a8a33349"
    API_KEY_S2 = "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjY1OTAwMTksImlhdCI6MTY5NTA1NDAxOSwicmF5IjoiY2Q0NzEyNDY2ODZlNTRlZGMwNWEyOTA1YjM0NzFhNDUiLCJzdWIiOjE3NTM2MTV9.OlXPJMQMDSKPmKmdao6KbxCgTuuOt_RKpyq90yS1sIDsKB7UUV8UA-Q7cf87xa1hKNxiEphQ2nqkcWj66hsHvcvxwAehVM0VgS0XpRoKBPnIILfJWlubLExFeO9NFSFs-vvcomyAh6KEvWsU5exr5S2SK1-WTnRA3T_rHMeIfJ7fI3y8bwcB6_B79RsAle4srqfmCSJk9fGG-hQhND8Lmg4Hl9-gKk5k5VDE9rZ4zU0ksM4z5L1ueLsrryRp47jo9UWLXkgEhIzBhUSt_LdwEF039hAeo2ORFueqwW3c8YQ0DcmOdObraz_Po4KZbrOk9pBLPmBsT1TGHfH4N1eQWQ"
    GATEWAY_API_KEY = "78cd31d209ff4f08890fce59dd9c849c"
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