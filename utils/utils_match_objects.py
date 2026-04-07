from . utils_detect import process_detect_result


def match_objects(slot):
    objects=process_detect_result()
    object1=[]
    object2=[]
    flag=0

    if len(slot) == 2:
        flag=1
        target = slot[0]['value']
        for obj in objects:
            if class_dict[int(obj['class_id'])] in target:
                objs={
                    'target': '0',
                    'class_id': obj['class_id'],
                    'name':  class_dict[int(obj['class_id'])],
                    'confidence': obj['confidence'],
                    'name': '',
                    'x': obj['x'],
                    'y': obj['y'],
                    'width': obj['width'],
                    'height': obj['height'] ,
                    'color':obj['color']
                }
                
                object1.append(objs)
            
    if len(slot) == 3:
        flag=2
        target1 = slot[0]['value']
        target2 = slot[1]['value']
        for obj in objects:
            if  class_dict[int(obj['class_id'])] in target1 :
                objs={
                    'target': '1',
                    'class_id': obj['class_id'],
                    'name':  class_dict[int(obj['class_id'])],
                    'confidence': obj['confidence'],
                    'name': '',
                    'x': obj['x'],
                    'y': obj['y'],
                    'width': obj['width'],
                    'height': obj['height'] ,
                    'color':obj['color']
                }
                
                object1.append(objs)
            if  class_dict[int(obj['class_id'])] in target2:
                objs={
                    'target': '2',
                    'class_id': obj['class_id'],
                    'name':  class_dict[int(obj['class_id'])],
                    'confidence': obj['confidence'],
                    'name': '',
                    'x': obj['x'],
                    'y': obj['y'],
                    'width': obj['width'],
                    'height': obj['height'] ,
                    'color':obj['color']
                }
                
                object2.append(objs)
    return object1 ,object2,flag