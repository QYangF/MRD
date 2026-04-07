from .. scene_processor.common_processor import CommonProcessor
from .. scene_processor.action_recognition import Action_Recognition
from .. utils.utils_llm import *
from .. utils.utils_data_format import *
from .. utils.API_KEY import *

from .. utils.utils_match_objects import match_objects
from .. utils.draw_picture_result import *
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

audio_path = 'D:/myProject/HRI/temp/speech_record.wav'
image_path='D:/myProject/HRI/temp/draw.jpg'

class ChatbotModel:
    def __init__(self,scene_templates:dict):
        self.scene_templates = scene_templates
        self.templates: dict = scene_templates
     
        self.current_purpose: str=''
   
        self.processors= {}

    @staticmethod
    def load_scene_processor(current_purpose, scene_config):
     
        try:
            if current_purpose == 'action_recognition':  
           
                return Action_Recognition(scene_config)
            
            else :
       
         
                return CommonProcessor(scene_config)
        except (ImportError, AttributeError, KeyError):
            raise ImportError({scene_config}")

    def is_related_to_last_intent(self, user_input):
       
        if  not self.current_purpose :   
            
            return False
        
        
        prompt =  {self.scene_templates[self.current_purpose]['description']}
        result = send_message('user',prompt)
        return extract_float(result["result"])>RELATED_INTENT_THRESHOLD

    def get_processor_for_scene(self, current_purpose):
        if current_purpose in self.processors:
            return self.processors[current_purpose]

        scene_config = self.scene_templates.get(current_purpose)
        if not scene_config:
            raise ValueError()

        processor_class = self.load_scene_processor(self.current_purpose, scene_config)
        self.processors[current_purpose] = processor_class
        return self.processors[current_purpose]
    def recognize_intent(self, user_input):
     
        purpose_options = {}
        purpose_description = {}
        index = 1

        for template_key, template_info in self.scene_templates.items():
         
            purpose_options[str(index)] = template_key 
            purpose_description[str(index)] = template_info["description"] 
            index += 1
        options_prompt = "\n".join([f"{key}. {value} - 请回复{key}" for key, value in purpose_description.items()])
        options_prompt += ""
        
     
        user_choice = send_message('user',{options_prompt}\n")
        
        user_choices = extract_continuous_digits(user_choice["result"])

        if user_choices and user_choices[0] != '0':
            self.current_purpose = purpose_options[user_choices[0]]

        if self.current_purpose:
           
        else:

    def process_multi_question(self , user_input ):     

        if not self.is_related_to_last_intent(user_input) :
   
            self.recognize_intent(user_input)

        if self.current_purpose in self.scene_templates:
        
            self.get_processor_for_scene(self.current_purpose)
            

            self.processors[self.current_purpose].process(user_input, None)

            return 1  

        return 0    
        











