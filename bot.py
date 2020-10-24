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
    await bot.send_message(message.chat.id, f"Hats off to you, I am slave of <i>Senior sudo</i> – "
                                            f"<b>{me.first_name}</b>! What can I do for you?",
                           parse_mode="html", reply_to_message_id=sticker_message.message_id)


@dp.message_handler(commands=['schedule'])
async def schedule(message: types.Message):
    amizone_api.login(AMIZONE_ID, AMIZONE_PASSWORD)
    args = message.text.split()
    if len(args) == 1:
        response_text = amizone_api.get_time_table()
    elif len(args) == 2:
        response_text = amizone_api.get_time_table(args[1])
    else:
        response_text = "Error in given arguments"
    await message.reply(response_text)


if __name__ == '__main__':
    executor.start_polling(dp)
