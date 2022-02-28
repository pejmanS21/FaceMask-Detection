import torch
import torchvision.transforms as T
from deep_utils import face_detector_loader
from .model import FaceMask_Detection


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

size = 224
stats = (0.5,), (0.5,)

model_path = '../models/face_mask_detection_checkpoint.pth'

model = FaceMask_Detection(3, 32, 2)
model.eval()
model.load_state_dict(torch.load(model_path, map_location=device))

face_detector = face_detector_loader('MTCNNTorchFaceDetector')

classes = {0: 'without_mask', 1: 'with_mask'}

transformer = T.Compose([
    T.Resize(size),
    T.CenterCrop(size),
    T.ToTensor(),
    T.Normalize(*stats)])

setup = {
    'model': model,
    'face_detector': face_detector,
    'classes': classes,
    'transformer': transformer,
    'stats': stats,
    'device': device,

}