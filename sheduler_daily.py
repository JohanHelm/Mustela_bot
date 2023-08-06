
from asyncio import run, gather, sleep
from datetime import datetime, timedelta
# from time import time
from database import db
from aio_pika import Message, connect


'''ВЫПОЛНЯЕТСЯ РАЗ В ДЕНЬ'''

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


# Напоминалка пользователю об окончании ПП
async def try_period_reminder():
    tpd = db.try_period_data()
    for i in range(len(tpd)):
        if datetime.today() <= datetime.fromisoformat(tpd[i][2]) <= datetime.today() + timedelta(days=1):
            # print(f'Осталось менее суток до окончания ПП: ОЧЕРЕДЬ {tpd[0]}')
            tpd_in_progress = list(tpd[i])
            for j in range(len(tpd[i])):
                tpd_in_progress[j] = str(tpd_in_progress[j])
            await command_for_bot('For_User ' + 'one_day_left_try_period ' + ' '.join(tpd_in_progress))
        elif datetime.today() + timedelta(days=1) <= datetime.fromisoformat(tpd[i][2]) \
                <= datetime.today() + timedelta(days=2):
            # print(f'Осталось менее двух суток до окончания ПП: ОЧЕРЕДЬ {tpd[0]}')
            tpd_in_progress = list(tpd[i])
            for j in range(len(tpd[i])):
                tpd_in_progress[j] = str(tpd_in_progress[j])
            await command_for_bot('For_User ' + 'two_days_left_try_period ' + ' '.join(tpd_in_progress))
        elif datetime.fromisoformat(tpd[i][2]) > datetime.today() + timedelta(days=2):
            break
        await sleep(2)


async def payed_config_reminder():
    pcd = db.payed_config_data()
    for i in range(len(pcd)):
        if datetime.today() <= datetime.fromisoformat(pcd[i][10]) <= datetime.today() + timedelta(days=1):
            # print(f'Осталось менее суток до окончания ОК: ОЧЕРЕДЬ {pcd[i]}')
            pcd_in_progress = list(pcd[i])
            for j in range(len(pcd[i])):
                pcd_in_progress[j] = str(pcd_in_progress[j])
            await command_for_bot('For_User ' + 'one_day_payed_left ' + ' '.join(pcd_in_progress))
        elif datetime.today() + timedelta(days=1) <= datetime.fromisoformat(pcd[i][10]) \
                <= datetime.today() + timedelta(days=2):
            # print(f'Осталось менее двух суток до окончания ОК: ОЧЕРЕДЬ {pcd[i]}')
            pcd_in_progress = list(pcd[i])
            for j in range(len(pcd[i])):
                pcd_in_progress[j] = str(pcd_in_progress[j])
            await command_for_bot('For_User ' + 'two_days_payed_left ' + ' '.join(pcd_in_progress))
        elif datetime.fromisoformat(pcd[i][10]) > datetime.today() + timedelta(days=2):
            break
        await sleep(2)


async def starter():
    await gather(try_period_reminder(), payed_config_reminder())


run(starter())

# end = time() - start
# print(end)
