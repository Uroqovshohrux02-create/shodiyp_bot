import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from cryptography.fernet import Fernet

# Bot tokeningizni o'zgartirmang
API_TOKEN = '8778035897:AAGBeXmpBJt_FW04erV_...' 

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("🔒 Salom! Matn yuborsangiz - shifrlayman.\n"
                        "🔓 Ochish uchun: 'Shifr | Kalit' shaklida yuboring.")

@dp.message_handler()
async def process_message(message: types.Message):
    text = message.text
    # Agar foydalanuvchi tayoqcha bilan yuborsa, ochishga harakat qiladi
    if " | " in text:
        try:
            cipher_text, key = text.split(" | ")
            cipher_suite = Fernet(key.strip().encode())
            decoded_text = cipher_suite.decrypt(cipher_text.strip().encode()).decode()
            await message.answer(f"🔓 Asl matn:\n\n{decoded_text}")
        except Exception:
            await message.answer("❌ Xato! Shifr yoki Kalit noto'g'ri.")
    else:
        # Oddiy matnni shifrlash
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        cipher_text = cipher_suite.encrypt(text.encode())
        shifr = cipher_text.decode()
        kalit = key.decode()
        await message.answer(f"🔒 Shifr:\n`{shifr}`\n\n🔑 Kalit:\n`{kalit}`\n\n"
                             f"Ochish uchun shunday yuboring:\n`{shifr} | {kalit}`", 
                             parse_mode="Markdown")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

