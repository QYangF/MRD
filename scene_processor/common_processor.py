
from .. scene_config import scene_prompts
from .. scene_processor.scene_processor import SceneProcessor
from .. utils.utils_llm import send_message
from .. utils.helpers import *
from .. utils.utils_prompt import *

class CommonProcessor(SceneProcessor):

    def __init__(self,scene_config,):
       
        parameters = scene_config["parameters"]

        self.scene_config = scene_config
        self.scene_name = scene_config["name"]
        self.slot_template = get_raw_slot(parameters)
        self.slot_dynamic_example = get_dynamic_example(scene_config)
        self.slot = get_raw_slot(parameters)
        self.scene_prompts = scene_prompts

    def process(self, user_input, context):

        message = get_slot_update_message(self.scene_name, self.slot_dynamic_example, self.slot_template, user_input)  
        new_info_json_raw = send_message('user',message)
        current_values = extract_json_from_string(new_info_json_raw["result"])


        update_slot(current_values, self.slot)  

        result={}
        if is_slot_fully_filled(self.slot): 
          
            result= {
            "complete": True,
            "slot": self.slot,
            "message": format_name_value_for_logging(self.slot) 
            }
            
        else:
          
            result= {
            "complete": False,
            "slot": self.slot,
            "message": self.ask_user_for_missing_data(user_input)   
            }
        return result

    
    def ask_user_for_missing_data(self, user_input):
      
        message = get_slot_query_user_message(self.scene_name, self.slot, user_input)

        result = send_message('user',message)  #  result["result"]
        return result
