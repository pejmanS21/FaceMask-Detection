import warnings
warnings.simplefilter("ignore")

import cv2
from PIL import Image
from deep_utils import Box, get_logger
from inc.utility.settings import setup
from inc.utility.func import draw_write_image, box_modifier

logger = get_logger(name='image', log_path='../logs/runtime.log', )

imagePath = '../images/img.jpeg'
image = cv2.imread(imagePath)


result = setup['face_detector'].detect_faces(image, is_rgb=False)

if result['boxes'] == []:
    logger.error('0 Face Detected!')
else:
    image = Box.put_box(image, result.boxes, color=(255, 0, 0))

    boxes = box_modifier(image, result)
    logger.info(f'Number of detected faces={len(boxes)}')


    image = draw_write_image(image, boxes)
    Image.fromarray(image[...,::-1]).show() # convert to rgb and show image

