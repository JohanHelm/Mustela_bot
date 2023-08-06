import asyncio

from aio_pika import connect
from aio_pika.abc import AbstractIncomingMessage
import config as cfg
from create_bot import bot
from database import db
from infmsg import close_try_period_msg, one_d_left_try_period_msg, two_d_left_try_period_msg, block_payed_config_msg, \
    days_payed_left_msg


async def on_message(message: AbstractIncomingMessage) -> None:
    mfq = message.body.decode('UTF-8').split()  # message_from_queue
    # await bot.send_message(cfg.ADMIN_ID, mfq)
    if mfq[0] == 'For_User':
        if mfq[1] == 'one_day_payed_left':
            try:
                await bot.send_message(mfq[3], days_payed_left_msg('1', mfq[2], mfq[4] + mfq[5][:8], mfq[8], mfq[6]))
                if db.get_user_data(mfq[3])[5] != 1:
                    db.set_active(mfq[3], 1)
            except:
                db.set_active(mfq[3], 0)
        elif mfq[1] == 'two_days_payed_left':
            try:
                await bot.send_message(mfq[3], days_payed_left_msg('2', mfq[2], mfq[4] + mfq[5][:8], mfq[8], mfq[6]))
                if db.get_user_data(mfq[3])[5] != 1:
                    db.set_active(mfq[3], 1)
            except:
                db.set_active(mfq[3], 0)
        elif mfq[1] == 'one_day_left_try_period':
            try:
                await bot.send_message(mfq[2], one_d_left_try_period_msg )
                if db.get_user_data(mfq[2])[5] != 1:
                    db.set_active(mfq[2], 1)
            except:
                db.set_active(mfq[2], 0)
        elif mfq[1] == 'two_days_left_try_period':
            try:
                await bot.send_message(mfq[2], two_d_left_try_period_msg )
                if db.get_user_data(mfq[2])[5] != 1:
                    db.set_active(mfq[2], 1)
            except:
                db.set_active(mfq[2], 0)
        elif mfq[1] == 'close_try_period':
            try:
                await bot.send_message(mfq[2], close_try_period_msg)
                if db.get_user_data(mfq[2])[5] != 1:
                    db.set_active(mfq[2], 1)
            except:
                db.set_active(mfq[2], 0)
        elif mfq[1] == 'block_interface':
            try:
                await bot.send_message(mfq[3], block_payed_config_msg(mfq[13] + ' ' + mfq[14][:8], mfq[8], mfq[6]))
                if db.get_user_data(mfq[2])[5] != 1:
                    db.set_active(mfq[2], 1)
            except:
                db.set_active(mfq[2], 0)

    # elif mfq[0] == 'For_Bot':
    #     pass
    elif mfq[0] == 'For_Admin':
        if mfq[1] == 'недоступен_с_бота':
            await bot.send_message(cfg.ADMIN_ID, f'Cервер {mfq[2]} недоступен с бота')
        elif mfq[1] == 'Cкорость':
            await bot.send_message(cfg.ADMIN_ID, f'Сервер: {mfq[2]}\n'
                                                 f'sender: {mfq[3]} {mfq[4]}\nreciever: {mfq[5]} {mfq[6]}')


async def waiter_from_queue() -> None:
    connection = await connect("amqp://guest:guest@localhost/")
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("to_bot_queue")
        # Принимает сообщения из очереди без подтверждения
        await queue.consume(on_message, no_ack=True)
        await asyncio.Future()
