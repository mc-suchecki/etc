#!/bin/bash

# Author:      Maciej 'mc' Suchecki
# Description: Script downloading photos from camera and organizing
#              them into folders (/YYYY/YYYY-MM-DD)

camera='Canon'                       # camera manufacturer (not important)
extension='JPG'                      # extension of photos from camera
vid_extension='MOV'                  # extension of videos from camera
directory='/home/mc/Pictures/'       # directory where photos should be placed
vid_directory='/home/mc/Videos/'     # directory where videos should be placed

# checking if parent directory exist
if [ ! -d "$directory" ]; then
  echo 'Error - directory does not exist, aborting!'
  exit 1
fi

# checking if year subdirectory exist, if not create it
year=`date +"%Y"`
if [ ! -d "$directory$year" ]; then
  echo "Year $year subdirectory doesn't exist - creating..."
  mkdir "$directory$year"
fi

# checking if year subfolder was created and changing path
if [ ! -d "$directory$year" ]; then
  echo "Error - directory $directory$year not created!"
  exit 1
else
  directory="$directory$year/"
  echo "Photos will be copied to: $directory"
fi

# connecting to camera and downloading photos
#echo 'Detecting camera...'
#gphoto2 --auto-detect | grep $camera
#echo 'Downloading new photos...'
#gphoto2 --get-all-files 

# trying to move to card standard location
cd /run/media/mc/3939-6463/DCIM/100CANON/ || { echo "Moving to card folder failed! Is the card mounted?"; exit 1; }

# copying photos
echo 'Copying photos...'
for photo in `ls *.$extension`; do

  subdirectory=`exiv2 $photo | grep timestamp -a | cut -c 19- | cut -c -10 | sed 's/:/-/g'`

  if [ ! -d "$directory$subdirectory" ]; then
    echo "Creating directory $directory$subdirectory"
    mkdir "$directory$subdirectory"
  fi

  if [ ! -d "$directory$subdirectory" ]; then
    echo "Error - directory $directory$subdirectory not created!"
  else
    echo "Copying $photo"
    cp $photo "$directory$subdirectory"
  fi

done

# copying videos
echo 'Copying videos...'
count=0
if [ stat -t *.$vid_extension >/dev/null 2>&1 ]; then
  for video in `ls *.$vid_extension`; do
    echo "Copying $video"
    cp $video $vid_directory
    let count++
  done
fi
echo "Copied $count videos!"

echo 'Done!'
exit 0
