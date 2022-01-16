import cv2
import numpy as np
import sys
import os
import yaml 

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from network import Net
import torch

#with covid [0,1] , normal [1,0]

with open("config.yaml",encoding='utf8') as f:
        config = yaml.safe_load(f)['Train']

img_resolution = config['image_resolution']

device = torch.device('cpu')
model = Net(config)
model.load_state_dict(torch.load(r"Models/0.911#watershed", map_location=device))

def testPhoto(path):

  imgg = cv2.imread(path,cv2.IMREAD_GRAYSCALE)

  img = cv2.resize(imgg,(img_resolution,img_resolution))
  img_array =  np.array(img)
  img_tensor = torch.Tensor(img_array)
  net_output = model(img_tensor.view(-1,1,img_resolution,img_resolution))
  return {
    "covid":round(np.exp(net_output[0][1].item()), 3) *100,
    "normal":round(np.exp(net_output[0][0].item()), 3) *100
  }

