from aiogram import Router, types, F

auth_router = Router()


@auth_router.message(F.text.lower() == "без предоставления номера")
async def auth_without_phone(message: types.Message):
    await message.reply(f"Твой ID {message.from_user.id}. Обратись с этим к администратору.",
                        reply_markup=types.ReplyKeyboardRemove())


@auth_router.message(F.contact)
async def auth_with_phone(message: types.Message):
    user_phone = message.contact.phone_number
    user_id = message.contact.user_id
    await message.reply(f"Теперь ты в теме с номером {message.contact.phone_number}",
                        reply_markup=types.ReplyKeyboardRemove())
