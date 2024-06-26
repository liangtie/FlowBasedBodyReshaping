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
OUT_DIR = "out"

class ReShaping:
    def __init__(self) -> None:
        # remove all content in OUT_DIR
        if os.path.exists(OUT_DIR):
            shutil.rmtree(OUT_DIR)

        # mkdir the OUT_DIR
        os.mkdir(OUT_DIR)

        # use current date time as the name of the folder
        current_date_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.src_dir_name =  os.path.join(OUT_DIR, f'{current_date_time}_src')
        self.dst_dir_name =  os.path.join(OUT_DIR,f'{current_date_time}_dst')
        # convert the relative path to absolute path
        self.src_dir_name = os.path.abspath(self.src_dir_name)
        self.dst_dir_name = os.path.abspath(self.dst_dir_name)

        for i in self.src_dir_name, self.dst_dir_name:
            if not os.path.exists(i):
                os.mkdir(i)

    def reshape_body(self, img_binary, degree=1.0 , roi = ROI.ALL):
        img_binary.save(os.path.join(self.src_dir_name, img_binary.filename))
        TESTCONFIG.degree = degree
        TESTCONFIG.src_dir = self.src_dir_name
        TESTCONFIG.save_dir = self.dst_dir_name
        TESTCONFIG.flow_scales = [ AVAILABLE_SCALES[roi] if roi < len(AVAILABLE_SCALES) else AVAILABLE_SCALES[2]  ]
        output_path = os.path.join(self.dst_dir_name, 'test_demo_setting.toml')
        with open(output_path, 'w') as f:
            toml.dump(TESTCONFIG, f)

        run_test()

    def get_out_img_path(self):
        # literate the dst dir , find image name end with body_reshape_model
        for i in os.listdir(self.dst_dir_name):
            # get the image name
            image_name = i.split('.')[0]
            if image_name.endswith('body_reshape_model'):
                return os.path.join(self.dst_dir_name, i)
        return None
    def __del__(self):
        self.clear_up_dirs()
    def clear_up_dirs(self):
        for i in self.dst_dir_name, self.src_dir_name:
            if os.path.exists(i):
                shutil.rmtree(i)


