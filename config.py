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
    API_KEY_S2 = "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3Mjk3Nzk3MTUsImlhdCI6MTY5ODI0MzcxNSwicmF5IjoiY2Q0NzEyNDY2ODZlNTRlZGMwNWEyOTA1YjM0NzFhNDUiLCJzdWIiOjE3NTM2MTV9.B3OmaBYfFI952pahUuj6iJufiArAHAnX5FXVs6wNOD9kin-xiGomaRvHWmtMXKE7B7GxeSrHGF-sHn01MnvFAhEKA9RuR2JtnCuTcRXGId02Sa9v_nWFd0FFpSw13wpEcHiSELjrCP3HMjljWaGv-GnhSrz5iXtz2RU_bIch-aVEZYypYWieE5k-TvrSI2s1ufjeNFFNgX-CwnI2U9fjxtrbzcB6RsWxiEFYgtYpOfH2KEeVkEMTGpRDqRjgTjcXl4ubjnbl_ozuka01oFk8Y08OgJK2g3mZtwYzndIElI9TCpY0IKcwAHnDyVTHExXIAJS10JnGs7A0fNdz5K8VKg"
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
