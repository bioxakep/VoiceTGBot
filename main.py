import asyncio
import logging
from aiogram import Bot, Dispatcher
from bot_core.handlers import auth, common, audio
from config import bot_config
logging.basicConfig(level=logging.INFO)
bot = Bot(token=bot_config.bot_key)
dp = Dispatcher()


async def main():
    dp.include_routers(auth.auth_router, audio.audio_router, common.common_router)
    await bot.send_message(bot_config.admin_id, "Бот запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
