import cv2
from HRI.utils.utils_detect import process_detect_result

image_path='D:/myProject/HRI/temp/draw.jpg'
def draw_picture_result(matched_results):
    '''
    matched_results：
        {'target': '2'
        'class_id': class_id,
        'name':  class_dict[int(obj['class_id'])],
        'confidence': confidence,
        'name': '',
        'x': xmin,
        'y': ymin,
        'width': w,
        'height': h ,
        'color':corlor
        }
    '''

    image = cv2.imread(image_path)

    print('draw_picture的matched_results是:========='+str(matched_results))
    for obj in matched_results:
        x = int(obj['x'])
        y = int(obj['y'])
        w = int(obj['width'])
        h = int(obj['height'])
        confidence = obj['confidence']
        name=obj['name']
        target = obj['target']

        x2 = x + w
        y2 = y + h

        color = (0, 255, 0) if target == '1' else (255, 0, 0)
        label = f"Target {target} {confidence:.2f}"

        cv2.rectangle(image, (x, y), (x2, y2), color, 2)
        cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    cv2.destroyAllWindows()

    window_name = f"Detection Result - {image_path.split('/')[-1]}"
    cv2.imshow(window_name, image)

    cv2.waitKey(0) 
    cv2.destroyAllWindows()  

if __name__ == "__main__":
    results=process_detect_result()
    draw_picture_result(results)

    cv2.waitKey(0)  
    cv2.destroyAllWindows()  