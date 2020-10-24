# in Python, hit Shift+Enter/Return to execute a command

# import modules
import os
import glob
import csv
from pymediainfo import MediaInfo


# list all files in a designated folder to give you a full view of the folder
# in quote 'your file path'
os.listdir('/Volumes/KLA_DATA/Asian_CineVision')


# make a new directory for folder path, here we use video_dir
# in quote 'your file path'
video_dir='/Volumes/KLA_DATA/Asian_CineVision'


# gather all mp4 files and make them in a new directory, here we use mov_list
mov_list = glob.glob(os.path.join(video_dir, "**", "*mp4"), recursive=True)


# run this and you will see a full list of mp4 files
mov_list


# run this to count how many files in mov_list
len(mov_list)


# run this and you will get a total file size of all the mp4 files in GigaBytes
size_list = []

for item in mov_list:
    size_list.append(os.stat(item).st_size)

sum(size_list)/(1000 ** 3)


# run this and you will get a list of file sizes of the files in the folder in GigaBytes
size_list_GB = []

for item in mov_list:
      size_list_GB.append((os.stat(item).st_size)/(1000**3))

size_list_GB


# run this and you will see different forms of showing duration of the FIRST video in the mov_list. Pick on format you like.
media_info = MediaInfo.parse(mov_list[0])

for track in media_info.tracks:
    if track.track_type == "General":
        print(track.to_data()["other_duration"])
        

# for example, you like the FIRST format which is minutes and seconds, then you run this code. In Python, items are ordered from 0, instead of 1.
for track in media_info.tracks:
    if track.track_type == "General":
        print(track.to_data()["other_duration"][0])
        
        
# run this and you will generate a list with file name, file extention, duration, and file size in GigaBytes
all_file_data =[]

for item in mov_list:
    media_info=MediaInfo.parse(item)
    for track in media_info.tracks:
        if track.track_type=='General':
            general_data=[track.file_name,track.file_extension,track.to_data()["other_duration"][0],(os.stat(item).st_size)/(1000**3)]
            print(general_data)
    all_file_data.append(general_data)
    
all_file_data


# this step leads to creation of a csv file
# in quote, 'your destination file path' of the csv
with open('/users/klavierwong/desktop/cctv_duration_size_survey.csv','w',encoding='utf8') as f:
    md_csv=csv.writer(f)
    md_csv.writerow(['filename','extension','duration','file_size_GB'])
    md_csv.writerows(all_file_data)