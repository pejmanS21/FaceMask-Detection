FROM tiangolo/uvicorn-gunicorn:python3.7

MAINTAINER pejmanS21

# os level reqs
RUN apt-get update -y \
     && apt install tesseract-ocr -y \
     && apt install libgl1-mesa-glx -y \
     && apt-get install 'ffmpeg' 'libsm6' 'libxext6' -y \
     && apt-get install -y build-essential libzbar-dev

RUN pip install install --upgrade pip

RUN pip install --no-cache-dir torch \ 
     && pip install --no-cache-dir numpy \
     && pip install --no-cache-dir opencv-python \
     && pip install --no-cache-dir torchvision \
     && pip install --no-cache-dir matplotlib \
     && pip install --no-cache-dir deep_utils


COPY . /app
WORKDIR /app/src

RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["uvicorn", "endpoints:app", "--host", "0.0.0.0", "--port", "8000"]
