from datetime import datetime
from reshape_base_algos.body_retoucher import BodyRetoucher
import time
import cv2
import argparse
import numpy as np
import glob
import tqdm
import os
import json
import shutil
from run_test import run_test
from utils.eval_util import cal_lpips_and_ssim, psnr
from config.test_config import TESTCONFIG, load_config
import toml

class ROI:
    UPPER = 0  # 胳膊
    LOWER = 1  # 腿
    ALL = 2  # 全身

AVAILABLE_SCALES = ['upper_0.2','lower_0.2', 'upper_2']

class ReShaping:
    def __init__(self) -> None:
        # use current date time as the name of the folder
        current_date_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.src_dir_name = f'{current_date_time}_src'
        self.dst_dir_name = f'{current_date_time}_dst'

    def reshape_body(self, img_binary, degree=1.0 , roi = ROI.ALL):
        img_binary.save(os.path.join(self.src_dir_name, img_binary.filename))
        TESTCONFIG.degree = degree
        TESTCONFIG.flow_scales = [ AVAILABLE_SCALES[roi] if roi < len(AVAILABLE_SCALES) else AVAILABLE_SCALES[2]  ]

        run_test()

    def get_out_img_path(self):
        # literate the dst dir , find image name end with body_reshape_model
        for i in os.listdir(self.dst_dir_name):
            # get the image name
            image_name = i.split('.')[0]
            if image_name.endswith('body_reshape_model'):
                return os.path.join(self.dst_dir_name, i)
        return None

    def clear_up_dirs(self):
        for i in self.dst_dir_name, self.src_dir_name:
            if os.path.exists(i):
                shutil.rmtree(i)


