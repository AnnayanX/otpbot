from os import getenv

ENVIRONMENT = False

API_ID = 25981592
API_HASH = "709f3c9d34d83873d3c7e76cdd75b866"

if ENVIRONMENT:
    BOT_TOKEN = getenv('BOT_TOKEN')
    BOT_USERNAME = getenv("BOT_USERNAME")
    OWNER_ID = int(getenv('OWNER_ID', 5890958471))
    CHANNEL = getenv('CHANNEL')
    SUPPORT = getenv('SUPPORT')
    PAYMENT_QR = getenv('PAYMENT_QR')
    GATEWAY_API_KEY = getenv('GATEWAY_API_KEY')
    API_KEY_S1 = getenv('API_KEY_S1')
    API_KEY_S2 = getenv('API_KEY_S2')
    LOGS = int(getenv("LOGS", -1001983402883))

else:
    BOT_TOKEN = "6693127174:AAGdXknv1ByxGi_NJQp40T_JDHVbkMtAsMw"   # Fill BOT_TOKEN here ( Get it from @BotFather )
    BOT_USERNAME = "Hindustan_Otp_bot"
    API_KEY_S1 = "cb6968481925290420535b470082f347"
    API_KEY_S2 = "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzA1NTUwNTcsImlhdCI6MTY5OTAxOTA1NywicmF5IjoiZThhZDY2NmQxZDBmYmQwMWEyOTUzMTk1YjI3OWEzYjMiLCJzdWIiOjE3MjE0ODh9.k0p6kfTH-CzRdmqnWIgYMyxuStfQO4jyr3y3py-t8mvLwv8kAzQWNNvHoowYK5UkcSN591kfFJI1q0-18a1G6Aqni5-4wsjbQ3FmjCeiOj_DeSnlO-4xloaTD6Gmk3sc4zPxf9Rh6I4mQdf8vsbRmKaCRSqbGBuMDAdn5SQdg1Uy8MaGaJTTvRaEmEbDgNi6lJCMLEeRGJqBy9NeGPCVMT3J_C13lFamsiAXjxthQcBQxBt95KUWiY2DALtegOpJ-r-9e53eE6t1La6nOvYy9Bh-KG8f9UT4hmYMZbyEH8P09Y17s6EKbMJ8UF8uTQzMgCMOaphhPXeDsv46FCLtSA"
    GATEWAY_API_KEY = "78cd31d209ff4f08890fce59dd9c849c"
    OWNER_ID = 5890958471
    CHANNEL = "https://t.me/HindustanOtp"
    SUPPORT = "https://t.me/Hindustan_Support"
    PAYMENT_QR = "https://te.legra.ph/file/8e9dd918a8e9a90e44458.jpg"
    LOGS = -1001983402883

DEVS = [5991613885]
DEVS.append(OWNER_ID)
FORCESUB = CHANNEL.split("/")[-1]

headers = {
    'Authorization': f'Bearer {API_KEY_S2}',
    'Accept': 'application/json',
}
