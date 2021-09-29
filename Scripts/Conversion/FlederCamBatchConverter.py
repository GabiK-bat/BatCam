# This script batch converts the raw .h264 videos, created by the Fledercam, to a more handlable MP4 format.
# Additional information can be found on GitHub: https://gabik-bat.github.io/FlederCam/

import glob
from subprocess import call
from time import sleep

source_path = "xxx" #set path of folder with raw videos(h264)
target_path = "xxx" #set path of folder to save converted videos(mp4)

videos = glob.glob(source_path + "*.h264")
counter = 1
print(videos)
for video in videos:
	base_name = video.split("/")[-1][0:-5]
	print(f"Converting {base_name} ({counter}/{len(videos)})")
	counter += 1
	source_name = source_path + base_name + ".h264"
	target_name = target_path + base_name + ".mp4"
	call(f"MP4Box -add '{source_name}' '{target_name}'",shell=True)
	print("\t-> conversion complete!")
	sleep(1)