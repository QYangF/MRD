from . utils import utils_record
from . utils import utils_asr
from . utils import utils_configs
from . utils import utils_playaudio
from . models.chatbot_model import ChatbotModel
from . utils.helpers import load_all_scene_configs
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def go_angent():

    utils_configs.configs()

    all_scene_configs=load_all_scene_configs()

    chatbot_model = ChatbotModel(all_scene_configs)
    audio_path = 'D:/myProject/HRI/temp/speech_record.wav'
    
    flag = 0   
    user_input=''  


    while True:

        if (utils.utils_record.record_auto()):  

            user_input=utils.utils_asr.speech_recognition(audio_path)
           
            if (flag == 0):  
                if('Hello' in user_input):
                    flag=1

                    utils.utils_playaudio.play_wav('D:/myProject/HRI/temp/welcome.wav')
  
                    if(utils.utils_record.record_auto()):
                        user_input=utils.utils_asr.speech_recognition(audio_path)

            if (flag == 1): 
                if ('End' in user_input ):  

                    utils.utils_playaudio.play_wav('D:/myProject/HRI/temp/goodbye.wav')
                    flag=0
                    continue   
                else :

                    if user_input.strip() != '':
 
                        chatbot_model.process_multi_question(user_input)
    
   

if __name__ == '__main__':
    go_angent()


