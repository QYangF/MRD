
import cv2
import os
import matplotlib.patches as patches
from matplotlib import pyplot as plt
import numpy as np
import yaml
import torch
from pathlib import Path
from sklearn.cluster import KMeans

import sys

YOLOV9_PATH = r'd:\myProject'
if YOLOV9_PATH not in sys.path:
    sys.path.insert(0, YOLOV9_PATH)


from yolov9.detect import run, parse_opt, main
from yolov9.models.common import DetectMultiBackend

image_path = 'D:/myProject/HRI/temp/detect.jpg'
weights='D:/myProject/yolov9/weights/gelan-c.pt'
detections_path = 'D:/myProject/HRI/temp/labels/detect.txt'
def process_detect_result():

    #  <class_id> <x_center> <y_center> <width> <height> <confidence>
    image = cv2.imread(image_path)
    image_height, image_width, _ = image.shape
    objects = []
    with open(detections_path, 'r') as file:
    
        for line in file:
            components = line.split()
            class_id = int(components[0])
            confidence = float(components[5])
            cx, cy, w, h = [float(x) for x in components[1:5]]  #  不包含5


            cx *= image_width
            cy *= image_height
            w *= image_width
            h *= image_height


            xmin = cx - w / 2
            ymin = cy - h / 2

            bbox = {
                'x': xmin,
                'y': ymin,
                'width': w,
                'height': h
            }
            corlor=get_dominant_color(image, bbox, 3)
            detect_result={
                'class_id': class_id,
                'confidence': confidence,
                'x': xmin,
                'y': ymin,
                'width': w,
                'height': h ,
                'color':corlor
            }
            objects.append(detect_result)
    return objects

def get_color_name(bgr_value):

    b, g, r = bgr_value  


    color = np.uint8([[[b, g, r]]])
    hsv_color = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)[0][0]

    hue = hsv_color[0]
    saturation = hsv_color[1]
    value = hsv_color[2]

    if saturation < 50 and value > 200:
        return "White"
    elif saturation < 50 and value < 50:
        return "Black"
    elif value < 100:
        return "Dark"
    elif hue < 10 or hue > 170:
        return "Red"
    elif 10 <= hue < 30:
        return "Orange"
    elif 30 <= hue < 70:
        return "Yellow"
    elif 70 <= hue < 150:
        return "Green"
    elif 150 <= hue < 170:
        return "Blue"
    else:
        return "Other"

def get_dominant_color(image, bbox, k):

    x = int(bbox['x'])
    y = int(bbox['y'])
    w = int(bbox['width'])
    h = int(bbox['height'])


    roi = image[y:y+h, x:x+w]


    if roi.size == 0:
        return (255, 255, 255), "White"


    roi = cv2.resize(roi, (64, 64))


    pixels = roi.reshape(-1, 3)


    kmeans = KMeans(n_clusters=k, n_init=10)
    kmeans.fit(pixels)

    counts = np.bincount(kmeans.labels_)
    cluster_centers = kmeans.cluster_centers_.astype(int)


    dominant_color = cluster_centers[np.argmax(counts)]


    color_name = get_color_name(dominant_color)

    return color_name
    

def yolov9_inference(image_path, weights, conf_thres=0.25, iou_thres=0.45, show_result=True,
                     save_result=True):
   
    opt = parse_opt()
    opt.source = image_path
    opt.weights = weights
    opt.conf_thres = conf_thres
    opt.iou_thres = iou_thres
    opt.view_img = show_result
    opt.save_txt = save_result  
    opt.save_conf = True  
    opt.nosave = save_result  

    opt.project = 'D:/myProject/HRI/temp'
    opt.name = ''                                 
    opt.exist_ok = True                           


    with open(detections_path, 'w') as file:
        file.write('') 


    with torch.no_grad():
        main(opt)


    image_name = os.path.basename(image_path)
    default_output_path = os.path.join(opt.project, '', image_name)

 
    custom_output_path = 'D:/myProject/HRI/temp/result_image.jpg'

    if os.path.exists(default_output_path):

        result_image = cv2.imread(default_output_path)
        cv2.imwrite(custom_output_path, result_image)


    return None  


