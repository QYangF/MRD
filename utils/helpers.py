# encoding=utf-8
import glob
import json
import re

def filename_to_classname(filename):

    parts = filename.split('_')
    class_name = ''.join(part.capitalize() for part in parts)
    return class_name


def load_scene_templates(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def load_all_scene_configs():

    all_scene_configs = {}


    for file_path in glob.glob("HRI/scene_config/**/*.json", recursive=True):
        current_config = load_scene_templates(file_path)

        for key, value in current_config.items():

            if key not in all_scene_configs:
                all_scene_configs[key] = value

    return all_scene_configs


def is_slot_fully_filled(json_data):
    
    for item in json_data:
      
        if item.get('value') == '':
            return False  
    return True 


def get_raw_slot(parameters):
   
    output_data = []
    for item in parameters:
        new_item = {"name": item["name"], "desc": item["desc"], "type": item["type"], "value": ""}
        output_data.append(new_item)

    return output_data


def get_dynamic_example(scene_config):

    if 'example' in scene_config:
        return scene_config['example']
    else:
        return '{"name":"xx","value":"xx"}'


def get_slot_update_json(slot):
 
    output_data = []
    for item in slot:
        new_item = {"name": item["name"], "desc": item["desc"], "value": item["value"]}
        output_data.append(new_item)
    return output_data


def get_slot_query_user_json(slot):

    output_data = []
    for item in slot:
        if not item["value"]:
            new_item = {"name": item["name"], "desc": item["desc"], "value":  item["value"]}
            output_data.append(new_item)
    return output_data


def update_slot(json_data, dict_target):
   
    for item in json_data:
      
        if item['value'] != '':
            for target in dict_target:
                if target['name'] == item['name']:
                    target['value'] = item.get('value')
                    break


def format_name_value_for_logging(json_data):
  
    log_strings = []
    for item in json_data:
        name = item.get('name', 'Unknown name')  
        value = item.get('value', 'N/A') 
        log_string = f"name: {name}, Value: {value}"
        log_strings.append(log_string)
    return '\n'.join(log_strings)


def extract_json_from_string(input_string):
   
    try:
        
        matches = re.findall(r'\{.*?\}', input_string, re.DOTALL)

        valid_jsons = []
        for match in matches:
            try:
                json_obj = json.loads(match)
                valid_jsons.append(json_obj)
            except json.JSONDecodeError:
                try:
                    valid_jsons.append(fix_json(match))
                except json.JSONDecodeError:
                    continue  
                continue  

        return valid_jsons
    except Exception as e:
        print(f"Error occurred: {e}")
        return []


def fix_json(bad_json):

    fixed_json = bad_json.replace("'", '"')
    try:

        return json.loads(fixed_json)
    except json.JSONDecodeError:



