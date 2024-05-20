import json
import os.path
import pyttsx3
from config import voice_config
from vosk import Model, KaldiRecognizer
from pydub import AudioSegment


class VoiceParser:
    FREQ = 16000

    def __init__(self, model_path: str):
        self.__model = Model(model_path)
        self.__recognizer = KaldiRecognizer(self.__model, VoiceParser.FREQ)
        AudioSegment.converter = '/opt/homebrew/Cellar/ffmpeg/7.0_1/bin/ffmpeg'

    def recognize_from_tg(self, ogg_file_path: str):
        voice_wav_path = os.path.join(
            voice_config.audio_files,
            os.path.basename(ogg_file_path.replace('.ogg', '.wav'))
        )
        print(voice_wav_path)
        print(ogg_file_path)
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
    def __init__(self):
        self.__engine = pyttsx3.init()
        self.__engine.setProperty('rate', 120)
        # for v in engine.getProperty('audio_files'):
        #     engine.setProperty('voice', v.id)
        #     print(v.id)
        #     engine.say("Hi John")
        #     engine.runAndWait()
        # out_file_path = os.path.join(voice_config.audio_files, 'output.ogg')
        # self.__engine.save_to_file(text='Привет, Варвара', filename=out_file_path)
        self.__engine.runAndWait()


if __name__ == '__main__':
    # AudioSegment.converter = '/opt/homebrew/Cellar/ffmpeg/7.0_1/bin/ffmpeg'
    a = AudioSegment.from_ogg(r'/Users/bx/PycharmProjects/ODBClient/audio_files/1267097955_20240519215004_file_12.ogg', parameters=None)
    print(a.channels)
    # small_vp = VoiceParser(voice_config.small_ru_model)
    # result = small_vp.recognize_from_tg()
    # v_f = VoiceFactory()
