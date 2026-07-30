import cv2
import argparse
import os
import sys
from tqdm import tqdm
from shutil import rmtree
import numpy as np

in_ = sys.argv[1]
out = sys.argv[2]
if os.path.exists(out):
    rmtree(out)
if not os.path.exists(out):
    os.makedirs(out)

for root,dirs,files in os.walk(in_):
    # print(dirs)
    # print(root)
    for file in tqdm(files):
    # Load image in grayscale
        img = cv2.imread(os.path.join(root,file), cv2.IMREAD_GRAYSCALE)
        
        # Apply Gaussian Blur to reduce noise
        blur = cv2.GaussianBlur(img, (5, 5), 1.4)
        
        # Apply Canny Edge Detector
        edges = cv2.Canny(blur, threshold1=100, threshold2=200)

        # Save
        cv2.imwrite(os.path.join(root,file),edges)
 
cv2.waitKey(0)
cv2.destroyAllWindows()