import io
import os.path
import datetime
import aiogram
from aiogram.filters import Command, StateFilter
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile

from voice_engines import VoiceRecognizer, VoiceFactory
from config import bot_config, voice_config

audio_router = Router()


class AudioStates(StatesGroup):
    recognize_text = State()


@audio_router.message(StateFilter(AudioStates.recognize_text), F.content_type == "voice")
async def catch_audio_from_auth_user(message: types.Message, state: FSMContext):
    # Сохранить в файл, прочитать распознаванием, вывести текст.
    voice_file_info = await message.bot.get_file(message.voice.file_id)
    voice_ogg = io.BytesIO()
    await message.bot.download_file(voice_file_info.file_path, voice_ogg)

    file_prefix = str(message.from_user.id) + '_' + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = file_prefix + '_' + voice_file_info.file_path.split('/')[1].replace('.oga', '.ogg')
    voice_ogg_path = os.path.join(voice_config.audio_files, file_name)
    with open(voice_ogg_path, 'wb') as out_voice_file:
        out_voice_file.write(voice_ogg.read())
    voice_recognizer = VoiceRecognizer(model_path=voice_config.small_ru_model)
    recognized_text = voice_recognizer.recognize_from_tg(voice_ogg_path)
    await message.reply(text=recognized_text)
    await state.clear()
    # await message.reply_audio(audio=FSInputFile(path=voice_ogg_path, filename='File.ogg'))


@audio_router.message(Command("text"))
async def start_recognize_text(message: types.Message, state: FSMContext):
    await state.set_state(AudioStates.recognize_text)
    await message.reply(text='Отправьте боту аудиозапись, текст из которой вам нужно получить.')


@audio_router.message(Command("voice"))
async def recognize_text(message: types.Message):
    text = message.text.replace('/voice', '')
    if len(text) < 5:
        await message.reply('Слишком короткий текст, он должен быть не менее 5 символов.')
        return
    if len(text) > 1000:
        await message.reply('Слишком длинный текст, он должен быть не более 999 символов.')
        return
    voice_factory = VoiceFactory()
    voice_file_path = voice_factory.text_to_audio_file(text=text[:1000])
    await message.bot.send_chat_action(message.from_user.id, aiogram.enums.ChatAction.UPLOAD_VOICE)
    await message.reply_audio(audio=FSInputFile(path=voice_file_path))
