from aiogram import Bot, Dispatcher, executor, types
from AmizoneAPI import amizone_api
from config import AMIZONE_ID, AMIZONE_PASSWORD, BOT_TOKEN


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    with open('static/welcome_sticker.webp', 'rb') as welcome_sticker:
        sticker_message = await bot.send_sticker(message.chat.id, welcome_sticker)
    me = await bot.get_me()
    await bot.send_message(message.chat.id, f"Hats off to you, I am slave of <i>Senior sudo</i> – <b>{me.first_name}</b>! What can I do for you?",
                           parse_mode="html", reply_to_message_id=sticker_message.message_id)


if __name__ == '__main__':
    executor.start_polling(dp)
