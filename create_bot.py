from aiogram import Bot, Dispatcher
import config as cfg
import logging
from aiogram.contrib.fsm_storage.memory import MemoryStorage
#from aiogram.contrib.fsm_storage.redis import RedisStorage2


# хранилище состояний FSM
stor = MemoryStorage()
#stor = RedisStorage2()

# Объект бота
bot = Bot(token=cfg.TOKEN, parse_mode="HTML")
# Диспетчер для бота
dp = Dispatcher(bot, storage=stor)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
