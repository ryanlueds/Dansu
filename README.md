# ExoJoust
Map pose estimation from camera to 2D model in a game where you hit notes. Inspired by Osu!
Dragos dancing
![](https://github.com/ryanlueds/ExoJoust/blob/main/videos/dragosdancing.gif)
Ryan dancing
![](https://github.com/ryanlueds/ExoJoust/blob/main/videos/ryandancing.gif)

# MMPose Installation Guide 
## 1. Prerequisite guide from [MMPpose](https://mmpose.readthedocs.io/en/latest/installation.html):
* Step 0. Download and install Miniconda from the [official website](https://docs.anaconda.com/free/miniconda/). **Note: Add this to path with [these instructions](https://stackoverflow.com/questions/44515769/conda-is-not-recognized-as-internal-or-external-command)**
* Step 1. Create a conda environment and activate it (do all next steps in `Anaconda Prompt (miniconda3)` in your user directory).
```
conda create --name openmmlab python=3.8 -y
conda activate openmmlab
```
* Step 2. Install PyTorch following official instructions, e.g.
```
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
```
* Step 3. Install MMEngine and MMCV using MIM.
```
pip install -U openmim
mim install mmengine
mim install "mmcv>=2.0.1"
mim install "mmdet>=3.1.0"
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
* Step 2. Run the inference demo. Run the following command under the folder `ExoJoust/mmpose/`:
```
python demo/image_demo.py tests/data/coco/000000000785.jpg td-hm_hrnet-w48_8xb32-210e_coco-256x192.py td-hm_hrnet-w48_8xb32-210e_coco-256x192-0e67c616_20220913.pth --out-file vis_results.jpg --draw-heatmap
```

# ExoJoust Installation
## 1. Clone the repository
```
git clone https://github.com/ryanlueds/ExoJoust.git
```
## 2. Install dependencies
```
pip install -r requirements.txt
```

# Usage
## 1. Run the game
```
python game_driver.py
```
## 2. Errors
* Solution to "RuntimeError: nms_impl: implementation for device cuda:0 not found." is to upgrade mmcv to 2.2.0
