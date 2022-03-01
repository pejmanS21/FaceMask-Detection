# FaceMask-Detection
<br>

## Usage 

in [src](./src/)<br>
for test on images run [image.py](./src/image.py)

    python3 image.py

or 
for test on videos run [video.py](./src/video.py)

    python3 video.py

or 

### `FastAPI`

for start webapp run [entrypoint.py](./src/entrypoint.py)

    python3 entrypoint.py

#### UI

![ui](./images/ui.gif)

<br>

## model

    dvc pull
don't forget to install [dvc](https://dvc.org/)

    pip install dvc

or use gdown and download from Google Drive 

    cd models
    chmod +x get_weights.sh
    ./get_weights.sh 

<br>

## Google Colab


[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1NU6HMEgHJfR_PttrfJJV8Gq8bPe7lwc_?usp=sharing)

<br>


## docker-compose

    sudo docker-compose up --build -d

