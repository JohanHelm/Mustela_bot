from aiogram import types, Dispatcher
from aiogram.utils.deep_linking import get_start_link
from datetime import datetime
from bot_queue import waiter_from_queue as wfq
import config as cfg
import markups as nav
#import scheduler as sch
from create_bot import bot  # , chat_member_status
from database import db
from infmsg import hello_new_user_msg, hello_admin_msg


# left отписался или не был подписан
# member подписан
# administrator администратор
# creator создатель

# запуск бота
# @dp.message_handler(commands="start", commands_prefix="/", chat_type=['private'])
async def cmd_start(message: types.Message):
    if message.from_user.id == int(cfg.ADMIN_ID):
        if not db.user_exists(message.from_user.id):  # проверяет есть ли пользователь в базе, если нет добавляет
            db.add_user(message.from_user.id, message.from_user.full_name, message.from_user.language_code,
                        message.from_user.mention, await get_start_link(message.from_user.id), message.get_args())
            db.set_admin(message.from_user.id, 1)  # отметить как админа в базе
        await message.answer('Привет {0.first_name}!\n'.format(message.from_user) + hello_admin_msg,
                             reply_markup=nav.admin_main_menu)
        # await sch.jobs()
        await wfq()
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
