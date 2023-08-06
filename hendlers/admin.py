from aiogram import types, Dispatcher
from os import system

import config as cfg
import markups as nav
from create_bot import bot  #, chat_member_status
from database import db
from infmsg import user_data_msg, user_orders_msg, user_income_msg, show_all_users_msg, show_all_tp_msg, \
    show_all_orders_msg, show_all_incomes_msg


# Сообщения в канал
# @dp.message_handler(content_types='text', text_contains='В канал\n', chat_type='private')
async def admin_functional(message: types.Message):
    # cms = chat_member_status(await bot.get_chat_member(chat_id=cfg.CHANNEL_NAME, user_id=message.from_user.id))
    # if cms in ['administrator', 'creator']:  # and message.chat.type == 'private':
    if message.from_user.id == int(cfg.ADMIN_ID):
        if cfg.BOT_NAME + ' В канал:' in message.text:
            await bot.send_message(cfg.CHANNEL_ID, message.text[29:], reply_markup=nav.to_bot_and_sup)
        elif cfg.BOT_NAME + ' Рассылка:' in message.text:
            for user in db.get_users():
                if not user[12]:
                    try:
                        await bot.send_photo(user[1], cfg.mustela, message.text[len(cfg.BOT_NAME + ' Рассылка:\n'):])
                        if user[5] != 1:
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


async def show_all(call: types.callback_query):
    if call.data == 'show_all_users':
        for user in db.get_users():
            await bot.send_message(cfg.ADMIN_ID, show_all_users_msg(user))
    elif call.data == 'show_all_TP':
        for tp in db.try_period_data():
            await bot.send_message(cfg.ADMIN_ID, show_all_tp_msg(tp))
    elif call.data == 'show_all_orders':
        for order in db.payed_config_data():
            await bot.send_message(cfg.ADMIN_ID, show_all_orders_msg(order))
    elif call.data == 'show_all_incomes':
        for income in db.incomes_data():
            await bot.send_message(cfg.ADMIN_ID, show_all_incomes_msg(income))
    elif call.data == 'show_all_restart_bot':
        system('systemctl restart Mu-bot.service')
        # system('pwd')


def register_admin_handlers(dp: Dispatcher):
    # dp.register_message_handler(cmd_client_main, text_contains='client')
    # dp.register_message_handler(cmd_client_help, text_contains='help')
    dp.register_message_handler(admin_functional, content_types='text', text_contains=cfg.BOT_NAME)  # , chat_type='private')
    dp.register_callback_query_handler(show_all, text_contains='show_all')
    # dp.register_message_handler(get_user_data, content_types='text', text_contains='данные', chat_type=['private', 'supergroup'])
