from aiogram import Bot
from aiogram.utils.exceptions import BotBlocked
import config as cfg
from asyncio import run, gather, sleep
from datetime import datetime
from dateutil.relativedelta import relativedelta
from os import system
from database import db
from hendlers.client import check_can_buy
from infmsg import close_try_period_msg, block_payed_config_msg


'''ВЫПОЛНЯЕТСЯ КАЖДЫЙ ЧАС'''


# ПП - пробный период
# ОК - оплаченный конфиг
# БД - база данных.
bot = Bot(token=cfg.TOKEN, parse_mode="HTML")


async def block_payed_config(pcd):
    system(f"/root/disable_payed_user.sh {pcd[7]}")
    try:
        await bot.send_message(pcd[1], block_payed_config_msg(pcd[10], pcd[5], pcd[3]))
        if db.get_user_data(pcd[1])[5] != 1:
            db.set_active(pcd[1], 1)
    except BotBlocked:
        db.set_active(pcd[1], 0)
    db.mark_order_inactive(pcd[0])



# Выключает просроченные ПП и делает их неактивным в БД
async def close_try_period():
    tpd = db.try_period_data()
    for i, try_period_user in enumerate(tpd):
        if datetime.today() >= datetime.fromisoformat(try_period_user[2]):
            system(f"/root/block_TP_user.sh {try_period_user[4]}")
            try:
                await bot.send_message(try_period_user[0], close_try_period_msg)
                if db.get_user_data(try_period_user[0])[5] != 1:
                    db.set_active(try_period_user[0], 1)
            except BotBlocked:
                db.set_active(try_period_user[0], 0)
            db.block_try_period(try_period_user[0])
            await sleep(2)
        else:
            break


async def close_payed_config():
    pcd = db.payed_config_data()
    for i, payed_user in enumerate(pcd):
        if datetime.today() >= datetime.fromisoformat(payed_user[10]):
            if payed_user[11]:
                price = db.check_price(payed_user[3], payed_user[8])[0]
                user_data = db.get_user_data(payed_user[1])
                can_buy = await check_can_buy(user_data[8], user_data[12], user_data[14], price)
                if can_buy[0]:
                    db.prolong_order(payed_user[1], can_buy[1], can_buy[2], payed_user[0],
                                     datetime.today() + relativedelta(months=payed_user[8]))
                else:
                    await block_payed_config(payed_user)
            else:
                await block_payed_config(payed_user)
            await sleep(2)
        else:
            break


async def starter():
    await gather(close_try_period(), close_payed_config())
    await bot.close()

run(starter())
