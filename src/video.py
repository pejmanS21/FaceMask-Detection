import warnings
warnings.simplefilter("ignore")

from random import random
import cv2
import torch
from typing import Union

from PIL import Image
from inc.utility.settings import setup
from inc.utility.func import draw_write_image, box_modifier
from deep_utils import Box


# text on image
fontFace = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 0.9
lineType = cv2.LINE_4


def video(path_to_video: Union[int, str] = 0):
    capture = cv2.VideoCapture(path_to_video)
    while True:
        isTrue, frame = capture.read()
        image = cv2.flip(frame, 1)

        result = setup['face_detector'].detect_faces(image, is_rgb=False)

        if result['boxes'] != []:
            image = Box.put_box(image, result.boxes, color=(255, 0, 0))
            boxes = box_modifier(image, result)

            image = draw_write_image(image, boxes)
        else:
            image = cv2.putText(image, "Can't detect any face!", (50, 50), fontFace, fontScale, (0, 255, 255), lineType)
        
        
        cv2.imshow('Video', image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    video(0)

