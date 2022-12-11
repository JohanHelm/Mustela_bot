from aiogram import types, Dispatcher

import config as cfg
import markups as nav
from create_bot import bot, chat_member_status
from database import db
from infmsg import user_data_msg, user_orders_msg, user_income_msg


# Сообщения в канал
# @dp.message_handler(content_types='text', text_contains='В канал\n', chat_type='private')
async def edit_channel(message: types.Message):
    cms = chat_member_status(await bot.get_chat_member(chat_id=cfg.CHANNEL_NAME, user_id=message.from_user.id))
    if cms in ['administrator', 'creator']:  # and message.chat.type == 'private':
        if cfg.BOT_NAME + ' В канал:' in message.text:
            await bot.send_message(cfg.CHANNEL_ID, message.text[29:], reply_markup=nav.to_bot_and_sup)
        elif cfg.BOT_NAME + ' Рассылка:' in message.text:
            for user in db.get_users():
                try:
                    await bot.send_photo(user[1], cfg.mustela, message.text[len(cfg.BOT_NAME + ' Рассылка:\n'):])
                    if user[3] != 1:
                        db.set_active(user[1], 1)
                except:
                    db.set_active(user[1], 0)
            await message.answer('Рассылка успешно доставлена.')
        elif cfg.BOT_NAME + ' Данные:' in message.text:
            await message.answer(user_data_msg(db.get_user_data(message.text[len(cfg.BOT_NAME + ' Данные:\n'):]),
                                               db.check_try_period(message.text[len(cfg.BOT_NAME + ' Данные:\n'):])))
        elif cfg.BOT_NAME + ' Заказы:' in message.text:
            if db.check_orders(message.text[len(cfg.BOT_NAME + ' Заказы:\n'):]):
                for order in db.check_orders(message.text[len(cfg.BOT_NAME + ' Заказы:\n'):]):
                    await message.answer(user_orders_msg(order))
            else:
                await message.answer('Заказов нет')
        elif cfg.BOT_NAME + ' Платежи:' in message.text:
            if db.check_income(message.text[len(cfg.BOT_NAME + ' Платежи:\n'):]):
                for income in db.check_income(message.text[len(cfg.BOT_NAME + ' Платежи:\n'):]):
                    await message.answer(user_income_msg(income))
            else:
                await message.answer('Платежей нет')


# async def get_user_data(message: types.Message):
#     cms = chat_member_status(await bot.get_chat_member(chat_id=cfg.CHANNEL_NAME, user_id=message.from_user.id))
#     if cms in ['administrator', 'creator']:
#         if hasattr(message.forward_from, 'id'):
#             print(message.forward_from)
#             print(message.forward_from.id)
#         else:
#             print('У пользователя включен режим приватности при пересылке его сообщений')


def register_admin_handlers(dp: Dispatcher):
    # dp.register_message_handler(cmd_client_main, text_contains='client')
    # dp.register_message_handler(cmd_client_help, text_contains='help')
    dp.register_message_handler(edit_channel, content_types='text', text_contains=cfg.BOT_NAME, chat_type='private')
    # dp.register_message_handler(get_user_data, content_types='text', text_contains='данные', chat_type=['private', 'supergroup'])
