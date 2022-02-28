import warnings
warnings.simplefilter("ignore")

from fastapi import File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse
from PIL import Image
import numpy as np
import io
import cv2
from service import app
from service_warmup import init
from template import templates
from inc.data.data import img_to_base64, img_to_bytes
from deep_utils import Box
from inc.utility.settings import setup
from inc.utility.func import draw_write_image, box_modifier

import time

settings = init()


'''----- HAS_CORS=True -----'''
# allow_access_origin = *
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/process/{output_type}")
async def process(output_type: str, image: UploadFile = File(...)):
    
    """[summary]<br>
        output_type: (str) `bytes` or `1` for image to bytes convertion<br><br>
                            `base64` or `2` for base64 format image<br><br>
                            `saved` or `3` for html visualization.<br><br>
        image (UploadFile, optional): [description]. Defaults to File(...).<br><br>        
    """
    if settings['POST_TYPE'] == "FILE":
        uploaded_file = await image.read()
        flag = settings['POST_TYPE']
    # elif settings['POST_TYPE'] == "JSON":                 ## request
        # uploaded_file = base64_to_img(content)
        # flag = settings['POST_TYPE']
    
    image = Image.open(io.BytesIO(uploaded_file)).convert("RGB")
    image = np.asarray(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    result = setup['face_detector'].detect_faces(image, is_rgb=False)

    if not result['boxes']:
        # logger.error('0 Face Detected!')
        print('0 Face Detected!')
    else:
        image = Box.put_box(image, result.boxes, color=(255, 0, 0))
        boxes = box_modifier(image, result)
        image = draw_write_image(image, boxes)

    if output_type == "bytes" or output_type == "1":

        bytes_mask = img_to_bytes(image)
        return StreamingResponse(io.BytesIO(bytes_mask), media_type="image/png")

    elif output_type == "base64" or output_type == "2":

        image64 = img_to_base64(image)
        output_dict = {'result': image64}
        return output_dict 

    elif output_type == "saved" or output_type == "3":
            
        cv2.imwrite('./static/images/result.png', image)
        output_dict = {"message": "Image Saved Successfully!",
                       "image_url": "http://0.0.0.0:8000/imshow", 
                       "image_shape": str(image.shape)}
        return output_dict
    
    else:
        return {'message': "Check output_type endpoint", 
                'status': 404}


# @app.get("/", response_class=HTMLResponse)
# async def main_page(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})


@app.get("/imshow", response_class=HTMLResponse)
async def imshow(request: Request):
    return templates.TemplateResponse("imshow.html", {"request": request})
