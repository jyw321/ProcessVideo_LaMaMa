# Before we start run the codes

After you download a production video file from La MaMa's server, make sure the file folder name does not contain any space or special characters. A file folder name that contains space will confuse our computer. Remember to replace "space" with a underscore "_".

For example, a file folder name "2012.04.28 Dream bridge" should be renamed to "20120428_Dreambridge".

# Let's start

Now, we need to import some modules which will help our jobs.


```python
import os
import path
import glob
import shutil
import subprocess
import bagit
```

## Fixity Check

Before starting the whole video transcoding project, let's first validate our files - fixity check. 
Every show folder was packaged with a method called "BagIt", which automatically included checksum files. We can use BagIt tool to validate all the files stored in the folder are valid.
For now, we use the "20120518_Mermaid" show folder as an example.


```python
bag = bagit.Bag('/volumes/samsung_t5/lamama_videos/20120518_Mermaid')
if bag.is_valid():
    print("yay :)")
else:
    print("boo :(")
```


```python
# If you got "Yay :)", you are good to proceed.
```

## First task - extract all the video files from the nested folders and put them into one file folder

First thing first, we change the directory to your working directory where our born-digital camera-original video file folders locate. For my daily habit, I use my own external hard drive to store all the La MaMa files. The external hard drive is loaded under "/volumes".



```python
os.chdir ('/volumes/samsung_t5/lamama_videos')

os.listdir() # use list command to check if all the file folders needed are here
```




    ['20120520_Chamber_2-editing',
     '2012.03.01 I Killed My Mother-edited',
     '2012.03.03 FediricoPreProduction',
     '20120519_Beauty',
     '20120518_Mermaid',
     '2012.03.03 FediricoPreProduction-edited',
     'Testing',
     '.__2020Fall_Internship_LaMaMa',
     '20120506_Judith_Of_Shimoda',
     '_2020Fall_Internship_LaMaMa',
     '20120519_Beauty-editing',
     'Unfinished',
     '20120506_Judith_Of_Shimoda-editing',
     '20120520_East_Village_Dance',
     '20120520_East_Village_Dance-editing',
     '20120520_Chamber_2']



From here, we start to handle each folder which represents each stage show. **Remember, this code script is semi-automated. To work on each stage show folder, you need to change the video_dir and destination_dir accordingly. But don't worry, these are the ONLY two places that need your attention every time.**


I then make video_dir the file folder from which my raw footage video files are derived. 

**Remember, here is the first time that needs you to change the file folder name accordingly.**


```python
video_dir = '/volumes/samsung_t5/lamama_videos/20120518_Mermaid' 
```

I make the destination_dir as the file folder where I will store all my extracted raw footage video files for later editing. I name this newly created fild foler "(original file folder name + editing". 

**Remember, this is the second and the last time that needs you to change the folder name accordingly. Here, in order to create a new working folder for further video editing, I name this folder by adding "-editing" at the end.**


```python
destination_dir = '/volumes/samsung_t5/lamama_videos/20120518_Mermaid-editing' 

if not os.path.exists(destination_dir):
    os.makedirs(destination_dir) 
    # Here it means if this file folder does not exist, the program will make one for you
```

Usually, all raw footage video files are MP4 format, as long as they are shot by the SONY digital camera. 

**But it is always worthwhile to open the file folder to double check.**



```python
mp4_list = glob.glob(os.path.join(video_dir, "**", "*MP4"), recursive=True) # grasp all the video files end with MP4
```


```python

mp4_list # make a list, and check how many MP4 files are found by the computer
```




    ['/volumes/samsung_t5/lamama_videos/20120518_Mermaid/data/Raw Footage/BPAV/CLPR/632_0001_01/632_0001_01.MP4',
     '/volumes/samsung_t5/lamama_videos/20120518_Mermaid/data/Raw Footage/BPAV/CLPR/632_0001_02/632_0001_02.MP4',
     '/volumes/samsung_t5/lamama_videos/20120518_Mermaid/data/Raw Footage/BPAV/CLPR/632_0001_03/632_0001_03.MP4',
     '/volumes/samsung_t5/lamama_videos/20120518_Mermaid/data/Raw Footage/BPAV/CLPR/632_0001_04/632_0001_04.MP4',
     '/volumes/samsung_t5/lamama_videos/20120518_Mermaid/data/Raw Footage/BPAV/CLPR/632_0001_05/632_0001_05.MP4',
     '/volumes/samsung_t5/lamama_videos/20120518_Mermaid/data/Raw Footage/BPAV/CLPR/632_0001_06/632_0001_06.MP4']



I then make a raw_footage folder to put all the extracted raw footage video files



```python
raw_footage_folder = os.path.join(destination_dir, 'raw_footage')
if not os.path.exists(raw_footage_folder):
    os.makedirs(raw_footage_folder)
    # here it means that if there is no raw_footage folder, the program will make one for you
```

**This is an important and beautiful step: A 'for loop' is created to extract all the raw footage MP4 files and put them all into the raw_footage folder.



```python
for item in mp4_list:
	shutil.copy(item, raw_footage_folder)
```


```python

os.listdir(raw_footage_folder) # to check if all the video files are put into the raw_footage folder
```




    ['632_0001_01.MP4',
     '632_0001_02.MP4',
     '632_0001_03.MP4',
     '632_0001_04.MP4',
     '632_0001_05.MP4',
     '632_0001_06.MP4']



**Perfect, we have extracted all the raw footage video files and have put them into one single folder for further processing.**

## Second task - transcode the extract raw footage video files into preservation master file format. 

**For now, La MaMa requires videos be exported to H.264 wrapped with MPEG-4 with bitrate 15Mb/s.**

**We will use FFmpeg to process the below actions.** 

Now you can see I have extracted all the needed raw footage video files into a new folder called "raw_foorage".

Then let's change the directory to raw_footage folder for the following actions.


```python
os.chdir(raw_footage_folder)
```


```python

video_dir = raw_footage_folder # make the raw footage folder the video dir
```

Again, make a list. This time we call the list raw_mp4_list. The list will contain the files we have extracted to the raw_footage folder.


```python
raw_mp4_list = glob.glob(os.path.join(video_dir, "*MP4"))
```


```python

raw_mp4_list.sort() # for more convenient viewing, we sort the list
```


```python
raw_mp4_list
```




    ['/volumes/samsung_t5/lamama_videos/20120518_Mermaid-editing/raw_footage/632_0001_01.MP4',
     '/volumes/samsung_t5/lamama_videos/20120518_Mermaid-editing/raw_footage/632_0001_02.MP4',
     '/volumes/samsung_t5/lamama_videos/20120518_Mermaid-editing/raw_footage/632_0001_03.MP4',
     '/volumes/samsung_t5/lamama_videos/20120518_Mermaid-editing/raw_footage/632_0001_04.MP4',
     '/volumes/samsung_t5/lamama_videos/20120518_Mermaid-editing/raw_footage/632_0001_05.MP4',
     '/volumes/samsung_t5/lamama_videos/20120518_Mermaid-editing/raw_footage/632_0001_06.MP4']



Now we are going to transcode the files in the raw_mp4_list into preservation master format.

First, we need to again define a destination directory to hold the video files after transcoding. Here, we create a new folder under raw_footage and name it "preservation"



```python
destination_dir = os.path.join (video_dir, 'preservation')
if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)
    # if the preservation directory does not exist, the program will make one
```

Again, I create a "for-loop", asking the program to do the same transcoding action with each item in the raw_mp4_list.


```python
for item in raw_mp4_list:
    if item.endswith('MP4'):
        
        # we define the directory for output_file for ffmpeg.
        output_file = os.path.join(destination_dir, os.path.basename(item).replace('.MP4','master.MP4'))
        
        # we use ffmpeg to transcode each raw footage video into preservation master format requirement
        # set the output format H.264 with max bitrate 15000kpbs for image and 576kpbs for aac audio
        subprocess.run (['ffmpeg', '-i', item, '-c:v', 'libx264', '-b:v', '15000k', '-c:a', 'aac', '-b:a', '576k', output_file])
   
```

     
**PLEASE NOTE, usually transcoding a video file of 1GB takes 30min. If you have multiple large video files here, be prepared.**

Now the computer has finished transcoding each video file, let's check if all the video files are transcoded and put into the preservation file folder.


```python
os.listdir(destination_dir)
```




    ['632_0001_01master.MP4',
     '632_0001_02master.MP4',
     '632_0001_03master.MP4',
     '632_0001_04master.MP4',
     '632_0001_05master.MP4',
     '632_0001_06master.MP4']



## Third task - concatenate all the transcoded files into one, making it the full recording of one stage show.

Before we concatenate the files, we need to make a "mylist.txt" file which will tell the program what files are to be concatenated

Documentation of concatenation and creation of mylist.txt could be [found here](https://trac.ffmpeg.org/wiki/Concatenate)


I change the directory to the "preservation" folder, so that the "mylist.txt" will be placed here as well. 

I then generate a mp4_master_list which contains all the transcoded videos.

I need to make sure the in the "mylist.txt" document, all files are listed in a correct order, so I also need to sort the mp4_master_list.



```python
os.chdir(destination_dir)
master_mp4_list = glob.glob(os.path.join(destination_dir, "*MP4"))
master_mp4_list.sort()
master_mp4_list
```




    ['/volumes/samsung_t5/lamama_videos/20120518_Mermaid-editing/raw_footage/preservation/632_0001_01master.MP4',
     '/volumes/samsung_t5/lamama_videos/20120518_Mermaid-editing/raw_footage/preservation/632_0001_02master.MP4',
     '/volumes/samsung_t5/lamama_videos/20120518_Mermaid-editing/raw_footage/preservation/632_0001_03master.MP4',
     '/volumes/samsung_t5/lamama_videos/20120518_Mermaid-editing/raw_footage/preservation/632_0001_04master.MP4',
     '/volumes/samsung_t5/lamama_videos/20120518_Mermaid-editing/raw_footage/preservation/632_0001_05master.MP4',
     '/volumes/samsung_t5/lamama_videos/20120518_Mermaid-editing/raw_footage/preservation/632_0001_06master.MP4']




```python
print(os.getcwd()) # make sure the current directory is the preservation folder
```

    /Volumes/Samsung_T5/LaMaMa_Videos/20120518_Mermaid-editing/raw_footage/preservation


To create the "mylist.txt", I ask python to create a txt file.

In the "mylist.txt", contents are arranged in a certain format, so that FFmpeg knows what files, in what order, to be concatenated.


```python
filename = 'mylist.txt'
with open (filename, 'w') as f:
    for item in master_mp4_list:
        f.write ('file \'' + os.path.basename(item) + '\'\n')
```

Now we use FFmpeg to concatenate these preservation master format videos into a FULL preservation master video

First we need to define the "mylist.txt" into a path.


```python
mylist = os.path.join (destination_dir, 'mylist.txt')
```

Next I define the output file path. Name the file "Preservation_Master", to make sure after being generated, it will be listed at the last place among all other video files. I will explain in the latter step why this order place is so important.



```python
output_file = os.path.join(destination_dir, 'Preservation_Master.MP4')
```

I then use the subprocess module to run FFmpeg which is supposed to be process in bash terminal; each FFmpeg command needs to be in a string form, so we put them in quotation marks.



```python
subprocess.run(['ffmpeg', '-f', 'concat', '-i', mylist, '-c', 'copy', output_file])
```




    CompletedProcess(args=['ffmpeg', '-f', 'concat', '-i', '/volumes/samsung_t5/lamama_videos/20120518_Mermaid-editing/raw_footage/preservation/mylist.txt', '-c', 'copy', '/volumes/samsung_t5/lamama_videos/20120518_Mermaid-editing/raw_footage/preservation/Preservation_Master.MP4'], returncode=0)



Now let's take a look at if the FULL preservation master video is successfully generation.


```python
os.listdir(destination_dir)
```




    ['632_0001_01master.MP4',
     '632_0001_02master.MP4',
     '632_0001_03master.MP4',
     '632_0001_04master.MP4',
     '632_0001_05master.MP4',
     '632_0001_06master.MP4',
     'mylist.txt',
     'Preservation_Master.MP4']



## Fourth step - transcode the preservation master video into a smaller size for public view

**For now, La MaMa requires videos be exported to H.264 wrapped with MPEG-4 with bitrate 5Mb/s.**

I first define the input_file, which is the preservation master video that we just created. Because I just named the preservation master video file as "preservation_master", it must be at the last place in the list (-1 place). **I told you this order place is important.**



```python
mp4_master_list = glob.glob (os.path.join(destination_dir,'**MP4'))

input_file = (mp4_master_list[-1])
```

Then I define the output file path and name the file "Public_View.MP4".



```python
output_file = os.path.join(destination_dir, 'Public_View.MP4')
```

I use the subprocess module to run FFmpeg which is supposed to be process in bash terminal; each FFmpeg command needs to be in a string form, so we put them in quotation marks.


```python
subprocess.run(['ffmpeg', '-i', input_file, '-c:v', 'libx264', '-b:v', '5000k', '-c:a', 'aac', output_file])
```




    CompletedProcess(args=['ffmpeg', '-i', '/volumes/samsung_t5/lamama_videos/20120518_Mermaid-editing/raw_footage/preservation/Preservation_Master.MP4', '-c:v', 'libx264', '-b:v', '5000k', '-c:a', 'aac', '/volumes/samsung_t5/lamama_videos/20120518_Mermaid-editing/raw_footage/preservation/Public_View.MP4'], returncode=0)



## Fifth step - add fade-in and fade-out effect to the public view file

After generating the public_view file which serves the access file of the video, I will need to add the fade-in and fade-out effect to the video.

Here again we use FFmpeg to process the task.

We define the input file as the "public_view" video which we just generated, and we also define the output file as the "public_view_final".


```python
input_file = os.path.join(destination_dir, 'Public_View.MP4')
output_file = os.path.join(destination_dir, 'Public_View_Final.MP4')
```

I then define the setting with fade-in and fade-out 2 seconds for both video and audio (the number of seconds is changeable).

The fade-in and fade-out command codes refer to [here](https://video.stackexchange.com/questions/19867/how-to-fade-in-out-a-video-audio-clip-with-unknown-duration)



```python
fade_video = '"fade=d=2, reverse, fade=d=2, reverse"'
fade_audio = '"afade=d=2, areverse, afade=d=2, areverse"'
# the fade-in fade-out command means: fade in for 2 seconds, reverse the whole track, fade in 2 seconds again, reverse back 

setting = '-c:v libx264 -b:v 5000k -c:a aac'

```

If here I write every FFmpeg command in the subprocess, the code will be too long. So here I first define the whole chain of codes into ffmpeg_cmd.


```python
ffmpeg_cmd = 'ffmpeg -i' + ' ' + input_file + ' ' + '-filter_complex' + ' ' + fade_video + ' ' + '-filter_complex' + ' ' + fade_audio + ' ' + setting + ' ' + output_file

# check this ffmpeg_cmd code, it should be identical to the commands that are supposed to be run in bash terminal

print (ffmpeg_cmd)
```

    ffmpeg -i /volumes/samsung_t5/lamama_videos/20120518_Mermaid-editing/raw_footage/preservation/Public_View.MP4 -filter_complex "fade=d=2, reverse, fade=d=2, reverse" -filter_complex "afade=d=2, areverse, afade=d=2, areverse" -c:v libx264 -b:v 5000k -c:a aac /volumes/samsung_t5/lamama_videos/20120518_Mermaid-editing/raw_footage/preservation/Public_View_Final.MP4


**PLEASE NOTE if the input file (public view) is too large, e.g. 5+GB, this program might not be able to process due to the limited RAM in personal computer.**

**If the input file is too large or the process pauses in the midway, you may need to use other video editing software to add the fade-in/out effect.**


```python
subprocess.call (ffmpeg_cmd, shell=True)
```




    -9



Now I have generated both the "Preservation_Master.MP4" and the "Public_View_Final.MP4". They serve as preservation master and public access file respectively.

## Last but not least - Name these files according to La MaMa's naming rules and upload them to La MaMa's server.
