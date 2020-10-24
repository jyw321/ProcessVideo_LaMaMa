import os
import glob
import csv
from pymediainfo import MediaInfo
import argparse

parser = argparse.ArgumentParser()
parser.description = "survey a directory for AV files and report on technical metadata"
parser.add_argument("-d", "--directory",
                    required = True,
                    help = "Path to a directory of AV files")
parser.add_argument("-e", "--extension",
                    required = True,
                    help = "Extension of AV file to survey")
parser.add_argument("-o", "--output",
                    required = True,
                    help = "Path to the save the metadata as a CSV")
args = parser.parse_args()

print(args.directory, args.extension, args.output)

video_dir = '/Users/klavierwong/Desktop/amia19'

mov_list = glob.glob(os.path.join(video_dir, '**', '*mov'))

all_file_data = []

for item in mov_list:
    media_info = MediaInfo.parse(item)
    for track in media_info.tracks:
        if track.track_type == "General":
            general_data = [
                track.file_name,
                track.file_extension,
                track.format,
                track.file_size,
                track.duration]
    all_file_data.append(general_data)


with open('/Users/klavierwong/desktop/amia19/script_output.csv', 'w') as f:
    md_csv = csv.writer(f)
    md_csv.writerow([
        'filename',
        'extension',
        'format',
        'size',
        'duration'
    ])
    md_csv.writerows(sorted(all_file_data))