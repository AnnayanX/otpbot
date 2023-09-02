from os import getenv

ENVIRONMENT = False

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
    BOT_TOKEN = "6693127174:AAFaNGdoRzu3YvNhf5woOApM4TRUXeMumio"   # Fill BOT_TOKEN here ( Get it from @BotFather )
    API_KEY_S1 = "88c8ae726dc7cfcd07440accd34ffe05"
    API_KEY_S2 = "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjUxNzA5MzYsImlhdCI6MTY5MzYzNDkzNiwicmF5IjoiNmUzZTdhNGJmZjlhODVkOWFlOWFmNGU5YTdhN2M0MmIiLCJzdWIiOjE3NTM2MTV9.Y2FE729jeg_rWqI-nwBl4kJCQFLAumRo1rbzrGzxfq9cIe3dR-aNZE20VdOsvck_34wxW8iy1fJn55zgtHpxtBfur32aVGgwNhX60buyvNbN1lqj6v0aCPlbnw0T5S7gBhQv8M23CBSUaZbeSdOYIh2KIhPICGbCnhk0fdrxDUSNYrOWSvCH94JtDTaQ2eZJSrBGJerbeqFTqkc_jCLMxvLPkTH4YZglguvwysAwLNSZ5k4uHLtNbZZkVBIHCim4kDKp0KtAv5V0qm5uDm0U_Yogkcbf3H7dnf69mlhi7BPxOix7EoKeZj2MR2mWWquMK0KO9VfpRLteTHdvztkkCw"
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
