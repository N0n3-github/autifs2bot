from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.chat_permissions import ChatPermissions
from AmizoneAPI import amizone_api
from config import AMIZONE_ID, AMIZONE_PASSWORD, BOT_TOKEN
from time import time


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
    await amizone_api.login(AMIZONE_ID, AMIZONE_PASSWORD)
    args = message.text.split()
    if len(args) == 1:
        response_text = await amizone_api.get_time_table()
    elif len(args) == 2:
        response_text = await amizone_api.get_time_table(args[1])
    else:
        response_text = "Error in given arguments"
    await message.reply(response_text)


@dp.message_handler(commands=['ban'])
async def ban(message: types.Message):
    user = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if user.status != 'creator':
        await message.reply('Only creator Senior can ban users!')
        return
    elif message.reply_to_message.from_user.id in [user.user.id, bot.id]:
        await message.reply('Admin cannot ban himself or bot')
        return

    if not message.reply_to_message:
        await message.reply('Reply a message from user you want to ban Senior')
        return
    permissions = ChatPermissions(can_send_messages = False,
                                  can_send_media_messages = False,
                                  can_send_polls = False,
                                  can_send_other_messages = False,
                                  can_add_web_page_previews = False,
                                  can_change_info = False,
                                  can_invite_users = False,
                                  can_pin_messages = False)
    xstr = lambda x: '' if x == None else str(x)
    full_name = message.reply_to_message.from_user.first_name + ' ' + xstr(message.reply_to_message.from_user.last_name)

    await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, permissions, int(time()) + 86400)  # for 1 day
    await message.reply("User " + full_name + " was banned for " + str(int(86400 / 3600)) + " hours!")


@dp.message_handler(commands=['bannedusers'])
async def get_banned_users(message: types.Message):
    await message.reply("Dopileee")


if __name__ == '__main__':
    executor.start_polling(dp)
