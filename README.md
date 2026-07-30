# Jigsaw-CV
An AI model for NVIDIA Jetson devices that tries to classify puzzle pieces by their number of sides.

# Explanation
Solving jigsaw puzzles is somewhat of an underutilized space in the machine-learning world, despite it being a good test of a broad range of AI capabilities, including vision (recognizing pieces), analysis (matching pieces together) and dexterity (physically assembling the puzzle). This project focuses on the first, specifically recognizing the difference between corner, edge and middle pieces. It mainly uses a synthetically-generated dataset, as I couldn't find an existing one that met my needs. The `gen_pieces.py` file uses Piecemaker to generate puzzles out of input images and place the pieces randomly on a background. `outline_images.py` is an optional step that runs the Canny edge detection algorithm on all the images, hopefully making the edges more visible. Then, `split.py` splits those images into a dataset with `train`, `test` and `val` folders.

# Instructions

## Dependencies
- [Piecemaker](https://pypi.org/project/piecemaker/)
- [tqdm](https://pypi.org/project/tqdm/)
- [Pillow](https://pypi.org/project/pillow/)
- [split-folders](https://pypi.org/project/split-folders/)
- [OpenCV2](https://pypi.org/project/opencv-python/)
- [NumPy](https://pypi.org/project/numpy/)
> [!NOTE]
> OpenCV requires NumPy 2, while jetson-inference requires NumPy 1. You might need to use a virtual environment for this.

1. Place the input images in the `images` folder. If you have any premade training images, split them into `corner`, `edge` and `mid` folders and pass the root directory in with the `-a` flag. These will be copied into the appropriate folders.
2. Run `gen_pieces.py`.
3. Optionally, run `outline_images.py` on the output folder.
4. Run `split.py` to split the images into dataset folders.
5. Load the dataset into the standard jetson-inference classification workflow (`train.py`, `onnx_export.py` and then `imagenet`).

# Video
[![View on YouTube](https://github.com/user-attachments/assets/6faaaf85-4b3b-4df4-98a7-f56d57b83409)](https://youtu.be/QPpG9Ezy7SE)

# Results
The model seems to be overfitting; it always gives the same result no matter what images I give it, even when those images are from its own training data. The Canny algorithm did sometimes make correct outlines, but other times it got confused by other patterns in the piece or the background, making the actual shape of the piece unreadable. Either way, the validation accuracy was usually only around 35-50%. I might just need more training data, since I didn't have any actual puzzles on hand and had to generate my own. However, I think it's more likely that this kind of model is just not suited for this task; an ImageNet network is good at finding the piece, but a different algorithm might do a better job at actually tracing the piece's outline and finding edges.

# Credits
The sample images in the `bg` and `images` folders were sourced from Unsplash.
