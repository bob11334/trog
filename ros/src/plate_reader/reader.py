import os
import sys
import time

import rospy
import requests
import cv2
from std_msgs import String
import numpy as np
#import matplotlib.pyplot as plt
#from matplotlib import patches
from PIL import Image

#from keras_retinanet.models import load_model
from db import Db

db = Db()
plate_model_path = '../models/resnet50_csv_08_inference.h5'
plotting = True


def read_plate(_):
    #model = load_model(plate_model_path, backbone_name='resnet50')
    #inputs = np.expand_dims(np.array(image), axis=0)

    #boxes, scores, labels = model.predict_on_batch(inputs)

    # Grab the most confident box
    #x1,y1,x2,y2 = boxes[0][0]
    #image_crop = Image.fromarray(image).crop((x1,y1,x2,y2))
    #image_crop.save('tmp.jpg')
    cap = cv2.VideoCapture(0)
    _,img = cap.read()
    cv2.imwrite('plate.jpg', img)
    time.sleep(1)
    with open('plate.jpg', 'rb') as f:
        response = requests.post(
            'https://platerecognizer.com/plate-reader/',
            files=dict(upload=f),
            headers={'Authorization': 'Token ' + '6aa8435106c4ce07b0d2608f1057f2fee9630f37'})
    os.remove('plate.jpg')
    plate_seq = response.json()['results'][0]['plate']
    rospy.loginfo('Read plate: {}'.format(plate_seq))

    # Add to db
    db.add_plate(plate_seq)


def main():
    rospy.init_node('reader')
    rospy.Subscriber('/read_plate', String, read_plate)
    rospy.spin()
    # image = np.array(Image.open(sys.argv[1]))


if __name__ == '__main__':
    main()
