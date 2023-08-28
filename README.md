# Smart Glasses for Blind People based on a tensor decomposition algorithm

## Description

This project focuses in making a ML model based on tensors to detect objects and its distances to the user of some smart glasses, implemented specifically for blind people. This repository includes the necessary CAD files for 3D printing the glasses frame and camera holder, and the necessary codes to run the algorithm. This project will help blind people to navigate with ease through certain indoor and outdoor scenarios and make the more secure  of going out. To receive the video uses a ZED mini camera, along with its API, and run in a Jetson Orin Nano computer.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Data](#data)
- [Usage](#usage)
- [Related links](#related_links)

## Requirements

This module requires the following modules:

- [PyZed](https://www.stereolabs.com/docs/)
- [Cv2](https://pypi.org/project/opencv-python/)
- [Tensorly](https://tensorly.org/stable/installation.html)
- [TLTorch](https://github.com/tensorly/torch)

## Installation

In order to use some of the codes of this repository (specifically to record or save the images), you will need to have access preferably to a Linux computer (but can be a Windows computer also), where you can download the [ZED SDK](https://www.stereolabs.com/developers/release/) and the [PyZed API](https://www.stereolabs.com/docs/app-development/python/install/) to have access to all functions in the camera. If you have access to a Jetson computer, make sure to download the specific SDK since you can have access to CUDA functions.

## Data

In order to access the data recorded from the Zed camera that was used in the experiment, you will need to have an University of Essex One Drive Account in order to download the next folder: [Data recordings](https://essexuniversity-my.sharepoint.com/:f:/g/personal/cr22144_essex_ac_uk/EpRaFdlUKGRIrvHqJGyQUgsBLk6QWljwuT4jpetEnfBcjA?e=h57Bli)

## Usage

To run the main code (`Codes/CameraRECTest.py`) you will need to run it from the terminal while having connected the ZED camera. Then, follow the instructions on the terminal in order to record or save a video or images.
An example to record is running this in terminal: 

    D:\22-23_CE901-CE902-SU_romano_gomez_carlos\Codes> python3 CameraRECTest.py
    Enter the name of the SVO file: FILE_NAME
    Do you want to use the default path (/home/nvidia/Downloads/test/) [y/n]?: n
    Enter the path to the SVO file: /path/to/folder/
    Do you want to record or store [r/s]?: r

And then the recording will start. It is important that when not using the default path, finish the path with an / to make sure it creates a folder if it does not exist.

## Related_Links

Some useful tutorials that relates to this project are the following:
- [Jetson Orin Nano Starter Guide](https://developer.nvidia.com/embedded/learn/get-started-jetson-orin-nano-devkit#intro)
- [Zed SDK Installation](https://www.stereolabs.com/developers/release/)
- [Zed tutorials](https://github.com/stereolabs/zed-sdk/tree/master/tutorials)
- [Tensorly examples](https://tensorly.org/stable/auto_examples/index.html)
