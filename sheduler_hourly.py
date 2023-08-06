from asyncio import run, gather, sleep
from datetime import datetime
from dateutil.relativedelta import relativedelta
# from time import time
from os import system
from aio_pika import Message, connect
from database import db
from hendlers.client import check_can_buy


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
    if system(f'ssh root@{pcd[4]}_{pcd[5]}_Work_{pcd[6]} -p 4522  /root/disable_payed_user.sh {pcd[7]}') == 0:
        pcd_in_progress = list(pcd)
        for j in range(len(pcd)):
            pcd_in_progress[j] = str(pcd_in_progress[j])
        # сообщение клиенту о блокировке его интерфейса
        await command_for_bot('For_User ' + 'block_interface ' + ' '.join(pcd_in_progress))
        db.mark_order_inactive(pcd[0])

    # pcd_in_progress = list(pcd)
    # for j in range(len(pcd)):
    #     pcd_in_progress[j] = str(pcd_in_progress[j])
    # # сообщение клиенту о блокировке его интерфейса
    # await command_for_bot('For_User ' + 'block_interface ' + ' '.join(pcd_in_progress))




# Выключает просроченные ПП и делает их неактивным в БД
async def close_try_period():
    tpd = db.try_period_data()
    for i in range(len(tpd)):
        if datetime.today() >= datetime.fromisoformat(tpd[i][2]):
            if system(f'ssh root@{tpd[i][3]}_{tpd[i][5]}_Try_{tpd[i][6]} -p 4522 /root/block_TP_user.sh {tpd[i][4]}')\
                    == 0:
                tpd_in_progress = list(tpd[i])
                for j in range(len(tpd[i])):
                    tpd_in_progress[j] = str(tpd_in_progress[j])
                # сообщение клиенту о конце его ПП
                await command_for_bot('For_User ' + 'close_try_period ' + ' '.join(tpd_in_progress))
                db.block_try_period(tpd[i][0])
                await sleep(2)
            # tpd_in_progress = list(tpd[i])
            # for j in range(len(tpd[i])):
            #     tpd_in_progress[j] = str(tpd_in_progress[j])
            # # сообщение клиенту о конце его ПП
            # await command_for_bot('For_User ' + 'close_try_period ' + ' '.join(tpd_in_progress))
        else:
            break


async def close_payed_config():
    pass
    pcd = db.payed_config_data()
    for i in range(len(pcd)):
        # await block_payed_config(pcd[i])
        if datetime.today() >= datetime.fromisoformat(pcd[i][10]):
            if pcd[i][11]:
                price = db.check_price(pcd[i][3], pcd[i][8])[0]
                user_data = db.get_user_data(pcd[i][1])
                can_buy = await check_can_buy(user_data[8], user_data[12], user_data[14], price)
                if can_buy[0]:
                    db.prolong_order(pcd[i][1], can_buy[1], can_buy[2], pcd[i][0],
                                     datetime.today() + relativedelta(months=pcd[i][8]))
                else:
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
