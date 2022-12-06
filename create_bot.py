from aiogram import Bot, Dispatcher
import config as cfg
import logging
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# хранилище состояний FSM
stor = MemoryStorage()

# Объект бота
bot = Bot(token=cfg.TOKEN, parse_mode="HTML")
# Диспетчер для бота
dp = Dispatcher(bot, storage=stor)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)


# проверяет статус пользователя
def chat_member_status(chat_member):
    return chat_member['status']
