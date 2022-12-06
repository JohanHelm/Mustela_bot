import sqlite3
from asyncio import run, gather, sleep
from datetime import datetime
# from time import time
from os import system
from aio_pika import Message, connect

con = sqlite3.connect('vpn_service.db')

'''ВЫПОЛНЯЕТСЯ КАЖДЫЙ ЧАС'''

# start = time()  # точка отсчета времени


# ПП - пробный период
# ОК - оплаченный конфиг
# БД - база данных.
# Вытаскивает из БД активные ПП
async def try_period_data(connection):
    curs = connection.cursor()
    return curs.execute('SELECT * FROM try_period WHERE active = ? ORDER BY expires_at',
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


# Выключает просроченные ПП и делает их неактивным в БД
async def close_try_period(connection):
    curs = connection.cursor()
    tpd = await try_period_data(connection)
    for i in range(len(tpd)):
        if datetime.today() >= datetime.fromisoformat(tpd[i][2]):
            if system(f'ssh root@WG_TRY -p 4522 /root/block_TP_user.sh {tpd[i][4]}') == 0:
                await command_for_bot(str(tpd[i][0]) + ' close_try_period')  # сообщение клиенту о конце его ПП
                curs.execute("UPDATE try_period SET active = 0 WHERE user_id = ?", (tpd[i][0],))
                await sleep(2)
            else:
                await command_for_bot(str(tpd[i][3]) + ' server_unreachable')
        else:
            break
        con.commit()


async def block_payed_config(connection):
    curs = connection.cursor()
    pcd = await payed_config_data(connection)
    for i in range(len(pcd)):
        if datetime.today() >= datetime.fromisoformat(pcd[i][1]):
            print(f'Заблокировать инерфейс {pcd[i][3]} клиента {pcd[i][0]} на сервере {pcd[i][2]}. ОТСЮДА!!!')
            # os.system(f'remote_control.sh {pcd[i][3]} {pcd[i][0]} {pcd[i][2]}')
            # сообщение клиенту о блокировке его интерфейса
            await command_for_bot((str(pcd[i]) + ' block_interface').replace('(', '').replace(')', '').replace(',', '')
                                  .replace('\'', ''))
            curs.execute("UPDATE orders SET active = 0 WHERE customer_id = ? AND expires_at = ? AND country = ? AND"
                         " interface = ?", (pcd[i][0], pcd[i][1], pcd[i][2], pcd[i][3],))
            await sleep(2)
        else:
            break
        con.commit()


async def starter():
    await gather(close_try_period(con), block_payed_config(con))
    # await close_try_period(con)

run(starter())

# end = time() - start
# print(end)
