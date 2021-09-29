# This is the main script of the FlederCam creating a continuous recording, broken into 15 minute chunks, during night.   
# Additional information can be found on GitHub: https://gabik-bat.github.io/FlederCam/

###################### Import Libraries #######################
import sys
from datetime import datetime
from picamera import PiCamera
import time
import RPi.GPIO as GPIO

###################### Define Functions #######################
#returns seconds passed since midnight
def sinceMidnight():![BatCam1](https://user-images.githubusercontent.com/79314212/123788121-ecf74e80-d8db-11eb-8f1a-7a6ae190ed75.jpg)

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

#set time for start and end of daytime 
#it will be NOT RECORDING during that time!
day = ("07:00:00","19:00:00")
daySec = (toSeconds(day[0]),toSeconds(day[1]))

GPIO.output(37,GPIO.HIGH) #turns green-LED shortly on when script starts
time.sleep(3)
GPIO.output(37,GPIO.LOW)

GPIO.output((16),GPIO.HIGH) #turns IR-light shortly on when script starts
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
		if firstRun or (currTime-nowVideo).total_seconds()>900:
			if not firstRun and isRecording:
				print("Stopping video recording")
				camera.stop_recording()
			nowVideo = datetime.now()
			GPIO.output((16),GPIO.HIGH)
			print(f"Start video recording {nowVideo}")
			camera.start_recording("FlederCam_"+
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