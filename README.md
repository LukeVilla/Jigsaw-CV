# Jigsaw-CV
An AI model for NVIDIA Jetson devices that tries to classify puzzle pieces by their number of sides.

# Explanation
Solving jigsaw puzzles is somewhat of an underutilized space in the machine-learning world, despite it being a good test of a broad range of AI capabilities, including vision (recognizing pieces), analysis (matching pieces together) and dexterity (physically assembling the puzzle). This project focuses on the first, specifically recognizing the difference between corner, edge and middle pieces. It mainly uses a synthetically-generated dataset, as I couldn't find an existing one that met my needs. The `gen_pieces.py` file uses Piecemaker to generate puzzles out of input images and place the pieces randomly on a background. Then, `split.py` splits those images into a dataset with `train`, `test` and `val` folders.

# Instructions

## Dependencies
- [Piecemaker](https://pypi.org/project/piecemaker/)
- [tqdm](https://pypi.org/project/tqdm/)
- [Pillow](https://pypi.org/project/pillow/)
- [split-folders](https://pypi.org/project/split-folders/)

1. Place the input images in the `images` folder. If you have any premade training images, split them into `corner`, `edge` and `mid` folders and pass the root directory in with the `-a` flag. These will be copied into the appropriate folders.
2. Run `gen_pieces.py`.
3. Run `split.py` to split the images into dataset folders.
4. Load the dataset into the standard jetson-inference classification workflow (`train.py`, `onnx_export.py` and then `imagenet`).

# Credits
The sample images in the `bg` and `images` folders were sourced from Unsplash.
