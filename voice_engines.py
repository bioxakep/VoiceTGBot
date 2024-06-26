import os
import json
from datetime import datetime

import pyttsx3
from vosk import Model, KaldiRecognizer
from pydub import AudioSegment
from config import voice_config


class VoiceRecognizer:
    FREQ = 16000

    def __init__(self, model_path: str):
        """ Инициализация модели распознавания с установкой частоты дискретизации аудиопотока """
        self.__model = Model(model_path)
        self.__recognizer = KaldiRecognizer(self.__model, VoiceRecognizer.FREQ)
        # AudioSegment.converter = '/opt/homebrew/Cellar/ffmpeg/7.0_1/bin/ffmpeg'

    def recognize_from_tg(self, ogg_file_path: str):
        voice_wav_path = os.path.join(
            voice_config.audio_files,
            os.path.basename(ogg_file_path.replace('.ogg', '.wav'))
        )
        audio = AudioSegment.from_ogg(ogg_file_path)
        audio = audio.set_sample_width(2).set_frame_rate(16000)
        audio.export(voice_wav_path, format="wav")
        audio = AudioSegment.from_wav(voice_wav_path)
        self.__recognizer.AcceptWaveform(audio.raw_data)
        os.remove(voice_wav_path)
        ru_res = json.loads(self.__recognizer.FinalResult())
        if 'text' in ru_res.keys():
            return f"Распознан текст: {ru_res.get('text')}"
        return "Не распознано."


class VoiceFactory:
    DEFAULT_RU_VOICE = 'com.apple.voice.enhanced.ru-RU.Milena'

    def __init__(self, voice: str | None = None, sex: str = 'Female', age: int | None = None):
        self.__engine = pyttsx3.init()
        self.__engine.setProperty('rate', 180)
        self.__engine.setProperty('volume', 1.0)
        self.__voices = list(map(lambda x: x.id, self.__engine.getProperty('voices')))
        if voice is not None and voice in self.__voices:
            self.__engine.setProperty('voice', voice)
        else:
            self.__engine.setProperty('voice', VoiceFactory.DEFAULT_RU_VOICE)

    def say_text(self, text: str):
        self.__engine.say(text)
        self.__engine.runAndWait()

    def text_to_audio_file(self, text: str):
        file_name: str = 'FROM_TEXT_' + datetime.now().strftime("%Y%m%d%H%M%S") + '.wav'
        temp_audio_file_path: str = os.path.join(voice_config.audio_files, file_name)
        self.__engine.save_to_file(text=text, filename=temp_audio_file_path)
        self.__engine.runAndWait()
        audio_file = AudioSegment.from_file(temp_audio_file_path)
        print(audio_file.channels, audio_file.duration_seconds)
        ogg_file_path: str = temp_audio_file_path.replace('.wav', '.ogg')
        audio_file.export(out_f=ogg_file_path, format='ogg', codec='libopus')
        del audio_file
        os.remove(temp_audio_file_path)
        return ogg_file_path

    def get_voices(self, synthesis: bool = False):
        if not synthesis:
            return self.__voices
        return list(filter(lambda x: 'synthesis' in x, self.__voices))


if __name__ == '__main__':
    factory = VoiceFactory()
    factory.text_to_audio_file(text='Привет малышка, как твои дела? Хотел увидеть отчет о проделанной работе')
