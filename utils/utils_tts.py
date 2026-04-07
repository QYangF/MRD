import appbuilder
from . import utils_configs


def tts(TEXT, tts_wav_path):

    tts_ab = appbuilder.TTS()
    inp = appbuilder.Message(content={"text": TEXT})
    out = tts_ab.run(inp, model="paddlespeech-tts", audio_type="wav")

    with open(tts_wav_path, "wb") as f:
        f.write(out.content["audio_binary"])

