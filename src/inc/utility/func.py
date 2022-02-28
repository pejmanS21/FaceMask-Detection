import torch
import cv2
from deep_utils import Box
from PIL import Image
from .settings import setup


stats = setup['stats']
transformer = setup['transformer']
model = setup['model']
classes = setup['classes']
device = setup['device']


def box_modifier(image, result):
    boxes = Box.box2box(result.boxes,
                    in_format='XYXY',
                    to_format=Box.BoxFormat.XYXY,
                    in_source="Numpy",
                    to_source=Box.BoxSource.CV,
                    in_relative=False,
                    to_relative=False,
                    shape=image.shape[:2],
                    shape_source='Numpy')
    return boxes


def denormal(pil_image, img_stats=stats):
    return pil_image * img_stats[1][0] + img_stats[0][0]


def pil_preparation(frame, transform=transformer):
    pil_frame = Image.fromarray(frame)
    pil_frame = transform(pil_frame)
    return pil_frame


def draw_write_image(image, boxes, img_size=(224, 224)):
    # text on image
    fontFace = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 0.9
    lineType = cv2.LINE_4

    for box in boxes:
        box = [int(point) for point in box]
        x0, y0, x1, y1 = box
        
        detected_face = image[y0:y1, x0:x1]
        detected_face = cv2.resize(detected_face, img_size)
        
        pil_image = cv2.cvtColor(detected_face, cv2.COLOR_BGR2RGB)
        pil_image = pil_preparation(pil_image)
        pil_image = pil_image.unsqueeze(0)
        pil_image = pil_image.to(device)
        
        output = model(pil_image)
        _, preds  = torch.max(output, dim=1)
        
        color = (0, 255, 0) if preds[0].item() == 1 else (0, 0, 255)
        
        image = cv2.putText(image, classes[preds[0].item()], (x0, y0), fontFace, fontScale, color, lineType)
    return image

