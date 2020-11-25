{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Before we start run the codes\n",
    "\n",
    "After you download a production video file from La MaMa's server, make sure the file folder name does not contain any space or special characters. A file folder name that contains space will confuse our computer. Remember to replace \"space\" with a underscore \"_\".\n",
    "\n",
    "For example, a file folder name \"2012.04.28 Dream bridge\" should be renamed to \"20120428_Dreambridge\"."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Let's start\n",
    "\n",
    "Now, we need to import some modules which will help our jobs."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 32,
   "metadata": {},
   "outputs": [],
   "source": [
    "import os\n",
    "import path\n",
    "import glob\n",
    "import shutil\n",
    "import subprocess\n",
    "import bagit"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "## Before starting the whole video transcoding project, let's first validate our files - fixity check. \n",
    "# Every show folder was packaged with a method called \"BagIt\", which automatically included checksum files. We can use BagIt tool to validate all the files stored in the folder are valid.\n",
    "# For now, we use the \"20120518_Mermaid\" show folder as an example."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "bag = bagit.Bag('/volumes/samsung_t5/lamama_videos/20120518_Mermaid')\n",
    "if bag.is_valid():\n",
    "    print(\"yay :)\")\n",
    "else:\n",
    "    print(\"boo :(\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# If you got \"Yay :)\", you are good to proceed."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## First task - extract all the video files from the nested folders and put them into one file folder\n",
    "\n",
    "First thing first, we change the directory to your working directory where our born-digital camera-original video file folders locate. For my daily habit, I use my own external hard drive to store all the La MaMa files. The external hard drive is loaded under \"/volumes\".\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 33,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "['20120520_Chamber_2-editing',\n",
       " '2012.03.01 I Killed My Mother-edited',\n",
       " '2012.03.03 FediricoPreProduction',\n",
       " '20120519_Beauty',\n",
       " '20120518_Mermaid',\n",
       " '2012.03.03 FediricoPreProduction-edited',\n",
       " 'Testing',\n",
       " '.__2020Fall_Internship_LaMaMa',\n",
       " '20120506_Judith_Of_Shimoda',\n",
       " '_2020Fall_Internship_LaMaMa',\n",
       " '20120519_Beauty-editing',\n",
       " 'Unfinished',\n",
       " '20120506_Judith_Of_Shimoda-editing',\n",
       " '20120520_East_Village_Dance',\n",
       " '20120520_East_Village_Dance-editing',\n",
       " '20120520_Chamber_2']"
      ]
     },
     "execution_count": 33,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "os.chdir ('/volumes/samsung_t5/lamama_videos')\n",
    "\n",
    "os.listdir() # use list command to check if all the file folders needed are here"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "From here, we start to handle each folder which represents each stage show. **Remember, this code script is semi-automated. To work on each stage show folder, you need to change the video_dir and destination_dir accordingly. But don't worry, these are the ONLY two places that need your attention every time.**\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "I then make video_dir the file folder from which my raw footage video files are derived. \n",
    "\n",
    "**Remember, here is the first time that needs you to change the file folder name accordingly.**"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 34,
   "metadata": {},
   "outputs": [],
   "source": [
    "video_dir = '/volumes/samsung_t5/lamama_videos/20120518_Mermaid' "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "I make the destination_dir as the file folder where I will store all my extracted raw footage video files for later editing. I name this newly created fild foler \"(original file folder name + editing\". \n",
    "\n",
    "**Remember, this is the second and the last time that needs you to change the folder name accordingly. Here, in order to create a new working folder for further video editing, I name this folder by adding \"-editing\" at the end.**"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 35,
   "metadata": {},
   "outputs": [],
   "source": [
    "destination_dir = '/volumes/samsung_t5/lamama_videos/20120518_Mermaid-editing' \n",
    "\n",
    "if not os.path.exists(destination_dir):\n",
    "    os.makedirs(destination_dir) \n",
    "    # Here it means if this file folder does not exist, the program will make one for you"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Usually, all raw footage video files are MP4 format, as long as they are shot by the SONY digital camera. \n",
    "\n",
    "**But it is always worthwhile to open the file folder to double check.**\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 36,
   "metadata": {},
   "outputs": [],
   "source": [
    "mp4_list = glob.glob(os.path.join(video_dir, \"**\", \"*MP4\"), recursive=True) # grasp all the video files end with MP4"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 37,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "['/volumes/samsung_t5/lamama_videos/20120518_Mermaid/data/Raw Footage/BPAV/CLPR/632_0001_01/632_0001_01.MP4',\n",
       " '/volumes/samsung_t5/lamama_videos/20120518_Mermaid/data/Raw Footage/BPAV/CLPR/632_0001_02/632_0001_02.MP4',\n",
       " '/volumes/samsung_t5/lamama_videos/20120518_Mermaid/data/Raw Footage/BPAV/CLPR/632_0001_03/632_0001_03.MP4',\n",
       " '/volumes/samsung_t5/lamama_videos/20120518_Mermaid/data/Raw Footage/BPAV/CLPR/632_0001_04/632_0001_04.MP4',\n",
       " '/volumes/samsung_t5/lamama_videos/20120518_Mermaid/data/Raw Footage/BPAV/CLPR/632_0001_05/632_0001_05.MP4',\n",
       " '/volumes/samsung_t5/lamama_videos/20120518_Mermaid/data/Raw Footage/BPAV/CLPR/632_0001_06/632_0001_06.MP4']"
      ]
     },
     "execution_count": 37,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "\n",
    "mp4_list # make a list, and check how many MP4 files are found by the computer"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "I then make a raw_footage folder to put all the extracted raw footage video files\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 38,
   "metadata": {},
   "outputs": [],
   "source": [
    "raw_footage_folder = os.path.join(destination_dir, 'raw_footage')\n",
    "if not os.path.exists(raw_footage_folder):\n",
    "    os.makedirs(raw_footage_folder)\n",
    "    # here it means that if there is no raw_footage folder, the program will make one for you"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "**This is an important and beautiful step: A 'for loop' is created to extract all the raw footage MP4 files and put them all into the raw_footage folder.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 39,
   "metadata": {},
   "outputs": [],
   "source": [
    "for item in mp4_list:\n",
    "\tshutil.copy(item, raw_footage_folder)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 40,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "['632_0001_01.MP4',\n",
       " '632_0001_02.MP4',\n",
       " '632_0001_03.MP4',\n",
       " '632_0001_04.MP4',\n",
       " '632_0001_05.MP4',\n",
       " '632_0001_06.MP4']"
      ]
     },
     "execution_count": 40,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "\n",
    "os.listdir(raw_footage_folder) # to check if all the video files are put into the raw_footage folder"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "**Perfect, we have extracted all the raw footage video files and have put them into one single folder for further processing.**"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Second task - transcode the extract raw footage video files into preservation master file format. \n",
    "\n",
    "**For now, La MaMa requires videos be exported to H.264 wrapped with MPEG-4 with bitrate 15Mb/s.**\n",
    "\n",
    "**We will use FFmpeg to process the below actions.** "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Now you can see I have extracted all the needed raw footage video files into a new folder called \"raw_foorage\".\n",
    "\n",
    "Then let's change the directory to raw_footage folder for the following actions."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 41,
   "metadata": {},
   "outputs": [],
   "source": [
    "os.chdir(raw_footage_folder)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 42,
   "metadata": {},
   "outputs": [],
   "source": [
    "\n",
    "video_dir = raw_footage_folder # make the raw footage folder the video dir"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Again, make a list. This time we call the list raw_mp4_list. The list will contain the files we have extracted to the raw_footage folder."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 43,
   "metadata": {},
   "outputs": [],
   "source": [
    "raw_mp4_list = glob.glob(os.path.join(video_dir, \"*MP4\"))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 44,
   "metadata": {},
   "outputs": [],
   "source": [
    "\n",
    "raw_mp4_list.sort() # for more convenient viewing, we sort the list"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 45,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "['/volumes/samsung_t5/lamama_videos/20120518_Mermaid-editing/raw_footage/632_0001_01.MP4',\n",
       " '/volumes/samsung_t5/lamama_videos/20120518_Mermaid-editing/raw_footage/632_0001_02.MP4',\n",
       " '/volumes/samsung_t5/lamama_videos/20120518_Mermaid-editing/raw_footage/632_0001_03.MP4',\n",
       " '/volumes/samsung_t5/lamama_videos/20120518_Mermaid-editing/raw_footage/632_0001_04.MP4',\n",
       " '/volumes/samsung_t5/lamama_videos/20120518_Mermaid-editing/raw_footage/632_0001_05.MP4',\n",
       " '/volumes/samsung_t5/lamama_videos/20120518_Mermaid-editing/raw_footage/632_0001_06.MP4']"
      ]
     },
     "execution_count": 45,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "raw_mp4_list"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Now we are going to transcode the files in the raw_mp4_list into preservation master format.\n",
    "\n",
    "First, we need to again define a destination directory to hold the video files after transcoding. Here, we create a new folder under raw_footage and name it \"preservation\"\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 46,
   "metadata": {},
   "outputs": [],
   "source": [
    "destination_dir = os.path.join (video_dir, 'preservation')\n",
    "if not os.path.exists(destination_dir):\n",
    "    os.makedirs(destination_dir)\n",
    "    # if the preservation directory does not exist, the program will make one"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Again, I create a \"for-loop\", asking the program to do the same transcoding action with each item in the raw_mp4_list."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 47,
   "metadata": {},
   "outputs": [],
   "source": [
    "for item in raw_mp4_list:\n",
    "    if item.endswith('MP4'):\n",
    "        \n",
    "        # we define the directory for output_file for ffmpeg.\n",
    "        output_file = os.path.join(destination_dir, os.path.basename(item).replace('.MP4','master.MP4'))\n",
    "        \n",
    "        # we use ffmpeg to transcode each raw footage video into preservation master format requirement\n",
    "        # set the output format H.264 with max bitrate 15000kpbs for image and 576kpbs for aac audio\n",
    "        subprocess.run (['ffmpeg', '-i', item, '-c:v', 'libx264', '-b:v', '15000k', '-c:a', 'aac', '-b:a', '576k', output_file])\n",
    "   "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "     \n",
    "**PLEASE NOTE, usually transcoding a video file of 1GB takes 30min. If you have multiple large video files here, be prepared.**"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Now the computer has finished transcoding each video file, let's check if all the video files are transcoded and put into the preservation file folder."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 48,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "['632_0001_01master.MP4',\n",
       " '632_0001_02master.MP4',\n",
       " '632_0001_03master.MP4',\n",
       " '632_0001_04master.MP4',\n",
       " '632_0001_05master.MP4',\n",
       " '632_0001_06master.MP4']"
      ]
     },
     "execution_count": 48,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "os.listdir(destination_dir)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Third task - concatenate all the transcoded files into one, making it the full recording of one stage show.\n",
    "\n",
    "Before we concatenate the files, we need to make a \"mylist.txt\" file which will tell the program what files are to be concatenated\n",
    "\n",
    "Documentation of concatenation and creation of mylist.txt could be [found here](https://trac.ffmpeg.org/wiki/Concatenate)\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "I change the directory to the \"preservation\" folder, so that the \"mylist.txt\" will be placed here as well. \n",
    "\n",
    "I then generate a mp4_master_list which contains all the transcoded videos.\n",
    "\n",
    "I need to make sure the in the \"mylist.txt\" document, all files are listed in a correct order, so I also need to sort the mp4_master_list.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 49,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "['/volumes/samsung_t5/lamama_videos/20120518_Mermaid-editing/raw_footage/preservation/632_0001_01master.MP4',\n",
       " '/volumes/samsung_t5/lamama_videos/20120518_Mermaid-editing/raw_footage/preservation/632_0001_02master.MP4',\n",
       " '/volumes/samsung_t5/lamama_videos/20120518_Mermaid-editing/raw_footage/preservation/632_0001_03master.MP4',\n",
       " '/volumes/samsung_t5/lamama_videos/20120518_Mermaid-editing/raw_footage/preservation/632_0001_04master.MP4',\n",
       " '/volumes/samsung_t5/lamama_videos/20120518_Mermaid-editing/raw_footage/preservation/632_0001_05master.MP4',\n",
       " '/volumes/samsung_t5/lamama_videos/20120518_Mermaid-editing/raw_footage/preservation/632_0001_06master.MP4']"
      ]
     },
     "execution_count": 49,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "os.chdir(destination_dir)\n",
    "master_mp4_list = glob.glob(os.path.join(destination_dir, \"*MP4\"))\n",
    "master_mp4_list.sort()\n",
    "master_mp4_list"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 50,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "/Volumes/Samsung_T5/LaMaMa_Videos/20120518_Mermaid-editing/raw_footage/preservation\n"
     ]
    }
   ],
   "source": [
    "print(os.getcwd()) # make sure the current directory is the preservation folder"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "To create the \"mylist.txt\", I ask python to create a txt file.\n",
    "\n",
    "In the \"mylist.txt\", contents are arranged in a certain format, so that FFmpeg knows what files, in what order, to be concatenated."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 51,
   "metadata": {},
   "outputs": [],
   "source": [
    "filename = 'mylist.txt'\n",
    "with open (filename, 'w') as f:\n",
    "    for item in master_mp4_list:\n",
    "        f.write ('file \\'' + os.path.basename(item) + '\\'\\n')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Now we use FFmpeg to concatenate these preservation master format videos into a FULL preservation master video\n",
    "\n",
    "First we need to define the \"mylist.txt\" into a path."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 52,
   "metadata": {},
   "outputs": [],
   "source": [
    "mylist = os.path.join (destination_dir, 'mylist.txt')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Next I define the output file path. Name the file \"Preservation_Master\", to make sure after being generated, it will be listed at the last place among all other video files. I will explain in the latter step why this order place is so important.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 53,
   "metadata": {},
   "outputs": [],
   "source": [
    "output_file = os.path.join(destination_dir, 'Preservation_Master.MP4')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "I then use the subprocess module to run FFmpeg which is supposed to be process in bash terminal; each FFmpeg command needs to be in a string form, so we put them in quotation marks.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 54,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "CompletedProcess(args=['ffmpeg', '-f', 'concat', '-i', '/volumes/samsung_t5/lamama_videos/20120518_Mermaid-editing/raw_footage/preservation/mylist.txt', '-c', 'copy', '/volumes/samsung_t5/lamama_videos/20120518_Mermaid-editing/raw_footage/preservation/Preservation_Master.MP4'], returncode=0)"
      ]
     },
     "execution_count": 54,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "subprocess.run(['ffmpeg', '-f', 'concat', '-i', mylist, '-c', 'copy', output_file])"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Now let's take a look at if the FULL preservation master video is successfully generation."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 55,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "['632_0001_01master.MP4',\n",
       " '632_0001_02master.MP4',\n",
       " '632_0001_03master.MP4',\n",
       " '632_0001_04master.MP4',\n",
       " '632_0001_05master.MP4',\n",
       " '632_0001_06master.MP4',\n",
       " 'mylist.txt',\n",
       " 'Preservation_Master.MP4']"
      ]
     },
     "execution_count": 55,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "os.listdir(destination_dir)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Fourth step - transcode the preservation master video into a smaller size for public view\n",
    "\n",
    "**For now, La MaMa requires videos be exported to H.264 wrapped with MPEG-4 with bitrate 5Mb/s.**\n",
    "\n",
    "I first define the input_file, which is the preservation master video that we just created. Because I just named the preservation master video file as \"preservation_master\", it must be at the last place in the list (-1 place). **I told you this order place is important.**\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 56,
   "metadata": {},
   "outputs": [],
   "source": [
    "mp4_master_list = glob.glob (os.path.join(destination_dir,'**MP4'))\n",
    "\n",
    "input_file = (mp4_master_list[-1])"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Then I define the output file path and name the file \"Public_View.MP4\".\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 57,
   "metadata": {},
   "outputs": [],
   "source": [
    "output_file = os.path.join(destination_dir, 'Public_View.MP4')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "I use the subprocess module to run FFmpeg which is supposed to be process in bash terminal; each FFmpeg command needs to be in a string form, so we put them in quotation marks."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 58,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "CompletedProcess(args=['ffmpeg', '-i', '/volumes/samsung_t5/lamama_videos/20120518_Mermaid-editing/raw_footage/preservation/Preservation_Master.MP4', '-c:v', 'libx264', '-b:v', '5000k', '-c:a', 'aac', '/volumes/samsung_t5/lamama_videos/20120518_Mermaid-editing/raw_footage/preservation/Public_View.MP4'], returncode=0)"
      ]
     },
     "execution_count": 58,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "subprocess.run(['ffmpeg', '-i', input_file, '-c:v', 'libx264', '-b:v', '5000k', '-c:a', 'aac', output_file])"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Fifth step - add fade-in and fade-out effect to the public view file\n",
    "\n",
    "After generating the public_view file which serves the access file of the video, I will need to add the fade-in and fade-out effect to the video.\n",
    "\n",
    "Here again we use FFmpeg to process the task.\n",
    "\n",
    "We define the input file as the \"public_view\" video which we just generated, and we also define the output file as the \"public_view_final\"."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 59,
   "metadata": {},
   "outputs": [],
   "source": [
    "input_file = os.path.join(destination_dir, 'Public_View.MP4')\n",
    "output_file = os.path.join(destination_dir, 'Public_View_Final.MP4')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "I then define the setting with fade-in and fade-out 2 seconds for both video and audio (the number of seconds is changeable).\n",
    "\n",
    "The fade-in and fade-out command codes refer to [here](https://video.stackexchange.com/questions/19867/how-to-fade-in-out-a-video-audio-clip-with-unknown-duration)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 60,
   "metadata": {},
   "outputs": [],
   "source": [
    "fade_video = '\"fade=d=2, reverse, fade=d=2, reverse\"'\n",
    "fade_audio = '\"afade=d=2, areverse, afade=d=2, areverse\"'\n",
    "# the fade-in fade-out command means: fade in for 2 seconds, reverse the whole track, fade in 2 seconds again, reverse back \n",
    "\n",
    "setting = '-c:v libx264 -b:v 5000k -c:a aac'\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "If here I write every FFmpeg command in the subprocess, the code will be too long. So here I first define the whole chain of codes into ffmpeg_cmd."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 61,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "ffmpeg -i /volumes/samsung_t5/lamama_videos/20120518_Mermaid-editing/raw_footage/preservation/Public_View.MP4 -filter_complex \"fade=d=2, reverse, fade=d=2, reverse\" -filter_complex \"afade=d=2, areverse, afade=d=2, areverse\" -c:v libx264 -b:v 5000k -c:a aac /volumes/samsung_t5/lamama_videos/20120518_Mermaid-editing/raw_footage/preservation/Public_View_Final.MP4\n"
     ]
    }
   ],
   "source": [
    "ffmpeg_cmd = 'ffmpeg -i' + ' ' + input_file + ' ' + '-filter_complex' + ' ' + fade_video + ' ' + '-filter_complex' + ' ' + fade_audio + ' ' + setting + ' ' + output_file\n",
    "\n",
    "# check this ffmpeg_cmd code, it should be identical to the commands that are supposed to be run in bash terminal\n",
    "\n",
    "print (ffmpeg_cmd)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "**PLEASE NOTE if the input file (public view) is too large, e.g. 5+GB, this program might not be able to process due to the limited RAM in personal computer.**\n",
    "\n",
    "**If the input file is too large or the process pauses in the midway, you may need to use other video editing software to add the fade-in/out effect.**"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 62,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "-9"
      ]
     },
     "execution_count": 62,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "subprocess.call (ffmpeg_cmd, shell=True)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Now I have generated both the \"Preservation_Master.MP4\" and the \"Public_View_Final.MP4\". They serve as preservation master and public access file respectively.\n",
    "\n",
    "## Last but not least - Name these files according to La MaMa's naming rules and upload them to La MaMa's server."
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
