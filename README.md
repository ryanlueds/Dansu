# ExoJoust
Map pose estimation from camera to 2D model in a game

# Installation Guide
## 0. Please use Windows. 
## 1. Prerequisite guide from [MMPpose](https://mmpose.readthedocs.io/en/latest/installation.html):
* Step 0. Download and install Miniconda from the [official website](http://example.com "Title").
* Step 1. Create a conda environment and activate it (do all next steps in Anaconda Prompt in your user directory).
```
conda create --name openmmlab python=3.8 -y
conda activate openmmlab
```
* Step 2. Install PyTorch following official instructions, e.g.
```
conda install pytorch torchvision pytorch-cuda=12.1 -c pytorch -c nvidia
```
* Step 3. Install MMEngine and MMCV using MIM.
```
pip install -U openmim
mim install mmengine
mim install "mmcv>=2.0.1"
mim install "mmdet>=3.1.0"
```
* Verify that versions match in case that matters
```
python --version
# Python 3.8.19
```
```
pip show torch
# Name: torch
# Version: 1.13.1
# Summary: Tensors and Dynamic neural networks in Python with strong GPU acceleration
# Home-page: https://pytorch.org/
# Author: PyTorch Team
# Author-email: packages@pytorch.org
# License: BSD-3
# Location: c:\users\secret:D\anaconda3\envs\openmmlab\lib\site-packages
# Requires: typing_extensions
# Required-by: torchvision
```
```
conda --version
# conda 4.11.0
```

## 2. Build MMPose from source
* Create a directory `ExoJoust/` in your user directory. Do all next steps in `ExoJoust/` directory.
* Install mmpose from source
```
git clone https://github.com/open-mmlab/mmpose.git
cd mmpose
pip install -r requirements.txt
pip install -v -e .
# "-v" means verbose, or more output
# "-e" means installing a project in editable mode,
# thus any local modifications made to the code will take effect without reinstallation.
```
## 3. Verify installation
* Step 1. We need to download config and checkpoint files.
```
mim download mmpose --config td-hm_hrnet-w48_8xb32-210e_coco-256x192  --dest .
```
* Step 2. Run the inference demo. Run the following command under the folder $MMPOSE:
```
python demo/image_demo.py tests/data/coco/000000000785.jpg td-hm_hrnet-w48_8xb32-210e_coco-256x192.py td-hm_hrnet-w48_8xb32-210e_coco-256x192-0e67c616_20220913.pth --out-file vis_results.jpg --draw-heatmap
```
