import sqlite3
from asyncio import run, gather
from datetime import datetime, timedelta
# from time import time

from aio_pika import Message, connect

con = sqlite3.connect('vpn_service.db')

'''ВЫПОЛНЯЕТСЯ РАЗ В ДЕНЬ'''

# start = time()  # точка отсчета времени


# ПП - пробный период
# ОК - оплаченный конфиг
# БД - база данных.
# Вытаскивает из БД активные ПП
async def try_period_data(connection):
    curs = connection.cursor()
    return curs.execute('SELECT user_id, expires_at FROM try_period WHERE active = ? ORDER BY expires_at',
                        (1,)).fetchall()


# Вытаскивает из БД оплаченные конфиги
async def payed_config_data(connection):
    curs = connection.cursor()
    return curs.execute('SELECT customer_id, expires_at, country, interface, tarif FROM orders WHERE active = ?'
                        ' ORDER BY expires_at', (1,)).fetchall()


# Создаёт очередь и отправляет туда сообщения
async def command_for_bot(command_text) -> None:
    connection = await connect("amqp://guest:guest@localhost/")
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("to_bot_queue")
        await channel.default_exchange.publish(Message(bytes(command_text, 'utf-8')), routing_key=queue.name, )


# Напоминалка пользователю об окончании ПП
async def try_period_reminder(connection):
    tpd = await try_period_data(connection)
    for i in range(len(tpd)):
        if datetime.today() <= datetime.fromisoformat(tpd[i][1]) <= datetime.today() + timedelta(days=1):
            # print('Осталось менее суток до окончания ПП: ОЧЕРЕДЬ')
            await command_for_bot(str(tpd[i][0]) + ' one_day_left_try_period')
        elif datetime.today() + timedelta(days=1) <= datetime.fromisoformat(tpd[i][1]) \
                <= datetime.today() + timedelta(days=2):
            # print('Осталось менее двух суток до окончания ПП: ОЧЕРЕДЬ')
            await command_for_bot(str(tpd[i][0]) + ' two_days_left_try_period')
        elif datetime.fromisoformat(tpd[i][1]) > datetime.today() + timedelta(days=2):
            break


async def payed_config_reminder(connection):
    pcd = await payed_config_data(connection)

    for i in range(len(pcd)):

        if datetime.today() <= datetime.fromisoformat(pcd[i][1]) <= datetime.today() + timedelta(days=1):
            # print('Осталось менее суток до окончания ОК: ОЧЕРЕДЬ')
            await command_for_bot(
                (str(pcd[i]) + ' one_day_payed_left').replace('(', '').replace(')', '').replace(',', '').replace('\'',
                                                                                                                 ''))
        elif datetime.today() + timedelta(days=1) <= datetime.fromisoformat(pcd[i][1]) \
                <= datetime.today() + timedelta(days=2):
            # print('Осталось менее двух суток до окончания ОК: ОЧЕРЕДЬ')
            await command_for_bot(
                (str(pcd[i]) + ' two_days_payed_left').replace('(', '').replace(')', '').replace(',', '').replace('\'',
                                                                                                                  ''))
        elif datetime.fromisoformat(pcd[i][1]) > datetime.today() + timedelta(days=2):
            break


async def starter():
    await gather(try_period_reminder(con), payed_config_reminder(con))


run(starter())

# end = time() - start
# print(end)
