from fastapi import FastAPI
from service_warmup import init

settings = init()

app = FastAPI(
    title=settings['APP_NAME'],
    description="""A face mask detection app with Pytorch, Upload your image to detect face(s) within the image
    and findout who wear a mask! """,
    version="0.1.0",
    Author="pejmanS21")
