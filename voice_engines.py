import os
import json
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
            return f"Распознано на русском языке: {ru_res.get('text')}"
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

    def text_to_audio_file(self, text: str, file_path: str):
        temp_file_path = file_path.rstrip('.ogg')
        self.__engine.save_to_file(text=text, filename=temp_file_path)
        self.__engine.runAndWait()
        audio_file = AudioSegment.from_file(temp_file_path)
        audio_file.export(out_f=file_path, format='OGG')
        del audio_file
        os.remove(temp_file_path)

    def get_voices(self, synthesis: bool = False):
        if not synthesis:
            return self.__voices
        return list(filter(lambda x: 'synthesis' in x, self.__voices))


if __name__ == '__main__':
    a = AudioSegment.from_ogg(
        file=r'/Users/bx/PycharmProjects/ODBClient/audio_files/1267097955_20240519215004_file_12.ogg',
        parameters=None
    )
    # print(a.channels)
    # small_vp = VoiceParser(voice_config.small_ru_model)
    # result = small_vp.recognize_from_tg()
    v_f = VoiceFactory()
    v_f.text_to_audio_file(
        text='Привет, я сохраню это в аудио файл',
        file_path=r'/Users/bx/PycharmProjects/ODBClient/audio_files/file.www'
    )

