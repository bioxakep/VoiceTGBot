from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from bot_core.kbrds import auth_kb

common_router = Router()


@common_router.message(Command("start"))  # /start
async def cmd_start(message: types.Message):
    await message.answer("Привет! Зарегистрируемся?", reply_markup=auth_kb.get_auth_kb())


@common_router.message(Command("id"))  # /id
async def cmd_start(message: types.Message):
    await message.answer(f"Привет! Твой ID: {message.from_user.id}")


@common_router.message(F.text)
async def cmd_start(message: types.Message):
    await message.reply("А ты не петушок?")


@common_router.message(F.sticker)
async def cmd_start(message: types.Message):
    await message.reply("А ты не петушок слать мне стикеры?")


@common_router.message(F.photo)
async def cmd_start(message: types.Message):
    await message.reply("А ты не петушок слать мне фото?")


@common_router.message(F.animation)
async def cmd_start(message: types.Message):
    await message.reply("А ты не петушок слать мне анимации всякие?")
