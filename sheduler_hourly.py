from asyncio import run, gather, sleep
from datetime import datetime
from dateutil.relativedelta import relativedelta
# from time import time
from os import system
from aio_pika import Message, connect
from database import db


'''ВЫПОЛНЯЕТСЯ КАЖДЫЙ ЧАС'''

# start = time()  # точка отсчета времени


# ПП - пробный период
# ОК - оплаченный конфиг
# БД - база данных.


# Создаёт очередь и отправляет туда сообщения
async def command_for_bot(command_text) -> None:
    connection = await connect("amqp://guest:guest@localhost/")
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("to_bot_queue")
        await channel.default_exchange.publish(Message(bytes(command_text, 'utf-8')), routing_key=queue.name, )


async def block_payed_config(pcd):
    # print(f'Заблокировать интерфейс {pcd[7]} клиента {pcd[1]} на сервере {pcd[4]}. ОТСЮДА!!!')
    db.mark_order_inactive(pcd[0])
    if system(f'ssh root@WG_WORK -p 4522 /root/disable_payed_user.sh {pcd[7]}') == 0:
        # сообщение клиенту о блокировке его интерфейса
        await command_for_bot((str(pcd) + ' block_interface').replace('(', '').replace(')', '').replace(',', '')
                              .replace('\'', ''))
        db.mark_order_inactive(pcd[0])
    else:
        await command_for_bot(str(pcd[4]) + ' server_unreachable')


# Выключает просроченные ПП и делает их неактивным в БД
async def close_try_period():
    tpd = db.try_period_data()
    for i in range(len(tpd)):
        if datetime.today() >= datetime.fromisoformat(tpd[i][2]):
            if system(f'ssh root@WG_TRY -p 4522 /root/block_TP_user.sh {tpd[i][4]}') == 0:
                await command_for_bot(str(tpd[i][0]) + ' close_try_period')  # сообщение клиенту о конце его ПП
                db.block_try_period(tpd[i][0])
                await sleep(2)
            else:
                await command_for_bot(str(tpd[i][3]) + ' server_unreachable')
        else:
            break


async def close_payed_config():
    pcd = db.payed_config_data()
    for i in range(len(pcd)):
        if datetime.today() >= datetime.fromisoformat(pcd[i][10]):
            if pcd[i][11]:
                price = db.check_price(pcd[i][3], pcd[i][8])[0]
                user_data = db.get_user_data(pcd[i][1])
                if user_data[8] >= price and user_data[12] == 0:
                    db.prolong_order(pcd[i][1], user_data[8], price, pcd[i][0],
                                     datetime.today() + relativedelta(months=pcd[i][8]))
                elif user_data[8] < price:
                    await block_payed_config(pcd[i])
            else:
                await block_payed_config(pcd[i])
            await sleep(2)
        else:
            break


async def starter():
    await gather(close_try_period(), close_payed_config())

run(starter())

# end = time() - start
# print(end)
