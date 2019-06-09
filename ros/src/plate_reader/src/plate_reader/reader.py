import os
import sys
import time
import subprocess

#import rospy
import requests
import cv2
#from std_msgs import String
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

from keras_retinanet.models import load_model
from db import Db

db = Db()
default_model_path = 'models/resnet50_coco_best_v2.1.0.h5'
plate_model_path = 'models/resnet50_csv_08_inference.h5'
plotting = True

# car_model = load_model(default_model_path, backbone_name='resnet50')
plate_model = load_model(plate_model_path, backbone_name='resnet50')
image_base = ''

def read_plate(image_path):
    # Sync up data with Troggie
    
    # Run on most recent image
    
    # for image_path in os.listdir(image_base):

    image = np.array(Image.open(os.path.join(image_base, image_path)))
    
    # _,image = cap.read()
    # cv2.imwrite('plate.jpg', img)

    image_pil = Image.fromarray(image).convert('RGBA')
    inputs = np.expand_dims(np.array(image), axis=0)

    # car_boxes, car_scores, car_labels = car_model.predict_on_batch(inputs)
    plate_boxes, plate_scores, plate_labels = plate_model.predict_on_batch(inputs)

    # Grab the most confident box
    x1,y1,x2,y2 = plate_boxes[0][0]
    if x1 == -1 or x2 == -1 or y1 == -1 or y2 == -1:
        cv2.imshow('Demo', np.array(image_pil))
        cv2.moveWindow('Demo', 0, 0)
        cv2.waitKey(1)
        return
    plate_image_crop = Image.fromarray(image).crop((x1,y1,x2,y2))
    try:
        plate_image_crop.save('plate.jpg')
    except SystemError:
        return
    # for i, (car_x1, car_y1, car_x2, car_y2) in enumerate(car_boxes[0]):
    #     if car_x1 <= x1 and car_x2 >= x2 and car_y1 <= y1 and car_y2 >= y2 and car_labels[0][i] == 2:
    #         break
    
    with open('plate.jpg', 'rb') as f:
        response = requests.post(
            'https://platerecognizer.com/plate-reader/',
            files=dict(upload=f),
            headers={'Authorization': 'Token ' + 'FILL IN'})
    os.remove('plate.jpg')
    try:
        plate_seq = response.json()['results'][0]['plate']
    except IndexError:
        return
    #time.sleep(1)

    # Draw and save
    
    draw = ImageDraw.Draw(image_pil)
    draw.rectangle(((x1,y1),(x2,y2)), outline='red', width=5)
    # draw.rectangle(((car_x1,car_y1), (car_x2,car_y2)), outline='blue', width=5)

    textbox = Image.new('RGBA', (int(x2-x1), 30), 'red')
    boxdraw = ImageDraw.Draw(textbox)
    fnt = ImageFont.truetype('/Library/Fonts/Arial.ttf', int(30*(x2-x1)//150))
    boxdraw.text((0,0), plate_seq.upper(), font=fnt)

    # car_textbox = Image.new('RGBA', (int(x2-x1), 50), 'blue')
    # car_boxdraw = ImageDraw.Draw(car_textbox)
    # car_boxdraw.text((0,0), 'car', font=fnt)

    image_pil.paste(textbox, (int(x1),int(y1-30)))
    # if car_y1 - 50 <= 50:
    #     image_pil.paste(car_textbox, (int(car_x1),int(car_y1)))
    # else:
    #     image_pil.paste(car_textbox, (int(car_x1),int(car_y1-50)))
    image_pil = image_pil.convert('RGB')
    #cv2.destroyAllWindows()
    cv2.imshow('Demo', np.array(image_pil))
    cv2.moveWindow('Demo', 0, 0)
    cv2.waitKey(1)
    #image_pil.save('../demo-images-proc/{}'.format(name))
    #rospy.loginfo('Read plate: {}'.format(plate_seq))

    # Add to db
    plates = db.get_plates()
    for p in plates:
        if plate_seq in p.get('plate'):
            return
        p_set = set(plate_seq)
        db_set = set(p.get('plate'))
        hamming = len(p_set.difference(db_set))
        if hamming < 2:
            return
    db.add_plate(plate_seq)


def main():
    # rospy.init_node('reader')
    # rospy.Subscriber('/read_plate', String, read_plate)
    # rospy.spin()
    # Load initial screen
    # cv2.imshow('test', np.zeros((480,720,3)))
    # cv2.moveWindow('test', 0,0)
    # cv2.waitKey(0)
    subprocess.call(['rsync', '-r', 'nvidia@131.179.46.29:data', 'demo_data'])
    image_paths = sorted(os.listdir(image_base))
    for im in image_paths:
        if os.path.splitext(im)[1] == '.jpg':
            read_plate(im)
    # for i in os.listdir('../demo-images/'):
    #     if os.path.splitext(i)[1] == '.jpg':
    #         image = Image.open('../demo-images/{}'.format(i))
    #         read_plate(image, i, car_model, plate_model)
    # read_plate(Image.open('../test_im.jpg'), 'test_im.jpg')


if __name__ == '__main__':
    main()
