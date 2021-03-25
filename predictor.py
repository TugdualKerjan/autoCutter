import torch
import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()

# import some common libraries
import numpy as np
import os, json, cv2, random

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog
# from vovnet import add_vovnet_config
# model = "vovnet-detectron2/configs/mask_rcnn_V_19_FPNLite_3x.yaml"
# model = "https://dl.dropbox.com/s/rptgw6stppbiw1u/vovnet19_ese_detectron2.pth"
model = "COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"


cfg = get_cfg()
# add_vovnet_config(cfg)
# cfg.merge_from_file(model)
cfg.merge_from_file(model_zoo.get_config_file(model))

cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set threshold for this model
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(model)
cfg.MODEL.DEVICE = "cpu"

predictor = DefaultPredictor(cfg)

def imsize(box):
  return (box[3]-box[1])*(box[2]-box[0])

def predict(image):
  height, width, _ = image.shape
  image_size = height * width * 0.1

  alphaimage = cv2.cvtColor(image, cv2.COLOR_RGB2RGBA)

  outputs = predictor(image)

  masks = outputs["instances"].pred_masks.cpu().numpy()
  boxes = outputs["instances"].pred_boxes.tensor.cpu().numpy()

  for x in range(0,len(outputs["instances"].pred_masks)):
    boxtemp = boxes[x].astype(int)
    masktemp = masks[x]

    if imsize(boxtemp) > image_size:
      yield alphaimage[boxtemp[1]:boxtemp[3],boxtemp[0]:boxtemp[2]] * masktemp[boxtemp[1]:boxtemp[3],boxtemp[0]:boxtemp[2], None]