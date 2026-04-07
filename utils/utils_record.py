import pyaudio
import wave
import numpy as np


def record_auto():
  
    MIC_INDEX = 1
    CHUNK = 1024 
    RATE = 16000  
    QUIET_DB = 600  
    delay_time = 2  
    FORMAT = pyaudio.paInt16  
    CHANNELS = 1  

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=MIC_INDEX
                    )

    frames = []  
    flag = False  
    quiet_flag = False  
    temp_time = 0  
    last_ok_time = 0  
    START_TIME = 0  
    END_TIME = 0  
    issuccess = False 
    while True:
    
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)
        temp_volume = np.max(np.frombuffer(data, dtype=np.short))

        if temp_volume > QUIET_DB and flag == False:
            flag = True
            START_TIME = temp_time
            last_ok_time = temp_time
            issuccess=True

        if flag:  

            if (temp_volume < QUIET_DB and quiet_flag == False):
                quiet_flag = True
                last_ok_time = temp_time

            if (temp_volume > QUIET_DB):
                quiet_flag = False
                last_ok_time = temp_time

            if (temp_time > last_ok_time + delay_time * 15 and quiet_flag == True):
                if (quiet_flag and temp_volume < QUIET_DB):
                    END_TIME = temp_time
                    break
                else:
                    quiet_flag = False
                    last_ok_time = temp_time

    
        temp_time += 1
        if temp_time > 150:  
            END_TIME = temp_time
            break

    stream.stop_stream()
    stream.close()
    p.terminate()


    if (issuccess == True):

        output_path = 'D:/myProject/HRI/temp/speech_record.wav'
        wf = wave.open(output_path, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames[START_TIME - 2:END_TIME]))
        wf.close()

        return True
    return False


