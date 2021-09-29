# This script uses the converted video recordings of the FlederCam and combines them with a file containing timestamps of
# external input to create shorter videos (snips) for easier reviewing. 
# Additional information can be found on GitHub: https://gabik-bat.github.io/FlederCam/

import numpy as np
import pandas as pd
import glob
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

det_path = "xxx" #set path of "Detections.txt" file containing the light barrier registrations
vid_path = "xxx" #set path of folder with converted video files
snip_path = "xxx" #setpath of folder to save snips

#load light barrier registrations
det = pd.read_table(det_path,sep=":| ",engine="python",header=None,names=["direction","date","hour", "min","sec"])
det["sec_mid"]=[row[2]*3600+row[3]*60+row[4] for index,row in det.iterrows()]
print("Detections loaded!")

#load converted video data	
vid = pd.DataFrame({"path":[],"file":[],"date":[],"hour":[],"min":[],"sec":[],"sec_mid":[]})
videos = glob.glob(vid_path + "*.mp4")
for video in videos:
	file_name = video.split("/")[-1][0:-4]
	print(file_name)
	date = file_name[10:20].split("_")
	date_re = str(date[2] + "." + date[1] + "." + date[0])
	time = file_name[21:29].split("_")
	sec_mid = int(time[0]) * 3600 + int(time[1]) * 60 + int(time[2])
	vid = vid.append({"path":video,"file":file_name,"date":date_re,"hour":time[0],"min":time[1],"sec":time[2],"sec_mid":sec_mid},ignore_index=True)
vid["sec_mid"] = vid["sec_mid"].astype(int)
print("Video information loaded!")
fails = 0

#loop over light barrier detections and find matching 15 min video 
print("Matching detections with video files")
for index, row in det.iterrows():
	fail = False
	print(f"  ->searching for detection at {row['hour']}:{row['min']}:{row['sec']} on the {row['date']}")
	target_vid=vid[(vid["date"]==row["date"]) & (vid["sec_mid"]<=row["sec_mid"]) & (vid["sec_mid"] >= row["sec_mid"]-15*60)]
	print(f"     -> video found: {target_vid['file'].to_string().split()[1]}")
	print("          -> extracting video snip...")
	print(target_vid["sec_mid"].values)
	vid_secmid = (target_vid["sec_mid"].values).tolist()
	target_file = (target_vid["file"].values).tolist()
	print(target_file)
	try:	
		print(vid_secmid[0])
		#3 sec before light barrier registration = start of snip
		t1 = row["sec_mid"] - vid_secmid[0] - 3 
		#3 sec after light barrier registration = end of snip
		t2 = row["sec_mid"] - vid_secmid[0] + 3 
		print(f"{t1} - {t2}")
		print(target_file[0] + ".mp4")
		target_file = target_file[0] + ".mp4"
	except:
		print("Empty Array")
	snip_date = "_".join(reversed(row["date"].split(".")))
	snip_name = "snip_"+snip_date+"_"+str(row["hour"]).zfill(2)+"_"+str(row["min"]).zfill(2)+"_"+str(row["sec"]).zfill(2)+"_"+row["direction"]+".mp4"
	
	#extract 6-second-long snip from video file
	try:		
		ffmpeg_extract_subclip(vid_path+target_file,int(t1),int(t2),snip_path+snip_name)
	#most common cause of failure are detections is outside of recording time -> no video for extraction
	except:
		fail = True	
		fails += 1
	if fail:
		print("          -> extraction FAILED!")
	else:
		print("          -> extraction complete!")
print(f"Conversion completed ({fails} detections could not be found)")