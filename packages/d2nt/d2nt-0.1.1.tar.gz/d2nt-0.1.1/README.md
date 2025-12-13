# D2NT: A High-Performing Depth-to-Normal Translator

This repo is the official implementation of the paper:
> ["D2NT: A High-Performing Depth-to-Normal Translator"](https://arxiv.org/abs/2304.12031)

> [[arXiv]](https://arxiv.org/abs/2304.12031)
> [[homepage]](https://mias.group/D2NT)
> [[video]](https://www.bilibili.com/video/BV1GX4y1m7jF/)


<p align="center">
  <img src="https://github.com/fengyi233/depth-to-normal-translator/raw/main/assets/compare.gif" width="500" alt="trade-off"/>
</p>

<p align="center">
  <img src="https://github.com/fengyi233/depth-to-normal-translator/raw/main/assets/tradeoff.png" width="500" alt="trade-off"/>
</p>


# Installation

## Install from PyPI (Recommended)

```bash
pip install d2nt
```

## Install from Source

```bash
# Clone the repository
git clone https://github.com/fengyi233/depth-to-normal-translator.git
cd depth-to-normal-translator

# Install in development mode
pip install -e .

# Or install normally
pip install .
```

## Prerequisites

+ Python >= 3.7
+ numpy >= 1.20.0
+ opencv-python >= 4.5.0
+ matplotlib >= 3.5.0 (optional, for visualization)

# Dataset Preparation

Public real-world datasets generally obtain surface normals by local plane fitting,
which makes the surface normal ground truth unreliable. Therefore, we use the synthesis **3F2N dataset** provided
in this [paper](https://ieeexplore.ieee.org/document/9381580) to evaluate estimation performance.

The 3F2N dataset can be downloaded from: \
[GoogleDrive](https://drive.google.com/drive/folders/1TLj033oV0aplLE6xcQaSRcZpggDVTCHY) \
The dataset is organized as follows:

```
3F2N
 |-- Easy
 |  |-- android
 |  |  |-- depth
 |  |  |-- normal
 |  |  |-- params.txt
 |  |  |-- pose.txt
 |  |-- cube
 |  |-- ...
 |  |-- torusknot
 |-- Medium
 |  |-- ...
 |-- Hard
 |  |-- ...
```

# Usage

## Python Package Usage

After installation, you can use the `depth2normal()` function directly:

```python
import numpy as np
from d2nt import depth2normal

# Prepare depth map (example)
depth = np.random.rand(480, 640) * 10.0

cam_intrinsic = np.array([
    [525.0, 0, 320.0],  # fx=525.0, u0=320.0
    [0, 525.0, 240.0],  # fy=525.0, v0=240.0
    [0, 0, 1]
])

# Convert depth to normal
normal = depth2normal(depth, cam_intrinsic, version='d2nt_v3')

print(f"Normal map shape: {normal.shape}")  # (480, 640, 3)
```

### Algorithm Versions

- **`d2nt_basic`**: Basic version without any optimization method
- **`d2nt_v2`**: With Discontinuity-Aware Gradient (DAG) filter
- **`d2nt_v3`**: With DAG filter and MRF-based Normal Refinement (MNR) module (recommended)

## Python Demo

Run the demo script in the root directory to see visualization results and error maps:

```bash
python demo.py
```

This will display:
- Ground truth normal map
- Estimated normal map
- Error map (in degrees) with mean angular error

The demo uses test data from `demo_data/` directory. 

You can change the `VERSION` parameter in `demo.py` to select different D2NT versions:
- **`d2nt_basic`**: Basic version without any optimization method
- **`d2nt_v2`**: With Discontinuity-Aware Gradient (DAG) filter
- **`d2nt_v3`**: With DAG filter and MRF-based Normal Refinement (MNR) module (recommended)




# Cite
If you find our work useful in your research, please consider citing our paper:

```
@inproceedings{feng2023d2nt,
	author      = {{Yi Feng, Bohuan Xue, Ming Liu, Qijun Chen, and Rui Fan}},
	title       = {{D2NT: A High-Performing Depth-to-Normal Translator}},
	booktitle   = {{IEEE International Conference on Robotics and Automation (ICRA)}},
	year        = {{2023}}
}
```