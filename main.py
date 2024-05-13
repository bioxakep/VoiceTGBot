import asyncio
import logging
from aiogram import Bot, Dispatcher
from bot_core.config import bot_config
from bot_core.handlers import auth, common
logging.basicConfig(level=logging.INFO)
bot = Bot(token=bot_config.bot_key)
dp = Dispatcher()


async def main():
    dp.include_routers(auth.auth_router, common.common_router)
    await bot.send_message(1267097955, "Бот запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
