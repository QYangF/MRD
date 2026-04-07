import sys
import os
import pyaudio
import wave

def play_wav(wav_file):
 
    wf = wave.open(wav_file, 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    chunk_size = 1024

    data = wf.readframes(chunk_size)

    while data != b'':
        stream.write(data)
        data = wf.readframes(chunk_size)

    stream.stop_stream()
    stream.close()
    p.terminate()
