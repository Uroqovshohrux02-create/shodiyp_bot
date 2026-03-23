import asyncio
from aiogram import Bot, Dispatcher, types, F
from cryptography.fernet import Fernet

# Sizning bot tokeningiz
API_TOKEN = "8778035897:AAGBeXmpBJt_FWO4erVsP47XxRSSLK1nm_s"
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

def encrypt_msg(message: str):
    key = Fernet.generate_key()
    f = Fernet(key)
    return f.encrypt(message.encode()).decode(), key.decode()

@dp.message(F.text == "/start")
async def start(message: types.Message):
    await message.answer("🔐 Salom! Matn yuboring, uni shifrlab beraman.")

@dp.message(F.text)
async def handle_msg(message: types.Message):
    try:
        s, k = encrypt_msg(message.text)
        await message.answer(f"🔒 Shifr:\n`{s}`\n\n🔑 Kalit: `{k}`", parse_mode="Markdown")
    except:
        await message.answer("Xatolik yuz berdi.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
