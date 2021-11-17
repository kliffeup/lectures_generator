"""
 # Copyright 2020 Adobe
 # All Rights Reserved.
 
 # NOTICE: Adobe permits you to use, modify, and distribute this file in
 # accordance with the terms of the Adobe license agreement accompanying
 # it.
 
"""

import sys
sys.path.append('thirdparty/AdaptiveWingLoss')
import os, glob
import numpy as np
import cv2
import argparse
from src.dataset.image_translation import landmark_extraction, landmark_image_to_data
from approaches.train_image_translation import Image_translation_block
import platform
import torch


if platform.release() == '4.4.0-83-generic':
    src_dir = r'/mnt/ntfs/Dataset/TalkingToon/VoxCeleb2_imagetranslation/raw_fl3d'
    mp4_dir = r'/mnt/ntfs/Dataset/VoxCeleb2/train_set/dev/mp4'
    jpg_dir = r'img_output'
    ckpt_dir = r'img_output'
    log_dir = r'img_output'
else: # 3.10.0-957.21.2.el7.x86_64
    # root = r'/mnt/nfs/scratch1/yangzhou/VoxCeleb2_imagetranslation'
    root = r'/mnt/nfs/scratch1/yangzhou/PreprocessedVox_imagetranslation'
    src_dir = os.path.join(root, 'raw_fl3d')
    # mp4_dir = r'/mnt/nfs/work1/kalo/yangzhou/VoxCeleb2/train_set/dev/mp4'
    mp4_dir = r'/mnt/nfs/scratch1/yangzhou/PreprocessedVox_mp4'
    jpg_dir = os.path.join(root, 'tmp_v')
    ckpt_dir = os.path.join(root, 'ckpt')
    log_dir = os.path.join(root, 'log')

''' Step 1. Data preparation '''
# landmark extraction
# landmark_extraction(int(sys.argv[1]), int(sys.argv[2]))

# save image data ahead -> saved file too large, will create data online
# landmark_image_to_data(0, 0, show=False)

''' Step 2. Train the network '''
parser = argparse.ArgumentParser()
parser.add_argument('--nepoch', type=int, default=150, help='number of epochs to train for')
parser.add_argument('--batch_size', type=int, default=8, help='batch size')
parser.add_argument('--num_frames', type=int, default=1, help='')
parser.add_argument('--num_workers', type=int, default=4, help='number of frames extracted from each video')
parser.add_argument('--lr', type=float, default=0.0001, help='')

parser.add_argument('--write', default=False, action='store_true')
parser.add_argument('--train', default=False, action='store_true')
parser.add_argument('--name', type=str, default='tmp')
parser.add_argument('--test_speed', default=False, action='store_true')

parser.add_argument('--jpg_dir', type=str, default=jpg_dir)
parser.add_argument('--ckpt_dir', type=str, default=ckpt_dir)
parser.add_argument('--log_dir', type=str, default=log_dir)

parser.add_argument('--jpg_freq', type=int, default=50, help='')
parser.add_argument('--ckpt_last_freq', type=int, default=1000, help='')
parser.add_argument('--ckpt_epoch_freq', type=int, default=1, help='')

parser.add_argument('--load_G_name', type=str, default='')
parser.add_argument('--use_vox_dataset', type=str, default='raw')


parser.add_argument('--add_audio_in', default=False, action='store_true')
parser.add_argument('--comb_fan_awing', default=False, action='store_true')
parser.add_argument('--fan_2or3D', type=str, default='3D')

parser.add_argument('--single_test', type=str, default='')

opt_parser = parser.parse_args()


model = Image_translation_block(opt_parser)

if(opt_parser.single_test != ''):
    with torch.no_grad():
        model.single_test()

if(opt_parser.train):
    model.train()
else:
    with torch.no_grad():
        model.test()