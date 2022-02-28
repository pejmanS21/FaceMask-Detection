from pydantic import BaseSettings
import os
from dotenv import load_dotenv

# load .env
load_dotenv()


APP_NAME = os.getenv('APP_NAME', 'facemask-detection')

POST_TYPE = os.getenv('POST_TYPE', 'FILE')
SAVE_PATH = os.getenv('SAVE_PATH', '../images/upload.png')

def init():
    settings = {
                'APP_NAME': APP_NAME,
                'POST_TYPE': POST_TYPE,
                'SAVE_PATH': SAVE_PATH,
                }
    
    return settings
