import sys
import argparse
import cv2
import ast 
import pandas as pd
import numpy as np

import tools.utils as pt
import tools.cli as cli
from collections import defaultdict
from models.CochlSense.load import cochlSense
from tools.utils import extract_audio
from tools.utils import transform
from tools.cli import cli
from models.whispers.load import whisper_result
from tools.transcript import generate_subtitles

from PIL import Image, ImageDraw, ImageFont


def visualizer(smi_data, args):
    cap = cv2.VideoCapture(args.input_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') if args.input_type == 'mp4' else \
            cv2.VideoWriter_fourcc(*'dvix') if args.input_type == 'avi' else \
            cv2.VideoWriter_fourcc(*'hevc')
    out = cv2.VideoWriter(args.output_path, fourcc, fps, (int(cap.get(3)), int(cap.get(4))))

    for _, frame_text in smi_data:
        ret, frame = cap.read()
        if not ret:
            break

        # 여기에 frame에 자막을 그리는 로직을 추가할 수 있습니다.
        # 예: cv2.putText()를 사용하여 frame에 frame_text를 출력
        
        out.write(frame)

    out.release()
    cv2.destroyAllWindows()


