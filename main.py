from aiogram import executor
from create_bot import dp
from hendlers import common, client, admin

admin.register_admin_handlers(dp)
client.register_client_handlers(dp)
common.register_common_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
