from os import system, listdir
from decimal import Decimal
from asyncio import run, gather, sleep
import subprocess
from aio_pika import Message, connect


# Создаёт очередь и отправляет туда сообщения
async def command_for_bot(command_text) -> None:
    connection = await connect("amqp://guest:guest@localhost/")
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("to_bot_queue")
        await channel.default_exchange.publish(Message(bytes(command_text, 'utf-8')), routing_key=queue.name, )


async def check_servers():
    for catalog in listdir('/root'):
        if catalog[0].isupper():
            for purpose in listdir(f'/root/{catalog}'):
                for num in listdir(f'/root/{catalog}/{purpose}'):
                    if system(f'ssh root@{catalog}_{purpose}_{num} -p 4522 ssh root@MU_BOT -p 4522 exit') != 0:
                        # await bot.send_message(cfg.ADMIN_ID, f'Cервер {catalog}_{purpose}_{num} недоступен с бота')

                        await command_for_bot(f'For_Admin недоступен_с_бота {catalog}_{purpose}_{num}')
                        await sleep(2)
                    else:
                        cmd = f'ssh root@{catalog}_{purpose}_{num} -p 4522 iperf3 -c iperf.par2.as49434.net -p 9225'
                        check_speed = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
                                                       universal_newlines=True)
                        real_speed = check_speed.communicate()[0].split('\n')[15:17]
                        # sender = real_speed[0].split()[6:8]
                        # receiver = real_speed[1].split()[6:8]
                        sender = real_speed[0][
                                 real_speed[0].find('Bytes') + len('Bytes'):real_speed[0].find('bits/sec')].split()
                        receiver = real_speed[1][
                                   real_speed[1].find('Bytes') + len('Bytes'):real_speed[1].find('bits/sec')].split()
                        if sender[1] == 'K' or receiver[1] == 'K':
                            # await bot.send_message(cfg.ADMIN_ID, f'{catalog}_{purpose}_{num}\n'
                            #                                      f'sender: {sender}\nreceiver: {receiver}')
                            sender = ' '.join(sender)
                            receiver = ' '.join(receiver)
                            await command_for_bot(f'For_Admin Cкорость {catalog}_{purpose}_{num} {sender} {receiver}')
                            await sleep(2)
                        else:
                            if Decimal(sender[0]) < 500 or Decimal(receiver[0]) < 500:
                                # await bot.send_message(cfg.ADMIN_ID, f'{catalog}_{purpose}_{num}\n'
                                #                                      f'sender: {sender}\nreceiver: {receiver}')
                                sender = ' '.join(sender)
                                receiver = ' '.join(receiver)
                                await command_for_bot(
                                    f'For_Admin Cкорость {catalog}_{purpose}_{num} {sender} {receiver}')
                                await sleep(2)


async def starter():
    await check_servers()


run(starter())
