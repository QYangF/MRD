from .. scene_config import scene_prompts
from .. scene_processor.scene_processor import SceneProcessor
from .. utils.utils_llm import send_message
from .. utils.helpers import *
from .. utils.utils_prompt import *
from .. utils.utils_data_format import *
from .. utils.utils_tts import tts
from .. utils.utils_playaudio import play_wav
from .. utils.utils_record import record_auto
from .. utils.utils_asr import speech_recognition
from .. utils.utils_match_objects import match_objects
from .. utils.draw_picture_result import draw_picture_result
from .. utils.utils_take_picture import take_picture
from ..  utils_detect import *

audio_path = 'D:/myProject/HRI/temp/speech_record.wav'
image_path='D:/myProject/HRI/temp/detect.jpg'
weights='D:/myProject/yolov9/weights/gelan-c.pt'

class Action_Recognition(SceneProcessor):

    def __init__(self,scene_config):
        parameters = scene_config["parameters"]
        self.scene_config = scene_config
        self.scene_name = scene_config["name"]
        self.slot_template = get_raw_slot(parameters)
        self.slot_dynamic_example = get_dynamic_example(scene_config)
        self.slot = get_raw_slot(parameters)
        self.scene_prompts = scene_prompts

    def process(self, user_input, context):

        take_picture()
        yolov9_inference(
        image_path=image_path,
        weights=weights,
        conf_thres=0.4,
        iou_thres=0.5,
        show_result=True, 
        save_result=True  
        )
        process_detect_result()

      
        
        return_message = send_message('user',message)
        action_class = extract_continuous_digits(return_message["result"])

        if action_class and action_class[0] == '1':
            
            new_scene_config['parameters'] = parameter
            
            parameters = new_scene_config["parameters"]
            self.scene_config = new_scene_config
            self.scene_name = new_scene_config["name"]
            self.slot_template = get_raw_slot(parameters)
            self.slot_dynamic_example = get_dynamic_example(new_scene_config)
            self.slot = get_raw_slot(parameters)
            self.scene_prompts = scene_prompts
 
              

        elif action_class and action_class == '2':

        

        message = get_slot_update_message(self.scene_name, self.slot_dynamic_example, self.slot_template, user_input)  
        new_info_json_raw = send_message('user',message)
        current_values = extract_json_from_string(new_info_json_raw["result"])
        
      
        update_slot(current_values, self.slot)  
        

        while  not is_slot_fully_filled(self.slot):   

            question=self.ask_user_for_missing_data(self, user_input)["result"]
            

            user_input = input(question + "\n ")
            message = get_slot_update_message(self.scene_name, self.slot_dynamic_example, self.slot_template, user_input)  
            new_info_json_raw = send_message('user',message)
            current_values = extract_json_from_string(new_info_json_raw["result"])

            update_slot(current_values, self.slot)  
            
        object1,object2,flag=match_objects(self.slot)
       
        picture=[]
        if flag == 1:
  
            if len(object1)==1:
                picture.append(object1[0]) 
            
            elif len(object1)==0:
                user_input = input(question + "\n ")
                return  False
            else:
                while True:
               
                    question=self.slot[0]["value"]
 
                    user_input = input(question + "\n ")
                    message = confirm_targets(user_input)  
                    new_info_json_raw = send_message('user',message)
                    current_values = extract_json_from_string(new_info_json_raw["result"])
                    if current_values[1]["value"] !=  ""  or  current_values[3]["value"] != "":
                        break
               
                if  'left' in current_values[1]["value"]:
          
                    matched_results = sorted(object1, key=lambda obj: obj['x'])
                    
             
                    num=int(current_values[2]["value"])-1
                    picture.append(matched_results[num])                    

                elif 'right' in current_values[1]["value"]:
                  
                    matched_results = sorted(object1, key=lambda obj: obj['x'])
                    
                
                    num=len(matched_results)-int(current_values[2]["value"])
                    picture.append(matched_results[num])                    

                elif 'back' in current_values[1]["value"]:
                
                    matched_results = sorted(object1, key=lambda obj: obj['y'])

          
                    num=len(matched_results)-1
                    picture.append(matched_results[num])               

                elif 'front' in current_values[1]["value"]:

                    matched_results = sorted(object1, key=lambda obj: obj['y'])
                    

                    num=len(matched_results)-int(current_values[2]["value"])
                    picture.append(matched_results[num]) 

        elif flag == 2:
            if len(object1)==1 :
                picture.append(object1[0])  
            if len(object2)==1:
                picture.append(object2[0])
            
            if len(object1)==0:
       
                question=self.slot[0]["value"]
              
                user_input = input(question + "\n ")
                return  False
            if len(object2)==0:
              
                question=self.slot[1]["value"]
          
                user_input = input(question + "\n ")
                return False
            
            if len(object1) !=1 :
        
                while True:
               
                    question=self.slot[0]["value"]
                   
                    user_input = input(question + "\n ")

                   
                    message = confirm_targets(user_input)  
                   
                    new_info_json_raw = send_message('user',message)
                    current_values = extract_json_from_string(new_info_json_raw["result"])

                    if current_values[1]["value"] !=  ""  or  current_values[3]["value"] != "":
                        break
                
                if  'left' in current_values[1]["value"]:
                    matched_results = sorted(object1, key=lambda obj: obj['x'])

                    num=int(current_values[2]["value"])-1
                    picture.append(matched_results[num])
                    

                elif 'right' in current_values[1]["value"]:

                    matched_results = sorted(object1, key=lambda obj: obj['x'])
                    
                    num=len(matched_results)-int(current_values[2]["value"])
                    
                    picture.append(matched_results[num])
                    

                elif 'back' in current_values[1]["value"]:
           
                    matched_results = sorted(object1, key=lambda obj: obj['y'])

                  
                    num=len(matched_results)-1
                    picture.append(matched_results[num])
                    

                elif 'front' in current_values[1]["value"]:
                   
                    matched_results = sorted(object1, key=lambda obj: obj['y'])
                    
                   
                    num=len(matched_results)-int(current_values[2]["value"])
                    picture.append(matched_results[num])

            elif  len(object2) !=1 :
                while True:
               
                    question= self.slot[1]["value"]
                    
                   

                 
                    user_input = input(question + "\n ")

                 
                    message = confirm_targets(user_input)  
                    new_info_json_raw = send_message('user',message)
                    current_values = extract_json_from_string(new_info_json_raw["result"])
                    if current_values[1]["value"] !=  ""  or  current_values[3]["value"] != "":
                        break
                if  'left' in current_values[1]["value"]:
                 
                    matched_results = sorted(object2, key=lambda obj: obj['x'])
                    

                    num=int(current_values[2]["value"])-1
                    picture.append(matched_results[num])

                elif 'right' in current_values[1]["value"]:

                    matched_results = sorted(object2, key=lambda obj: obj['x'])
                    
                 
                    num=len(matched_results)-int(current_values[2]["value"])
                    picture.append(matched_results[num])

                elif 'back' in current_values[1]["value"]:
                   
                    matched_results = sorted(object2, key=lambda obj: obj['y'])

                    num=len(matched_results)-1
                    picture.append(matched_results[num])
                    

                elif 'front' in current_values[1]["value"]:
                    matched_results = sorted(object2, key=lambda obj: obj['y'])

                    num=len(matched_results)-int(current_values[2]["value"])
                    picture.append(matched_results[num])
 
        draw_picture_result(picture)
        
        return  True      
             

    def ask_user_for_missing_data(self, user_input):

        message = get_slot_query_user_message(self.scene_name, self.slot, user_input)

        result = send_message('user',message)  #  result["result"]
        return result
