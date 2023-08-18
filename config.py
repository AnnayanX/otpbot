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
    API_KEY_S1 = "193b40046b3a8791c832fa2a8301e749"
    API_KEY_S2 = "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjMzMTEwNzcsImlhdCI6MTY5MTc3NTA3NywicmF5IjoiZDE1ZTRiY2NjZWMwOGYxZThmN2ZjNzlhNGVkOWYwOTMiLCJzdWIiOjE3NTM2MTV9.rguh-WyQqIHIBISwMB67s4JiE2h2gsONJFlajKPa5llo-q27UdJtyGvdWkTLswJRq0t0JVAJ7Asdkebrn3iNxbFW4Ti56EvLQUsPuMbA7_xPwTZTyKEOSH-eK-m1PPgXxsC3PfSNao2kqmnm23TIfXdlbpzriHJxTXhjGNdqiwwRBQHSgCGKWqkCsXgQideYcUGuUJdn4ubqZ5MGgaxPFust7UfcbK6OCNsq6lW-C9hNk8zKJ7jUbQ4NGDmvEiwCvY9um4G2ePZOofQfnzxoALthDD4vzk59vBUp1Voi_GoLwecX_Yejdwh7kDYLEZ-pw6JcNKEwCaowCmHWabwLQg"
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
