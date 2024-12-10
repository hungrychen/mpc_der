# mpc_der

## Overview
This software allows for the collection of the position of colored nodes along a structure with a video camera,
and for the visualization of the positions.
In the future, we hope to allow for the real time control of the structures position.

## Requirements
Note: We developed on Ubuntu Linux.
- Python 3.11
- Pipenv

You can install Pipenv with:
```shell
pip3 install Pipenv --user
```

## Getting Started
1. Once Pipenv is installed, run the setup script first. You only need to do this once.
```shell
./scripts/setup
```

2. Before running anything, ensure your current directory is the root of the repository. Run all programs and scripts from the repository root.
1. Before running anything, ensure the environment is activated. You might need to configure your IDE, or activate by running:
```shell
pipenv shell
```

3. We also set a lower than default USB latency by following the instructions for Linux at https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_wizard2/#usb-latency-setting.

## Setting the Configuration
The parameters can be configured by modifying `./config/config_collect_data.json`.  
Most importantly:
1. Set "calibration_distance" to the distance between the two reference nodes, in meters.
1. Set "node_offset_distance" to the assumed distance between the top node and the position of the origin, in meters.

## Checking the Camera
You can check that the camera is functioning properly by running:
```shell
python ./src/collect_video_data.py
```
This will show you how the nodes are detecting without saving any data files. You can click on the video and press "q" to exit.

## Collecting Data
To collect data, run:
```shell
python ./src/collect_video_data_2.py
```
This will read configuration information from `./config/config_collect_data.json`.  
The prompts will guide you with the calibration. Once data collection starts, you can click on the video and press "q" to exit if necessary.

Output files will appear in `./output/collect_video_data/`. You can clear the output data with:
```shell
./scripts/clean
```

## Visualizing Data
To visualize the output data, run:
```shell
python ./src/view_data.py [.npy data file]
```

For example:
```shell
python ./src/view_data.py ./output/collect_video_data/1732139076_data.npy
```

The figure will appear in `./output/view_data/`.
