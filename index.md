# Overview

**BatCam** is an open-source, low-cost, do-it-yourself infrared video camera built with off-the-shelf components. It was designed for automated monitoring of bat activity and behavior at hibernation and roosting sites equipped with infrared light barriers. However, it can be easily adapted to a wide variety of field applications, with particular focus on nocturnal animals. Custom recording schedules can be set by the user and the direct connection to the infrared light barrier allows us to convert the continuous video recordings into short clips of each bat passing through the light barrier. Additionally, any other sensors with analog output can serve as a trigger signal for clipping the full-night video recordings. 

We provide a step-by-step instruction to build, configure and use the camera in the field, along with Python codes for video post-processing, making it accessible to anyone with minimal technical and programming skills. 

This practical guide is a supplementary information of the publication: **title.** _Journal_ (authors). https://doi.org/

![image](https://user-images.githubusercontent.com/79314212/123310825-cc6b7500-d526-11eb-8b0b-0c3d7772a325.png)


## Example
*video example

## Parts list
*in a table format: name of parts, number of unit, price per unit; video/LB/power/..

## Schematics
An overview of the camera design that is connected to an infrared light barrier:


The Printed Circuit Board (PCB) is illustrated in the following graphic:


## Building instructions
A step-by-step detailed guide with photos showing the main steps of the building process.

### Step 1.

### Step 2.
...

## Configuration


## Video processing
### Converting h264 video format into mp4
`import glob
from subprocess import call
from time import sleep

#set raw video (source) and output folder (target) paths
source_path = ''
target_path = ''

videos = glob.glob(source_path + "*.h264")
counter = 1

print(videos)

for video in videos:
	#base_name = video[37:66]
	base_name = video.split("/")[-1][0:-5]
	print(f"Converting {base_name} ({counter}/{len(videos)})")
	counter += 1
	source_name = source_path + base_name + ".h264"
	target_name = target_path + base_name + ".mp4"
	call(f"MP4Box -add '{source_name}' '{target_name}'",shell = True)
	#print(f"MP4Box -add {source_name} {target_name}")
	print("\t-> conversion complete!")
	sleep(1)
`


- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)```
