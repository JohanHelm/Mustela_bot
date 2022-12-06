import asyncio

from aio_pika import connect
from aio_pika.abc import AbstractIncomingMessage
import config as cfg
from create_bot import bot
from database import db
from infmsg import close_try_period_msg, one_d_left_try_period_msg, two_d_left_try_period_msg, block_payed_config_msg, \
    one_d_payed_left_msg, two_d_payed_left_msg


async def on_message(message: AbstractIncomingMessage) -> None:
    message_from_queue = message.body.decode('UTF-8').split()
    if message_from_queue[1] == 'one_day_left_try_period':
        try:
            await bot.send_message(message_from_queue[0], one_d_left_try_period_msg)
            if db.get_user_data(message_from_queue[0])[5] != 1:
                db.set_active(message_from_queue[0], 1)
        except:
            db.set_active(message_from_queue[0], 0)
    elif message_from_queue[1] == 'two_days_left_try_period':
        try:
            await bot.send_message(message_from_queue[0], two_d_left_try_period_msg)
            if db.get_user_data(message_from_queue[0])[5] != 1:
                db.set_active(message_from_queue[0], 1)
        except:
            db.set_active(message_from_queue[0], 0)
    elif message_from_queue[1] == 'close_try_period':
        try:
            await bot.send_message(message_from_queue[0], close_try_period_msg)
            if db.get_user_data(message_from_queue[0])[5] != 1:
                db.set_active(message_from_queue[0], 1)
        except:
            db.set_active(message_from_queue[0], 0)
    elif message_from_queue[1] == 'server_unreachable':
        await bot.send_message(cfg.ADMIN_ID, f'Сервер {message_from_queue[0]} недоступен с бота')
    elif message_from_queue[6] == 'one_day_payed_left':
        try:
            await bot.send_message(message_from_queue[0],
                                   one_d_payed_left_msg(message_from_queue[1], message_from_queue[2],
                                                        message_from_queue[3], message_from_queue[5]))
            if db.get_user_data(message_from_queue[0])[5] != 1:
                db.set_active(message_from_queue[0], 1)
        except:
            db.set_active(message_from_queue[0], 0)
    elif message_from_queue[6] == 'two_days_payed_left':
        try:
            await bot.send_message(message_from_queue[0],
                                   two_d_payed_left_msg(message_from_queue[1], message_from_queue[2],
                                                        message_from_queue[3], message_from_queue[5]))
            if db.get_user_data(message_from_queue[0])[5] != 1:
                db.set_active(message_from_queue[0], 1)
        except:
            db.set_active(message_from_queue[0], 0)
    elif message_from_queue[6] == 'block_interface':
        try:
            await bot.send_message(message_from_queue[0], block_payed_config_msg(message_from_queue[1],
                                                                                 message_from_queue[2],
                                                                                 message_from_queue[3],
                                                                                 message_from_queue[5]))
            if db.get_user_data(message_from_queue[0])[5] != 1:
                db.set_active(message_from_queue[0], 1)
        except:
            db.set_active(message_from_queue[0], 0)


async def waiter_from_queue() -> None:
    connection = await connect("amqp://guest:guest@localhost/")
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("to_bot_queue")
        # Принимает сообщения из очереди без подтверждения
        await queue.consume(on_message, no_ack=True)
        await asyncio.Future()
