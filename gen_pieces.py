#!/bin/python

import random
import json
import os
import sys
import argparse
import subprocess
from shutil import rmtree,copy
from PIL import Image, ImageOps
from PIL.Image import Transpose
from image_utils import outline
from tqdm import tqdm,trange

# Constants
PIECEMAKER_PATH = "~/.local/bin/piecemaker"
def copy_all(src_dir:str,dst_dir:str):
    if os.path.exists(src_dir):
        for file in os.listdir(src_dir):
            copy(os.path.join(src_dir,file),dst_dir)

parser = argparse.ArgumentParser(
    prog="Puzzle Training Data Generator",
    description="This program generates random images of puzzle pieces to be used as training data."
)
parser.add_argument("-i","--image-dir",default="images",help="Where the input images are stored")
parser.add_argument("-p","--puzzles-dir",default="puzzles",help="Where the generated puzzles are stored")
parser.add_argument("-o","--out-dir",default="out",help="Where the output images are stored")
parser.add_argument("-n","--num-pieces",default=12,help="How many pieces to generate for each puzzle")
parser.add_argument("-a","--add-dir",action="append",default=None,help="Additional dir to copy images from")
parser.add_argument("-g","--generate",default=20,help="The number of images to generate per category per image")
parser.add_argument("-b","--bg-dir",default="bg",help="Where the backgrounds are stored")
parser.add_argument("--no-outline",action="store_true",help="Skip generating outlines for pieces")
args = parser.parse_args()
image_dir = args.image_dir
puzzles_dir = args.puzzles_dir
out_dir = args.out_dir
num_pieces = args.num_pieces
additional_dirs = args.add_dir
generate = args.generate
bg_dir = args.bg_dir
if args.no_outline:
    outline = lambda x: x

if os.path.exists(puzzles_dir):
    rmtree(puzzles_dir)
if os.path.exists(out_dir):
    rmtree(out_dir)
if not os.path.exists(puzzles_dir):
    os.makedirs(puzzles_dir)
if not os.path.exists(out_dir):
    os.makedirs(out_dir)
    os.mkdir(os.path.join(out_dir,"corner"))
    os.mkdir(os.path.join(out_dir,"edge"))
    os.mkdir(os.path.join(out_dir,"mid"))

images = os.listdir(image_dir)
for image in tqdm(images):
    image_out_dir = os.path.join(puzzles_dir,os.path.splitext(image)[0])
    os.mkdir(image_out_dir)
    print("")
    subprocess.run(["piecemaker","--dir",image_out_dir,"-n",str(num_pieces),os.path.join(image_dir,image)])

labels = {}
idx = 0
scale_min = 200
scale_max = 250

def gen(index_p1:str,scale:float,set:str):
    global idx
    with Image.open(os.path.join(pieces_dir,index_p1+".png")) as p1,Image.open(os.path.join(bg_dir,random.choice(os.listdir(bg_dir)))) as bg:
        p1 = p1.resize((int(p1.width*scale), int(p1.height*scale)))
        p1 = p1.rotate(random.randrange(360),expand=True)
        outline1 = outline(p1)
        bg = bg.convert("RGBA")
        bg.alpha_composite(outline1,(random.randrange(int(bg.width//2)),random.randrange(int(bg.height//2))))
        bg = bg.convert("RGB")
        bg.save(os.path.join(out_dir,set,str(idx)+".jpg"))
        labels[idx] = set
        idx += 1

for puzzle_name in tqdm(os.listdir(puzzles_dir)):
    puzzle_dir = os.path.join(puzzles_dir,puzzle_name)
    pieces_dir = os.path.join(puzzle_dir,list(filter(lambda x: x.startswith("size-"),os.listdir(puzzle_dir)))[0],"raster","image-0")
    adj:dict[str,list[str]] = json.load(open(os.path.join(puzzle_dir,"adjacent.json")))
    num_pieces = len(adj)
    
    print(f"Generating 'corner' images from puzzle {puzzle_name}")
    for i in range(generate):
        index_p1 = random.choice(list(filter(lambda x: len(adj[x])==2,adj.keys())))
        scale = random.randint(scale_min,scale_max)/100
        gen(index_p1,scale,"corner")
    
    print(f"Generating 'edge' images from puzzle {puzzle_name}")
    for i in range(generate):
        index_p1 = random.choice(list(filter(lambda x: len(adj[x])==3,adj.keys())))
        scale = random.randint(scale_min,scale_max)/100
        gen(index_p1,scale,"edge")

    print(f"Generating 'mid' images from puzzle {puzzle_name}")
    for i in range(generate):
        index_p1 = random.choice(list(filter(lambda x: len(adj[x])==4,adj.keys())))
        scale = random.randint(scale_min,scale_max)/100
        gen(index_p1,scale,"mid")

if additional_dirs:
    print("Copying additional images")
    for dir in tqdm(additional_dirs):
        copy_all(os.path.join(dir,"corner"),os.path.join(out_dir,"corner"))
        copy_all(os.path.join(dir,"edge"),os.path.join(out_dir,"edge"))
        copy_all(os.path.join(dir,"mid"),os.path.join(out_dir,"mid"))
