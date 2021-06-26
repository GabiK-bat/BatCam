---
driveId: 1eOBq-KuYQPmx111H_NuEgR9xyAI0cyde/preview
---

# Overview

**BatCam** is an open-source, low-cost, do-it-yourself infrared video camera built with off-the-shelf components. It was designed for automated monitoring of bat activity and behavior at hibernation and roosting sites equipped with infrared light barriers and camera traps. However, it can be easily adapted to a wide variety of field applications, with particular focus on nocturnal animals. Custom recording schedules can be set by the user and the direct connection to the infrared light barrier allows us to convert the continuous video recordings into short clips of each bat passing through the light barrier. Additionally, any other sensors with analog output can serve as a trigger signal for clipping the full-night video recordings. 

We provide a step-by-step instruction to build, configure and use the camera in the field, along with Python codes for video post-processing, making it accessible to anyone with minimal technical and programming skills. 

This practical guide is a supplementary information of the publication: **title.** _Journal_ (authors). https://doi.org/

![image](https://user-images.githubusercontent.com/79314212/123325849-cf6f6100-d538-11eb-9b66-f23d91d5e3c4.png)

## Example
The following video of a Greater mouse-eared bat (_Myotis myotis_) entering a hibernaculum was recorded using the BatCam. The short video snip was isolated from a full-night infrared video recording based on the information the light barrier registered and forwarded to the video camera.

{% include googleDrivePlayer.html id=page.driveId %}

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

![image](https://user-images.githubusercontent.com/79314212/123310825-cc6b7500-d526-11eb-8b0b-0c3d7772a325.png)


## Configuration

### Scheduled video recording
This operation mode allows configuring the start and end of recording time. To do so, we have set the time period when we DO NOT want to record, using the "day" variable (e.g. day = ("07:00:00","19:00:00") means no recording from 7AM to 7PM).

```python
###################### Import Libraries #######################
import sys
from datetime import datetime
from picamera import PiCamera
import time
import RPi.GPIO as GPIO

###################### Define functions #######################
#returns seconds passed since midnight
def sinceMidnight():
	timeNow = datetime.now()
	timeZero = timeNow.replace(hour=0,minute=0,second=0,microsecond=0)
	return (timeNow-timeZero).seconds

#converts time (formatted in hh:mm:ss) into seconds
def toSeconds(time):
	timeS = time.split(":")
	secs = int(timeS[0]) * 3600 + int(timeS[1]) * 60 + int(timeS[2])
	return secs

#initializes GPIO and sets passed pins as output
def setGPIO(pinsOut):
	GPIO.setmode(GPIO.BOARD) #use numbering of pins as reference
	GPIO.setwarnings(False) #disable warnings 
	GPIO.setup(pinsOut,GPIO.OUT)

###################### Set Variables ######################
#define pins for GPIO and initialize
pinsOut = (16,32,37)
#16 5W-IR-LED
#32 Button 1
#37 LED green
setGPIO(pinsOut)

# set time for start and end of daytime (it will be NOT RECORDING during that time)
day = ("07:00:00","19:00:00")
daySec = (toSeconds(day[0]),toSeconds(day[1]))

GPIO.output(37,GPIO.HIGH) #turns green LED shortly on when script starts
time.sleep(3)
GPIO.output(37,GPIO.LOW)

GPIO.output((16),GPIO.HIGH) #turns IR light shortly on when script starts
time.sleep(3)
GPIO.output((16),GPIO.LOW)

camera = PiCamera()
camera.resolution = (800, 600)
camera.framerate  = 25
camera.hflip = True
camera.vflip = True
camera.brightness = 60
indicator = False
isRecording = False
firstRun = True

###################### Main Loop ######################
while True:
	secs = sinceMidnight()
	now = datetime.now()
	#show current time when button1 is pressed
	if GPIO.input(32) == GPIO.HIGH:
		indicator = True
		GPIO.output(37,GPIO.HIGH)
		
	if indicator and GPIO.input(32) == GPIO.LOW:
		indicator = False	
		GPIO.output(37,GPIO.LOW)

	#check if it is night
	if(secs < daySec[0] or secs >= daySec[1]):
		#switches IR-LEDs on
		GPIO.output((16),GPIO.HIGH)
		#starts new recording every 15 minutes
		if not firstRun:
			currTime = datetime.now()
		if firstRun or (currTime-nowVideo).total_seconds() > 900:
			if not firstRun and isRecording:
				print("Stopping video recording")
				camera.stop_recording()
			nowVideo = datetime.now()
			GPIO.output((16),GPIO.HIGH)
			print(f"Start video recording {nowVideo}")
			camera.start_recording("BatCam_"+
			nowVideo.strftime("%Y_%m_%d_%H_%M_%S")+".h264")
			isRecording = True
			firstRun = False
	else:
		#switches IR-LEDs off
		GPIO.output((16),GPIO.LOW)
		if isRecording:
			print("Stopping video recording (morning)")
			camera.stop_recording()
			isRecording = False
```

## Video processing

### Converting h264 video format into mp4
The Raspberry Pi can easily record videos with different resolution and frame rate, but it saves recordings as .h264 files, which generally hard to view and work with. Using the following Python code, videos recorded with the BatCam can be converted into a widely applicable .mp4 format.

```python
import glob
from subprocess import call
from time import sleep

source_path = "xxx" #set path of folder with raw video files (h264)
target_path = "xxx" #set path of folder to save converted video files (mp4)

videos = glob.glob(source_path + "*.h264")
counter = 1
print(videos)
for video in videos:
	base_name = video.split("/")[-1][0:-5]
	print(f"Converting {base_name} ({counter}/{len(videos)})")
	counter += 1
	source_name = source_path + base_name + ".h264"
	target_name = target_path + base_name + ".mp4"
	call(f"MP4Box -add '{source_name}' '{target_name}'",shell = True)
	print("\t-> conversion complete!")
	sleep(1)
```

### Creating 6-second-long video snips based on light barrier registrations
The following Python code allows post-processing the full-night video recordings, creating short video snips for each bat pass registered by the infared light barrier. The length of the video snips can be set by the user (default=3 seconds before and after registered event) and the file names contain the date and time of the event and the direction of the bat pass (in or out).

```python
import numpy as np
import pandas as pd
import glob
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

det_path = "xxx" #set path of "Detections.txt" file containing the light barrier registrations
vid_path = "xxx" #set path of folder with converted video files
snip_path = "xxx" #setpath of folder to save snips

# load light barrier registrations
det = pd.read_table(det_path,sep=":| ",engine="python",header=None,names=["direction","date","hour",
"min","sec"])
det["sec_mid"] = [row[2] * 3600 + row[3] * 60 + row[4] for index, row in det.iterrows()]
print("Detections loaded!")

# load converted video data	
vid = pd.DataFrame({"path":[],"file":[],"date":[],"hour":[],"min":[],"sec":[],"sec_mid":[]})
videos = glob.glob(vid_path + "*.mp4")
for video in videos:
	file_name = video.split("/")[-1][0:-4]
	print(file_name)
	date = file_name[7:17].split("_")
	date_re = str(date[2] + "." + date[1] + "." + date[0])
	time = file_name[18:26].split("_")
	sec_mid = int(time[0]) * 3600 + int(time[1]) * 60 + int(time[2])
	vid = vid.append({"path":video,"file":file_name,"date":date_re,"hour":time[0],
	"min":time[1],"sec":time[2],"sec_mid":sec_mid},ignore_index=True)
vid["sec_mid"] = vid["sec_mid"].astype(int)
print("Video information loaded!")
fails = 0

# loop over light barrier detections and find matching (15 minute long) video file 
print("Matching detections with video files")
for index, row in det.iterrows():
	fail = False
	print(f"  -> searching for detection at {row['hour']}:{row['min']}:{row['sec']} 
	on the {row['date']}")
	target_vid = vid[(vid["date"] == row["date"]) & (vid["sec_mid"] <= row["sec_mid"]) 
	& (vid["sec_mid"] >= row["sec_mid"]-15*60)]
	print(f"     -> video found: {target_vid['file'].to_string().split()[1]}")
	print("          -> extracting video snip...")
	print(target_vid["sec_mid"].values)
	vid_secmid = (target_vid["sec_mid"].values).tolist()
	target_file = (target_vid["file"].values).tolist()
	print(target_file)
	try:	
		print(vid_secmid[0])
		#3 second before light barrier registration = start of snip
		t1 = row["sec_mid"] - vid_secmid[0] - 3 
		#3 second after light barrier registration = end of snip
		t2 = row["sec_mid"] - vid_secmid[0] + 3 
		print(f"{t1} - {t2}")
		print(target_file[0] + ".mp4")
		target_file = target_file[0] + ".mp4"
	except:
		print("Empty Array")
	snip_date = "_".join(reversed(row["date"].split(".")))
	snip_name = "snip_"+snip_date+"_"+str(row["hour"]).zfill(2)+"_"+str(row["min"]).zfill(2)
	+"_"+str(row["sec"]).zfill(2)+"_"+row["direction"]+".mp4"
	
	#extract 6-second-long snip from video file
	try:		
		ffmpeg_extract_subclip(vid_path+target_file,int(t1),int(t2),snip_path+snip_name)
	# most common cause of failure are detections outside of recording time 
	# no video for extraction
	except:
		fail = True	
		fails += 1
	
	if fail:
		print("          -> extraction FAILED!")
	else:
		print("          -> extraction complete!")
	
print(f"Conversion completed ({fails} detections could not be found)")
```
