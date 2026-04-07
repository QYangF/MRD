
import re


def extract_float(s):

    float_pattern = r'-?\d+(?:\.\d+)?'
    found = re.findall(float_pattern, s)
    if not found: 
        return 0.0
    else:
        return [float(num) for num in found][0]


def extract_floats(s):

    float_pattern = r'-?\d+(?:\.\d+)?'
    found = re.findall(float_pattern, s)
    if not found:  
        return [0.0]
    else:
        return [float(num) for num in found]


def extract_continuous_digits(text):

    continuous_digits = re.findall(r'\d+', text)
    return continuous_digits


def clean_json_string(json_str):

    cleaned_str = re.search(r'(\{.*\}|\[.*\])', json_str)
    if cleaned_str:
        return cleaned_str.group()
    else:
        return None
