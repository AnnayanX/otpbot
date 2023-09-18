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
    API_KEY_S1 = "1e6d3c05418295c4a45c742d3d0c3c1e"
    API_KEY_S2 = "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjUyMDQ3MDcsImlhdCI6MTY5MzY2ODcwNywicmF5IjoiY2Q0NzEyNDY2ODZlNTRlZGMwNWEyOTA1YjM0NzFhNDUiLCJzdWIiOjE3NTM2MTV9.XlkIxmjfpOCJJPuFU45CMpiecjc8cOmJlIPBbL5c6qzm2Q3UGPcwxG_PZ1VcCYERY03OPgakItXPQ5uEh5udLVRjgqclxENfEL9eSzxkCfFbhtgYb4NxKvVKJ86sbfMk7IrPgYQp_BpI7jrHr6PKcc0VM5BEYaKNUwB7oRNpVKeu2oEhOP8kCEj4RbtdNpoMNBir2e7HPfaakweHw3nRfdvnMsgAGiz4wL6IMNtgQKYDenLFXWeAVGjsMXqseYXJozMcgiOdHQd8koRtySnZ6qEEURMJx2UNMzQIgjPbiazE1eLLUQ2yFXrfEqYLYBjIvmh_z3iVLvn8SIN59liqzw"
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