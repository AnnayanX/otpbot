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
    API_KEY_S1 = "d07081cb63c28fa954153ddfc33c9210"
    API_KEY_S2 = "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjQ3ODczMDksImlhdCI6MTY5MzI1MTMwOSwicmF5IjoiZDE1ZTRiY2NjZWMwOGYxZThmN2ZjNzlhNGVkOWYwOTMiLCJzdWIiOjE3NTM2MTV9.h372NPCFp0D7c3KDY3zHs8jTtsaCvTHIqO5zJngi59Jc0L6zqUGEftQiGTpelVrLNDD4CwGW-9rhn_A6MkqbxWHK7FOF54loXlmLaQc0NvQF_usYO0VfMh3lntK9feArXKV5LW8_hF3dZu-TfzLei65BnxboHitmDHp8sdS3JF6eWmi2as-mzJPGV99-14HllLCWDKt0KLV6zXB5DvdTQuo01CWSl382zCm4wFKdPB-XEK2cn7lHTAqFXy9iW_ymACPceOfDcPvHlXQxQPutt6HLtFUBQhRJ_FLBWEvUzW3F0tDaBXvbmB7Lj4GwN2ARJcZT976vyDn9dOcSbwx7Aw"
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
