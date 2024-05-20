import io
import os.path
import datetime

from aiogram.filters import Command
from aiogram import Router, types, F
from voice_engines import VoiceParser
from config import bot_config, voice_config

audio_router = Router()
voice_parser = VoiceParser(model_path=voice_config.small_ru_model)


@audio_router.message(F.content_type == "voice")
async def catch_audio(message: types.Message):
    if str(message.from_user.id) != str(bot_config.admin_id):
        await message.reply(text='Не слышно...')
    # Сохранить в файл, прочитать распознаванием, вывести текст.
    voice_file_info = await message.bot.get_file(message.voice.file_id)
    voice_ogg = io.BytesIO()
    await message.bot.download_file(voice_file_info.file_path, voice_ogg)
    file_prefix = str(message.from_user.id) + '_' + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = file_prefix + '_' + voice_file_info.file_path.split('/')[1]
    print(file_name)
    voice_ogg_path = os.path.join(
        voice_config.audio_files,
        file_name.replace('.oga', '.ogg')
    )
    with open(voice_ogg_path, 'wb') as out_voice_file:
        out_voice_file.write(voice_ogg.read())
    recognized_text = voice_parser.recognize_from_tg(voice_ogg_path)
    await message.reply(text=recognized_text)


@audio_router.message(Command("voice"))
async def create_audio(message: types.Message):
    if str(message.from_user.id) != str(bot_config.admin_id):
        await message.reply(text='Не понятно...')
    await message.reply(text='Скоро здесь будет звук')
