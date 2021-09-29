# This script uses the ADC of the FlederCam to record timestamps of light-barrier events, by detecting drops in the output
# voltage of the signals normally used to trigger external DSLRs
# Additional information can be found on GitHub: https://gabik-bat.github.io/FlederCam/

import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from datetime import datetime

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
chanIn = AnalogIn(ads, ADS.P2)
chanOut = AnalogIn(ads, ADS.P3)

while True:
	if chanIn.voltage <= 1:
		print("IN Trigger detected!")
		now = datetime.now()
		f = open("Detections.txt","a")
		f.write("in "+now.strftime("%d.%m.%Y %H:%M:%S")+"\n")
		f.close
		time.sleep(0.2)	
	if chanOut.voltage <= 1:
		print("OUT Trigger detected!")
		now = datetime.now()
		f = open("Detections.txt","a")
		f.write("out "+now.strftime("%d.%m.%Y %H:%M:%S")+"\n")
		f.close
		time.sleep(0.2)	
	time.sleep(0.025)