#!/bin/python

import argparse
import splitfolders
from shutil import rmtree
import os

parser = argparse.ArgumentParser(
    prog="Puzzle Dataset Splitter",
    description="This script splits all the generated puzzle images into train, test and val folders."
)
parser.add_argument("-i","--input-dir",default="out",help="The input directory for images. Should be the output dir from gen_pieces.py.")
parser.add_argument("-o","--output-dir",default="dataset",help="The directory where the dataset is output to.")
args = parser.parse_args()
input_dir:str = args.input_dir
output_dir:str = args.output_dir

if os.path.exists(output_dir):
    rmtree(output_dir)

splitfolders.ratio(input_dir,output_dir)