```python
# after you download a production video file from La MaMa's server, make sure the file folder name does not contain any space.
# space contained in a file folder name or a file name will confuse our computer.
# replace "space" with a underscore "_"
```


```python
# before we start, we need to import some modules

import os
import path
import glob
import shutil
import subprocess
```


```python
# change directory to your working directory where born-digital camera-original video file folders locate
# in this case, I use my own external hard drive which is loaded under  "/volumes"

os.chdir ('/volumes/samsung_t5/lamama_videos')

# use list command to check if all the file folders needed are here
os.listdir()
```


```python
# from here, we start to handle each show folder.
# let's take "2012.03.31 The Pi-roject" as a demonstration

# to process the same workflow with each folder, you just simple change the directory

# the very first step is to extract all raw footage video files from the complicatedly nested file folder structure
# I use the below codes to put all the raw footage video files into one folder called "raw_footage"
```


```python
# make video_dir the file fold from which your raw footage is drived

video_dir = '/volumes/samsung_t5/lamama_videos/20120428_Dreambridge'
```


```python
# make destination_dir the file fold that you will store your raw footage for later editing
# If this file folder does not exist, the program will make one for you

destination_dir = '/volumes/samsung_t5/lamama_videos/20120428_Dreambridge-editing'
if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)
```


```python
# we know that all raw footage video files are MP4 format
# grasp all the video files end with MP4
# make a list for these MP4 files

mp4_list = glob.glob(os.path.join(video_dir, "**", "*MP4"), recursive=True)
```


```python
# let's check how many MP4 files are found

mp4_list
```


```python
# make a raw_footage folder to put all the extracted raw footage video files
# if there is no raw_footage folder, the program will make one for you

raw_footage_folder = os.path.join(destination_dir, 'raw_footage')
if not os.path.exists(raw_footage_folder):
    os.makedirs(raw_footage_folder)
```


```python
# a 'for loop' to put all the raw footage video files ending with MP4 into the raw_footage folder

for item in mp4_list:
	shutil.copy(item, raw_footage_folder)
```


```python
# to check if all the video files are put into the raw_footage folder

os.listdir(raw_footage_folder)
```


```python
# perfect, we have extracted all the raw footage video files and have put them into one single folder for further processing

# the next step is to transcode them into preservation level and access level files
# after each video files are transcoded to the needed formats, we then concatenate the separate files into one single video for uploading to server

# we will use FFmpeg tool to process the below actions. 
```


```python
# you can see we have extracted all the needed raw footage video files to a new folder
# let's change the directory to raw_footage folder for further actions

os.chdir(raw_footage_folder)
```


```python
# make the current directory the video directory

video_dir = raw_footage_folder
```


```python
# again, make a list.
# This time we call the list raw_mp4_list. 
#The list contains the files we have extracted to raw_footage

raw_mp4_list = glob.glob(os.path.join(video_dir, "*MP4"))
```


```python
raw_mp4_list
```


```python
# for more convenient viewing, we sort the list

raw_mp4_list.sort()
```


```python
raw_mp4_list
```


```python
# now we are going to transcode the files in raw_mp4_list into preservation master format
# first we define a destination directory to hold the video files after transcoding 
# here, we create a new folder under raw_footage and name it "preservation"
# if the preservation directory does not exist, the program will make one

destination_dir = os.path.join (video_dir, 'preservation')
if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)
```


```python
# to create a "for-loop", asking the program to do the same transcoding action with each item in raw_mp4_list
for item in raw_mp4_list:
    if item.endswith('MP4'):
        
        # we define the directory for output_file for ffmpeg.
        output_file = os.path.join(destination_dir, os.path.basename(item).replace('.MP4','master.MP4'))
        
        # we use ffmpeg to transcode each raw footage video into preservation master format requirement
        # set the output format H.264 with max bitrate 15000kpbs for image and 576kpbs for aac audio
        subprocess.run (['ffmpeg', '-i', item, '-c:v', 'libx264', '-b:v', '15000k', '-c:a', 'aac', '-b:a', '576k', output_file])
        
# PLEASE NOTE, usually transcoding a video file of 1GB takes 30min. If you have multiple large video files here, be prepared.
```


```python
# let's take a look at if all the video files are transcoded into preservation master format

os.listdir(destination_dir)
```


```python
# the next step is to concatenate all the transcoded video files into ONE file, which represents the full recording of a performance show

# before we concatenate the files, we need to make a "mylist.txt" file which will tell the program what files are to be concatenated

# documentation of concatenation and "mylist.txt" could be found here https://trac.ffmpeg.org/wiki/Concatenate  
```


```python
# we change the directory to the "preservation" file folder, so that the "mylist.txt" will be placed here as well
# we then generate a mp4_master_list which contains all the transcoded videos
# we need to make sure the "mylist.txt" will the files in a correct order, so we need to sort the mp4_master_list first

os.chdir(destination_dir)
master_mp4_list = glob.glob(os.path.join(destination_dir, "*MP4"))
master_mp4_list.sort()
master_mp4_list
```


```python
print(os.getcwd())
```


```python
# to create the "mylist.txt", we ask python to create a file
# in the "mylist.txt", contents are arranged in a certain format, so that FFmpeg knows what files, in what order, to be concatenated

filename = 'mylist.txt'
with open (filename, 'w') as f:
    for item in master_mp4_list:
        f.write ('file \'' + os.path.basename(item) + '\'\n')

```


```python
# now we use ffmpeg to concatenate these preservation master format videos into a FULL preservation master video

# first we need to define the "mylist.txt" into a path
mylist = os.path.join (destination_dir, 'mylist.txt')

# define the output file path
# name the file "Preservation_Master", to make sure it will be listed after the other video files

output_file = os.path.join(destination_dir, 'Preservation_Master.MP4')

# we use subprocess module to run FFmpeg which is supposed to be process in bash terminal; each FFmpeg command needs to be in a string form, so we put them in quotation marks
subprocess.run(['ffmpeg', '-f', 'concat', '-i', mylist, '-c', 'copy', output_file])
```


```python
# now let's take a look at if the FULL preservation master video is successfully generation

os.listdir(destination_dir)
```


```python
# now we transcode the preservation master video into a smaller size for public viewing

# we first define the input_file, which is the preservation master video that we just created
# because we just named the FULL preservation master video file as "preservation_master", it must be at the last place in the list (-1 place)
mp4_master_list = glob.glob (os.path.join(destination_dir,'**MP4'))

input_file = (mp4_master_list[-1])

# then we define the output file path and name the file "Public_View.MP4"

output_file = os.path.join(destination_dir, 'Public_View.MP4')
```


```python
# we use subprocess module to run FFmpeg which is supposed to be process in bash terminal; each FFmpeg command needs to be in a string form, so we put them in quotation marks

subprocess.run(['ffmpeg', '-i', input_file, '-c:v', 'libx264', '-b:v', '5000k', '-c:a', 'aac', output_file])
```


```python
# after generating the public_view file which serves the access file of the video, we add the fade in and fade out effect to it
# here again we use FFmpeg to process the task
# we define the input file as the "public_view" video which we just generated, and we also define the output file as the "public_view_final"

input_file = os.path.join(destination_dir, 'Public_View.MP4')
output_file = os.path.join(destination_dir, 'Public_View_Final.MP4')

# we then define the setting with fade-in and fade-out 3 seconds for both video and audio
# the video with fade-in fade-out effects will be exported in h264 with aac in bitrate 10Mbps (settings refer to FFmpeg documentation or ffprovisor)
# the fade-in fade-out command means: fade in for 3 seconds, reverse the whole track, fade in 3 seconds again, reverse back 
fade_video = '"fade=d=2, reverse, fade=d=2, reverse"'
fade_audio = '"afade=d=2, areverse, afade=d=2, areverse"'
setting = '-c:v libx264 -b:v 5000k -c:a aac'

# if we write every FFmpeg command in the subprocess, the code will be too long
# so here we first define the whole chain of codes into ffmpeg_cmd
ffmpeg_cmd = 'ffmpeg -i' + ' ' + input_file + ' ' + '-filter_complex' + ' ' + fade_video + ' ' + '-filter_complex' + ' ' + fade_audio + ' ' + setting + ' ' + output_file

# check this ffmpeg_cmd code, it should be identical to the commands that are supposed to be run in bash terminal
print (ffmpeg_cmd)
```


```python
# PLEASE NOTE if the input file (public view) is too large, e.g. 5+GB, this program might not be able to process due to the limited RAM in personal computer
# if the input file is too large, you may need to use other video editing software to add the fade-in/out effect

subprocess.call (ffmpeg_cmd, shell=True)
```


```python
# Now you have both the "Preservation_Master.MP4" and the "Public_View_Final.MP4". They serve as preservation master and public access file respectively.
# Name these files according to La MaMa's naming rules and upload back to the server.
```
