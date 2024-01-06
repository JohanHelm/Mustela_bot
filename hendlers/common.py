from aiogram import types, Dispatcher
from aiogram.utils.deep_linking import get_start_link
from datetime import datetime

import config as cfg
import markups as nav

from create_bot import bot  # , chat_member_status
from database import Database, db
from infmsg import hello_new_user_msg, hello_admin_msg


# left отписался или не был подписан
# member подписан
# administrator администратор
# creator создатель

# запуск бота
# @dp.message_handler(commands="start", commands_prefix="/", chat_type=['private'])
async def cmd_start(message: types.Message):
    # db = Database('vpn_service.db')
    if message.from_user.id == int(cfg.ADMIN_ID):
        if not db.user_exists(message.from_user.id):  # проверяет есть ли пользователь в базе, если нет добавляет
            db.add_user(message.from_user.id, message.from_user.full_name, message.from_user.language_code,
                        message.from_user.mention, await get_start_link(message.from_user.id), message.get_args())
        await message.answer('Привет {0.first_name}!\n'.format(message.from_user) + hello_admin_msg,
                             reply_markup=nav.admin_main_menu)
    else:
        if not db.user_exists(message.from_user.id):  # проверяет есть ли пользователь в базе, если нет добавляет
            db.add_user(message.from_user.id, message.from_user.full_name, message.from_user.language_code,
                        message.from_user.mention, await get_start_link(message.from_user.id), message.get_args(),
                        datetime.today())
            if message.get_args():
                db.add_refs_amount(message.get_args())
        # await bot.send_message(message.from_user.id, '<b>Привет {0.first_name}!</b>\n'
        #                      .format(message.from_user) + hello_new_user_msg, reply_markup=nav.client_main_menu)
        await bot.send_photo(message.from_user.id, cfg.mustela, '<b>Привет {0.first_name}!</b>\n'
                             .format(message.from_user) + hello_new_user_msg, reply_markup=nav.client_main_menu)


def register_common_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands='start', commands_prefix="/", state="*")  # , chat_type='private')
