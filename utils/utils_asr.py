import os
import appbuilder
import wave

from . import utils_configs
from . import API_KEY


def speech_recognition(audio_path):
    os.environ["APPBUILDER_TOKEN"] = API_KEY.APPBUILDER_TOKEN
    asr = appbuilder.ASR()  
    
    with wave.open(audio_path, 'rb') as wav_file:

        num_channels = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()
        framerate = wav_file.getframerate()
        num_frames = wav_file.getnframes()


        frames = wav_file.readframes(num_frames)


    content_data = {"audio_format": "wav", "raw_audio": frames, "rate": framerate}
    message = appbuilder.Message(content_data)
    speech_result = asr.run(message).content['result'][0]
    return speech_result


