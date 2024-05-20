import io
import os.path
import datetime

import aiogram
from aiogram.filters import Command, StateFilter
from aiogram import Router, types, F
from aiogram.types import FSInputFile

from voice_engines import VoiceRecognizer, VoiceFactory
from config import bot_config, voice_config
from .auth import AuthState

audio_router = Router()


@audio_router.message(StateFilter(AuthState.auth_with_phone), F.content_type == "voice")
async def catch_audio_from_auth_user(message: types.Message):
    if str(message.from_user.id) != str(bot_config.admin_id):
        await message.reply(text='Не слышно...')
    # Сохранить в файл, прочитать распознаванием, вывести текст.
    voice_file_info = await message.bot.get_file(message.voice.file_id)
    voice_ogg = io.BytesIO()
    await message.bot.download_file(voice_file_info.file_path, voice_ogg)
    file_prefix = str(message.from_user.id) + '_' + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = ''.join(
        [
            file_prefix,
            '_',
            voice_file_info.file_path.split('/')[1]
        ]
    )
    voice_ogg_path = os.path.join(
        voice_config.audio_files,
        file_name.replace('.oga', '.ogg')
    )
    with open(voice_ogg_path, 'wb') as out_voice_file:
        out_voice_file.write(voice_ogg.read())
    voice_recognizer = VoiceRecognizer(model_path=voice_config.small_ru_model)
    recognized_text = voice_recognizer.recognize_from_tg(voice_ogg_path)
    await message.reply(text=recognized_text)


@audio_router.message(Command("voice"))
async def create_audio(message: types.Message):
    if str(message.from_user.id) != str(bot_config.admin_id):
        await message.reply(text='Не понятно...')
    new_file_path: str = os.path.join(voice_config.audio_files, 'new_file.ogg')
    await message.bot.send_chat_action(message.from_user.id, aiogram.enums.ChatAction.TYPING)
    voice_factory = VoiceFactory()
    voice_factory.text_to_audio_file(text='Отправка аудиофайла', file_path=new_file_path)
    await message.bot.send_chat_action(message.from_user.id, aiogram.enums.ChatAction.UPLOAD_VOICE)
    input_file = FSInputFile(path=new_file_path, filename='Аудио.ogg')
    await message.answer_audio(audio=open(new_file_path, 'rb'), title='Hello', caption='Sound', performer='AAA')
