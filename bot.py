from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.chat_permissions import ChatPermissions
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from AmizoneAPI import amizone_api
from config import AMIZONE_ID, AMIZONE_PASSWORD, BOT_TOKEN
from time import time
import random
import json


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
xstr = lambda x: '' if x == None else str(x)
restricted_permissions = ChatPermissions(can_send_messages = False,
                                  can_send_media_messages = False,
                                  can_send_polls = False,
                                  can_send_other_messages = False,
                                  can_add_web_page_previews = False,
                                  can_change_info = False,
                                  can_invite_users = False,
                                  can_pin_messages = False)


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
    else:
        if not message.reply_to_message:
            await message.reply('Reply a message from user you want to ban Senior')
            return
        elif message.reply_to_message.from_user.id in [user.user.id, bot.id]:
            await message.reply('Admin cannot ban himself or bot')
            return

    ban_user = await bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    full_name = (ban_user.user.first_name + ' ' + xstr(ban_user.user.last_name)).strip()
    if ban_user.status == "restricted":
        await message.reply("User " + full_name + " is already banned")
        return

    ban_hours = 2
    unix_ban_timeout = int(time()) + ban_hours * 3600
    json_data['banned_users'][str(message.reply_to_message.from_user.id)] = {
        "name": full_name,
        "till_time": unix_ban_timeout
    }
    with open('data.json', 'w') as f:
        json.dump(json_data, f, indent=4)
    await bot.restrict_chat_member(message.chat.id,  ban_user.user.id, restricted_permissions, unix_ban_timeout)
    await message.reply("User " + full_name + " was banned for " + str(ban_hours) + " hours!")


@dp.message_handler(commands=['unban'])
async def unban(message: types.Message):
    user = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if user.status != 'creator':
        await message.reply('Only creator Senior can unban users!')
        return

    inline_markup = InlineKeyboardMarkup(row_width=1)
    text = "Banned users:\n"
    for id, user_data in json_data['banned_users'].items():
        if user_data['till_time'] <= int(time()):
            del json_data['banned_users'][id]
            continue
        inline_markup.add(InlineKeyboardButton(user_data["name"], callback_data=str(id)))
        text += user_data["name"] + "\n"
    with open('data.json', 'w') as f:
        json.dump(json_data, f, indent=4)
    if not inline_markup['inline_keyboard']:
        await bot.send_message(message.chat.id, "No banned users found")
        return
    text += "\nChoose a user to unban Senior:"
    await bot.send_message(message.chat.id, text, reply_markup=inline_markup)


@dp.callback_query_handler(lambda call: True)
async def unban_callback_handler(call):
    caller = await bot.get_chat_member(call.message.chat.id, call.from_user.id)
    if caller.status != "creator":
        await bot.answer_callback_query(call.id, show_alert=True,
                                  text="Only Senior can choose whom to unban")
        return
    banned_user = await bot.get_chat_member(call.message.chat.id, int(call.data))
    full_name = (banned_user.user.first_name + ' ' + xstr(banned_user.user.last_name)).strip()
    if banned_user.status == "restricted":
        alert_text = "User " + full_name + " will be unbanned in 30 seconds."
        await bot.restrict_chat_member(call.message.chat.id, int(call.data), restricted_permissions, int(time()) + 31)
    else:
        alert_text = "User " + full_name +" is already unbanned"

    if json_data['banned_users'].get(call.data):
        del json_data['banned_users'][call.data]
        with open('data.json', 'w') as f:
            json.dump(json_data, f, indent=4)

    await bot.answer_callback_query(call.id, show_alert=True,
                              text=alert_text)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=alert_text,
                          reply_markup=None)


@dp.message_handler(commands=['gimmejoke'])
async def joke(message: types.Message):
    jokes = ["Diiooo :)",
             "Haaa? Haaa?? You wanna laugh?",
             "Don't worry, here is your joke",
             "Oke, now you can share",
             "Do you want to share your screen? Yes, show me please",
             "Oke so, oke, you wanted me to text, so oke",
             "Temuuuullll",
             "Mirdul. NO! Senior Mirdul :D",
             "You wanna say something?",
             "Switch on your cameras, everyoneee...",
             "Aleksandreee",
             "Zoulfiyaa? Dio, can you send the link to the group?",
             "There are some Internet issues... (No)",
             "I think something is wrong with my connection!",
             "I had a power cut, so please be patient",
             "My camera is not working! (Well, actually it is LOL :D)",
             "I have some problems with my mic (speaking via mic)",
             "Artuuur, Kamidova! Please, send the join link to your group",
             "Zoulfiya, where are you today? Please switch on your camera",
             "Can't you solve it in mind? It is easy! (12301258^2131385)",
             "Have you uploaded your assignment? Have you?... Oke",
             "Is my screen visibleee to you? Or not?",
             "I will tell you one joke:\nOne day... One person... flushed the toilet and forgot to turn his mike off",
             "Oh, why Amizone is working too slow today?",
             "Oke, let's read this \x22short\x22 story now)",
             "Easter egg is found! Thanks to Senior Mirdul for creating me LOL :D"
             ]
    await message.reply(random.choice(jokes))


if __name__ == '__main__':
    try:
        with open('data.json') as f:
            json_data = json.load(f)
    except FileNotFoundError:
        json_data = {"banned_users": {}}
        with open('data.json', 'w') as f:
            json.dump(json_data, f, indent=4)
    executor.start_polling(dp)
