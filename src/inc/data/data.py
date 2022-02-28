import cv2
import os
import numpy as np
from PIL import Image
import io
import base64


def img_to_bytes(img):
    """[summary]
    change numpy image to bytes image for visualization

    Args:
        img ([cv2 format]): [predicted mask]

    Returns:
        [bytes]
    """
    ceofficient = 1

    _, encoded_img = cv2.imencode(".png", img * ceofficient)
    bytes_img = encoded_img.tobytes()
    return bytes_img


def img_to_base64(img):
    """
    :param image: image to convert
    :return: b64 image
    """

    ceofficient = 1

    # img is a numpy array / opencv image
    _, encoded_img = cv2.imencode('.png', img * ceofficient)
    base64_img = base64.b64encode(encoded_img).decode('utf-8')
    return base64_img


def base64_to_img(img_string):
    """
    :param image_string: base64 image string
    :return: numpy image
    """
    img_data = base64.b64decode(img_string)
    image = Image.open(io.BytesIO(img_data))
    return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)



