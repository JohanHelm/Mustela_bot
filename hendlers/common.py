import string

from aiogram import types, Dispatcher
from aiogram.utils.deep_linking import get_start_link

import bot_queue
import config as cfg
import markups as nav
from create_bot import bot, chat_member_status
from database import db
from infmsg import hello_new_user_msg, sub_to_use_msg, hello_admin_msg


# @dp.message_handler(commands="test", commands_prefix="/")
async def cmd_test(message: types.Message):  # если команда/кнопка в группу или боту
    await message.answer(message.from_user.id)
    await message.answer(message.from_user.full_name)
    await message.answer(message.from_user.mention)
    await message.answer(message.from_user.language_code)
    await message.answer(message.chat.type)
    # await bot.send_photo(cfg.CHANNEL_ID, cfg.mustela, 'hello', nav.to_bot_and_sup)
    # await message.answer(message.forward_from_message_id)
    await message.answer(message.forward_sender_name)

    # print(message.get_args())


# left отписался или не был подписан
# member подписан
# administrator администратор
# creator создатель

# запуск бота
# @dp.message_handler(commands="start", commands_prefix="/", chat_type=['private'])
async def cmd_start(message: types.Message):
    cms = chat_member_status(await bot.get_chat_member(chat_id=cfg.CHANNEL_NAME, user_id=message.from_user.id))
    if cms == 'member': # and message.chat.type == 'private':
        if not db.user_exists(message.from_user.id):  # проверяет есть ли пользователь в базе, если нет добавляет
            db.add_user(message.from_user.id, message.from_user.full_name, message.from_user.language_code,
                        message.from_user.mention, await get_start_link(message.from_user.id), message.get_args())
        await bot.send_photo(message.from_user.id, cfg.mustela, '<b>Привет {0.first_name}!</b>\n'
                             .format(message.from_user) + hello_new_user_msg, reply_markup=nav.client_main_menu)

    elif cms in ['administrator', 'creator']: # and message.chat.type == 'private':
        if not db.user_exists(message.from_user.id):  # проверяет есть ли пользователь в базе, если нет добавляет
            db.add_user(message.from_user.id, message.from_user.full_name, message.from_user.language_code,
                        message.from_user.mention, await get_start_link(message.from_user.id), message.get_args())
            db.set_admin(message.from_user.id, 1)  # отметить как админа в базе
        await message.answer('Привет {0.first_name}!\n'.format(message.from_user) + hello_admin_msg,
                             reply_markup=nav.admin_main_menu)
        # await bot.send_photo(message.from_user.id, cfg.mustela,
        #                      '<b>Привет {0.first_name}!</b>\n'.format(message.from_user) + hello_new_user_msg,
        #                      reply_markup=nav.client_main_menu)
        await bot_queue.waiter_from_queue()
    elif cms == 'left': # and message.chat.type == 'private':
        if not db.user_exists(message.from_user.id):  # проверяет есть ли пользователь в базе, если нет добавляет
            db.add_user(message.from_user.id, message.from_user.full_name, message.from_user.language_code,
                        message.from_user.mention, await get_start_link(message.from_user.id), message.get_args())
            if message.get_args():
                db.add_refs_amount(message.get_args())
        await message.answer(sub_to_use_msg, reply_markup=nav.ch_menu)
        await message.delete()


# Проверяет вновь подписанных
# new_subscribed
async def cmd_new_sub(call: types.callback_query):
    cms = chat_member_status(await bot.get_chat_member(chat_id=cfg.CHANNEL_NAME, user_id=call.from_user.id))
    if cms == 'left':
        await call.answer('Вы всё ещё не подписаны!', show_alert=True)
    elif cms == 'member':
        if not db.user_exists(call.from_user.id):  # проверяет есть ли пользователь в базе, если нет добавляет
            db.add_user(call.from_user.id, call.from_user.full_name, call.from_user.language_code,
                        call.from_user.mention, await get_start_link(call.from_user.id))
        await bot.send_photo(call.from_user.id, cfg.mustela, 'Привет {0.first_name}!\n'.format(call.from_user) +
                             hello_new_user_msg, reply_markup=nav.client_main_menu)


# Отправляет новых пользователей подписаться на канал, проверяет маты
# @dp.message_handler(content_types='text')
mat = ['хуй', 'пизда', 'блядь', 'ебать', 'пидор', 'гандон', 'шлюха', 'проститутка', 'сука']


async def cmd_join_channel(message: types.Message):  # вывод кнопок в группу
    cms = chat_member_status(await bot.get_chat_member(chat_id=cfg.CHANNEL_NAME, user_id=message.from_user.id))
    if cms == 'left':
        await message.answer(sub_to_use_msg, reply_markup=nav.ch_menu)
        await message.delete()
    elif cms == 'member' and message.chat.type == 'supergroup':
        for bad_word in mat:
            if bad_word in message.text.lower().translate(str.maketrans('', '', string.punctuation)):
                await message.reply('Ругаться запрещено!!')
                await message.delete()


def register_common_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(cmd_new_sub, text='new_subscribed')
    dp.register_message_handler(cmd_test, commands="test", commands_prefix="/")
    dp.register_message_handler(cmd_start, commands='start', commands_prefix="/", chat_type='private')
    dp.register_message_handler(cmd_join_channel, content_types='text')
