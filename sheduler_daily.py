from asyncio import run, gather, sleep
from datetime import datetime, timedelta

from aiogram import Bot
from aiogram.utils.exceptions import BotBlocked

import config as cfg
from database import db
from infmsg import (one_d_left_try_period_msg,
                    two_d_left_try_period_msg,
                    days_payed_left_msg,
                    )

'''ВЫПОЛНЯЕТСЯ РАЗ В ДЕНЬ'''

# ПП - пробный период
# ОК - оплаченный конфиг
# БД - база данных.
bot = Bot(token=cfg.TOKEN, parse_mode="HTML")


# Напоминалка пользователю об окончании ПП
async def try_period_reminder():
    tpd = db.try_period_data()
    for i, try_period_user in enumerate(tpd):
        if datetime.today() <= datetime.fromisoformat(try_period_user[2]) <= datetime.today() + timedelta(days=1):
            try:
                await bot.send_message(try_period_user[0], one_d_left_try_period_msg)
                if db.get_user_data(try_period_user[0])[5] != 1:
                    db.set_active(try_period_user[0], 1)
            except BotBlocked:
                db.set_active(try_period_user[0], 0)
        elif datetime.today() + timedelta(days=1) <= datetime.fromisoformat(try_period_user[2]) \
                <= datetime.today() + timedelta(days=2):
            try:
                await bot.send_message(try_period_user[0], two_d_left_try_period_msg)
                if db.get_user_data(try_period_user[0])[5] != 1:
                    db.set_active(try_period_user[0], 1)
            except BotBlocked:
                db.set_active(try_period_user[0], 0)
        elif datetime.fromisoformat(try_period_user[2]) > datetime.today() + timedelta(days=2):
            break
        await sleep(2)


async def payed_config_reminder():
    pcd = db.payed_config_data()
    for i, payed_user in enumerate(pcd):
        if datetime.today() <= datetime.fromisoformat(payed_user[10]) <= datetime.today() + timedelta(days=1):
            try:
                await bot.send_message(payed_user[1],
                                       days_payed_left_msg(1, payed_user[0], payed_user[10], payed_user[5],
                                                           payed_user[3]))
                if db.get_user_data(payed_user[1])[5] != 1:
                    db.set_active(payed_user[1], 1)
            except BotBlocked:
                db.set_active(payed_user[1], 0)
        elif datetime.today() + timedelta(days=1) <= datetime.fromisoformat(payed_user[10]) \
                <= datetime.today() + timedelta(days=2):
            try:
                await bot.send_message(payed_user[1],
                                       days_payed_left_msg(2, payed_user[0], payed_user[10], payed_user[5],
                                                           payed_user[3]))
                if db.get_user_data(payed_user[1])[5] != 1:
                    db.set_active(payed_user[1], 1)
            except BotBlocked:
                db.set_active(payed_user[1], 0)
        elif datetime.fromisoformat(pcd[i][10]) > datetime.today() + timedelta(days=2):
            break
        await sleep(2)


async def starter():
    await gather(try_period_reminder(), payed_config_reminder())
    await bot.close()


run(starter())
